import google.generativeai as genai
import inspect

print(f"Version: {genai.__version__}")
print(f"Attributes of genai: {dir(genai)}")

try:
    model = genai.GenerativeModel('imagen-3.0-generate-001')
    print(f"Model attributes: {dir(model)}")
except Exception as e:
    print(f"Error initializing model: {e}")
