import re

filepath = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog\posts\2026-02-10-the-death-of-the-middle-manager.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

print(f"File size: {len(content)}")

# Test 1: Open Graph
og_match = re.search(r'<meta property="og:image" content="(.*?)"', content)
print(f"OG Match: {og_match.group(1) if og_match else 'None'}")

# Test 2: CSS Background (Current Regex)
css_match = re.search(r"background(?:-image)?: url\(['\"]?(.*?)['\"]?\)", content)
print(f"CSS Match: {css_match.group(1) if css_match else 'None'}")

# Test 3: Debugging the line
lines = content.split('\n')
for i, line in enumerate(lines):
    if "background: url" in line:
        print(f"Found line {i+1}: {line.strip()}")
        # Test regex on just this line
        m = re.search(r"background(?:-image)?: url\(['\"]?(.*?)['\"]?\)", line)
        print(f"Line match: {m.group(1) if m else 'None'}")
