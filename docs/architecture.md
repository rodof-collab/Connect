# Архитектура Connect

## Компоненты

```mermaid
flowchart LR
    subgraph Clients[Интерфейсы]
        BOT[Telegram Bot<br/>aiogram 3]
        MA[Mini App<br/>Vite + @telegram-apps/sdk]
        ADM[Admin UI<br/>HTML + Chart.js]
    end

    subgraph API[FastAPI]
        R1[Bot webhook / API]
        R2[User API<br/>initData HMAC]
        R3[Admin API<br/>ADMIN_IDS]
    end

    subgraph Logic[Бизнес-слой]
        S[services<br/>мэтчинг, приглашения]
        REPO[repositories<br/>AsyncSession]
    end

    PG[(PostgreSQL 17)]
    RD[(Redis 7<br/>FSM + cache)]

    BOT --> R1
    MA  --> R2
    ADM --> R3
    R1 --> S
    R2 --> S
    R3 --> S
    S --> REPO --> PG
    BOT -.FSM.-> RD
    S -.cache.-> RD
```

## Поток запроса

1. Интерфейс (bot/miniapp/admin_ui) вызывает API.
2. Роутер валидирует входные данные (Pydantic v2) и вызывает `service`.
3. Service — чистая бизнес-логика, вызывает `repository`.
4. Repository — единственное место с SQLAlchemy-запросами.
5. Ответ — через Pydantic-схему; ошибки — единым форматом через exception-хендлеры.

## Слои и правила

| Слой | Где лежит | Можно | Нельзя |
|---|---|---|---|
| Интерфейсы | `src/connect/bot/`, `src/connect/api/routers/`, `miniapp/`, `admin_ui/` | валидация, вызов сервиса | SQL, бизнес-логика |
| Services | `src/connect/services/` | бизнес-логика, вызов repo | SQL-запросы напрямую |
| Repositories | `src/connect/repositories/` | SQLAlchemy-запросы | бизнес-решения |
| Модели | `src/connect/models/` | описание таблиц | логика |

## Ключевые инварианты

- Бизнес-логики в роутерах и хендлерах нет.
- SQL — только в `repositories/`.
- Datetime — только timezone-aware, храним в UTC.
- Секреты — только в `.env` через `pydantic-settings`.
- Весь Python — async, type hints везде, `ruff` чистый.
