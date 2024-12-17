document.querySelector('.footer-logo-open').addEventListener('click', function() {
    document.querySelector('.footer-content-item').classList.toggle('active');
    document.querySelector('.footer-logo-close').classList.toggle('active');
    document.querySelector('.footer-logo-open').classList.toggle('active');
    document.querySelector('.footer-menu').classList.toggle('active');
});

document.querySelector('.footer-logo-close').addEventListener('click', function() {
    document.querySelector('.footer-content-item').classList.toggle('active');
    document.querySelector('.footer-logo-close').classList.toggle('active');
    document.querySelector('.footer-logo-open').classList.toggle('active');
    document.querySelector('.footer-menu').classList.toggle('active');
});

function scrollToCategory(categoryId) {
    const target = document.getElementById(categoryId);
    if (target) {
        target.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
        });
    }
    setActiveButton(categoryId);
}

// Функция для установки активной кнопки
function setActiveButton(categoryId) {
    const buttons = document.querySelectorAll('.category-scroll');
    buttons.forEach(button => {
        if (button.getAttribute('data-target') === categoryId) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll('.category-title');
    const buttons = document.querySelectorAll('.category-scroll');

    // Добавляем событие клика для кнопок
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            scrollToCategory(targetId);
        });
    });

    // Настройка IntersectionObserver для более точного отслеживания
    const observerOptions = {
        root: null, // viewport
        threshold: [0, 0.5] // Срабатывает при частичном или 50% появлении
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                setActiveButton(entry.target.id);
            }
        });
    }, observerOptions);

    // Наблюдаем за всеми секциями
    sections.forEach(section => {
        observer.observe(section);
    });

    // Изначально активная кнопка (первая категория)
    if (sections.length > 0) {
        setActiveButton(sections[0].id);
    }
});

// Исправить не отображает секцию списка продуктов каталога
