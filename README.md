# Crypto Bot

A Python-based futures trading bot for Bybit with a Streamlit dashboard and PostgreSQL storage.

## Tech Stack

- Python 3.11+
- Bybit API
- Streamlit
- PostgreSQL
- SQLAlchemy
- Alembic
- pandas / numpy
- pytest

## Project Structure

```text
app/
├─ bot/
├─ config/
├─ domain/
├─ infrastructure/
├─ services/
├─ dashboard/
├─ api/
└─ utils/

scripts/
tests/
alembic/
```

## Setup

### 1. Create virtual environment

```bash
python -m venv .venv
```

Purpose:
Creates an isolated Python environment for this project.

### 2. Activate virtual environment

```bash
.\.venv\Scripts\activate
```

Purpose:
Ensures package installs go into the project environment only.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Purpose:
Installs all runtime and test libraries required by the project.

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your credentials.

Purpose:
Keeps secrets and environment-specific values outside of source code.

### 5. Run the app entrypoint

```bash
python app/main.py
```

Purpose:
Runs the bot runner entrypoint.

### 6. Run dashboard

```bash
streamlit run app/dashboard/streamlit_app.py
```

Purpose:
Launches the Streamlit UI dashboard.

### 7. Run tests

```bash
pytest
```

Purpose:
Runs the test suite.

## PostgreSQL Setup

This project uses your **local PostgreSQL installation** directly.

Recommended `.env` value:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/crypto_bot
```

Adjust the username, password, host, port, and database name to match your local PostgreSQL configuration.

## Next Milestones

- Implement configuration loader
- Implement PostgreSQL connection validation
- Implement Bybit client wrapper
- Implement core trading services
- Implement Streamlit dashboard pages
