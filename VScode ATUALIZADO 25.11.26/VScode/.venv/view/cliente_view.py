## .venv\view\cliente_view.py
from decimal import Decimal
from services.loja_services import (
    listar_produtos,
    buscar_produto,
    finalizar_compra,
    listar_compras_cliente,
)


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


def panel_cliente(user_auth):
    carrinho = []

    while True:
        print(f"\n=== PAINEL CLIENTE | {user_auth[1]} ({user_auth[7]}) ===")
        print("1 - Ver produtos a venda")
        print("2 - Carrinho")
        print("3 - Finalizar compra")
        print("4 - Minhas compras")
        print("5 - Deslogar")

        opcao = _ler_inteiro("Digite sua escolha: ")
        if opcao is None:
            continue

        if opcao == 1:
            produtos = listar_produtos()
            print("\n--- PRODUTOS A VENDA ---")
            linhas_produtos = [
                (
                    p[0],
                    p[1],
                    _formatar_moeda(p[3]),
                    p[4],
                    p[2] or "-",
                )
                for p in produtos
            ]
            _imprimir_tabela(
                ["Cod", "Produto", "Preco", "Estoque", "Descricao"],
                linhas_produtos,
                "Nenhum produto disponivel no momento.",
            )

            if produtos:
                add = input("\nDeseja adicionar algum produto ao carrinho? (s/n): ").strip().lower()
                if add == "s":
                    cod = _ler_inteiro("Digite o codigo do produto: ")
                    qtd = _ler_inteiro("Digite a quantidade: ")
                    if cod is not None and qtd is not None:
                        prod = buscar_produto(cod)
                        if prod and qtd > 0 and qtd <= prod[4]:
                            carrinho.append({
                                "codigo_produto": prod[0],
                                "nome": prod[1],
                                "quantidade": qtd,
                                "preco_unitario": float(prod[3]),
                            })
                            print("Produto adicionado ao carrinho!")
                        else:
                            print("Produto invalido ou quantidade maior que o estoque.")

        elif opcao == 2:
            print("\n--- CARRINHO ---")
            if not carrinho:
                print("Carrinho vazio.")
            else:
                total = 0.0
                linhas_carrinho = []
                for idx, item in enumerate(carrinho, start=1):
                    subtotal = item["quantidade"] * item["preco_unitario"]
                    total += subtotal
                    linhas_carrinho.append((
                        idx,
                        item["nome"],
                        item["quantidade"],
                        _formatar_moeda(item["preco_unitario"]),
                        _formatar_moeda(subtotal),
                    ))
                _imprimir_tabela(
                    ["#", "Produto", "Qtd", "Unitario", "Subtotal"],
                    linhas_carrinho,
                )
                print(f"Total parcial: {_formatar_moeda(total)}")

                remover = input("\nDeseja remover algum item do carrinho? (s/n): ").strip().lower()
                if remover == "s":
                    num_item = _ler_inteiro("Digite o numero (#) do item para remover: ")
                    if num_item is not None and 1 <= num_item <= len(carrinho):
                        removido = carrinho.pop(num_item - 1)
                        print(f"Item '{removido['nome']}' removido do carrinho.")
                    else:
                        print("Numero de item invalido.")

        elif opcao == 3:
            if finalizar_compra(user_auth[0], carrinho):
                carrinho.clear()

        elif opcao == 4:
            compras = listar_compras_cliente(user_auth[0])
            print("\n--- MINHAS COMPRAS ---")
            linhas_compras = [
                (
                    c[0],
                    _formatar_data(c[1]),
                    c[2],
                    c[3],
                    _formatar_moeda(c[4]),
                    _formatar_moeda(c[5]),
                    _formatar_moeda(c[6]),
                )
                for c in compras
            ]
            _imprimir_tabela(
                ["Venda #", "Data", "Produto", "Qtd", "Unitario", "Subtotal", "Total Venda"],
                linhas_compras,
                "Voce ainda nao realizou nenhuma compra.",
            )

        elif opcao == 5:
            break

        else:
            print("\n\nEscolha invalida, escolha uma numeração VALIDA!!!!!\n")