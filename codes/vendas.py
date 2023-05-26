import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def obter_vendas():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT vendas.ID, vendas.DataHora, clientes.Nome, vendas.Total, vendas.FormaPagamento FROM `vendas` INNER JOIN `clientes` ON vendas.ClienteID = clientes.ID")
    vendas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return vendas


def obter_itens_venda(venda_id):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT produto_id, quantidade FROM `itens_venda` WHERE venda_id = %s", (venda_id,))
    itens_venda = cursor.fetchall()

    cursor.close()
    conexao.close()

    return itens_venda


def editar_venda():
    global janela_edicao
    global datahora_entry
    global cliente_entry
    global total_entry
    global forma_pagamento_entry

    item_selecionado = vendas_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma venda para editar.")
        return

    venda_selecionada = vendas_treeview.item(item_selecionado)
    dados_venda = venda_selecionada['values']

    id_atual = dados_venda[0]
    datahora_atual = dados_venda[1]
    cliente_atual = dados_venda[2]
    total_atual = dados_venda[3]
    forma_pagamento_atual = dados_venda[4]

    janela_edicao = tk.Toplevel(janela)
    janela_edicao.title("Editar Venda")

    frame_campos = tk.Frame(janela_edicao)
    frame_campos.pack(pady=10)

    datahora_label = tk.Label(frame_campos, text="Data e Hora:")
    datahora_label.grid(row=0, column=0)

    cliente_label = tk.Label(frame_campos, text="Cliente Nome:")
    cliente_label.grid(row=1, column=0)

    total_label = tk.Label(frame_campos, text="Total:")
    total_label.grid(row=2, column=0)

    forma_pagamento_label = tk.Label(frame_campos, text="Forma de Pagamento:")
    forma_pagamento_label.grid(row=3, column=0)

    datahora_entry = tk.Entry(frame_campos)
    datahora_entry.grid(row=0, column=1)
    datahora_entry.insert(tk.END, datahora_atual)

    cliente_entry = tk.Entry(frame_campos)
    cliente_entry.grid(row=1, column=1)
    cliente_entry.insert(tk.END, cliente_atual)

    total_entry = tk.Entry(frame_campos)
    total_entry.grid(row=2, column=1)
    total_entry.insert(tk.END, total_atual)

    forma_pagamento_entry = tk.Entry(frame_campos)
    forma_pagamento_entry.grid(row=3, column=1)
    forma_pagamento_entry.insert(tk.END, forma_pagamento_atual)

    botao_salvar = tk.Button(janela_edicao, text="Salvar",
                             command=lambda: salvar_venda(id_atual, datahora_entry.get(), cliente_entry.get(), total_entry.get(),
                                                          forma_pagamento_entry.get()))
    botao_salvar.pack()

    botao_deletar = tk.Button(janela_edicao, text="Deletar", command=lambda: deletar_venda(id_atual))
    botao_deletar.pack()

    botao_mais_info = tk.Button(janela_edicao, text="Mais Info", command=lambda: exibir_info_itens_venda(id_atual))
    botao_mais_info.pack()

    janela_edicao.protocol("WM_DELETE_WINDOW", janela_edicao.destroy)


def salvar_venda(id_venda, datahora, cliente, total, forma_pagamento):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("UPDATE `vendas` SET DataHora = %s, ClienteID = (SELECT ID FROM `clientes` WHERE Nome = %s), Total = %s, FormaPagamento = %s WHERE ID = %s",
                   (datahora, cliente, total, forma_pagamento, id_venda))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Venda atualizada com sucesso.")

    janela_edicao.destroy()
    carregar_vendas()


def adicionar_venda_db(datahora, cliente, total, forma_pagamento):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("INSERT INTO `vendas` (DataHora, ClienteID, Total, FormaPagamento) SELECT %s, ID, %s, %s FROM `clientes` WHERE Nome = %s",
                   (datahora, total, forma_pagamento, cliente))
    conexao.commit()

    cursor.close()
    conexao.close()

    messagebox.showinfo("Sucesso", "Venda adicionada com sucesso.")

    janela_adicao.destroy()
    carregar_vendas()


def deletar_venda(id_venda):
    if messagebox.askyesno("Confirmação", "Tem certeza de que deseja excluir esta venda?"):
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='root0',
        )

        cursor = conexao.cursor()
        cursor.execute("DELETE FROM `itens_venda` WHERE venda_id = %s", (id_venda,))
        cursor.execute("DELETE FROM `vendas` WHERE ID = %s", (id_venda,))
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Venda excluída com sucesso.")

        janela_edicao.destroy()
        carregar_vendas()


def exibir_info_itens_venda(id_venda):
    itens_venda = obter_itens_venda(id_venda)

    janela_info_itens_venda = tk.Toplevel(janela)
    janela_info_itens_venda.title("Informações dos Itens de Venda")

    frame_itens_venda = tk.Frame(janela_info_itens_venda)
    frame_itens_venda.pack(pady=10)

    treeview_itens_venda = ttk.Treeview(frame_itens_venda, columns=("Produto", "Quantidade"), show="headings")
    treeview_itens_venda.column("Produto", width=200)
    treeview_itens_venda.column("Quantidade", width=100)
    treeview_itens_venda.heading("Produto", text="Produto")
    treeview_itens_venda.heading("Quantidade", text="Quantidade")
    treeview_itens_venda.pack()

    for item in itens_venda:
        produto_id = item[0]
        quantidade = item[1]

        produto = obter_nome_produto(produto_id)
        treeview_itens_venda.insert("", tk.END, values=(produto, quantidade))


def obter_nome_produto(produto_id):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT Nome FROM `produtos` WHERE ID = %s", (produto_id,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado:
        return resultado[0]
    else:
        return "Produto não encontrado"

def carregar_vendas():
    vendas = obter_vendas()
    vendas_treeview.delete(*vendas_treeview.get_children())
    for venda in vendas:
        vendas_treeview.insert('', tk.END, values=venda)

def criar_janela_vendas():
    global janela
    global vendas_treeview
    janela = tk.Tk()
    janela.title("Sistema de Gerenciamento de Vendas")
    janela.geometry("800x600")
    janela.configure(bg="orange")
    vendas_treeview = ttk.Treeview(janela, columns=("ID", "Data e Hora", "Cliente Nome", "Total", "Forma de Pagamento"),
                                   show="headings")
    vendas_treeview.column("ID", width=30)
    vendas_treeview.column("Data e Hora", width=150)
    vendas_treeview.column("Cliente Nome", width=150)
    vendas_treeview.column("Total", width=80)
    vendas_treeview.column("Forma de Pagamento", width=150)
    vendas_treeview.heading("ID", text="ID")
    vendas_treeview.heading("Data e Hora", text="Data e Hora")
    vendas_treeview.heading("Cliente Nome", text="Cliente Nome")
    vendas_treeview.heading("Total", text="Total")
    vendas_treeview.heading("Forma de Pagamento", text="Forma de Pagamento")
    vendas_treeview.pack(pady=20)

    scrollbar = ttk.Scrollbar(janela, orient="vertical", command=vendas_treeview.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    vendas_treeview.configure(yscrollcommand=scrollbar.set)

    vendas = obter_vendas()
    for venda in vendas:
        vendas_treeview.insert('', tk.END, values=venda)

    editar_button = tk.Button(janela, text="Mais", command=editar_venda)
    editar_button.pack()

    janela.mainloop()
