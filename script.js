// الإمساك بعناصر الصفحة
const cartToggle = document.getElementById('cart-toggle');
const cartDrawer = document.getElementById('cart-drawer');
const closeCart = document.getElementById('close-cart');
const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
const cartCount = document.getElementById('cart-count');
const cartItemsList = document.getElementById('cart-items-list');
const totalPriceElement = document.getElementById('total-price');
const goToCheckout = document.getElementById('go-to-checkout');
const checkoutSection = document.getElementById('checkout-section');
const orderForm = document.getElementById('order-form');

let cart = []; // مصفوفة السلة لحفظ المنتجات المشتراة

// 1. فتح وإغلاق السلة الجانبية
cartToggle.addEventListener('click', () => cartDrawer.classList.add('open'));
closeCart.addEventListener('click', () => cartDrawer.classList.remove('open'));

// 2. إضافة المنتجات للسلة وحساب المجموع تلقائياً
addToCartButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        const productCard = e.target.closest('.product-card');
        const name = productCard.querySelector('.p-name').textContent;
        const price = parseInt(productCard.querySelector('.p-price').textContent);

        // إضافة المنتج ككائن (Object) داخل مصفوفة السلة
        cart.push({ name, price });
        updateCartUI();
    });
});

// 3. تحديث واجهة السلة والأرقام
function updateCartUI() {
    // تحديث عدد العناصر في الأيقونة العلوية
    cartCount.textContent = cart.length;

    // تفريغ القائمة القديمة وإعادة بنائها بالجديد
    cartItemsList.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `<span>${item.name}</span> <span>${item.price} ر.س</span>`;
        cartItemsList.appendChild(li);
        total += item.price;
    });

    // تحديث السعر الإجمالي
    totalPriceElement.textContent = total;
}

// 4. الانتقال لقسم تأكيد الدفع والطلب
goToCheckout.addEventListener('click', () => {
    if(cart.length === 0) {
        alert("سلتك فارغة حالياً! يرجى إضافة بعض المنتجات الفاخرة أولاً.");
        return;
    }
    cartDrawer.classList.remove('open');
    checkoutSection.style.display = 'block';
    checkoutSection.scrollIntoView({ behavior: 'smooth' });
});

// 5. استقبال وإتمام الطلب وإرساله إلى واتساب (نسخة معدلة لحل مشكلة عدم الفتح)
orderForm.addEventListener('submit', (e) => {
    e.preventDefault(); // منع الصفحة من التحديث

    const name = document.getElementById('client-name').value;
    const phone = document.getElementById('client-phone').value;
    const address = document.getElementById('client-address').value;
    const finalTotal = totalPriceElement.textContent;

    // تجميع أسماء المنتجات الموجودة في السلة في نص واحد
    let productsList = "";
    cart.forEach((item, index) => {
        productsList += `${index + 1}- ${item.name} (${item.price} ر.س)%0A`;
    });

    // ضع رقم واتساب الخاص بك هنا (تأكد من كتابة مفتاح الدولة 966 ثم رقمك بدون الصفر الأول)
    const myWhatsAppNumber = "966500000000"; 

    // صياغة نص الرسالة
    const message = `🛍️ *طلب جديد من متجر الفخامة* %0A%0A` +
                    `👤 *اسم العميل:* ${name}%0A` +
                    `📱 *رقم الجوال:* ${phone}%0A` +
                    `📍 *العنوان:* ${address}%0A%0A` +
                    `📦 *المنتجات المطلوبة:*%0A${productsList}%0A` +
                    `💰 *المجموع الإجمالي:* *${finalTotal} ر.س*`;

    // إنشاء رابط الواتساب العالمي
    const whatsAppUrl = `https://api.whatsapp.com/send?phone=${myWhatsAppNumber}&text=${message}`;

    alert(`شكراً لك يا ${name}! 🎉\nاضغط موافق ليتم توجيهك فوراً إلى الواتساب لتأكيد طلبك.`);
    
    // الحل الأضمن: تحويل المتصفح مباشرة في نفس التبويب لتجنب حظر النوافذ المنبثقة
    window.location.href = whatsAppUrl;

    // تصفير السلة وإعادة تهيئة المتجر
    cart = [];
    updateCartUI();
    orderForm.reset();
    checkoutSection.style.display = 'none';
});