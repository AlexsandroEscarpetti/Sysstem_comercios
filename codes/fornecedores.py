import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def obter_fornecedores():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM `fornecedores`")
    fornecedores = cursor.fetchall()

    cursor.close()
    conexao.close()

    return fornecedores


def editar_fornecedor():
    global janela_edicao
    global nome_entry
    global endereco_entry
    global email_entry
    global telefone_entry

    item_selecionado = fornecedores_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um fornecedor para editar.")
        return

    fornecedor_selecionado = fornecedores_treeview.item(item_selecionado)
    dados_fornecedor = fornecedor_selecionado['values']

    id_atual = dados_fornecedor[0]
    nome_atual = dados_fornecedor[1]
    endereco_atual = dados_fornecedor[2]
    email_atual = dados_fornecedor[3]
    telefone_atual = dados_fornecedor[4]

    janela_edicao = tk.Toplevel(janela)
    janela_edicao.title("Editar Fornecedor")

    frame_campos = tk.Frame(janela_edicao)
    frame_campos.pack(pady=10)

    nome_label = tk.Label(frame_campos, text="Nome:")
    nome_label.grid(row=0, column=0)

    endereco_label = tk.Label(frame_campos, text="Endereço:")
    endereco_label.grid(row=1, column=0)

    email_label = tk.Label(frame_campos, text="E-mail:")
    email_label.grid(row=2, column=0)

    telefone_label = tk.Label(frame_campos, text="Telefone:")
    telefone_label.grid(row=3, column=0)

    nome_entry = tk.Entry(frame_campos)
    nome_entry.grid(row=0, column=1)
    nome_entry.insert(tk.END, nome_atual)

    endereco_entry = tk.Entry(frame_campos)
    endereco_entry.grid(row=1, column=1)
    endereco_entry.insert(tk.END, endereco_atual)

    email_entry = tk.Entry(frame_campos)
    email_entry.grid(row=2, column=1)
    email_entry.insert(tk.END, email_atual)

    telefone_entry = tk.Entry(frame_campos)
    telefone_entry.grid(row=3, column=1)
    telefone_entry.insert(tk.END, telefone_atual)

    botao_salvar = tk.Button(janela_edicao, text="Salvar",
                             command=lambda: salvar_fornecedor(nome_entry.get(), endereco_entry.get(),
                                                              email_entry.get(), telefone_entry.get()))
    botao_salvar.pack()

    janela_edicao.protocol("WM_DELETE_WINDOW", janela_edicao.destroy)


def salvar_fornecedor(nome, endereco, email, telefone):
    item_selecionado = fornecedores_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um fornecedor para editar.")
        return

    fornecedor_selecionado = fornecedores_treeview.item(item_selecionado)
    dados_fornecedor = fornecedor_selecionado['values']
    id_fornecedor = dados_fornecedor[0]

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("UPDATE `fornecedores` SET Nome = %s, Endereco = %s, Email = %s, Telefone = %s WHERE ID = %s",
                   (nome, endereco, email, telefone, id_fornecedor))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso.")

    janela_edicao.destroy()
    carregar_fornecedores()


def carregar_fornecedores():
    global fornecedores_treeview
    fornecedores = obter_fornecedores()
    fornecedores_treeview.delete(*fornecedores_treeview.get_children())
    for fornecedor in fornecedores:
        fornecedores_treeview.insert('', tk.END, values=fornecedor)


def adicionar_fornecedor():
    global janela
    janela_adicao = tk.Toplevel(janela)
    janela_adicao.title("Adicionar Fornecedor")

    frame_campos = tk.Frame(janela_adicao)
    frame_campos.pack(pady=10)

    nome_label = tk.Label(frame_campos, text="Nome:")
    nome_label.grid(row=0, column=0)

    endereco_label = tk.Label(frame_campos, text="Endereço:")
    endereco_label.grid(row=1, column=0)

    email_label = tk.Label(frame_campos, text="E-mail:")
    email_label.grid(row=2, column=0)

    telefone_label = tk.Label(frame_campos, text="Telefone:")
    telefone_label.grid(row=3, column=0)

    nome_entry = tk.Entry(frame_campos)
    nome_entry.grid(row=0, column=1)

    endereco_entry = tk.Entry(frame_campos)
    endereco_entry.grid(row=1, column=1)

    email_entry = tk.Entry(frame_campos)
    email_entry.grid(row=2, column=1)

    telefone_entry = tk.Entry(frame_campos)
    telefone_entry.grid(row=3, column=1)

    botao_adicionar = tk.Button(janela_adicao, text="Adicionar",
                                command=lambda: salvar_novo_fornecedor(nome_entry.get(), endereco_entry.get(),
                                                                        email_entry.get(), telefone_entry.get()))
    botao_adicionar.pack()


def salvar_novo_fornecedor(nome, endereco, email, telefone):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("INSERT INTO `fornecedores` (Nome, Endereco, Email, Telefone) VALUES (%s, %s, %s, %s)",
                   (nome, endereco, email, telefone))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Fornecedor adicionado com sucesso.")

    carregar_fornecedores()

def criar_janela_fornecedores():
    global janela
    global fornecedores_treeview
    janela = tk.Tk()
    janela.title("Sistema de Gerenciamento de Fornecedores")
    janela.geometry("800x600")
    janela.configure(bg="orange")

    fornecedores_treeview = ttk.Treeview(janela, columns=("ID", "Nome", "Endereço", "E-mail", "Telefone"), show="headings")
    fornecedores_treeview.column("ID", width=30)
    fornecedores_treeview.column("Nome", width=150)
    fornecedores_treeview.column("Endereço", width=200)
    fornecedores_treeview.column("E-mail", width=150)
    fornecedores_treeview.column("Telefone", width=100)
    fornecedores_treeview.heading("ID", text="ID")
    fornecedores_treeview.heading("Nome", text="Nome")
    fornecedores_treeview.heading("Endereço", text="Endereço")
    fornecedores_treeview.heading("E-mail", text="E-mail")
    fornecedores_treeview.heading("Telefone", text="Telefone")
    fornecedores_treeview.pack(pady=20)

    scrollbar = ttk.Scrollbar(janela, orient="vertical", command=fornecedores_treeview.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    fornecedores_treeview.configure(yscrollcommand=scrollbar.set)

    fornecedores = obter_fornecedores()
    for fornecedor in fornecedores:
        fornecedores_treeview.insert('', tk.END, values=fornecedor)

    editar_button = tk.Button(janela, text="Editar", command=editar_fornecedor)
    editar_button.pack()

    adicionar_button = tk.Button(janela, text="Adicionar Fornecedor", command=adicionar_fornecedor)
    adicionar_button.pack()

    janela.mainloop()
