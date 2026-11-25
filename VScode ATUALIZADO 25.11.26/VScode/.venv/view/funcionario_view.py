##.venv\view\funcionario_view.py
from decimal import Decimal
from services.task_services import (
    create_task,
    search_tasks,
    remove_task,
    update_task,
    join_vendas_cliente_funcionario,
    join_itens_venda_detalhados,
    join_clientes_e_tasks,
    join_vendas_por_funcionario,
    join_itens_com_cliente,
)
from services.produtos_services import list_produtos, add_produto, update_produto


def _formatar_moeda(valor) -> str:
    try:
        return f"R$ {Decimal(str(valor)):.2f}".replace(".", ",")
    except Exception:
        return str(valor)


def _formatar_data(data) -> str:
    if hasattr(data, "strftime"):
        return data.strftime("%d/%m/%Y")
    return str(data)


def _ler_inteiro(mensagem: str) -> int | None:
    while True:
        valor = input(mensagem).strip()
        try:
            return int(valor)
        except ValueError:
            print("Entrada invalida! Digite apenas numeros inteiros.")


def _ler_float(mensagem: str) -> float | None:
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("Entrada invalida! Digite um numero valido (ex: 49.90).")


def _imprimir_tabela(colunas: list[str], linhas: list[tuple], mensagem_vazia: str = "Nenhum registro encontrado."):
    if not linhas:
        print(mensagem_vazia)
        return

    formatadas = [[str(campo) if campo is not None else "-" for campo in linha] for linha in linhas]
    larguras = [len(col) for col in colunas]

    for linha in formatadas:
        for i, valor in enumerate(linha):
            if i < len(larguras) and len(valor) > larguras[i]:
                larguras[i] = len(valor)

    cabecalho = " | ".join(col.ljust(larguras[i]) for i, col in enumerate(colunas))
    separador = "-+-".join("-" * larguras[i] for i in range(len(colunas)))

    print(cabecalho)
    print(separador)
    for linha in formatadas:
        preenchida = [linha[i] if i < len(linha) else "" for i in range(len(colunas))]
        print(" | ".join(preenchida[i].ljust(larguras[i]) for i in range(len(colunas))))


def _exibir_relatorios_joins():
    print("\n=== RELATORIOS ANALITICOS (JOINS) ===")

    print("\n--- Vendas, Cliente e Funcionario ---")
    dados_j1 = join_vendas_cliente_funcionario()
    linhas_j1 = [
        (r[0], _formatar_data(r[1]), _formatar_moeda(r[2]), r[3], r[4], r[5])
        for r in dados_j1
    ]
    _imprimir_tabela(
        ["Venda #", "Data", "Total", "Cliente", "Responsavel", "Cargo"],
        linhas_j1,
        "Nenhuma venda registrada.",
    )

    print("\n--- Join 2: Itens de Venda Detalhados ---")
    dados_j2 = join_itens_venda_detalhados()
    linhas_j2 = [
        (r[0], r[1], r[2], r[3], _formatar_moeda(r[4]), _formatar_moeda(r[5]))
        for r in dados_j2
    ]
    _imprimir_tabela(
        ["Venda #", "Cliente", "Produto", "Qtd", "Unitario", "Subtotal"],
        linhas_j2,
        "Nenhum item de venda encontrado.",
    )

    print("\n--- Clientes e Tasks ---")
    dados_j3 = join_clientes_e_tasks()
    _imprimir_tabela(
        ["ID", "Cliente", "Cargo", "ID Task", "Tarefa"],
        dados_j3,
        "Nenhum cliente encontrado.",
    )

    print("\n--- Vendas por Funcionario ---")
    dados_j4 = join_vendas_por_funcionario()
    linhas_j4 = [
        (r[0], r[1], r[2], r[3], _formatar_moeda(r[4]))
        for r in dados_j4
    ]
    _imprimir_tabela(
        ["ID", "Funcionario", "Cargo", "Total Vendas", "Faturamento"],
        linhas_j4,
        "Nenhum funcionario encontrado.",
    )

    print("\n--- tens Vendidos por Cliente (ID, Nome e Cargo) ---")
    dados_j5 = join_itens_com_cliente()
    linhas_j5 = [
        (r[0], r[1], r[2], r[3], r[4], r[5], _formatar_moeda(r[6]), _formatar_moeda(r[7]))
        for r in dados_j5
    ]
    _imprimir_tabela(
        ["Venda #", "ID Cliente", "Cliente", "Cargo", "Item", "Qtd", "Unitario", "Subtotal"],
        linhas_j5,
        "Nenhum item encontrado para clientes.",
    )


def panel_funcionario(user_auth):
    while True:
        print(f"\nBem vindo {user_auth[1]} ({user_auth[7]})")
        print("1 - Cadastrar Task")
        print("2 - Buscar Task")
        print("3 - Remover Task")
        print("4 - Atualizar Task")
        print("5 - Adicionar Produto")
        print("6 - Atualizar Produto")
        print("7 - Relatorios")
        print("8 - Deslogar")

        opcao = _ler_inteiro("Digite sua escolha: ")
        if opcao is None:
            continue

        if opcao == 1:
            title = input("Digite uma tarefa: ").strip()
            if title:
                create_task(user_auth[0], title)
            else:
                print("A tarefa nao pode ficar em branco.")

        elif opcao == 2:
            tasks = search_tasks(user_auth[0])
            print("\n--- Suas Tasks ---")
            _imprimir_tabela(["ID", "Tarefa"], [(t[0], t[1]) for t in tasks], "Nenhuma task cadastrada.")

        elif opcao == 3:
            tasks = search_tasks(user_auth[0])
            if not tasks:
                print("Nenhuma task encontrada para remover.")
            else:
                print("\n--- Suas Tasks ---")
                _imprimir_tabela(["ID", "Tarefa"], [(t[0], t[1]) for t in tasks])
                task_id = _ler_inteiro("Digite o ID da task para remover: ")
                if task_id is not None:
                    remove_task(task_id)

        elif opcao == 4:
            tasks = search_tasks(user_auth[0])
            if not tasks:
                print("Nenhuma task encontrada para atualizar.")
            else:
                print("\n--- Suas Tasks ---")
                _imprimir_tabela(["ID", "Tarefa"], [(t[0], t[1]) for t in tasks])
                task_id = _ler_inteiro("Digite o ID da task para atualizar: ")
                if task_id is not None:
                    new_title = input("Digite o novo titulo: ").strip()
                    if new_title:
                        update_task(task_id, new_title)
                    else:
                        print("O novo titulo nao pode ficar em branco.")

        elif opcao == 5:
            nome = input("Digite o nome do produto: ").strip()
            descricao = input("Digite a descricao do produto: ").strip()
            preco = _ler_float("Digite o preco do produto: ")
            estoque = _ler_inteiro("Digite a quantidade em estoque: ")
            if nome and preco is not None and estoque is not None:
                add_produto(nome, descricao, preco, estoque)
            else:
                print("Nome do produto nao pode ficar em branco.")

        elif opcao == 6:
            produtos = list_produtos()
            if not produtos:
                print("Nenhum produto cadastrado.")
            else:
                print("\n--- Produtos Cadastrados ---")
                _imprimir_tabela(
                    ["Codigo", "Nome", "Preco", "Estoque"],
                    [(p[0], p[1], _formatar_moeda(p[3]), p[4]) for p in produtos],
                )
                codigo_produto = _ler_inteiro("Digite o codigo do produto para atualizar: ")
                novo_preco = _ler_float("Digite o novo preco: ")
                novo_estoque = _ler_inteiro("Digite o novo estoque: ")
                if codigo_produto is not None and novo_preco is not None and novo_estoque is not None:
                    update_produto(codigo_produto, novo_preco, novo_estoque)

        elif opcao == 7:
            _exibir_relatorios_joins()

        elif opcao == 8:
            break

        else:
            print("\n\nEscolha invalida, escolha uma numeração VALIDA!!!!!\n")