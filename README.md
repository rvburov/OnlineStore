# Установка и настройка приложения OnlineStore


## 📂 Структура приложения

```bash
mr-tomato/
│
├── backend/
│   └── config/
│       └── settings.py               
│   └── core/
│   └── data/
│   └── homepages/
│   └── madia/
│   └── static/
│   └── users/
│   └── catalog/
│   └── cart/
├── venv/                    # Виртуальное окружение (не добавляйте в Git)
├── .gitignore               # Исключение виртуального окружения из репозитория
├── requirements.txt         # Зависимости проекта
├── README.md                # Документация для проекта
└── .env                     # Переменные окружения (не для публичного репозитория)
```

---

### 🔑 Настройка переменных окружения (.env)

Для конфигурации проекта создайте файл `.env` в корневой директории проекта. Этот файл должен содержать конфиденциальные данные, такие как ключи API, настройки базы данных и другие параметры.

#### Пример файла `.env`:

```bash
# Секретный ключ Django
SECRET_KEY=...

# Режим отладки (True для разработки, False для продакшена)
DEBUG=...

# Список разрешённых хостов
ALLOWED_HOSTS=...

# CSRF доверенные источники
CSRF_TRUSTED_ORIGINS=...
```

#### Как подключить `.env` в проект:
1. Убедитесь, что файл `.env` добавлен в `.gitignore`, чтобы он не попал в публичный репозиторий.
2. Для использования переменных из файла `.env`, проект уже настроен на использование библиотеки **`python-decouple`** (или аналогичной).
```bash
pip install python-decouple
```
3. Убедитесь, что файл `.env` находится в корневой папке проекта.

#### 💡 Рекомендации:
- Никогда не храните конфиденциальные данные (такие как `SECRET_KEY`, пароли или ключи API) в репозитории.
- Для продакшена рекомендуется использовать безопасное хранилище секретов, например AWS Secrets Manager или HashiCorp Vault.

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

---

### 2. Запуск серверана локальной машине

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