import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

def obter_compras():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT compras.ID, compras.DataHora, fornecedores.Nome, produtos.Nome, compras.Quantidade, compras.PrecoCompra FROM compras INNER JOIN fornecedores ON compras.FornecedorID = fornecedores.ID INNER JOIN produtos ON compras.ProdutoID = produtos.ID")
    compras = cursor.fetchall()

    cursor.close()
    conexao.close()

    return compras


def editar_compra():
    global janela_edicao
    global fornecedor_combobox
    global produto_combobox
    global quantidade_entry
    global preco_entry

    item_selecionado = compras_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma compra para editar.")
        return

    compra_selecionada = compras_treeview.item(item_selecionado)
    dados_compra = compra_selecionada['values']

    id_atual = dados_compra[0]
    datahora_atual = dados_compra[1]
    fornecedor_atual = dados_compra[2]
    produto_atual = dados_compra[3]
    quantidade_atual = dados_compra[4]
    preco_atual = dados_compra[5]

    janela_edicao = tk.Toplevel(janela)
    janela_edicao.title("Editar Compra")

    frame_campos = tk.Frame(janela_edicao)
    frame_campos.pack(pady=10)

    fornecedor_label = tk.Label(frame_campos, text="Fornecedor:")
    fornecedor_label.grid(row=0, column=0)

    produto_label = tk.Label(frame_campos, text="Produto:")
    produto_label.grid(row=1, column=0)

    quantidade_label = tk.Label(frame_campos, text="Quantidade:")
    quantidade_label.grid(row=2, column=0)

    preco_label = tk.Label(frame_campos, text="Preço de Compra:")
    preco_label.grid(row=3, column=0)

    fornecedores = obter_fornecedores()
    fornecedor_combobox = ttk.Combobox(frame_campos, values=fornecedores, state="readonly")
    fornecedor_combobox.grid(row=0, column=1)
    fornecedor_combobox.set(fornecedor_atual)

    produtos = obter_produtos()
    produto_combobox = ttk.Combobox(frame_campos, values=produtos, state="readonly")
    produto_combobox.grid(row=1, column=1)
    produto_combobox.set(produto_atual)

    quantidade_entry = tk.Entry(frame_campos)
    quantidade_entry.grid(row=2, column=1)
    quantidade_entry.insert(tk.END, quantidade_atual)

    preco_entry = tk.Entry(frame_campos)
    preco_entry.grid(row=3, column=1)
    preco_entry.insert(tk.END, preco_atual)

    botao_salvar = tk.Button(janela_edicao, text="Salvar", command=salvar_compra)
    botao_salvar.pack()

    janela_edicao.protocol("WM_DELETE_WINDOW", janela_edicao.destroy)


def salvar_compra():
    item_selecionado = compras_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma compra para editar.")
        return

    compra_selecionada = compras_treeview.item(item_selecionado)
    dados_compra = compra_selecionada['values']
    id_compra = dados_compra[0]

    fornecedor_selecionado = fornecedor_combobox.get()
    produto_selecionado = produto_combobox.get()
    quantidade = quantidade_entry.get()
    preco = preco_entry.get()

    # Obtendo os IDs dos fornecedores e produtos selecionados
    fornecedor_id = obter_id_fornecedor(fornecedor_selecionado)
    produto_id = obter_id_produto(produto_selecionado)

    if fornecedor_id is None or produto_id is None:
        messagebox.showwarning("Aviso", "Selecione um fornecedor e um produto válidos.")
        return

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("UPDATE compras SET FornecedorID = %s, ProdutoID = %s, Quantidade = %s, PrecoCompra = %s WHERE ID = %s",
                   (fornecedor_id, produto_id, quantidade, preco, id_compra))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Compra atualizada com sucesso.")

    janela_edicao.destroy()
    carregar_compras()


def adicionar_compra():
    global janela_adicao
    global fornecedor_combobox
    global produto_combobox
    global quantidade_entry
    global preco_entry

    janela_adicao = tk.Toplevel(janela)
    janela_adicao.title("Adicionar Compra")

    frame_campos = tk.Frame(janela_adicao)
    frame_campos.pack(pady=10)

    fornecedor_label = tk.Label(frame_campos, text="Fornecedor:")
    fornecedor_label.grid(row=0, column=0)

    produto_label = tk.Label(frame_campos, text="Produto:")
    produto_label.grid(row=1, column=0)

    quantidade_label = tk.Label(frame_campos, text="Quantidade:")
    quantidade_label.grid(row=2, column=0)

    preco_label = tk.Label(frame_campos, text="Preço de Compra:")
    preco_label.grid(row=3, column=0)

    fornecedores = obter_fornecedores()
    fornecedor_combobox = ttk.Combobox(frame_campos, values=fornecedores, state="readonly")
    fornecedor_combobox.grid(row=0, column=1)

    produtos = obter_produtos()
    produto_combobox = ttk.Combobox(frame_campos, values=produtos, state="readonly")
    produto_combobox.grid(row=1, column=1)

    quantidade_entry = tk.Entry(frame_campos)
    quantidade_entry.grid(row=2, column=1)

    preco_entry = tk.Entry(frame_campos)
    preco_entry.grid(row=3, column=1)

    botao_salvar = tk.Button(janela_adicao, text="Salvar", command=salvar_nova_compra)
    botao_salvar.pack()

    janela_adicao.protocol("WM_DELETE_WINDOW", janela_adicao.destroy)


def salvar_nova_compra():
    fornecedor_selecionado = fornecedor_combobox.get()
    produto_selecionado = produto_combobox.get()
    quantidade = quantidade_entry.get()
    preco = preco_entry.get()

    # Obtendo os IDs dos fornecedores e produtos selecionados
    fornecedor_id = obter_id_fornecedor(fornecedor_selecionado)
    produto_id = obter_id_produto(produto_selecionado)

    if fornecedor_id is None or produto_id is None:
        messagebox.showwarning("Aviso", "Selecione um fornecedor e um produto válidos.")
        return

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("INSERT INTO compras (DataHora, FornecedorID, ProdutoID, Quantidade, PrecoCompra) VALUES (%s, %s, %s, %s, %s)",
                   (datetime.now(), fornecedor_id, produto_id, quantidade, preco))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Nova compra adicionada.")

    janela_adicao.destroy()
    carregar_compras()


def deletar_compra():
    item_selecionado = compras_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma compra para excluir.")
        return

    confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta compra?")
    if confirmacao:
        compra_selecionada = compras_treeview.item(item_selecionado)
        dados_compra = compra_selecionada['values']
        id_compra = dados_compra[0]

        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='root0',
        )

        cursor = conexao.cursor()
        cursor.execute("DELETE FROM compras WHERE ID = %s", (id_compra,))
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Compra excluída com sucesso.")

        carregar_compras()


def obter_fornecedores():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT Nome FROM fornecedores")
    fornecedores = [fornecedor[0] for fornecedor in cursor.fetchall()]

    cursor.close()
    conexao.close()

    return fornecedores


def obter_produtos():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT Nome FROM produtos")
    produtos = [produto[0] for produto in cursor.fetchall()]

    cursor.close()
    conexao.close()

    return produtos


def obter_id_fornecedor(nome_fornecedor):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT ID FROM fornecedores WHERE Nome = %s", (nome_fornecedor,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado:
        return resultado[0]
    else:
        return None


def obter_id_produto(nome_produto):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT ID FROM produtos WHERE Nome = %s", (nome_produto,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado:
        return resultado[0]
    else:
        return None


def carregar_compras():
    compras = obter_compras()

    # Limpa as compras existentes na treeview
    compras_treeview.delete(*compras_treeview.get_children())

    # Insere as compras atualizadas na treeview
    for compra in compras:
        compras_treeview.insert("", tk.END, values=compra)

def criar_janela_compras():
    global compras_treeview
    global janela

    # Criando a janela principal
    janela = tk.Tk()
    janela.title("Gerenciamento de Compras")
    janela.configure(bg="orange")
    # Criando a treeview para exibir as compras
    compras_treeview = ttk.Treeview(janela, columns=(1, 2, 3, 4, 5, 6), show="headings", height=15)
    compras_treeview.pack(pady=20)

    compras_treeview.heading(1, text="ID")
    compras_treeview.heading(2, text="Data/Hora")
    compras_treeview.heading(3, text="Fornecedor")
    compras_treeview.heading(4, text="Produto")
    compras_treeview.heading(5, text="Quantidade")
    compras_treeview.heading(6, text="Preço de Compra")

    compras_treeview.column(1, width=30)
    compras_treeview.column(2, width=120)
    compras_treeview.column(3, width=150)
    compras_treeview.column(4, width=150)
    compras_treeview.column(5, width=80)
    compras_treeview.column(6, width=100)

    # Carregando as compras na treeview
    carregar_compras()

    # Criando os botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    botao_adicionar = tk.Button(frame_botoes, text="Adicionar Compra", command=adicionar_compra)
    botao_adicionar.grid(row=0, column=0, padx=10)

    botao_editar = tk.Button(frame_botoes, text="Editar Compra", command=editar_compra)
    botao_editar.grid(row=0, column=1, padx=10)

    botao_deletar = tk.Button(frame_botoes, text="Deletar Compra", command=deletar_compra)
    botao_deletar.grid(row=0, column=2, padx=10)

    # Executando a janela principal
    janela.mainloop()
