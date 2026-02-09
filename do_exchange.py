import requests

APP_ID = "3825496444422258"
APP_SECRET = "0dbd2cddd4f8e8f30d06efb10433437b"
SHORT_LIVED_TOKEN = "EAA2XRMyoyHIBQgNZA4ZADoTqub5gwtefgImEPZBQLGM0ttVIOVaEgeUU6JqnOf8FZBVUZBHfJuQ39DopMRxtQQLBltZAw557Pncyl9GSjAEo3Vdvyxqh7qtfdoZAAURH3QGTvYzb2taF1cVNc9C4Mtg7DzmpRpJv5g60tSDN6ZAhukiBl30Wicb9ZAekA6joSE2CE0cTCNh0FUaXkcF5VhW0GBlZCWY4c0qgiGpimHyV3FwSA5znMllcKpylES9hAOrE1RPHU0dMyor2C9KjjAKKRF"

def exchange():
    print("⏳ Exchanging token...")
    
    # Step 1: Get Long-Lived User Token
    url_1 = "https://graph.facebook.com/v19.0/oauth/access_token"
    params_1 = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": SHORT_LIVED_TOKEN
    }
    
    r1 = requests.get(url_1, params=params_1)
    data1 = r1.json()
    
    if "access_token" not in data1:
        print(f"❌ Error Step 1: {data1}")
        return

    long_lived_user_token = data1["access_token"]
    print(f"✅ User Token Extended.")
    
    # Step 2: Get Page Token
    url_2 = f"https://graph.facebook.com/v19.0/me/accounts"
    params_2 = {
        "access_token": long_lived_user_token
    }
    
    r2 = requests.get(url_2, params=params_2)
    data2 = r2.json()
    
    if "data" not in data2:
        print(f"❌ Error Step 2: {data2}")
        import json
        print(json.dumps(data2, indent=2))
        return
        
    for page in data2["data"]:
        print(f"PAGE_NAME: {page['name']}")
        print(f"PAGE_ID: {page['id']}")
        print(f"PERMANENT_TOKEN: {page['access_token']}")

if __name__ == "__main__":
    exchange()
