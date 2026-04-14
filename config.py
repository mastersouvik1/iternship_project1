import os


# class Config:
#     SECRET_KEY = "super-secret-key-123"
#     SQLALCHEMY_DATABASE_URI =  "sqlite:///app.db"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     # Add other configuration variables as needed



BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI =  "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
