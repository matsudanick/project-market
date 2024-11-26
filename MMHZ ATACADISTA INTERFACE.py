import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

inventario = []

def salvar_inventario():
    with open("inventario.txt", "w") as arquivo:
        for produto in inventario:
            linha = f"{produto[0]},{produto[1]},{produto[2]},{produto[3]},{produto[4]}\n"
            arquivo.write(linha)

def carregar_inventario():
    try:
        with open("inventario.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                produto = [int(dados[0]), dados[1], dados[2], int(dados[3]), float(dados[4])]
                inventario.append(produto)
    except FileNotFoundError:
        pass

def My_Select():
    tree.delete(*tree.get_children())
    for produto in inventario:
        tree.insert('', 'end', values=produto)

def filtrar_produtos():
    filtro = filtro_entry.get().lower()
    tree.delete(*tree.get_children())
    for produto in inventario:
        if filtro.isdigit():
            try:
                preco_limite = float(filtro)
                if produto[4] <= preco_limite:
                    tree.insert('', 'end', values=produto)
            except ValueError:
                pass
        else:
            if filtro in produto[1].lower():
                tree.insert('', 'end', values=produto)

def adicionar_produto():
    codigo = simpledialog.askinteger("Código do produto", "Digite o código do produto:")
    if codigo is None or codigo < 0:
        return

    for produto in inventario:
        if produto[0] == codigo:
            messagebox.showerror("Erro", f"Produto com o código {codigo} já existe!")
            return

    categoria = simpledialog.askstring("Categoria do produto", "Digite a categoria do produto:")
    if categoria is None or not categoria.isalpha():
        messagebox.showerror("Erro", "Categoria inválida!")
        return

    produto = simpledialog.askstring("Nome do produto", "Digite o nome do produto:")
    if produto is None or not all(c.isalpha() or c.isspace() or c == '-' for c in produto):
        messagebox.showerror("Erro", "Nome do produto inválido!")
        return

    quantidade = simpledialog.askinteger("Quantidade do produto", "Digite a quantidade do produto:")
    if quantidade is None or quantidade < 0:
        messagebox.showerror("Erro", "Quantidade inválida!")
        return

    preco = simpledialog.askfloat("Preço do produto", "Digite o preço do produto:")
    if preco is None or preco < 0:
        messagebox.showerror("Erro", "Preço inválido!")
        return

    inventario.append([codigo, categoria, produto, quantidade, preco])
    salvar_inventario()
    My_Select()
    messagebox.showinfo("Sucesso", f"Produto {produto} adicionado ao inventário com sucesso!")

def alterar_produto():
    codigo = simpledialog.askinteger("Código do produto", "Digite o código do produto que deseja alterar:")
    if codigo is None or codigo < 0:
        return

    for produto in inventario:
        if produto[0] == codigo:
            novo_produto = simpledialog.askstring("Nome do produto", f"Digite o novo nome do produto (atualmente: {produto[2]}): ")
            nova_categoria = simpledialog.askstring("Categoria do produto", f"Digite a nova categoria do produto (atualmente: {produto[1]}): ")
            nova_quantidade = simpledialog.askinteger("Quantidade do produto", f"Digite a nova quantidade do produto (atualmente: {produto[3]}): ")
            novo_preco = simpledialog.askfloat("Preço do produto", f"Digite o novo preço do produto (atualmente: {produto[4]}): ")

            if novo_produto:
                produto[2] = novo_produto
            if nova_categoria:
                produto[1] = nova_categoria
            if nova_quantidade is not None:
                produto[3] = nova_quantidade
            if novo_preco is not None:
                produto[4] = novo_preco

            salvar_inventario()
            My_Select()
            messagebox.showinfo("Sucesso", f"Produto {produto[2]} alterado com sucesso!")
            return

    messagebox.showerror("Erro", "Produto não encontrado no inventário.")

def excluir_produto():
    codigo = simpledialog.askinteger("Código do produto", "Digite o código do produto que deseja excluir:")
    if codigo is None or codigo < 0:
        return

    for produto in inventario:
        if produto[0] == codigo:
            inventario.remove(produto)
            salvar_inventario()
            My_Select()
            messagebox.showinfo("Sucesso", f"Produto com código {codigo} excluído com sucesso!")
            return

    messagebox.showerror("Erro", "Produto não encontrado no inventário.")

def relatorio_geral():
    global tree, filtro_frame
    if 'tree' not in globals():
        columns = ('Codigo', 'Categoria', 'Produto', 'Quantidade', 'Preço')
        tree = ttk.Treeview(Janela, columns=columns, show='headings')
        tree.column('Codigo', width=100)
        tree.column('Categoria', width=150)
        tree.column('Produto', width=150)
        tree.column('Quantidade', width=100)
        tree.column('Preço', width=100)
        tree.heading('Codigo', text='Código')
        tree.heading('Categoria', text='Categoria')
        tree.heading('Produto', text='Produto')
        tree.heading('Quantidade', text='Quantidade')
        tree.heading('Preço', text='Preço')
        tree.pack(fill=tk.BOTH, expand=True)

    filtro_frame.pack()
    My_Select()

def sair_programa():
    salvar_inventario()
    Janela.quit()

def menu():
    global Janela, filtro_entry, filtro_frame
    Janela = tk.Tk()
    Janela.title("𝙼𝙼𝙷𝚉 𝙰𝚃𝙰𝙲𝙰𝙳𝙸𝚂𝚃𝙰")

    style = ttk.Style(Janela)
    style.theme_use("clam")  
    style.configure("TButton", padding=10, relief="flat")  
    style.configure("TLabel", font=("Helvetica", 12))  
    style.configure("Treeview", rowheight=30, font=("Helvetica", 10))  

    Janela.configure(background="#f0f0f0")
    title = tk.Label(Janela, text="MMHZ ATACADISTA", font=("Helvetica", 16, "bold"), background="#f0f0f0", foreground="#333333")
    title.pack(pady=10)

    subtitle = tk.Label(Janela, text="Olá, seja bem-vindo ao menu do inventário:", background="#f0f0f0", foreground="#333333")
    subtitle.pack()

    button_frame = ttk.Frame(Janela)
    button_frame.pack(pady=10)

    btn_style = {"fill": tk.X, "padx": 5, "pady": 5}
    ttk.Button(button_frame, text="Adicionar produto", command=adicionar_produto, style="TButton").grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Excluir produto", command=excluir_produto, style="TButton").grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Alterar produto", command=alterar_produto, style="TButton").grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Relatório Geral", command=relatorio_geral, style="TButton").grid(row=3, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Sair", command=sair_programa, style="TButton").grid(row=4, column=0, padx=5, pady=5)

    footer = tk.Label(Janela, text="𝘊𝘰𝘱𝘺𝘳𝘪𝘨𝘩𝘵 © 2024. 𝘈𝘭𝘭 𝘳𝘪𝘨𝘩𝘵𝘴 𝘳𝘦𝘴𝘦𝘳𝘷𝘦𝘥 𝘣𝘺 𝘔𝘔𝘏𝘡 𝘈𝘵𝘢𝘤𝘢𝘥𝘪𝘴𝘵𝘢.", font=("Helvetica", 8), background="#f0f0f0", foreground="#333333")
    footer.pack(pady=10)

    filtro_frame = tk.Frame(Janela)
    filtro_label = tk.Label(filtro_frame, text="Digite a categoria ou preço para filtrar:")
    filtro_label.pack()
    filtro_entry = tk.Entry(filtro_frame)
    filtro_entry.pack(padx=10, pady=5)
    filtro_button = ttk.Button(filtro_frame, text="Filtrar", command=filtrar_produtos, style="TButton")
    filtro_button.pack(pady=5)

    Janela.geometry("900x600")
    Janela.mainloop()

carregar_inventario()
menu()
