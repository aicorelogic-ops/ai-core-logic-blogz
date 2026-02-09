import requests
import os

def get_long_lived_token():
    print("🔐 Facebook Long-Lived Token Generator")
    print("---------------------------------------")
    print("To get a permanent token, we need to exchange your short-lived keys.")
    print("You can find App ID and Secret in: developers.facebook.com -> My Apps -> Settings -> Basic\n")

    app_id = input("Enter your App ID: ").strip()
    app_secret = input("Enter your App Secret: ").strip()
    short_lived_token = input("Enter a fresh generic 'User Access Token' (from Graph API Explorer): ").strip()
    
    if not app_id or not app_secret or not short_lived_token:
        print("❌ Missing details. Please try again.")
        return

    # Step 1: Exchange Short-Lived User Token for Long-Lived User Token (60 Days)
    print("\n⏳ Step 1: Getting Long-Lived User Token...")
    url_1 = "https://graph.facebook.com/v19.0/oauth/access_token"
    params_1 = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_lived_token
    }
    
    try:
        r1 = requests.get(url_1, params=params_1)
        data1 = r1.json()
        
        if "access_token" not in data1:
            print(f"❌ Error getting User Token: {data1}")
            return
            
        long_lived_user_token = data1["access_token"]
        print("✅ Got Long-Lived User Token!")
        
        # Step 2: Get Page Token using the Long-Lived User Token
        # (Page Tokens generated this way DO NOT EXPIRE)
        print("⏳ Step 2: Fetching Permanent Page Token...")
        url_2 = f"https://graph.facebook.com/v19.0/me/accounts"
        params_2 = {
            "access_token": long_lived_user_token
        }
        
        r2 = requests.get(url_2, params=params_2)
        data2 = r2.json()
        
        if "data" not in data2:
            print(f"❌ Error getting Page Token: {data2}")
            return
            
        print("\n🎉 SUCCESS! Here are your Permanent Page Tokens:")
        print("---------------------------------------------------")
        for page in data2["data"]:
            print(f"Page Name: {page['name']}")
            print(f"Page ID:   {page['id']}")
            print(f"TOKEN:     {page['access_token']}")
            print("---------------------------------------------------")
            print("👉 Copy the 'TOKEN' above and paste it into your .env file as FB_PAGE_ACCESS_TOKEN")
            
    except Exception as e:
        print(f"❌ Network/Script Error: {e}")

if __name__ == "__main__":
    get_long_lived_token()
