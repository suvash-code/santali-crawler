import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime

def is_ol_chiki(text):
    """Ol Chiki script check karta hai (U+1C50–U+1C7F)."""
    return bool(re.search(r'[\u1C50-\u1C7F]', text))

def is_santali(text):
    """Santali text check (Ol Chiki + keywords)."""
    if is_ol_chiki(text):
        return True
    keywords = ['santali', 'santhal', 'ᱥᱟᱱᱛᱟᱞᱤ']
    return any(k in text.lower() for k in keywords)

def crawl_santali_pages(urls):
    records = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for para in soup.find_all("p"):
                text = para.get_text().strip()
                if text and is_santali(text):
                    records.append({
                        "url": url,
                        "text": text,
                        "is_ol_chiki": is_ol_chiki(text),
                        "timestamp": datetime.datetime.now().isoformat()
                    })
            print(f"✅ Crawled {url}")
        except Exception as e:
            print(f"❌ Error: {url} → {e}")
    return pd.DataFrame(records)

if __name__ == "__main__":
    urls = [
        "https://santali.wikipedia.org/wiki/%E1%B1%A5%E1%B1%9F%E1%B1%B1%E1%B1%9B%E1%B1%9F%E1%B1%9E%E1%B1%A4",
        "https://www.jharkhandmirror.net/category/santali/",
        "https://tribal.nic.in/"  # govt site (may/may not have Santali)
    ]
    df = crawl_santali_pages(urls)
    if not df.empty:
        df.to_csv("santali_data.csv", index=False)
        print("💾 Saved santali_data.csv")
    else:
        print("⚠️ No Santali content found")
