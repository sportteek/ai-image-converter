# AI Image Converter

موقع بسيط لتحويل الصور باستخدام FastAPI. يدعم تحويلات محلية متعددة (grayscale, cartoonize, edge-detect) ويمكن تمديده للاتصال بخدمات ذكاء اصطناعي خارجية.

## التشغيل
```bash
python -m venv venv
source venv/bin/activate  # أو venv\Scripts\activate على ويندوز
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
ثم افتح المتصفح على: http://localhost:8000
