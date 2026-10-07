import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="segredo-para-testes-e-desenvolvimento",
        ROOT_URLCONF="manage",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "usuarios",
        ],
        MIDDLEWARE=[
            "django.middleware.common.CommonMiddleware",
        ],
    )

from django.urls import path
from usuarios import listar_usuarios, cadastrar_usuario, login_usuario

urlpatterns = [
    path("", listar_usuarios),
    path("cadastro/", cadastrar_usuario),
    path("login/", login_usuario),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)