import os

from dotenv import load_dotenv
from spielberg.entrypoint.api import create_app

load_dotenv()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "engineio": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


class BaseAppConfig:
    DEBUG: bool = 1
    TESTING: bool = 1
    SECRET_KEY: str = "secret"
    LOGGING_CONFIG: dict = LOGGING_CONFIG
    DB_TYPE: str = "sqlite"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENV_PREFIX: str = "SERVER"


class LocalAppConfig(BaseAppConfig):
    TESTING: bool = 0


class ProductionAppConfig(BaseAppConfig):
    DEBUG: bool = 0
    TESTING: bool = 0
    SECRET_KEY: str = "production"


configs = dict(local=LocalAppConfig, production=ProductionAppConfig)

app = create_app(app_config=configs[os.getenv("SERVER_ENV", "local")])

if __name__ == "__main__":
    app.run(
        host=os.getenv("SERVER_HOST", app.config["HOST"]),
        port=os.getenv("SERVER_PORT", app.config["PORT"]),
        reloader_type="stat" 
    )
