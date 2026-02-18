
import requests
import os
from .settings import FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID

class FacebookPublisher:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v19.0"
        self.token = FB_PAGE_ACCESS_TOKEN
        self.page_id = FB_PAGE_ID

    def post_content(self, message, link=None, attached_media=None):
        """
        Publishes a post to the Facebook Page feed.
        If a link is provided, it becomes a 'link post'.
        If attached_media is provided, it becomes a 'status with media'.
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
            
        if attached_media:
            # attached_media should be a list of dicts: [{'media_fbid': '...'}]
            # It must be JSON encoded string for form-data, or part of JSON body
            # We'll use json encoding to be safe with requests data=payload
            import json
            payload["attached_media"] = json.dumps(attached_media)

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            print(f"Successfully posted to Facebook! Post ID: {data.get('id')}")
            return data.get('id')
        except requests.exceptions.RequestException as e:
            self._handle_error(e, response if 'response' in locals() else None)
            return None

    def post_photo(self, photo_source, message=None, published=True):
        """
        Publishes a photo post to the Facebook Page.
        Accepts either a local file path OR a URL.
        
        Args:
            photo_source: Either an absolute file path (str) or URL (str)
            message: Caption for the Facebook post
            published: Boolean, set to False to upload without posting (for attached_media)
        
        Returns:
            str: Facebook photo ID if successful, None otherwise
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None

        url = f"{self.base_url}/{self.page_id}/photos"
        
        # Determine if photo_source is a local file or URL
        image_content = None
        
        if os.path.exists(photo_source):
            # LOCAL FILE - Read directly (most reliable!)
            print(f"📁 Reading local image file: {photo_source}")
            try:
                with open(photo_source, 'rb') as f:
                    image_content = f.read()
                print(f"✅ Local file loaded ({len(image_content):,} bytes)")
            except Exception as e:
                print(f"❌ Error reading local file: {e}")
                return None
        else:
            # URL - Download with retry logic
            print(f"🌐 Downloading image from URL: {photo_source}")
            import time
            max_retries = 3
            retry_delay = 5
            
            for attempt in range(max_retries):
                try:
                    print(f"   Attempt {attempt + 1}/{max_retries}...")
                    content = self._download_image_content(photo_source)
                    
                    if content and len(content) > 1000:
                        print(f"✅ Image downloaded ({len(content):,} bytes)")
                        image_content = content
                        break
                    else:
                        print(f"⚠️ Image too small or empty. Retrying in {retry_delay}s...")
                        time.sleep(retry_delay)
                except Exception as e:
                    print(f"❌ Download error: {e}. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
            
            if not image_content:
                print("❌ Failed to retrieve valid image after retries.")
                return None
        
        # Upload image to Facebook
        try:
            print(f"📤 Uploading image to Facebook ({len(image_content):,} bytes). Published={published}...")
            
            files = {
                'source': ('image.jpg', image_content, 'image/jpeg')
            }
            
            params = {
                "access_token": self.token
            }
            
            # Convert boolean published to string "true"/"false"
            data = {
                "published": str(published).lower()
            }
            
            if message:
                data["caption"] = message

            response = requests.post(url, files=files, data=data, params=params, timeout=60)
            
            if response.status_code >= 400:
                print(f"Facebook API Error Response: {response.text}")
                
            response.raise_for_status()
            result = response.json()
            print(f"✅ Successfully posted photo to Facebook! ID: {result.get('id')}")
            return result.get('id')
            
        except requests.exceptions.RequestException as e:
            self._handle_error(e, response if 'response' in locals() else None)
            return None
    
    def post_video(self, video_path, caption):
        """
        Post a video to Facebook Page (simpler than Reels API).
        Works for any video format including vertical 9:16 reels.
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None
        
        url = f"{self.base_url}/{self.page_id}/videos"
        
        try:
            import os
            video_size = os.path.getsize(video_path)
            print(f"Uploading video to Facebook...")
            print(f"   Video size: {video_size:,} bytes")
            
            with open(video_path, 'rb') as video_file:
                files = {'file': video_file}
                data = {
                    'description': caption,
                    'access_token': self.token
                }
                
                response = requests.post(url, files=files, data=data, timeout=120)
                response.raise_for_status()
                
                video_data = response.json()
                print(f"Successfully posted video!")
                print(f"Video ID: {video_data.get('id')}")
                return video_data.get('id')
                    
        except Exception as e:
            print(f"Video upload error: {e}")
            if 'response' in locals():
                self._handle_error(e, response)
            return None
    
    def post_reel(self, video_path, caption):
        """
        Post a video as a Reel to Facebook Page using 3-phase upload.
        Video should be vertical format (9:16), 15-90 seconds.
        """
        if not self.token or not self.page_id:
            print("Error: Missing Facebook Page Token or Page ID.")
            return None
        
        try:
            import os
            video_size = os.path.getsize(video_path)
            
            print(f"Uploading reel to Facebook (3-phase upload)...")
            print(f"   Video size: {video_size:,} bytes")
            
            # PHASE 1: Initialize upload session
            print("   Phase 1: Initializing upload session...")
            init_url = f"{self.base_url}/{self.page_id}/video_reels"
            init_data = {
                'upload_phase': 'start',
                'file_size': video_size,
                'access_token': self.token
            }
            
            init_response = requests.post(init_url, data=init_data)
            init_response.raise_for_status()
            init_result = init_response.json()
            
            video_id = init_result.get('video_id')
            upload_session_id = init_result.get('upload_session_id')
            
            if not video_id or not upload_session_id:
                print(f"Failed to initialize upload: {init_result}")
                return None
            
            print(f"   Session ID: {upload_session_id}")
            
            # PHASE 2: Upload video file
            print("   Phase 2: Uploading video file...")
            upload_url = f"{self.base_url}/{self.page_id}/video_reels"
            
            with open(video_path, 'rb') as video_file:
                upload_data = {
                    'upload_phase': 'transfer',
                    'upload_session_id': upload_session_id,
                    'access_token': self.token
                }
                upload_files = {'video_file_chunk': video_file}
                
                upload_response = requests.post(upload_url, data=upload_data, files=upload_files)
                upload_response.raise_for_status()
                upload_result = upload_response.json()
            
            print(f"   Video uploaded")
            
            # PHASE 3: Finalize and publish
            print("   Phase 3: Publishing reel...")
            finish_url = f"{self.base_url}/{self.page_id}/video_reels"
            finish_data = {
                'upload_phase': 'finish',
                'upload_session_id': upload_session_id,
                'description': caption,
                'access_token': self.token
            }
            
            finish_response = requests.post(finish_url, data=finish_data)
            finish_response.raise_for_status()
            finish_result = finish_response.json()
            
            if finish_result.get('success'):
                print(f"Successfully posted Reel!")
                print(f"Reel ID: {video_id}")
                return video_id
            else:
                print(f"Failed to finalize: {finish_result}")
                return None
                    
        except Exception as e:
            print(f"Reel upload error: {e}")
            if 'init_response' in locals():
                self._handle_error(e, init_response)
            elif 'upload_response' in locals():
                self._handle_error(e, upload_response)
            elif 'finish_response' in locals():
                self._handle_error(e, finish_response)
            return None

    def _handle_error(self, exception, response):
        print(f"Error posting to Facebook: {exception}")
        if response is not None:
            with open("fb_error.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Response saved to fb_error.txt")
            
    def _download_image_content(self, url):
        """
        Robustly downloads image content, handling redirects and headers.
        """
        print(f"Downloading image from: {url}")
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            })
            
            response = session.get(url, stream=True, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            content = b""
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    content += chunk
                    
            if len(content) == 0:
                print("WARNING: Downloaded content is empty.")
                return None
                
            return content
        except Exception as e:
            print(f"Download invalid: {e}")
            return None

    def post_comment(self, object_id, message):
        """
        Publishes a comment on a specific Facebook object (post, photo, video).
        
        Args:
            object_id: The ID of the post/photo to comment on.
            message: The comment text.
            
        Returns:
            str: Comment ID if successful, None otherwise.
        """
        if not self.token:
            print("Error: Missing Facebook Page Token.")
            return None

        url = f"{self.base_url}/{object_id}/comments"
        payload = {
            "message": message,
            "access_token": self.token
        }

        try:
            print(f"💬 Posting comment on {object_id}...")
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            print(f"✅ Successfully posted comment! ID: {data.get('id')}")
            return data.get('id')
        except requests.exceptions.RequestException as e:
            self._handle_error(e, response if 'response' in locals() else None)
            return None

if __name__ == "__main__":
    # Test run
    publisher = FacebookPublisher()
    # publisher.post_content("Hello World! This is a test post from AI Core Logic Bot. #AI #Automation")

