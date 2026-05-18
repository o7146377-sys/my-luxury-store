from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

# 1. إنشاء تطبيق الـ FastAPI الرئيسي
app = FastAPI()

# 2. ربط ملفات التصميم والألوان (CSS) لكي يراها السيرفر
app.mount("/static", StaticFiles(directory="."), name="static")

# 3. تجهيز مجلد الـ HTML لقراءة الصفحات منه
templates = Jinja2Templates(directory="templates")

# 4. قاعدة بيانات مصغرة في الذاكرة لحفظ المنتجات
products_db = [
    {
        "id": 1,
        "name": "ساعة كلاسيكية فاخرة",
        "price": 450,
        "img": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?q=80&w=500"
    }
]

# 5. نموذج البيانات الخاص بالمنتج
class Product(BaseModel):
    name: str
    price: int
    img: str

# -------------------------------------------------------------------
# 🌐 قنوات الاتصال (Routes) - متوافقة مع أحدث نسخ بايثون 3.14+
# -------------------------------------------------------------------

# قناة (أ): فتح صفحة المتجر الرئيسية للمشترين
@app.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    return templates.TemplateResponse(request, "index.html")

# قناة (ب): فتح صفحة لوحة تحكم البائع
@app.get("/seller", response_class=HTMLResponse)
def read_seller(request: Request):
    return templates.TemplateResponse(request, "seller.html")

# قناة (ج): إرسال المنتجات المحفوظة في السيرفر إلى المتجر
@app.get("/api/products")
def get_products():
    return products_db

# قناة (د): استقبال منتج جديد من البائع وحفظه في الذاكرة فوراً
@app.post("/api/products")
def add_product(product: Product):
    new_id = len(products_db) + 1
    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "img": product.img
    }
    products_db.append(new_product)
    return {"message": "تم نشر المنتج بنجاح!", "product": new_product}

# 6. أمر تشغيل السيرفر تلقائياً على المنفذ 8000
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)