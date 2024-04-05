"""SQLAlchemy Engine singleton"""

import os
from sqlalchemy import create_engine

postgres_port = os.environ.get("POSTGRES_PORT")

with open(os.environ["POSTGRES_USER_FILE"], "r", encoding="utf-8") as f:
    postgres_user = f.read().strip()

with open(os.environ["POSTGRES_PASSWORD_FILE"], "r", encoding="utf-8") as f:
    postgres_password = f.read().strip()

with open(os.environ["POSTGRES_DB_FILE"], "r", encoding="utf-8") as f:
    postgres_db = f.read().strip()

connection_uri = f"postgresql+psycopg://{postgres_user}:{postgres_password}@db:{postgres_port}/{postgres_db}"

raw_uri = connection_uri.replace("postgresql+psycopg", "postgresql")

engine = create_engine(
    connection_uri,
    echo=True,
)
