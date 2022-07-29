import os

CLIENT = os.environ.get("DATABASE_CLIENT", "postgres")
DB_NAME = os.environ.get("DATABASE_NAME", "postgres")
USERNAME = os.environ.get("DATABASE_USERNAME", "postgres")
PASSWORD = os.environ.get("DATABASE_PASSWORD", "postgres")
PORT = os.environ.get("DATABASE_PORT", 5432)


DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{CLIENT}:{PORT}/{DB_NAME}"
