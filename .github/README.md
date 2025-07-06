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
foodgram/
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
├── infra/                     # Конфигурация для продакшена
├── docs/                      # Документация
└── postman_collection/        # Коллекция Postman для тестирования API
```

## Инструкции для ревьюера

### Быстрый запуск проекта

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/STIMPEM/foodgram.git
   cd foodgram
   ```

2. **Запуск проекта**
   ```bash
   docker-compose up -d
   ```

3. **Проверка работы**
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

1. **Docker Desktop**
   - Скачайте и установите [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Убедитесь, что Docker Desktop запущен

2. **Git**
   - Скачайте и установите [Git](https://git-scm.com/)

### Шаги установки

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/STIMPEM/foodgram.git
   cd foodgram
   ```

2. **Настройка переменных окружения (опционально)**
   Проект работает с настройками по умолчанию. Если хотите изменить настройки, создайте файл `.env` в корневой директории:
   ```env
   DB_NAME=foodgram_db
   POSTGRES_USER=foodgram_user
   POSTGRES_PASSWORD=foodgram_password
   SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
   DEBUG=False
   ```

3. **Запуск проекта**
   ```bash
   docker-compose up -d
   ```

3. **Создание суперпользователя (опционально)**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

4. **Загрузка тестовых данных (опционально)**
   ```bash
   docker-compose exec backend python manage.py loaddata fixtures/ingredients.json
   ```
   
   **Примечание:** В проекте уже загружено 2186 ингредиентов и создан тестовый рецепт для демонстрации функциональности.

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

### Доступ к приложению

- **Веб-интерфейс**: http://localhost
- **API документация**: http://localhost/api/
- **Админ-панель**: http://localhost/admin/

**Проект готов к использованию сразу после запуска!** Все необходимые данные уже загружены, включая ингредиенты и административного пользователя.

## Управление проектом

### Запуск и остановка
```bash
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
```bash
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
```bash
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
```bash
docker-compose exec backend python manage.py test
```

### Проверка кода
```bash
docker-compose exec backend flake8
```

### Создание миграций
```bash
docker-compose exec backend python manage.py makemigrations
```

### Отладка контейнеров
```bash
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
```bash
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
- GitHub: https://github.com/STIMPEM 
