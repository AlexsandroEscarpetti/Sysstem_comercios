import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def obter_usuarios():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    cursor = conexao.cursor()
    cursor.execute("SELECT `ID`, `Usuario`, `Permissoes` FROM `usuarios`")
    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return usuarios

def editar_usuario():
    global janela_edicao
    global senha_entry
    item_selecionado = usuarios_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um usuário para editar.")
        return

    usuario_selecionado = usuarios_treeview.item(item_selecionado)
    dados_usuario = usuario_selecionado['values']
    nome_atual = dados_usuario[1]
    permissoes_atual = dados_usuario[2]

    janela_edicao = tk.Toplevel(janela)
    janela_edicao.title("Editar Usuário")

    frame_campos = tk.Frame(janela_edicao)
    frame_campos.pack(pady=10)

    nome_label = tk.Label(frame_campos, text="Nome:")
    nome_label.grid(row=0, column=0)

    permissoes_label = tk.Label(frame_campos, text="Permissões:")
    permissoes_label.grid(row=1, column=0)

    senha_label = tk.Label(frame_campos, text="Senha:")
    senha_label.grid(row=2, column=0)

    senha_entry = tk.Entry(frame_campos, show="*")
    senha_entry.grid(row=2, column=1)



    nome_entry = tk.Entry(frame_campos)
    nome_entry.grid(row=0, column=1)
    nome_entry.insert(tk.END, nome_atual)

    permissoes_entry = tk.Entry(frame_campos)
    permissoes_entry.grid(row=1, column=1)
    permissoes_entry.insert(tk.END, permissoes_atual)


    botao_salvar = tk.Button(janela_edicao, text="Salvar", command=lambda: salvar_usuario(nome_entry.get(), permissoes_entry.get()))
    botao_salvar.pack()

    janela_edicao.protocol("WM_DELETE_WINDOW", janela_edicao.destroy)

def salvar_usuario(nome_novo, permissoes_nova):
    global senha_entry
    global janela_edicao
    if not nome_novo:
        messagebox.showerror("Erro", "O nome do usuário não pode estar vazio.")
        return

    if not permissoes_nova:
        messagebox.showerror("Erro", "As permissões não podem estar vazias.")
        return

    try:
        permissoes_nova = int(permissoes_nova)
    except ValueError:
        messagebox.showerror("Erro", "O valor de permissões deve ser numérico.")
        return

    item_selecionado = usuarios_treeview.focus()
    usuario_selecionado = usuarios_treeview.item(item_selecionado)
    dados_usuario = usuario_selecionado['values']
    nome_atual = dados_usuario[0]
    senha_nova = senha_entry.get()

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='root0',
    )

    comando_atualizacao = "UPDATE `usuarios` SET `Usuario` = %s, `Senha` = %s, `Permissoes` = %s WHERE `Usuario` = %s"

    valores = (nome_novo, senha_nova, permissoes_nova, nome_atual)

    cursor = conexao.cursor()
    cursor.execute(comando_atualizacao, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

    atualizar_usuarios()
    messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso.")
    janela_edicao.destroy()
def excluir_usuario():
    item_selecionado = usuarios_treeview.focus()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um usuário para excluir.")
        return

    resposta = messagebox.askquestion("Confirmação", "Tem certeza de que deseja excluir o usuário selecionado?")
    if resposta == "yes":
        usuario_selecionado = usuarios_treeview.item(item_selecionado)
        dados_usuario = usuario_selecionado['values']
        nome = dados_usuario[0]

        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='root0',
        )

        comando_exclusao = "DELETE FROM `usuarios` WHERE `Usuario` = %s"
        valor = (nome,)

        cursor = conexao.cursor()
        cursor.execute(comando_exclusao, valor)
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
        atualizar_usuarios()

def atualizar_usuarios():
    usuarios = obter_usuarios()
    usuarios_treeview.delete(*usuarios_treeview.get_children())

    for usuario in usuarios:
        usuarios_treeview.insert('', tk.END, values=(usuario[0], usuario[1],usuario[2]))

def criar_janela_usuarios():
    global janela
    global usuarios_treeview

    janela = tk.Tk()
    janela.title("Gerenciador de Usuários")
    janela.configure(bg="orange")

    frame_treeview = tk.Frame(janela)
    frame_treeview.pack(pady=10)

    scrollbar = ttk.Scrollbar(frame_treeview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    usuarios_treeview = ttk.Treeview(frame_treeview, yscrollcommand=scrollbar.set)
    usuarios_treeview['columns'] = ('id', 'Nome', 'Permissões')
    usuarios_treeview.column('#0', width=0, stretch=tk.NO)
    usuarios_treeview.column('id', anchor=tk.W, width=50)
    usuarios_treeview.column('Nome', anchor=tk.W, width=200)
    usuarios_treeview.column('Permissões', anchor=tk.W, width=100)
    usuarios_treeview.heading('#0', text='', anchor=tk.W)
    usuarios_treeview.heading('id', text='ID', anchor=tk.W)
    usuarios_treeview.heading('Nome', text='Nome', anchor=tk.W)
    usuarios_treeview.heading('Permissões', text='Permissões', anchor=tk.W)
    usuarios_treeview.pack()

    scrollbar.config(command=usuarios_treeview.yview)

    menu_contexto = tk.Menu(janela, tearoff=0)
    menu_contexto.add_command(label="Editar", command=editar_usuario)
    menu_contexto.add_command(label="Excluir", command=excluir_usuario)

    def exibir_menu_contexto(event):
        item_selecionado = usuarios_treeview.identify_row(event.y)
        if item_selecionado:
            usuarios_treeview.selection_set(item_selecionado)
            menu_contexto.post(event.x_root, event.y_root)

    usuarios_treeview.bind("<Button-3>", exibir_menu_contexto)

    botao_adicionar = tk.Button(janela, text="Adicionar Usuário", command=lambda: criar_janela_adicao())
    botao_adicionar.pack()

    def criar_janela_adicao():
        global janela_adicao
        global nome_entry
        global permissoes_entry
        global senha_entry

        janela_adicao = tk.Toplevel(janela)
        janela_adicao.title("Adicionar Usuário")

        frame_campos = tk.Frame(janela_adicao)
        frame_campos.pack(pady=10)

        nome_label = tk.Label(frame_campos, text="Nome:")
        nome_label.grid(row=0, column=0)

        permissoes_label = tk.Label(frame_campos, text="Permissões:")
        permissoes_label.grid(row=1, column=0)

        senha_label = tk.Label(frame_campos, text="Senha:")
        senha_label.grid(row=2, column=0)

        nome_entry = tk.Entry(frame_campos)
        nome_entry.grid(row=0, column=1)

        permissoes_entry = tk.Entry(frame_campos)
        permissoes_entry.grid(row=1, column=1)

        senha_entry = tk.Entry(frame_campos)
        senha_entry.grid(row=2, column=1)


        botao_salvar = tk.Button(janela_adicao, text="Salvar", command=lambda: adicionar_usuario())
        botao_salvar.pack()

        janela_adicao.protocol("WM_DELETE_WINDOW", janela_adicao.destroy)

    def adicionar_usuario():
        nome = nome_entry.get()
        permissoes = permissoes_entry.get()
        senha = senha_entry.get()

        if not nome or not permissoes or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            permissoes = int(permissoes)
        except ValueError:
            messagebox.showerror("Erro", "As permissões devem ser numéricas.")
            return

        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='root0',
        )

        comando_insercao = "INSERT INTO `usuarios` (`Usuario`, `Senha`, `Permissoes`) VALUES (%s, %s, %s)"
        valores = (nome, senha, permissoes)

        cursor = conexao.cursor()
        cursor.execute(comando_insercao, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso.")
        janela_adicao.destroy()
        atualizar_usuarios()

    atualizar_usuarios()

    janela.mainloop()
