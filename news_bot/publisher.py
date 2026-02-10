import requests
from .settings import FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID

class FacebookPublisher:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v19.0"
        self.token = FB_PAGE_ACCESS_TOKEN
        self.page_id = FB_PAGE_ID

    def post_content(self, message, link=None):
        """
        Publishes a post to the Facebook Page feed.
        If a link is provided, it becomes a 'link post'.
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None

        url = f"{self.base_url}/{self.page_id}/feed"
        payload = {
            "message": message,
            "access_token": self.token
        }
        
        if link:
            payload["link"] = link

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            print(f"✅ Successfully posted to Facebook! Post ID: {data.get('id')}")
            return data.get('id')
        except requests.exceptions.RequestException as e:
            self._handle_error(e, response if 'response' in locals() else None)
            return None

    def post_photo(self, photo_url, message):
        """
        Publishes a photo post to the Facebook Page.
        This is typically more 'attention-grabbing' than a standard link post.
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None

        url = f"{self.base_url}/{self.page_id}/photos"
        payload = {
            "url": photo_url,
            "caption": message,
            "access_token": self.token
        }

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            print(f"📸 Successfully posted photo to Facebook! ID: {data.get('id')}")
            return data.get('id')
        except requests.exceptions.RequestException as e:
            self._handle_error(e, response if 'response' in locals() else None)
            return None
    
    def post_reel(self, video_path, caption):
        """
        Post a video as a Reel to Facebook Page.
        Video should be vertical format (9:16), 15-90 seconds.
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None
        
        url = f"{self.base_url}/{self.page_id}/video_reels"
        
        try:
            print(f"🎬 Uploading reel to Facebook...")
            
            # Read video file
            with open(video_path, 'rb') as video_file:
                files = {'source': video_file}
                data = {
                    'description': caption,
                    'access_token': self.token
                }
                
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                
                reel_data = response.json()
                print(f"✅ Successfully posted Reel!")
                print(f"Reel ID: {reel_data.get('id')}")
                return reel_data.get('id')
                    
        except Exception as e:
            print(f"❌ Reel upload error: {e}")
            if 'response' in locals():
                self._handle_error(e, response)
            return None

    def _handle_error(self, exception, response):
        print(f"❌ Error posting to Facebook: {exception}")
        if response is not None:
            with open("fb_error.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Response saved to fb_error.txt")

if __name__ == "__main__":
    # Test run
    publisher = FacebookPublisher()
    # publisher.post_content("Hello World! This is a test post from AI Core Logic Bot. #AI #Automation")

