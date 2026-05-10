import requests
from bs4 import BeautifulSoup
import json

url = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

catalog = []

for link in links:

    text = link.get_text(strip=True)
    href = link.get("href")

    if text and href:

        if "/products/" in href:

            item = {
                "name": text,
                "url": href if href.startswith("http") else "https://www.shl.com" + href,
                "test_type": "Unknown"
            }

            catalog.append(item)

# Remove duplicates
unique_catalog = []
seen = set()

for item in catalog:

    if item["url"] not in seen:
        seen.add(item["url"])
        unique_catalog.append(item)

with open("catalog.json", "w") as f:
    json.dump(unique_catalog, f, indent=2)

print(f"Saved {len(unique_catalog)} assessments")