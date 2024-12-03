document.querySelectorAll('.product-button-container form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Отключаем стандартное поведение формы
        const url = this.action;
        const method = this.method;

        fetch(url, {
            method: method,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Обновляем блок каталога
                const catalog = document.querySelector('.catalog');
                fetch(location.href)
                    .then(res => res.text())
                    .then(html => {
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        catalog.innerHTML = doc.querySelector('.catalog').innerHTML;
                    });
            }
        });
    });
});
