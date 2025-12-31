import cv2, easyocr, numpy as np
import sys
sys.path.append('src')
from iso6346_validator import validate_container

print('🚢 NIGERIA CUSTOMS CONTAINER AI v1.0')

img = cv2.imread('data/nigeria_customs.jpg')
if img is None:
    print('❌ No image - run demo generator first')
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
reader = easyocr.Reader(['en'])
results = reader.readtext(gray)

print('📦 LIVE SCAN RESULTS:')
found = False
for (bbox, text, conf) in results:
    code = ''.join(c for c in text.strip().upper() if c.isalnum())
    if len(code) == 11 and conf > 0.5:
        valid, expected = validate_container(code)
        status = '✅ VALID ISO 6346' if valid else '❌ INVALID'
        print(f'  {code} {status} (conf: {conf:.1f})')
        found = True

if not found:
    print('  No valid container codes detected')
print('🇳🇬 MSc Robotics Prototype READY!')
