import os

CLIENT = os.environ.get("DATABASE_CLIENT", "postgres")
DB_NAME = os.environ.get("DATABASE_NAME", "postgres")
USERNAME = os.environ.get("DATABASE_USERNAME", "postgres")
PASSWORD = os.environ.get("DATABASE_PASSWORD", "postgres")
PORT = os.environ.get("DATABASE_PORT", 5432)


DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{CLIENT}:{PORT}/{DB_NAME}"

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ.get("SECRET_KEY", "change_me_please!")
ALGORITHM = os.environ.get("ALGORITM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
