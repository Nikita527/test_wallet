# Wallet Service

## Описание

Микросервис для управления кошельками пользователей. Позволяет создавать кошельки, пополнять баланс, снимать средства и получать текущий баланс. Все операции безопасны для конкурентного доступа.

## Технологии

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Alembic (миграции)
- Docker, Docker Compose
- Pytest (тесты)

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone git@github.com:Nikita527/test_wallet.git
```

### 2. Запуск через Docker Compose

Если установлен Make можно запустить проект через Makefile
```bash
make start
```

Если нет Make
```bash
docker-compose -f infra/dev/docker-compose.dev.yaml up -d --build
```

- Приложение будет доступно на [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Миграции

Миграции применяются автоматически при старте контейнера. Если нужно вручную:

```bash
docker-compose exec -f infra/dev/docker-compose.dev.yaml app alembic upgrade head
```

### 4. Тесты

```bash
docker-compose -f infra/dev/docker-compose.dev.yaml app exec pytest
```


---

## API

### Авторизация

- POST `/api/auth/login` — получить JWT токен (username = email, password)
- тестовый пользователь создается автоматически при старте проекта(email = admin@admin.ru, password = admin)
- Все методы кошелька требуют заголовок `Authorization: Bearer <token>`

### Кошелек

- **Создать кошелек**
    - `POST /api/v1/wallets`
    - Ответ: `{ "uuid": "...", "balance": "0.00" }`

- **Получить баланс**
    - `GET /api/v1/wallets/{wallet_uuid}`
    - Ответ: `{ "uuid": "...", "balance": "100.00" }`

- **Операция (DEPOSIT/WITHDRAW)**
    - `POST /api/v1/wallets/{wallet_uuid}/operation`
    - Тело:
      ```
    - Ответ: `{ "uuid": "...", "balance": "..." }`

---

## Примеры запросов

**Создать кошелек**

```bash
curl -X POST http://localhost:8000/api/v1/wallets -H "Authorization: Bearer <token>"
```

**Пополнить баланс**

```bash
bash curl -X POST http://localhost:8000/api/v1/wallets/<uuid>/operation
-H "Authorization: Bearer <token>"
-H "Content-Type: application/json"
-d '{"operation_type": "DEPOSIT", "amount": 1000}'
```

---

## Конкурентная безопасность

- Все операции с балансом используют блокировку строки в базе (`SELECT ... FOR UPDATE`), что гарантирует корректность при параллельных запросах.

---

## Тесты

- Покрывают создание кошелька, операции, ошибки, работу с несуществующим кошельком.
- Для тестов авторизация подменяется фикстурой.

---

## Контакты

Автор: Nikita527
