import time 
import os
from tabulate import tabulate

# Função para limpar a tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

inventario = []

# Função para salvar os dados no .txt
def salvar_inventario():
    with open("inventario.txt", "w") as arquivo:
        for produto in inventario:
            linha = f"{produto[0]},{produto[1]},{produto[2]},{produto[3]},{produto[4]}\n"
            arquivo.write(linha)

# Função para carregar os dados do .txt
def carregar_inventario():
    try:
        with open("inventario.txt", "r") as arquivo:
            for linha in arquivo:
                try:
                    dados = linha.strip().split(",")
                    if len(dados) != 5:
                        raise ValueError("Linha incompleta.")
                    produto = [int(dados[0]), dados[1], dados[2], int(dados[3]), float(dados[4])]
                    inventario.append(produto)
                except (ValueError, IndexError):
                    print(f"Linha inválida ignorada: {linha.strip()}")
    except FileNotFoundError:
        pass
# Função para adicionar produto ao inventário
def adicionar_produto():
    def obter_codigo():
        while True:
            try:
                codigo = int(input("Digite o código do produto: "))
                if codigo <= 0:
                    print("Erro! O código deve ser maior que zero.")
                    continue
                if any(produto[0] == codigo for produto in inventario):
                    print(f"Erro! O código {codigo} já está cadastrado.")
                    continue 
                return codigo
            except ValueError:
                print("Erro! Digite apenas números válidos.")
                
    def obter_categoria():
        while True:
            categoria = input("Digite a categoria do produto: ").strip()
            if categoria.isalpha():
                return categoria
            else:
                print("Erro! Digite uma categoria válida (Apenas letras).")

    def obter_produto():
        while True:
            produto = input("Digite o nome do produto: ").strip()
            if produto:
                partes = produto.split()
            if all(c.isalpha() or c == '-' for c in partes[0]):
                if len(partes) > 1 and all(c.isalnum() or c == '-' for c in partes[1]):
                    return produto
                elif len(partes) == 1:
                    return produto
                print("Erro! Digite um nome válido (letras na primeira parte, letras/números na segunda).")
                
    def obter_quantidade():
        while True:
            try:
                quantidade = int(input("Digite a quantidade do produto: "))
                if quantidade < 0:
                    print("Erro! Digite um número válido.")
                else:
                    return quantidade
            except ValueError:
                print("Erro! Digite apenas números.")

    def obter_preco():
        while True:
            try:
                preco = float(input("Digite o preço do produto: "))
                if preco < 0:
                    print("Erro! Digite um número válido.")
                else:
                    return preco
            except ValueError:
                print("Erro! Digite um número válido.")

    codigo = obter_codigo()
    categoria = obter_categoria()
    produto = obter_produto()
    quantidade = obter_quantidade()
    preco = obter_preco()

    inventario.append([codigo, categoria, produto, quantidade, preco])
    print('''Produto adicionado ao inventário com sucesso!''')
    salvar_inventario()

# Função para excluir produto do inventário
def excluir_produto():
    try:
        codigo = int(input("Digite o código do produto que deseja excluir: "))
    except ValueError:
        print("Erro! Digite um número válido.")
        return

    for produto in inventario:
        if produto[0] == codigo:
            inventario.remove(produto)
            print("Produto excluído do inventário com sucesso!")
            salvar_inventario()
            return

    print("Produto não encontrado!")



# Função para alterar produto do inventário
def alterar_produto():
    try:
        codigo = int(input("Digite o código do produto que deseja alterar: "))
    except ValueError:
        print("Erro! Digite um número válido.")
        return

    for produto in inventario:
        if produto[0] == codigo:
            while True:
                novo_produto = input("Digite o novo nome do produto: ").strip()
                if novo_produto:
                    break
                print("Erro! O nome não pode estar vazio.")
            while True:
                nova_categoria = input("Digite a nova categoria do produto: ").strip()
                if nova_categoria:
                    break
                print("Erro! A categoria não pode estar vazia.")
            try:
                nova_quantidade = int(input("Digite a nova quantidade do produto: "))
                novo_preco = float(input("Digite o novo preço do produto: "))
                if nova_quantidade < 0 or novo_preco < 0:
                    raise ValueError("Valores negativos não são permitidos.")
            except ValueError:
                print("Erro! Digite valores numéricos válidos.")
                return

            produto[2] = novo_produto
            produto[1] = nova_categoria
            produto[3] = nova_quantidade
            produto[4] = novo_preco
            print("Produto alterado com sucesso!")
            salvar_inventario()
            return

    print("Produto não encontrado no inventário.")

# Função de relatório geral dos produtos
def relatorio_geral():
    if inventario:
        headers = ["Código", "Categoria", "Produto", "Quantidade", "Preço"]
        print("\nRelatório Geral do Inventário:")
        print(tabulate(inventario, headers=headers, tablefmt="grid"))
    else:
        print("\nNenhum produto cadastrado no inventário.")

    input("\nPressione Enter para continuar...")
    limpar_tela()

# Função de relatório pela categoria
def relatorio_categoria():
    while True:
        categoria = input("Digite a categoria dos produtos que deseja ver: ").strip()
        if categoria:
            break
        print("Erro! A categoria não pode estar vazia.")
    produtos_filtrados = [p for p in inventario if p[1].lower() == categoria.lower()]
    if produtos_filtrados:
        headers = ["Código", "Categoria", "Produto", "Quantidade", "Preço", "Total"]
        tabela = [[p[0], p[1], p[2], p[3], p[4], p[3] * p[4]] for p in produtos_filtrados]
        print(f"\nRelatório da Categoria '{categoria}':")
        print(tabulate(tabela, headers=headers, tablefmt="grid"))
    else:
        print(f"\nNenhum produto encontrado na categoria '{categoria}'.")
    input("\nPressione Enter para continuar...")
    limpar_tela()


# Função de relatório por preço
def relatorio_preco():
    try:
        preco = float(input("Digite o preço máximo dos produtos que deseja ver: "))
    except ValueError:
        print("Erro! Digite um valor numérico válido.")
        return

    produtos_filtrados = [p for p in inventario if p[4] <= preco]
    if produtos_filtrados:
        headers = ["Código", "Categoria", "Produto", "Quantidade", "Preço", "Total"]
        tabela = [[p[0], p[1], p[2], p[3], p[4], p[3] * p[4]] for p in produtos_filtrados]
        print(f"\nRelatório de Produtos com Preço Até R$ {preco:.2f}:")
        print(tabulate(tabela, headers=headers, tablefmt="grid"))
    else:
        print(f"\nNenhum produto encontrado com preço até R$ {preco:.2f}.")

    input("\nPressione Enter para continuar...")
    limpar_tela()

# Menu principal do inventário
def menu():
    while True:
        time.sleep(1)
        limpar_tela()
        print(''' 
                   /$$      /$$ /$$      /$$ /$$   /$$ /$$$$$$$$                                
                  | $$$    /$$$| $$$    /$$$| $$  | $$|_____ $$                                                                
                  | $$ $$/$$ $$| $$ $$/$$ $$| $$$$$$$$    /$$/                                  
                  | $$  $$$| $$| $$  $$$| $$| $$__  $$   /$$/                                   
                  | $$\  $ | $$| $$\  $ | $$| $$  | $$  /$$/____                                                              
                  |__/     |__/|__/     |__/|__/  |__/|________/                                                                                                                                                                                                                                           
  /$$$$$$  /$$$$$$$$ /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$  /$$$$$$  /$$$$$$$$ /$$$$$$ 
 /$$__  $$|__  $$__//$$__  $$ /$$__  $$ /$$__  $$| $$__  $$|_  $$_/ /$$__  $$|__  $$__//$$__  $$
| $$  \ $$   | $$  | $$  \ $$| $$  \__/| $$  \ $$| $$  \ $$  | $$  | $$  \__/   | $$  | $$  \ $$
| $$$$$$$$   | $$  | $$$$$$$$| $$      | $$$$$$$$| $$  | $$  | $$  |  $$$$$$    | $$  | $$$$$$$$
| $$__  $$   | $$  | $$__  $$| $$      | $$__  $$| $$  | $$  | $$   \____  $$   | $$  | $$__  $$
| $$  | $$   | $$  | $$  | $$| $$    $$| $$  | $$| $$  | $$  | $$   /$$  \ $$   | $$  | $$  | $$
|__/  |__/   |__/  |__/  |__/ \______/ |__/  |__/|_______/ |______/ \______/    |__/  |__/  |__/                                       
Olá, seja bem-vindo ao menu do inventário:
1. Adicionar produto
2. Excluir produto
3. Alterar produto
4. Relatório geral
5. Relatório por categoria
6. Relatório por preço
7. Sair''')
        try:
            opcao = int(input("Digite a opção desejada: "))
            if opcao == 1:
                adicionar_produto()
            elif opcao == 2:
                excluir_produto()
            elif opcao == 3:
                alterar_produto()
            elif opcao == 4:
                relatorio_geral()
            elif opcao == 5:
                relatorio_categoria()
            elif opcao == 6:
                relatorio_preco()
            elif opcao == 7:
                print("Saindo do inventário...")
                salvar_inventario()
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida, digite um número.")

# Carregar os dados armazenados primeiro e iniciar o menu
carregar_inventario()
menu() 