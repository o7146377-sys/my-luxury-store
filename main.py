import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")

# لضمان تعامل السيرفر مع المتغير الأساسي
application = app

# قاعدة البيانات المؤقتة للمنتجات
PRODUCTS_DB = [
    {
        "id": 1,
        "name": "ساعة ذكية فاخرة بنظام أندرويد",
        "price": "299 ريال",
        "category": "accessories",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=400&auto=format&fit=crop"
    },
    {
        "id": 2,
        "name": "عطر العود الملكي الخاص",
        "price": "450 ريال",
        "category": "perfumes",
        "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?q=80&w=400&auto=format&fit=crop"
    }
]

# 1. الصفحة الرئيسية للمتجر
@app.route("/")
def read_root():
    return render_template("index.html", products=PRODUCTS_DB)


# 2. لوحة تحكم البائعين والزبائن لإضافة المنتجات
@app.route("/seller")
def seller_dashboard():
    return """
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>لوحة تحكم البائعين والمنتجات</title>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Cairo', sans-serif; background: #faf9f6; padding: 40px; text-align: center; color: #1e2522; direction: rtl; }
            .box { background: white; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 12px; border: 1px solid #eae5d9; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: right; }
            h1 { color: #bfa15f; text-align: center; margin-bottom: 25px; }
            label { display: block; margin-top: 15px; font-weight: 600; color: #1e2522; }
            input, select { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #eae5d9; border-radius: 6px; font-family: 'Cairo'; font-size: 14px; box-sizing: border-box; }
            .btn-submit { width: 100%; display: block; background: linear-gradient(135deg, #bfa15f, #9a7f43); color: white; padding: 12px; text-decoration: none; border-radius: 6px; margin-top: 25px; border: none; font-weight: 700; cursor: pointer; font-size: 16px; }
            .btn-back { display: inline-block; text-align: center; margin-top: 20px; color: #666; text-decoration: none; font-size: 14px; width: 100%; text-align: center; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>إضافة منتج جديد للمتجر 📦</h1>
            <p style="color: #666; text-align: center; font-size: 14px;">بصفتك تاجر أو زبون، يمكنك عرض بضاعتك وتحديد قسمها فوراً من هنا</p>
            
            <form action="/seller/add-product" method="post">
                <label>اسم المنتج البضاعة:</label>
                <input type="text" name="name" placeholder="مثال: طائرة درون تصوير 4K" required>
                
                <label>السعر (بالريال السعودي):</label>
                <input type="text" name="price" placeholder="مثال: 1500 ريال" required>
                
                <label>اختر القسم الصحيح لبضاعتك:</label>
                <select name="category" required>
                    <option value="electronics">electronics</option>
                    <option value="perfumes">perfumes</option>
                    <option value="cosmetics">cosmetics</option>
                    <option value="drones">drones</option>
                    <option value="accessories">accessories</option>
                    <option value="general">general</option>
                </select>
                
                <label>رابط صورة المنتج من الإنترنت (اختياري):</label>
                <input type="url" name="image" placeholder="ضع رابط الصورة هنا أو اتركها فارغة">
                
                <button type="submit" class="btn-submit">🚀 عرض المنتج فوراً في المتجر</button>
            </form>
            
            <a href="/" class="btn-back">← العودة للمتجر الرئيسي</a>
        </div>
    </body>
    </html>
    """

# 3. استقبال وحفظ المنتجات الجديدة
@app.route("/seller/add-product", methods=["POST"])
def add_product():
    name = request.form.get("name")
    price = request.form.get("price")
    category = request.form.get("category")
    image = request.form.get("image")
    
    if not image:
        image = "https://images.unsplash.com/photo-1513151233558-d860c5398176?q=80&w=400&auto=format&fit=crop"
    
    new_product = {
        "id": len(PRODUCTS_DB) + 1,
        "name": name,
        "price": price,
        "category": category,
        "image": image
    }
    PRODUCTS_DB.append(new_product)
    return redirect(url_for("read_root"))


# 4. عرض المنتجات داخل الأقسام بشكل مأمن
@app.route("/category/<category_name>")
def show_category(category_name):
    categories_titles = {
        "electronics": "عالم الإلكترونيات والتقنية",
        "perfumes": "العطور الفاخرة والزيوت العطرية",
        "cosmetics": "أدوات التجميل ومنتجات العناية",
        "drones": "طائرات الدرون والتصوير الجوي",
        "accessories": "الإكسسوارات والموضة والساعات",
        "general": "الكماليات والمستلزمات العامة"
    }
    
    title = categories_titles.get(category_name, "قسم منوع")
    filtered_products = [p for p in PRODUCTS_DB if p["category"] == category_name]
    
    products_html = ""
    for prod in filtered_products:
        products_html += f"""
        <div class="product-card">
            <img src="{prod['image']}" alt="{prod['name']}">
            <div class="prod-details">
                <h3>{prod['name']}</h3>
                <div class="price">{prod['price']}</div>
                <a href="#" class="btn-buy">🛒 إضافة للسلة</a>
            </div>
        </div>
        """
    
    if not filtered_products:
        products_html = """
        <div class="no-products" style="grid-column: 1/-1; text-align:center; background:white; padding:40px; border-radius:12px; border:1px solid #eae5d9;">
            <p style="color:#666;">📦 لا توجد بضائع معروضة حالياً في هذا القسم.. كن أول من يرفع بضاعته هنا!</p>
        </div>
        """

    return f"""
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>{title} | المعرض الفخم</title>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Cairo', sans-serif; background-image: url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop'); background-size: cover; background-position: center; background-attachment: fixed; margin: 0; padding: 0; }}
            .overlay {{ background: rgba(255, 255, 255, 0.94); min-height: 100vh; padding: 40px 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            header {{ background: linear-gradient(135deg, #1e2522, #2d3833); color: #fff; padding: 30px; border-radius: 12px; border-bottom: 4px solid #bfa15f; margin-bottom: 40px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            header h1 {{ color: #bfa15f; margin: 0 0 10px 0; font-size: 26px; }}
            .products-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }}
            .product-card {{ background: white; border-radius: 12px; overflow: hidden; border: 1px solid #eae5d9; box-shadow: 0 4px 15px rgba(0,0,0,0.03); text-align: center; }}
            .product-card img {{ width: 100%; height: 200px; object-fit: cover; }}
            .prod-details {{ padding: 20px; }}
            .prod-details h3 {{ color: #1e2522; font-size: 16px; margin-bottom: 10px; }}
            .price {{ color: #bfa15f; font-weight: 700; font-size: 18px; margin-bottom: 15px; }}
            .btn-buy {{ display: inline-block; background: #1e2522; color: #bfa15f; padding: 8px 20px; border-radius: 20px; text-decoration: none; font-size: 13px; font-weight: 600; border: 1px solid #bfa15f; }}
            .back-main {{ display: block; text-align: center; margin-top: 40px; color: #1e2522; font-weight: 600; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="overlay">
            <div class="container">
                <header>
                    <h1>{title}</h1>
                    <p>البضائع المتوفرة المعروضة للبيع حالياً</p>
                </header>
                <div class="products-grid">{products_html}</div>
                <a href="/" class="back-main">← العودة لتصفح باقي أقسام المتجر</a>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
