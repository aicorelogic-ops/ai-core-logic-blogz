import requests
from settings import FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID

def debug_token():
    if not FB_PAGE_ACCESS_TOKEN:
        print("❌ FB_PAGE_ACCESS_TOKEN is missing in .env")
        return

    print(f"Token (first 10 chars): {FB_PAGE_ACCESS_TOKEN[:10]}...")
    print(f"Configured Page ID: {FB_PAGE_ID}")

    # Check /me endpoint
    url = f"https://graph.facebook.com/v19.0/me?access_token={FB_PAGE_ACCESS_TOKEN}"
    response = requests.get(url)
    data = response.json()

    print("\n--- /me Endpoint Analysis ---")
    if 'error' in data:
        print(f"❌ Error: {data['error']['message']}")
        return

    print(f"ID: {data.get('id')}")
    print(f"Name: {data.get('name')}")
    
    if data.get('id') == FB_PAGE_ID:
        print("✅ Token identifies as the PAGE (This is a Page Access Token).")
    else:
        print("⚠️ Token identifies as a USER (This is likely a User Access Token).")
        print("   If this is a User Token, posts to the Page might appear as 'Visitor Posts'.")

    # Check permissions (debug_token)
    # Requires an app access token or just trying to inspect it if possible.
    # A simpler way is to check /me/permissions if it's a user token, or just try to post functionality.

if __name__ == "__main__":
    debug_token()
