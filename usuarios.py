from django.db import models
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json

class Usuario(models.Model):
    """
    Modelo simplificado que representa um usuário cadastrado no sistema.
    """
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "usuarios"

    def __str__(self) -> str:
        return self.nome

def listar_usuarios(request: HttpRequest) -> JsonResponse:
    """
    Retorna todos os usuários cadastrados no banco de dados sem expor a senha.
    """
    usuarios = list(Usuario.objects.values("id", "nome", "email"))
    return JsonResponse(usuarios, safe=False, json_dumps_params={"ensure_ascii": False})

@csrf_exempt
def cadastrar_usuario(request: HttpRequest) -> JsonResponse:
    """
    Cadastra um novo usuário com nome, email e senha (armazenada de forma segura).
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            email = data.get("email")
            senha = data.get("senha")

            if not nome or not email or not senha:
                return JsonResponse({"erro": "Nome, email e senha são obrigatórios"}, status=400)

            if Usuario.objects.filter(email=email).exists():
                return JsonResponse({"erro": "Este email já está cadastrado"}, status=400)

            usuario = Usuario.objects.create(
                nome=nome,
                email=email,
                senha=make_password(senha)
            )
            return JsonResponse({"id": usuario.id, "status": "cadastrado com sucesso"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"erro": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
            
    return JsonResponse({"erro": "Método não permitido"}, status=405)

@csrf_exempt
def login_usuario(request: HttpRequest) -> JsonResponse:
    """
    Autentica um usuário verificando a correspondência do email e da senha.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            senha = data.get("senha")

            if not email or not senha:
                return JsonResponse({"erro": "Email e senha são obrigatórios"}, status=400)

            try:
                usuario = Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                return JsonResponse({"erro": "Credenciais inválidas"}, status=401)

            if check_password(senha, usuario.senha):
                return JsonResponse({
                    "mensagem": "Login realizado com sucesso",
                    "usuario": {
                        "id": usuario.id,
                        "nome": usuario.nome,
                        "email": usuario.email
                    }
                }, status=200)
            
            return JsonResponse({"erro": "Credenciais inválidas"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"erro": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
            
    return JsonResponse({"erro": "Método não permitido"}, status=405)