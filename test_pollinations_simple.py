"""
Test Pollinations AI directly
"""
import requests

url = 'https://image.pollinations.ai/prompt/test?width=100&height=100'
print(f'Testing Pollinations API: {url}')

try:
    r = requests.get(url, timeout=30)
    print(f'Status: {r.status_code}')
    print(f'Content-Type: {r.headers.get("Content-Type")}')
    print(f'Content-Length: {len(r.content)} bytes')
    print(f'Success: {r.status_code == 200 and len(r.content) > 0}')
    
    if r.status_code == 200:
        # Save test image
        with open('test_pollinations.jpg', 'wb') as f:
            f.write(r.content)
        print('✅ Saved test image to test_pollinations.jpg')
    else:
        print(f'❌ Failed with status {r.status_code}')
        print(f'Response: {r.text[:200]}')
except Exception as e:
    print(f'❌ Error: {e}')
