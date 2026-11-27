##.venv\main.py
##  SUS    ඞ  SUS    ඞ  SUS    ඞ  SUS    ඞ  SUS    ඞ  SUS    ඞ  SUS    ඞ  SUS    ඞ  SUS    ඞ  SUS    ඞ

import getpass
from services.User_services import import_user, login
from view.admin_view import panel
from view.funcionario_view import panel_funcionario
from view.cliente_view import panel_cliente

try:
    import msvcrt
except ImportError:
    msvcrt = None


def ler_senha(mensagem: str = "Digite sua senha: ") -> str:
    print(mensagem, end="", flush=True)

    if msvcrt is None:
        return getpass.getpass("")

    chars = []
    while True:
        tecla = msvcrt.getwch()

        if tecla in ("\r", "\n"):
            print()
            return "".join(chars)
        elif tecla == "\x03":
            print()
            raise KeyboardInterrupt
        elif tecla == "\b":
            if chars:
                chars.pop()
                print("\b \b", end="", flush=True)
        elif tecla in ("\x00", "\xe0"):
            msvcrt.getwch()
        elif tecla >= " ":
            chars.append(tecla)
            print("*", end="", flush=True)


while True:
    try:
        print("\n1 - Criar novo usuario\n2 - Sou cadastrado\n3 - Sair")
        opcao = int(input("Digite uma opção, preferencialmente valida: "))

        if opcao == 1:
            nome = input("Digite seu Nome completo: ")
            email = input("Digite seu Email: ")
            senha = ler_senha("Digite sua Senha: ")
            telefone = input("Digite seu numero de telefone com DDD da sua cidade: ")
            endereco = input("Digite seu endereço: ")
            cpf = ler_senha("Digite seu CPF: ")
            import_user(nome, email, senha, telefone, endereco, cpf, "Cliente")
        elif opcao == 2:
            email = input("Digite seu Email: ")
            senha = ler_senha("Digite sua senha: ")
            user_auth = login(email, senha)
            if user_auth:  # DEFINE SE É CLIENTE, FUNCIONARIO OU ADM
                cargo = user_auth[7].strip().lower()
                if cargo == "administrador":
                    panel(user_auth)
                elif cargo in ("funcionario", "funcionário"):
                    panel_funcionario(user_auth)
                else:
                    panel_cliente(user_auth)
            else:
                print("Usuario ou senha inválido")
        elif opcao == 3:
            break
        else:
            print("Digite uma opção VALIDA!")
    except ValueError:
        print("Entrada inválida! Digite apenas números.")