import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manage")
django.setup()

from django.test import TestCase, Client
from usuarios import Usuario

class UsuariosTestCase(TestCase):
    """
    Conjunto de testes automatizados para verificar as operações de Cadastro e Login.
    """
    def setUp(self) -> None:
        self.client = Client()

    def test_fluxo_cadastro_e_login(self) -> None:
        payload_cadastro = {
            "nome": "Carlos Silva",
            "email": "carlos@example.com",
            "senha": "senha123"
        }
        
        # 1. Tenta cadastrar um novo usuário
        response_cadastro = self.client.post(
            "/cadastro/",
            data=json.dumps(payload_cadastro),
            content_type="application/json"
        )
        self.assertEqual(response_cadastro.status_code, 201)
        self.assertIn("id", response_cadastro.json())

        # 2. Tenta listar os usuários para confirmar cadastro
        response_listar = self.client.get("/")
        self.assertEqual(response_listar.status_code, 200)
        usuarios = response_listar.json()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0]["email"], "carlos@example.com")

        # 3. Tenta realizar login correto
        payload_login_valido = {
            "email": "carlos@example.com",
            "senha": "senha123"
        }
        response_login_valido = self.client.post(
            "/login/",
            data=json.dumps(payload_login_valido),
            content_type="application/json"
        )
        self.assertEqual(response_login_valido.status_code, 200)
        self.assertIn("usuario", response_login_valido.json())

        # 4. Tenta realizar login com senha incorreta
        payload_login_invalido = {
            "email": "carlos@example.com",
            "senha": "senha_errada"
        }
        response_login_invalido = self.client.post(
            "/login/",
            data=json.dumps(payload_login_invalido),
            content_type="application/json"
        )
        self.assertEqual(response_login_invalido.status_code, 401)