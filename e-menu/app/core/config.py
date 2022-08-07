import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    CLIENT: str = os.environ.get("DATABASE_CLIENT", "postgres")
    DB_NAME: str = os.environ.get("DATABASE_NAME", "postgres")
    USERNAME: str = os.environ.get("DATABASE_USERNAME", "postgres")
    PASSWORD: str = os.environ.get("DATABASE_PASSWORD", "postgres")
    PORT: int = int(os.environ.get("DATABASE_PORT", 5432))

    DATABASE_URL: str = f"postgresql://{USERNAME}:{PASSWORD}@{CLIENT}:{PORT}/{DB_NAME}"

    # APP description
    APP_TITLE: str = "e-MENU app for managing menus and dishes"
    APP_DESCRIPTION: str = """
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

    # V1 api root path prefix
    API_V1_PREFIX: str = os.environ.get("API_V1_PREFIX", "/v1")

    # CORS origin
    BACKEND_CORS_ORIGINS: str = os.environ.get("BACKEND_CORS_ORIGINS", "*")

    # Password hashing and token
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "change_me_please!")
    ALGORITHM: str = os.environ.get("ALGORITM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


settings = Settings()
