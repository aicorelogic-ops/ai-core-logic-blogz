
import os
from dotenv import load_dotenv
import requests

load_dotenv("news_bot/.env")
token = os.getenv("FB_PAGE_ACCESS_TOKEN")
page_id = os.getenv("FB_PAGE_ID")

print(f"Testing Token: {token[:10]}...")
url = f"https://graph.facebook.com/v19.0/me?access_token={token}"
resp = requests.get(url)
print(f"User/Page Node Status: {resp.status_code}")
print(resp.text)

if page_id:
    url_page = f"https://graph.facebook.com/v19.0/{page_id}?access_token={token}"
    resp_page = requests.get(url_page)
    print(f"Page Access Status: {resp_page.status_code}")
    print(resp_page.text)
