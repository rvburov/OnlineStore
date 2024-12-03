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