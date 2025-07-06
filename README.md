# Foodgram - Платформа для обмена рецептами

## Описание проекта

Foodgram - это веб-приложение для создания, хранения и обмена кулинарными рецептами. Пользователи могут создавать рецепты, добавлять их в избранное, формировать список покупок и подписываться на других авторов.

## Автор

**Соколов Матвей Ильич ПИ04у/23б РЭУ им.Плеханова**

## Технологии

### Backend
- **Django 4.2** - веб-фреймворк
- **Django REST Framework** - API
- **PostgreSQL** - база данных
- **Docker** - контейнеризация
- **Nginx** - веб-сервер и прокси
- **Gunicorn** - WSGI сервер

### Frontend
- **React** - пользовательский интерфейс
- **JavaScript (ES6+)** - логика приложения

### Инфраструктура
- **Docker Compose** - оркестрация контейнеров
- **GitHub Actions** - CI/CD

## Функциональность

### Для авторизованных пользователей
- Создание, редактирование и удаление рецептов
- Добавление рецептов в избранное
- Формирование списка покупок
- Подписка на других авторов
- Загрузка и изменение аватара
- Скачивание списка покупок в текстовом формате

### Для неавторизованных пользователей
- Просмотр рецептов
- Просмотр профилей авторов
- Регистрация и авторизация

### Для администраторов
- Полный доступ к админ-панели
- Управление пользователями, рецептами и ингредиентами

## Структура проекта

```
foodgram-matvey-sokolov/
├── backend/                    # Backend часть проекта
│   ├── foodgram_backend/       # Django проект
│   ├── requirements.txt        # Зависимости Python
│   └── Dockerfile             # Docker образ для backend
├── frontend/                   # Frontend часть проекта
│   ├── src/                   # Исходный код React
│   ├── public/                # Статические файлы
│   └── Dockerfile             # Docker образ для frontend
├── docker-compose.yml         # Конфигурация Docker Compose
├── nginx.conf                 # Конфигурация Nginx
├── .env                       # Переменные окружения
├── docs/                      # Документация
└── postman_collection/        # Коллекция Postman для тестирования API
```

## Инструкции для ревьюера

### Быстрый запуск проекта

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd foodgram-matvey-sokolov
   ```

2. **Создание файла .env**
   Создайте файл `.env` в корневой директории проекта:
   ```env
   DB_NAME=foodgram_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   SECRET_KEY=django-insecure-your-secret-key-here
   DEBUG=False
   ```

3. **Запуск проекта**
   ```bash
   docker-compose up -d
   ```

4. **Проверка работы**
   - Веб-интерфейс: http://localhost
   - API: http://localhost/api/
   - Админ-панель: http://localhost/admin/
     - Логин: `admin`
     - Пароль: `admin123`

### Проверка функциональности

1. **Регистрация и авторизация**
   - Откройте http://localhost
   - Зарегистрируйтесь или войдите в систему

2. **Создание рецепта**
   - Нажмите "Создать рецепт"
   - Заполните все поля
   - Добавьте ингредиенты
   - Сохраните рецепт

3. **Тестирование API**
   - Получите токен: `POST /api/auth/token/login/`
   - Создайте рецепт: `POST /api/recipes/`
   - Добавьте в избранное: `POST /api/recipes/{id}/favorite/`
   - Добавьте в корзину: `POST /api/recipes/{id}/shopping_cart/`

4. **Проверка фильтрации**
   - API с фильтрами: `GET /api/recipes/?is_favorited=1`
   - API корзины: `GET /api/recipes/?is_in_shopping_cart=1`

### Проверка кода

1. **Запуск тестов**
   ```bash
   docker-compose exec backend python manage.py test
   ```

2. **Проверка стиля кода**
   ```bash
   docker-compose exec backend flake8 foodgram_backend/ --max-line-length=79
   ```

3. **Проверка миграций**
   ```bash
   docker-compose exec backend python manage.py makemigrations --check
   ```

### Остановка проекта
```bash
docker-compose down
```

## Установка и запуск

### Предварительные требования

1. **Docker Desktop для Windows**
   - Скачайте и установите [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Убедитесь, что Docker Desktop запущен
   - Включите WSL 2 (Windows Subsystem for Linux) если потребуется

2. **Git для Windows**
   - Скачайте и установите [Git for Windows](https://git-scm.com/download/win)

3. **Терминал**
   - Используйте PowerShell, Command Prompt или Windows Terminal
   - Рекомендуется использовать [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701)

### Шаги установки

1. **Клонирование репозитория**
   ```cmd
   git clone <repository-url>
   cd foodgram-matvey-sokolov
   ```

2. **Настройка переменных окружения**
   Создайте файл `.env` в корневой директории проекта:
   ```env
   DB_NAME=foodgram_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ```

3. **Запуск проекта**
   ```cmd
   docker-compose up -d
   ```

4. **Создание суперпользователя (опционально)**
   ```cmd
   docker-compose exec backend python manage.py createsuperuser
   ```

5. **Загрузка тестовых данных (опционально)**
   ```cmd
   docker-compose exec backend python manage.py loaddata fixtures/ingredients.json
   ```

### Админ пользователь

В проекте уже создан административный пользователь для доступа к админ-панели Django:

**Данные для входа:**
- **Логин:** `admin`
- **Пароль:** `admin123`
- **Email:** `admin@foodgram.com`

**Доступ к админ-панели:**
- URL: http://localhost/admin/
- Полные права администратора для управления пользователями, рецептами и ингредиентами

**Возможности админ-панели:**
- Управление пользователями сайта
- Создание, редактирование и удаление рецептов
- Управление ингредиентами и их единицами измерения
- Просмотр статистики и аналитики
- Настройка параметров приложения

### Альтернативные команды для PowerShell

Если вы используете PowerShell, можете использовать следующие команды:

```powershell
# Запуск проекта
docker-compose up -d

# Выполнение команд в контейнере
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py loaddata fixtures/ingredients.json
```

### Доступ к приложению

- **Веб-интерфейс**: http://localhost
- **API документация**: http://localhost/api/
- **Админ-панель**: http://localhost/admin/

## Управление проектом

### Запуск и остановка
```cmd
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов
docker-compose logs backend
docker-compose logs frontend
docker-compose logs nginx
```

### Пересборка контейнеров
```cmd
# Пересборка backend
docker-compose build backend
docker-compose up -d backend

# Пересборка frontend
docker-compose build frontend
docker-compose up -d frontend

# Пересборка всех контейнеров
docker-compose build
docker-compose up -d
```

### Очистка данных
```cmd
# Остановка и удаление контейнеров с данными
docker-compose down -v

# Удаление всех неиспользуемых образов
docker system prune -a
```

## API Endpoints

### Аутентификация
- `POST /api/auth/token/login/` - Получение токена
- `POST /api/auth/token/logout/` - Выход из системы

### Пользователи
- `GET /api/users/` - Список пользователей
- `GET /api/users/me/` - Профиль текущего пользователя
- `PUT /api/users/me/avatar/` - Изменение аватара

### Рецепты
- `GET /api/recipes/` - Список рецептов
- `POST /api/recipes/` - Создание рецепта
- `GET /api/recipes/{id}/` - Детали рецепта
- `PUT /api/recipes/{id}/` - Обновление рецепта
- `DELETE /api/recipes/{id}/` - Удаление рецепта
- `POST /api/recipes/{id}/favorite/` - Добавление в избранное
- `DELETE /api/recipes/{id}/favorite/` - Удаление из избранного
- `POST /api/recipes/{id}/shopping_cart/` - Добавление в корзину
- `DELETE /api/recipes/{id}/shopping_cart/` - Удаление из корзины
- `GET /api/recipes/download_shopping_cart/` - Скачивание списка покупок

### Подписки
- `GET /api/users/subscriptions/` - Список подписок
- `POST /api/users/{id}/subscribe/` - Подписка на пользователя
- `DELETE /api/users/{id}/subscribe/` - Отписка от пользователя

### Ингредиенты
- `GET /api/ingredients/` - Список ингредиентов
- `GET /api/ingredients/?search=название` - Поиск ингредиентов

## Фильтрация и поиск

### Рецепты
- `?author={id}` - фильтр по автору
- `?is_favorited=1` - только избранные рецепты
- `?is_in_shopping_cart=1` - только рецепты в корзине
- `?search=название` - поиск по названию

### Пользователи
- `?search=имя` - поиск по имени пользователя

## Разработка

### Запуск тестов
```cmd
docker-compose exec backend python manage.py test
```

### Проверка кода
```cmd
docker-compose exec backend flake8
```

### Создание миграций
```cmd
docker-compose exec backend python manage.py makemigrations
```

### Отладка контейнеров
```cmd
# Вход в контейнер backend
docker-compose exec backend bash

# Вход в контейнер frontend
docker-compose exec frontend sh

# Просмотр переменных окружения
docker-compose exec backend env
```

## Решение проблем

### Проблемы с Docker Desktop
1. Убедитесь, что Docker Desktop запущен
2. Проверьте, что WSL 2 включен (если требуется)
3. Перезапустите Docker Desktop

### Проблемы с портами
Если порт 80 занят, измените порт в `docker-compose.yml`:
```yaml
ports:
  - "8080:80"  # Вместо "80:80"
```

### Проблемы с правами доступа
В Windows права доступа обычно не являются проблемой, но если возникают ошибки:
1. Запустите терминал от имени администратора
2. Проверьте настройки антивируса

### Очистка Docker
```cmd
# Остановка всех контейнеров
docker stop $(docker ps -a -q)

# Удаление всех контейнеров
docker rm $(docker ps -a -q)

# Удаление всех образов
docker rmi $(docker images -q)

# Очистка неиспользуемых ресурсов
docker system prune -a
```

## Деплой

Проект настроен для автоматического деплоя через GitHub Actions. При пуше в ветку `main` автоматически:

1. Запускаются тесты
2. Собираются Docker образы
3. Публикуются образы в Docker Hub

## Лицензия

Этот проект создан в образовательных целях.

## Контакты

**Соколов Матвей Ильич**
- Email: stimpemka@yandex.ru
- GitHub: [ваш GitHub профиль] 