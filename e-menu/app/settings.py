import os

CLIENT = os.environ.get("DATABASE_CLIENT", "postgres")
DB_NAME = os.environ.get("DATABASE_NAME", "postgres")
USERNAME = os.environ.get("DATABASE_USERNAME", "postgres")
PASSWORD = os.environ.get("DATABASE_PASSWORD", "postgres")
PORT = os.environ.get("DATABASE_PORT", 5432)

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{CLIENT}:{PORT}/{DB_NAME}"


APP_TITLE = "e-MENU app for managing menus and dishes"
APP_DESCRIPTION = """
## API developed using FastAPI 🚀 🚀 🚀

### In MENU section you can:
* **Read, order and filter menu items**.
* **Create menu item**.
* **Update menu item**.
* **Delete menu item**.
* **Add dish to menu**.
* **Delete dish from menu**.

## In dish section you are able to:
* **Read all dishes**.
* **Create new dish**.
* **Update existing dish**.
* **Delete existing dish**.

## In user section you can:
* **Create new user**
"""

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ.get("SECRET_KEY", "change_me_please!")
ALGORITHM = os.environ.get("ALGORITM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
