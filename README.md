# Gestor de Usuários

Este é um projeto funcional e minimalista construído em Django para gerenciar o cadastro e login de usuários de forma ágil e sem complicações de configuração.

## Funcionalidades

- Listar usuários cadastrados (sem expor senhas).
- Cadastrar novos usuários via requisição JSON com criptografia de senha.
- Autenticar usuários via login com verificação segura de credenciais.

## Como Executar

1. Instale o Django:
```bash
pip install django
```

2. Inicialize as tabelas do banco de dados (SQLite embutido):
```bash
python manage.py migrate
```

3. Inicie o servidor:
```bash
python manage.py runserver
```

## Como Testar

Para executar os testes automatizados da aplicação:
```bash
python manage.py test tests
```