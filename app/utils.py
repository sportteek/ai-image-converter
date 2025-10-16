from PIL import Image, ImageFilter, ImageOps
import io, cv2, numpy as np, os

def convert_image_local(image_bytes: bytes, method: str = "grayscale") -> bytes:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    if method == "grayscale":
        out = ImageOps.grayscale(img)
    elif method == "edge":
        arr = np.array(img)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        out = Image.fromarray(edges_rgb)
    elif method == "cartoon":
        arr = np.array(img)
        for _ in range(2):
            arr = cv2.bilateralFilter(arr, 9, 75, 75)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        edges = cv2.adaptiveThreshold(cv2.medianBlur(gray, 7), 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 2)
        color = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(color, edges_colored)
        cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
        out = Image.fromarray(cartoon)
    else:
        out = img.filter(ImageFilter.DETAIL)
    buf = io.BytesIO()
    out.save(buf, format="PNG")
    return buf.getvalue()

def convert_with_external_api(image_bytes: bytes, params: dict) -> bytes:
    # مكان مخصص لإضافة نموذج ذكاء اصطناعي خارجي لاحقًا
    return convert_image_local(image_bytes, params.get("method", "grayscale"))
