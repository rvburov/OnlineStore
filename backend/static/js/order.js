document.addEventListener('DOMContentLoaded', function() {
    var phoneInput = document.querySelector('#id_phone'); // Получаем элемент поля телефона по его id

    // Функция для форматирования телефонного номера
    const formatPhoneNumber = (input) => {
        // Очищаем значение от всех символов, кроме цифр
        let cleaned = ('' + input).replace(/\D/g, '');
        // Удаляем возможный префикс +7
        if (cleaned.startsWith('7')) {
            cleaned = cleaned.slice(1);
        }
        // Применяем формат +7(***)***-**-**
        let formatted = '+7';
        let length = cleaned.length;
        // Добавляем скобки и тире в зависимости от количества введенных цифр
        if (length > 0) {
            formatted += '(' + cleaned.substring(0, Math.min(length, 3));
        }
        if (length > 3) {
            formatted += ')' + cleaned.substring(3, Math.min(length, 6));
        }
        if (length > 6) {
            formatted += '-' + cleaned.substring(6, Math.min(length, 8));
        }
        if (length > 8) {
            formatted += '-' + cleaned.substring(8, Math.min(length, 10));
        }
        return formatted;
    };
    // Функция для обновления значения поля
    const updateValue = () => {
        phoneInput.value = formatPhoneNumber(phoneInput.value);
    };

    // Событие input для отслеживания ввода
    phoneInput.addEventListener('input', updateValue);
});
