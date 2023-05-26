import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def obter_clientes():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return clientes


def editar_cliente():
    global clientes_treeview
    global janela_edicao
    global endereco_entry
    global email_entry
    global telefone_entry
    global credito_entry
    global cod_cliente_entry

    item_selecionado = clientes_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
        return

    cliente_selecionado = clientes_treeview.item(item_selecionado)
    dados_cliente = cliente_selecionado['values']

    id_atual = dados_cliente[0]
    nome_atual = dados_cliente[1]
    endereco_atual = dados_cliente[2]
    email_atual = dados_cliente[3]
    telefone_atual = dados_cliente[4]
    credito_atual = dados_cliente[5]
    cod_cliente_atual = dados_cliente[6]

    janela_edicao = tk.Toplevel(janela)
    janela_edicao.title("Editar Cliente")

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

    credito_label = tk.Label(frame_campos, text="Crédito:")
    credito_label.grid(row=4, column=0)

    cod_cliente_label = tk.Label(frame_campos, text="Código do Cliente:")
    cod_cliente_label.grid(row=5, column=0)

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

    credito_entry = tk.Entry(frame_campos)
    credito_entry.grid(row=4, column=1)
    credito_entry.insert(tk.END, credito_atual)

    cod_cliente_entry = tk.Entry(frame_campos)
    cod_cliente_entry.grid(row=5, column=1)
    cod_cliente_entry.insert(tk.END, cod_cliente_atual)

    botao_salvar = tk.Button(janela_edicao, text="Salvar",
                             command=lambda: salvar_cliente(id_atual, nome_entry.get(), endereco_entry.get(), email_entry.get(),
                                                            telefone_entry.get(), credito_entry.get(),
                                                            cod_cliente_entry.get()))
    botao_salvar.pack()

    janela_edicao.protocol("WM_DELETE_WINDOW", janela_edicao.destroy)


def salvar_cliente(id_cliente, nome, endereco, email, telefone, credito, cod_cliente):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("UPDATE `clientes` SET nome = %s, endereco = %s, email = %s, telefone = %s, credito = %s, cod_cliente = %s WHERE ID = %s", (nome, endereco, email, telefone, credito, cod_cliente, id_cliente))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")

    janela_edicao.destroy()
    carregar_clientes()


def adicionar_cliente():
    global janela_adicao
    global novo_nome_entry
    global novo_endereco_entry
    global novo_email_entry
    global novo_telefone_entry
    global novo_credito_entry
    global novo_cod_cliente_entry

    janela_adicao = tk.Toplevel(janela)
    janela_adicao.title("Adicionar Cliente")

    frame_campos = tk.Frame(janela_adicao)
    frame_campos.pack(pady=10)

    novo_nome_label = tk.Label(frame_campos, text="Nome:")
    novo_nome_label.grid(row=0, column=0)

    novo_endereco_label = tk.Label(frame_campos, text="Endereço:")
    novo_endereco_label.grid(row=1, column=0)

    novo_email_label = tk.Label(frame_campos, text="E-mail:")
    novo_email_label.grid(row=2, column=0)

    novo_telefone_label = tk.Label(frame_campos, text="Telefone:")
    novo_telefone_label.grid(row=3, column=0)

    novo_credito_label = tk.Label(frame_campos, text="Crédito:")
    novo_credito_label.grid(row=4, column=0)

    novo_cod_cliente_label = tk.Label(frame_campos, text="Código do Cliente:")
    novo_cod_cliente_label.grid(row=5, column=0)

    novo_nome_entry = tk.Entry(frame_campos)
    novo_nome_entry.grid(row=0, column=1)

    novo_endereco_entry = tk.Entry(frame_campos)
    novo_endereco_entry.grid(row=1, column=1)

    novo_email_entry = tk.Entry(frame_campos)
    novo_email_entry.grid(row=2, column=1)

    novo_telefone_entry = tk.Entry(frame_campos)
    novo_telefone_entry.grid(row=3, column=1)

    novo_credito_entry = tk.Entry(frame_campos)
    novo_credito_entry.grid(row=4, column=1)

    novo_cod_cliente_entry = tk.Entry(frame_campos)
    novo_cod_cliente_entry.grid(row=5, column=1)

    botao_salvar = tk.Button(janela_adicao, text="Salvar", command=adicionar_cliente_db)
    botao_salvar.pack()

    janela_adicao.protocol("WM_DELETE_WINDOW", janela_adicao.destroy)


def adicionar_cliente_db():
    nome = novo_nome_entry.get()
    endereco = novo_endereco_entry.get()
    email = novo_email_entry.get()
    telefone = novo_telefone_entry.get()
    credito = novo_credito_entry.get()
    cod_cliente = novo_cod_cliente_entry.get()

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("INSERT INTO `clientes` (nome, endereco, email, telefone, credito, cod_cliente) VALUES (%s, %s, %s, %s, %s, %s)",
                   (nome, endereco, email, telefone, credito, cod_cliente))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso.")

    janela_adicao.destroy()
    carregar_clientes()


def deletar_cliente():
    item_selecionado = clientes_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um cliente para deletar.")
        return

    confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar o cliente selecionado?")
    if confirmacao:
        cliente_selecionado = clientes_treeview.item(item_selecionado)
        id_cliente = cliente_selecionado['values'][0]

        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='root0',
        )
        try:

            cursor = conexao.cursor()
            cursor.execute("DELETE FROM `clientes` WHERE ID = %s", (id_cliente,))
            conexao.commit()

            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", "Cliente deletado com sucesso.")
        except:
            messagebox.showinfo("Falha", "Esse cliente tem vendas,apague os dados dessa venda para continuar ")

        carregar_clientes()


def carregar_clientes():
    clientes = obter_clientes()
    clientes_treeview.delete(*clientes_treeview.get_children())
    for cliente in clientes:
        clientes_treeview.insert('', tk.END, values=cliente)

def criar_janela_clientes():
    global clientes_treeview
    global janela
    janela = tk.Tk()
    janela.title("Sistema de Gerenciamento de Clientes")
    janela.geometry("800x600")
    janela.configure(bg="orange")

    clientes_treeview = ttk.Treeview(janela, columns=("ID", "Nome", "Endereço", "E-mail", "Telefone", "Crédito", "Código do Cliente"), show="headings")
    clientes_treeview.column("ID", width=30)
    clientes_treeview.column("Nome", width=150)
    clientes_treeview.column("Endereço", width=200)
    clientes_treeview.column("E-mail", width=150)
    clientes_treeview.column("Telefone", width=100)
    clientes_treeview.column("Crédito", width=80)
    clientes_treeview.column("Código do Cliente", width=100)
    clientes_treeview.heading("ID", text="ID")
    clientes_treeview.heading("Nome", text="Nome")
    clientes_treeview.heading("Endereço", text="Endereço")
    clientes_treeview.heading("E-mail", text="E-mail")
    clientes_treeview.heading("Telefone", text="Telefone")
    clientes_treeview.heading("Crédito", text="Crédito")
    clientes_treeview.heading("Código do Cliente", text="Código do Cliente")
    clientes_treeview.pack(pady=20)

    scrollbar = ttk.Scrollbar(janela, orient="vertical", command=clientes_treeview.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    clientes_treeview.configure(yscrollcommand=scrollbar.set)

    clientes = obter_clientes()
    for cliente in clientes:
        clientes_treeview.insert('', tk.END, values=cliente)

    editar_button = tk.Button(janela, text="Editar", command=editar_cliente)
    editar_button.pack()

    adicionar_button = tk.Button(janela, text="Adicionar Cliente", command=adicionar_cliente)
    adicionar_button.pack()

    deletar_button = tk.Button(janela, text="Deletar", command=deletar_cliente)
    deletar_button.pack()

    janela.mainloop()
