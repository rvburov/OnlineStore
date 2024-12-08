# OnlineStore


## 📂 Структура приложения

```bash
mr-tomato/
│
├── backend/
│   └── index.py             # Основной файл с кодом
├── venv/                    # Виртуальное окружение (не добавляйте в Git)
├── .gitignore               # Исключение виртуального окружения из репозитория
├── requirements.txt         # Зависимости проекта
├── README.md                # Документация для проекта
└── .env                     # Переменные окружения (не для публичного репозитория)
```

---

### 1. Настройте виртуальное окружение и зависимости

**Linux/MacOS:**
```bash
python3 -m venv venv               # Создаем виртуальное окружение в папке `venv`
source venv/bin/activate           # Активируем виртуальное окружение (Linux/MacOS)
```

```bash
python -m venv venv                # Создаем виртуальное окружение в папке `venv`
venv\Scripts\activate              # Активируем виртуальное окружение (Windows)
```

```bash
pip install --upgrade pip           # Обновляем `pip` до последней версии (универсально для всех систем)
pip install -r requirements.txt     # Устанавливаем зависимости из `requirements.txt`
```

### 2. Запуск серверана локальной машине

**Применение миграций**
```bash
python manage.py makemigrations
python manage.py migrate
```
**Создание суперпользователя**
```bash
python manage.py createsuperuser
```
**Загрузите базу данных CSV-файла**
```bash
python3 manage.py import_products data/Products.csv
```
**Запустите сервер**
```bash
python manage.py runserver
```

### 3. Запуск серверана локальной машине

**Применение миграций**
```bash
python manage.py makemigrations
python manage.py migrate
```
**Соберите статические файлы**
```bash
python manage.py collectstatic
```
**Создание суперпользователя**
```bash
python manage.py createsuperuser
```
**Загрузите базу данных CSV-файла**
```bash
python3 manage.py import_products data/Products.csv
```
**Запустите сервер**
```bash
python manage.py runserver
```