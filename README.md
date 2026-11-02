# Connect — платформа поиска тиммейтов для студентов

Telegram-бот + Mini App + админ-панель на одном FastAPI-бэкенде и одной PostgreSQL.

> 🚧 Проект в активной разработке: часть модулей в работе (см. структуру ниже).

## Что умеет
- **Seeker** — ищет команду: анкета + отклики на проекты.
- **Recruiter** — набирает команду: объявления и приглашения.
- **Social** — подбор по интересам.
- Взаимный интерес → **match** → открываются контакты.

## Стек

**Бэкенд и API**
- Python 3.12+
- FastAPI (OpenAPI на `/docs`)
- uvicorn
- aiogram 3 + RedisStorage (FSM)
- Pydantic v2 + pydantic-settings

**Данные**
- PostgreSQL 17
- SQLAlchemy 2.0 async + asyncpg
- Alembic (миграции)
- Redis 7 (FSM бота + кэш)

**Фронтенд**
- Vite
- @telegram-apps/sdk (Mini App)
- Chart.js (админка)
- vanilla JS

**DevOps и тесты**
- Docker + Docker Compose
- pytest + pytest-asyncio + httpx
- ruff (lint + format) + pre-commit
- GitHub Actions (CI) → Render (CD)

## Архитектура
Слои: **интерфейсы** (bot / miniapp / admin_ui) → **services** → **repositories** → **PostgreSQL**.
Бизнес-логики в роутерах и хендлерах нет. Подробно — [docs/architecture.md](docs/architecture.md).

## Структура репозитория
```
Connect/
├── src/connect/         # Python-пакет (src-layout)
│   ├── __init__.py
│   ├── main.py          # точка входа FastAPI
│   ├── bot/             # aiogram 3: роутеры, FSM, keyboards, middlewares
│   ├── api/             # routers, telegram_auth, admin_routes, exceptions
│   ├── core/            # config, db, redis, logging
│   ├── models/          # SQLAlchemy-таблицы
│   ├── schemas/         # Pydantic-схемы
│   ├── repositories/    # доступ к БД (AsyncSession)
│   ├── services/        # бизнес-логика, чистые функции
│   └── migrations/      # Alembic
├── miniapp/             # Vite + @telegram-apps/sdk (сборка раздаётся FastAPI)
├── admin_ui/            # статика админки (HTML/JS + Chart.js)
├── tests/               # unit/ и integration/
├── docs/                # архитектура, QA-чек-листы
├── pyproject.toml       # зависимости + конфиг ruff/pytest
├── .env.example         # шаблон переменных окружения
├── .github/workflows/   # CI
├── Dockerfile
└── docker-compose.yml
```

## Быстрый старт (локально)

> ⚠️ Пока в репо нет `pyproject.toml`, `alembic.ini` и `docker-compose.yml` — шаги 2, 3 и 5 **не пройдут**. Они описывают **целевой** запуск; по мере добавления файлов (см. issue) — заработают.

1. **Клонировать репо и создать venv:**
   ```bash
   git clone https://github.com/rodof-collab/Connect
   cd Connect
   python3.12 -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   ```
2. **Установить пакет в editable-режиме с dev-зависимостями:**
   ```bash
   pip install -e ".[dev]"
   # ⚠️ требует pyproject.toml с [project.optional-dependencies] dev
   ```
3. **Скопировать `.env.example` → `.env` и заполнить:**
   ```dotenv
   DATABASE_URL=postgresql+asyncpg://connect:connect@localhost:5432/connect
   REDIS_URL=redis://localhost:6379/0
   BOT_TOKEN=<токен из @BotFather>
   ADMIN_IDS=123456789,987654321
   # ADMIN_IDS парсится как list[int] через pydantic-валидатор в core/config.py
   ```
4. **Поднять Postgres и Redis** (⚠️ требует `docker-compose.yml` с healthcheck):
   ```bash
   docker compose up -d --wait postgres redis
   ```
   `--wait` ждёт `healthy`-статуса контейнеров, чтобы `alembic upgrade` не упал с `connection refused`.
5. **Применить миграции:**
   ```bash
   alembic upgrade head
   # ⚠️ требует alembic.ini в корне (script_location = src/connect/migrations)
   ```
6. **Собрать Mini App** (⚠️ требует `miniapp/package.json`):
   ```bash
   cd miniapp && npm ci && npm run build && cd ..
   ```
   Сборка кладётся в `miniapp/dist/` и раздаётся FastAPI как статика.
7. **Запустить API:**
   ```bash
   uvicorn connect.main:app --reload --app-dir src
   # ⚠️ требует app = FastAPI(...) в main.py
   ```
8. Открыть http://localhost:8000/docs

## Команды разработчика
```bash
ruff check .        # линт
ruff format .       # формат
pytest -q           # тесты
pre-commit install  # один раз — хук на commit
```

## CI/CD
GitHub Actions: `ruff` → `alembic upgrade head` → `pytest` (Postgres через `services:`).
Деплой на Render — автоматически из `main` после зелёного CI.

## Команда
См. [CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензия
См. [LICENSE](LICENSE).
