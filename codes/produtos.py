import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def obter_produtos():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM `produtos`")
    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return produtos


def editar_produto():
    global janela_edicao
    global nome_entry
    global descricao_entry
    global preco_entry
    global quantidade_entry
    global codigo_entry

    item_selecionado = produtos_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um produto para editar.")
        return

    produto_selecionado = produtos_treeview.item(item_selecionado)
    dados_produto = produto_selecionado['values']

    id_atual = dados_produto[0]
    nome_atual = dados_produto[1]
    descricao_atual = dados_produto[2]
    preco_atual = dados_produto[3]
    quantidade_atual = dados_produto[4]
    codigo_atual = dados_produto[5]

    janela_edicao = tk.Toplevel(janela)
    janela_edicao.title("Editar Produto")

    frame_campos = tk.Frame(janela_edicao)
    frame_campos.pack(pady=10)

    nome_label = tk.Label(frame_campos, text="Nome:")
    nome_label.grid(row=0, column=0)

    descricao_label = tk.Label(frame_campos, text="Descrição:")
    descricao_label.grid(row=1, column=0)

    preco_label = tk.Label(frame_campos, text="Preço:")
    preco_label.grid(row=2, column=0)

    quantidade_label = tk.Label(frame_campos, text="Quantidade em Estoque:")
    quantidade_label.grid(row=3, column=0)

    codigo_label = tk.Label(frame_campos, text="Código do Produto:")
    codigo_label.grid(row=4, column=0)

    nome_entry = tk.Entry(frame_campos)
    nome_entry.grid(row=0, column=1)
    nome_entry.insert(tk.END, nome_atual)

    descricao_entry = tk.Entry(frame_campos)
    descricao_entry.grid(row=1, column=1)
    descricao_entry.insert(tk.END, descricao_atual)

    preco_entry = tk.Entry(frame_campos)
    preco_entry.grid(row=2, column=1)
    preco_entry.insert(tk.END, preco_atual)

    quantidade_entry = tk.Entry(frame_campos)
    quantidade_entry.grid(row=3, column=1)
    quantidade_entry.insert(tk.END, quantidade_atual)

    codigo_entry = tk.Entry(frame_campos)
    codigo_entry.grid(row=4, column=1)
    codigo_entry.insert(tk.END, codigo_atual)

    botao_salvar = tk.Button(janela_edicao, text="Salvar",
                             command=lambda: salvar_produto(nome_entry.get(), descricao_entry.get(), preco_entry.get(),
                                                            quantidade_entry.get(), codigo_entry.get()))
    botao_salvar.pack()

    janela_edicao.protocol("WM_DELETE_WINDOW", janela_edicao.destroy)


def salvar_produto(nome, descricao, preco, quantidade, codigo):
    item_selecionado = produtos_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um produto para editar.")
        return

    produto_selecionado = produtos_treeview.item(item_selecionado)
    dados_produto = produto_selecionado['values']
    id_produto = dados_produto[0]

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("UPDATE `produtos` SET Nome = %s, Descricao = %s, Preco = %s, QuantidadeEstoque = %s, codigo_de_produtos = %s WHERE ID = %s", (nome, descricao, preco, quantidade, codigo, id_produto))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")

    janela_edicao.destroy()
    carregar_produtos()


def adicionar_produto():
    janela_adicao = tk.Toplevel(janela)
    janela_adicao.title("Adicionar Produto")

    frame_campos = tk.Frame(janela_adicao)
    frame_campos.pack(pady=10)

    nome_label = tk.Label(frame_campos, text="Nome:")
    nome_label.grid(row=0, column=0)

    descricao_label = tk.Label(frame_campos, text="Descrição:")
    descricao_label.grid(row=1, column=0)

    preco_label = tk.Label(frame_campos, text="Preço:")
    preco_label.grid(row=2, column=0)

    quantidade_label = tk.Label(frame_campos, text="Quantidade em Estoque:")
    quantidade_label.grid(row=3, column=0)

    codigo_label = tk.Label(frame_campos, text="Código do Produto:")
    codigo_label.grid(row=4, column=0)

    nome_entry = tk.Entry(frame_campos)
    nome_entry.grid(row=0, column=1)

    descricao_entry = tk.Entry(frame_campos)
    descricao_entry.grid(row=1, column=1)

    preco_entry = tk.Entry(frame_campos)
    preco_entry.grid(row=2, column=1)

    quantidade_entry = tk.Entry(frame_campos)
    quantidade_entry.grid(row=3, column=1)

    codigo_entry = tk.Entry(frame_campos)
    codigo_entry.grid(row=4, column=1)

    botao_adicionar = tk.Button(janela_adicao, text="Adicionar",
                                command=lambda: salvar_novo_produto(nome_entry.get(), descricao_entry.get(), preco_entry.get(),
                                                                   quantidade_entry.get(), codigo_entry.get()))
    botao_adicionar.pack()

    janela_adicao.protocol("WM_DELETE_WINDOW", janela_adicao.destroy)


def salvar_novo_produto(nome, descricao, preco, quantidade, codigo):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("INSERT INTO `produtos` (Nome, Descricao, Preco, QuantidadeEstoque, codigo_de_produtos) VALUES (%s, %s, %s, %s, %s)", (nome, descricao, preco, quantidade, codigo))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Novo produto adicionado.")

    carregar_produtos()


def deletar_produto():
    item_selecionado = produtos_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um produto para deletar.")
        return

    confirmacao = messagebox.askyesno("Confirmar", "Tem certeza de que deseja deletar o produto selecionado?")
    if confirmacao:
        produto_selecionado = produtos_treeview.item(item_selecionado)
        dados_produto = produto_selecionado['values']
        id_produto = dados_produto[0]

        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='root0',
        )

        cursor = conexao.cursor()
        cursor.execute("DELETE FROM `produtos` WHERE ID = %s", (id_produto,))
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Produto deletado com sucesso.")

        carregar_produtos()


def carregar_produtos():
    produtos = obter_produtos()
    produtos_treeview.delete(*produtos_treeview.get_children())
    for produto in produtos:
        produtos_treeview.insert('', tk.END, values=produto)

def criar_janela_produtos():
    global janela
    global produtos_treeview
    janela = tk.Tk()
    janela.title("Sistema de Gerenciamento de Produtos")
    janela.geometry("800x600")
    janela.configure(bg="orange")
    produtos_treeview = ttk.Treeview(janela, columns=("ID", "Nome", "Descrição", "Preço", "Quantidade em Estoque", "Código do Produto"), show="headings")
    produtos_treeview.column("ID", width=30)
    produtos_treeview.column("Nome", width=150)
    produtos_treeview.column("Descrição", width=200)
    produtos_treeview.column("Preço", width=80)
    produtos_treeview.column("Quantidade em Estoque", width=150)
    produtos_treeview.column("Código do Produto", width=100)
    produtos_treeview.heading("ID", text="ID")
    produtos_treeview.heading("Nome", text="Nome")
    produtos_treeview.heading("Descrição", text="Descrição")
    produtos_treeview.heading("Preço", text="Preço")
    produtos_treeview.heading("Quantidade em Estoque", text="Quantidade em Estoque")
    produtos_treeview.heading("Código do Produto", text="Código do Produto")
    produtos_treeview.pack(pady=20)

    scrollbar = ttk.Scrollbar(janela, orient="vertical", command=produtos_treeview.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    produtos_treeview.configure(yscrollcommand=scrollbar.set)

    produtos = obter_produtos()
    for produto in produtos:
        produtos_treeview.insert('', tk.END, values=produto)

    editar_button = tk.Button(janela, text="Editar", command=editar_produto)
    editar_button.pack()

    deletar_button = tk.Button(janela, text="Deletar", command=deletar_produto)
    deletar_button.pack()

    adicionar_button = tk.Button(janela, text="Adicionar Produto", command=adicionar_produto)
    adicionar_button.pack()

    janela.mainloop()
