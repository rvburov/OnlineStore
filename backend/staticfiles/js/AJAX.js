document.addEventListener('DOMContentLoaded', function () {
    console.log('DOMContentLoaded: Инициализация...');

    // Проверяем, зарегистрирован ли пользователь
    const isAuthenticated = document.body.dataset.userAuthenticated === 'True';

    // Если пользователь зарегистрирован, очищаем данные localStorage
    if (isAuthenticated) {
        console.log('Пользователь зарегистрирован. Удаляем данные localStorage...');
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith('product_')) {
                localStorage.removeItem(key);
                console.log(`Удалён localStorage ключ: ${key}`);
            }
        });
    }

    // Обрабатываем каждый контейнер с продуктом
    document.querySelectorAll('.product').forEach(productContainer => {
        const productId = productContainer.dataset.productId;

        // Для незарегистрированного пользователя получаем вес из localStorage
        const weight = isAuthenticated 
            ? 0 
            : parseFloat(localStorage.getItem(`product_${productId}_weight`)) || 0;

        console.log(`Загружено состояние продукта ${productId}: вес = ${weight}`);

        const productButton = productContainer.querySelector('.product-button-add');
        const productDelete = productContainer.querySelector('.product-button-delete');
        const productQuantity = productContainer.querySelector('.product-quantity');

        if (weight > 0) {
            console.log(`Продукт ${productId}: показываем элементы`);
            productButton.classList.add('fixed');
            productDelete.style.display = 'block';
            productQuantity.style.display = 'block';
        } else {
            console.log(`Продукт ${productId}: скрываем элементы`);
            productButton.classList.remove('fixed');
            productDelete.style.display = 'none';
            productQuantity.style.display = 'none';
        }
    });
});

// Обработчик кликов по кнопкам управления
document.addEventListener('click', function (event) {
    // Ищем кнопку, по которой был совершен клик
    const button = event.target.closest(
        '.cart-product-add, .cart-product-delete, .product-button-add, .product-button-delete'
    );
    if (!button) return; // Выходим, если кнопка не найдена
    if (button.disabled) return; // Выходим, если кнопка уже заблокирована

    console.log(`Клик по кнопке: ${button.className}`);
    button.disabled = true; // Блокируем кнопку, чтобы избежать повторного клика
    setTimeout(() => (button.disabled = false), 100); // Снимаем блокировку через 100 мс

    event.preventDefault(); // Отменяем стандартное действие (например, отправку формы)

    // Получаем форму и её данные
    const form = button.closest('form');
    const url = form.getAttribute('action'); // URL для отправки запроса
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value; // Токен CSRF для защиты

    console.log(`Отправка запроса: URL = ${url}`);
    fetch(url, {
        method: 'POST', // HTTP-метод запроса
        headers: {
            'Content-Type': 'application/json', // Указываем, что отправляем JSON
            'X-CSRFToken': csrfToken, // Передаём токен CSRF
        },
        body: JSON.stringify({}), // Отправляем пустое тело запроса
    })
        .then(response => response.json()) // Обрабатываем ответ сервера как JSON
        .then(data => {
            console.log('Ответ сервера:', data);

            // Обработка добавления или удаления продукта в корзине
            if (button.classList.contains('cart-product-add') || button.classList.contains('cart-product-delete')) {
                console.log('Обновляем данные корзины...');
                const cartContainer = form.closest('.cart-product');
                const totalItems = document.querySelector('.total-items-cart'); // Общее количество товаров
                const totalPrice = document.querySelector('.sum-cart-products button'); // Общая цена товаров

                if (data.removed) {
                    console.log('Продукт удалён из корзины');
                    cartContainer.remove(); // Удаляем контейнер продукта из DOM

                    // Попытка получить идентификатор продукта для очистки localStorage
                    let productId = form.dataset.productId;
                    if (!productId) {
                        productId = cartContainer.dataset.productId; // Ищем в контейнере
                    }
                    if (!productId) {
                        // Извлекаем productId из URL, если он не задан
                        const urlMatch = form.action.match(/\/cart\/cart_remove\/(\d+)\//);
                        if (urlMatch) {
                            productId = urlMatch[1];
                        }
                    }

                    // Удаляем данные о весе продукта из localStorage
                    if (productId) {
                        localStorage.removeItem(`product_${productId}_weight`);
                        console.log(`LocalStorage очищен для продукта ${productId}`);
                    } else {
                        console.error('Ошибка: productId не найден для удаления из localStorage');
                    }
                } else {
                    console.log('Обновление информации о продукте в корзине');
                    // Обновляем данные веса и цены
                    const productWeight = cartContainer.querySelector('.cart-product-weight');
                    const productPrice = cartContainer.querySelector('.cart-product-price');

                    if (productWeight) productWeight.textContent = `${data.weight} кг`;
                    if (productPrice) productPrice.textContent = `${data.price} ₽`;
                }

                // Обновляем общие данные корзины
                if (totalItems) totalItems.textContent = data.total_items;
                if (totalPrice) totalPrice.textContent = `Перейти к заказу ${data.total_price} ₽`;

                // Если корзина пуста, отображаем сообщение
                if (data.is_cart_empty) {
                    console.log('Корзина пуста');
                    const cartSection = document.querySelector('.list-cart-products');
                    if (cartSection) {
                        cartSection.innerHTML = `
                            <div class="cart-logo">
                                <p>Ваша корзина пуста!</p>
                                <img src="/static/logo/cart-empty.png" alt="Изображение">
                            </div>
                        `;
                    }
                }
            }

            // Обновление данных каталога (для продуктов вне корзины)
            if (button.classList.contains('product-button-add') || button.classList.contains('product-button-delete')) {
                console.log('Обновляем данные каталога...');
                const productContainer = form.closest('.product');
                const productId = productContainer.dataset.productId;
                const productButton = productContainer.querySelector('.product-button-add');
                const productDelete = productContainer.querySelector('.product-button-delete');
                const productQuantity = productContainer.querySelector('.product-quantity');

                if (data.weight > 0) {
                    console.log(`Продукт ${productId}: вес обновлён, новый вес = ${data.weight}`);
                    productButton.classList.add('fixed');
                    productDelete.style.display = 'block';
                    productQuantity.style.display = 'block';
                    productQuantity.textContent = `${data.weight} кг`;
                    localStorage.setItem(`product_${productId}_weight`, data.weight); // Сохраняем данные в localStorage
                } else {
                    console.log(`Продукт ${productId}: вес обнулён`);
                    productButton.classList.remove('fixed');
                    productDelete.style.display = 'none';
                    productQuantity.style.display = 'none';
                    localStorage.removeItem(`product_${productId}_weight`); // Удаляем данные из localStorage
                }

                // Обновляем общее количество товаров в каталоге
                const totalItems = document.querySelector('.total-items-cart');
                if (totalItems) totalItems.textContent = data.total_items || 0;
            }
        })
        .catch(error => console.error('Ошибка при обновлении корзины:', error)); // Обработка ошибок
});
