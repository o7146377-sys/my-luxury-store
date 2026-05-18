from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
import uvicorn

app = FastAPI()

# ربط ملفات static
app.mount("/static", StaticFiles(directory="static"), name="static")

# ربط مجلد templates
templates = Jinja2Templates(directory="templates")

# قاعدة بيانات مؤقتة
products_db = [
    {
        "id": 1,
        "name": "ساعة كلاسيكية فاخرة",
        "price": 450,
        "img": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?q=80&w=500"
    }
]

# نموذج المنتج
class Product(BaseModel):
    name: str
    price: int
    img: HttpUrl


@app.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "products": products_db
        }
    )


@app.get("/seller", response_class=HTMLResponse)
def read_seller(request: Request):
    return templates.TemplateResponse(
        "seller.html",
        {
            "request": request
        }
    )


@app.get("/api/products")
def get_products():
    return products_db


@app.post("/api/products")
def add_product(product: Product):
    new_id = len(products_db) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "img": str(product.img)
    }

    products_db.append(new_product)

    return {
        "message": "تم نشر المنتج بنجاح",
        "product": new_product
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
