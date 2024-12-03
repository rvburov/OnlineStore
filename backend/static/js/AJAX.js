document.querySelectorAll('.cart-product-add, .cart-product-delete').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        const form = this.closest('form');
        const url = form.action;
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            const productElement = form.closest('.cart-product');
            const totalPrice = document.querySelector('.sum-cart-products button');
            const totalItems = document.querySelector('.total-items-cart');
            const cartSection = document.querySelector('.list-cart-products');

            if (data.removed) {
                // Если продукт удалён из корзины, удаляем HTML-элемент
                productElement.remove();
            } else {
                // Обновляем вес и цену
                const productWeight = productElement.querySelector('.cart-product-weight');
                const productPrice = productElement.querySelector('.cart-product-price');
                productWeight.textContent = `${data.weight} кг`;
                productPrice.textContent = `${data.price} ₽`;
            }

            // Обновляем общую стоимость
            totalPrice.textContent = `Перейти к заказу ${data.total_price} ₽`;

            // Обновляем количество товаров
            totalItems.textContent = data.total_items;

            // Если корзина пуста, показываем сообщение
            if (data.is_cart_empty) {
                cartSection.innerHTML = `
                    <div class="cart-logo">
                        <p>Ваша корзина пуста!</p>
                        <img src="/static/logo/cart-empty.png" alt="Изображение">
                    </div>
                `;
            }
        })
        .catch(error => console.error('Ошибка при обновлении корзины:', error));
    });
});





