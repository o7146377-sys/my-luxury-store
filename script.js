

        const productCard = e.target.closest('.product-card');

        const name = productCard.querySelector('.p-name').textContent;

        const price = parseInt(
            productCard.querySelector('.p-price').textContent
        );

        cart.push({ name, price });

        updateCartUI();
    });
});

function updateCartUI() {

    cartCount.textContent = cart.length;

    cartItemsList.innerHTML = '';

    let total = 0;

    cart.forEach(item => {

        const li = document.createElement('li');

        li.textContent = `${item.name} - ${item.price} ر.س`;

        cartItemsList.appendChild(li);

        total += item.price;
    });

    totalPriceElement.textContent = total;
}

if(goToCheckout){
    goToCheckout.addEventListener('click', () => {

        if(cart.length === 0){
            alert('السلة فارغة');
            return;
        }

        checkoutSection.style.display = 'block';

        checkoutSection.scrollIntoView({
            behavior: 'smooth'
        });
    });
}

if(orderForm){
    orderForm.addEventListener('submit', (e) => {

        e.preventDefault();

        alert('تم إرسال الطلب بنجاح');

        cart = [];

        updateCartUI();

        orderForm.reset();
    });
}
