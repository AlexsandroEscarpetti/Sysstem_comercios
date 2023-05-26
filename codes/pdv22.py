import time
import tkinter as tk
import mysql.connector
from datetime import datetime
from tkinter import Scrollbar
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import Tk, Toplevel, Label, Button


terminou_pagamento = False
iniciou_pagamento = False
valor_devido = 0
conexao = mysql.connector.connect(host='localhost',user='root',password='',database='root0',)
conexao.close()

def show_custom_message(title, message, bg_color='orange', fg_color='yellow'):
    root = Tk()
    root.withdraw()

    # Crie uma nova janela personalizada
    custom_window = Toplevel(root)
    custom_window.title(title)
    custom_window.configure(bg=bg_color)  # Defina a cor de fundo da janela

    # Adicione um rótulo com o texto
    label = Label(custom_window, text=message, fg=fg_color, bg=bg_color,font=('Arial', 22, 'bold'),)  # Defina as cores do texto e do fundo do rótulo
    label.pack()

    # Adicione um botão para fechar a janela
    button = Button(custom_window, text="Fechar", command=custom_window.destroy,fg='black',bg='red')
    button.pack()
    # Remova a barra de título e os botões de fechar, maximizar e minimizar
    custom_window.overrideredirect(True)

    # Defina o foco no botão "Fechar"
    button.focus_set()
    custom_window.focus_force()

    def press_enter(event):
        # Verifique se a tecla pres
        if event.keysym == 'Return':
            button.invoke()

    # Vincule a função press_enter ao evento "Return" (Enter) da janela
    custom_window.bind('<Return>', press_enter)

    # Obtenha as dimensões da tela
    screen_width = custom_window.winfo_screenwidth()
    screen_height = custom_window.winfo_screenheight()

    # Calcule as coordenadas para centralizar a janela
    window_width = custom_window.winfo_width()
    window_height = custom_window.winfo_height()
    x = int((screen_width - window_width) / 3)
    y = int((screen_height - window_height) / 5)

    # Posicione a janela no centro da tela
    custom_window.geometry(f"{400}x{200}+{x}+{y}")

    root.mainloop()

def insert_centered_text(widget, text):
    widget.insert(tk.END, text + '\n', 'center')  # Insere o texto com a tag 'center' e uma nova linha
    widget.tag_configure('center', justify='center')  # Configura a tag 'center' para centralizar o texto


def clear_text(widget):
    widget.delete(1.0, tk.END)



def abrir_conexao():
    global conexao
    conexao = mysql.connector.connect(host='localhost',user='root',password='',database='root0',)


def validar_cpf(cpf):

    # Remover caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))
    # Verificar se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False
    # Verificar se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    # Verificar o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False
    # Verificar o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[10]):
        return False
    return True

def atualizar_credito_cliente(cod_cliente, novo_credito):
    try:
        abrir_conexao()
        cursor = conexao.cursor()
        # Executa a atualização do crédito do cliente no banco de dados
        atualizacao = "UPDATE clientes SET Credito = %s WHERE cod_cliente = %s"
        valores = (novo_credito, cod_cliente)
        cursor.execute(atualizacao, valores)
        conexao.commit()  # Confirma a atualização no banco de dados
        cursor.close()
        conexao.close()
        return True
    except:
        return False
def encontrar_credito_cliente(cod_cliente_):
    abrir_conexao()
    cursor = conexao.cursor()
    # Executa a consulta SQL para encontrar o crédito do cliente com base no código
    consulta = "SELECT Credito FROM clientes WHERE cod_cliente = %s"
    cursor.execute(consulta, (cod_cliente_,))
    resultado = cursor.fetchone()  # Obtém o resultado da consulta
    cursor.close()
    conexao.close()
    if resultado:
        credito_cliente = resultado[0]
        return credito_cliente
    else:
        return None
def encontrar_id_produto(codigo_de_produtos_):
    abrir_conexao()
    cursor = conexao.cursor()
    # Executa a consulta SQL para encontrar o ID do produto com base no código
    consulta = "SELECT ID FROM produtos WHERE codigo_de_produtos = %s"
    cursor.execute(consulta, (codigo_de_produtos_,))
    resultado = cursor.fetchone()  # Obtém o resultado da consulta
    cursor.close()
    conexao.close()
    if resultado:
        id_produto = resultado[0]
        return id_produto
    else:
        return None
# ===============================================================================================
def encontrar_id_venda(DataHora, ClienteID, Total, FormaPagamento):
    abrir_conexao()
    cursor = conexao.cursor()
    # Executa a consulta SQL para encontrar o ID da venda com base nos parâmetros fornecidos
    consulta = "SELECT ID FROM vendas WHERE DataHora = %s AND ClienteID = %s AND Total = %s AND FormaPagamento = %s"
    cursor.execute(consulta, (DataHora, ClienteID, Total, FormaPagamento))
    resultado = cursor.fetchone()  # Obtém o resultado da consulta
    cursor.close()
    conexao.close()
    if resultado:
        id_venda = resultado[0]
        return id_venda
    else:
        return None
def verificar_cliente(cod_cliente):
    abrir_conexao()
    cursor = conexao.cursor()
    # Executa a consulta SQL para verificar se existe um cliente com o código fornecido
    consulta = "SELECT ID, Nome FROM clientes WHERE cod_cliente = %s"
    cursor.execute(consulta, (cod_cliente,))
    resultado = cursor.fetchone()  # Obtém o resultado da consulta
    cursor.close()
    conexao.close()
    if resultado:
        id_cliente, nome_cliente = resultado
        return [id_cliente, nome_cliente]
    else:
        return False
#===================================================================================
def pegar_data_e_hora_formato_mysql():
    current_datetime = datetime.now()
    datetime_mysql = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return datetime_mysql
#-----------------------------------------------------------
def obter_valor_produto(cod_prod__):
    abrir_conexao()
    cursor = conexao.cursor()
    # Executa a consulta SQL para obter o valor do produto
    cursor.execute("SELECT Preco FROM produtos WHERE codigo_de_produtos = %s", (cod_prod__,))
    # Obtém o resultado da consulta
    resultado = cursor.fetchone()
    # Verifica se existe algum resultado
    if resultado:
        valor = resultado[0]  # Obtém o valor do primeiro campo retornado
        conexao.close()
        return valor
    else:
        conexao.close()
        return 0
# ----------------------------------
def verificar_prod(codigo_do_produto_):
    abrir_conexao()
    cursor = conexao.cursor()
    # Executa a consulta SQL para verificar se o produto existe
    cursor.execute("SELECT * FROM produtos WHERE codigo_de_produtos = %s", (codigo_do_produto_,))
    # Obtém o resultado da consulta
    resultado = cursor.fetchone()
    # Verifica se existe algum resultado
    if resultado:
        # Produto encontrado
        conexao.close()
        return True
    else:
        # Produto não encontrado
        conexao.close()
        return False




def obter_nome_produto(codigo_produto):
    abrir_conexao()
    cursor = conexao.cursor()
    # Executa a consulta SQL para obter o nome do produto
    cursor.execute("SELECT Nome FROM produtos WHERE codigo_de_produtos = %s", (codigo_produto,))
    # Obtém o resultado da consulta
    resultado = cursor.fetchone()
    # Verifica se existe algum resultado
    if resultado:
        nome_produto = resultado[0]  # Obtém o nome do produto do primeiro campo retornado
        conexao.close()
        return nome_produto
    else:
        conexao.close()
        return None




#----------------------------------------------------
def verificar_login(id_usuario_, senha_usuario_):
    abrir_conexao()
    cursor = conexao.cursor()
    query = "SELECT * FROM usuarios WHERE ID = %s AND Senha = %s"
    valores = (id_usuario_, senha_usuario_)
    cursor.execute(query, valores)
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    if resultado:
        return True
    else:
        return False

def criar_janela_login():

    def fazer_login(event=None):
        id_usuario = id_entry.get()
        senha_usuario = senha_entry.get()

        if verificar_login(id_usuario, senha_usuario):
            login_window.destroy()
            processar_venda()
        else:
            dados_invalidos_label.config(text="Dados inválidos")  # Atualiza o texto do rótulo
            senha_entry.delete(0, tk.END)  # Limpa o campo "Senha"
            id_entry.delete(0, tk.END)  # Limpa o campo "ID"
            id_entry.focus_set()  # Retorna o foco para o campo "ID"

    def transferir_foco(event=None):
        senha_entry.focus_set()  # Transfere o foco para o campo "Senha"

    def transferir_foco_id(event=None):
        id_entry.focus_set()  # Transfere o foco para o campo "Senha"

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x150")
    login_window.configure(bg="orange")

    id_label = tk.Label(login_window, text="ID:")
    id_label.pack()

    id_entry = tk.Entry(login_window)
    id_entry.pack()

    senha_label = tk.Label(login_window, text="Senha:")
    senha_label.pack()

    senha_entry = tk.Entry(login_window, show="*")
    senha_entry.pack()

    dados_invalidos_label = tk.Label(login_window, text="---Faça login---", fg="red")  # Rótulo para a mensagem de dados inválidos
    dados_invalidos_label.pack()

    # Adiciona os eventos de pressionar tecla para as entradas
    id_entry.bind("<Return>", transferir_foco)
    id_entry.bind("<Down>", transferir_foco)

    senha_entry.bind("<Return>", fazer_login)
    senha_entry.bind("<Up>", transferir_foco_id)

    # Define o campo de entrada "ID" como foco inicial
    id_entry.focus_set()
    login_window.focus_force()

    login_window.mainloop()



# -----------------------------------------------------------------------------------

# Função para processar a venda

def processar_venda():
    global terminou_pagamento
    global iniciou_pagamento
    terminou_pagamento = terminou_pagamento
    lista_produtos = []
    total_compra = 0

    # Função para processar a venda
    def processar(event=None):

        nonlocal lista_produtos, total_compra


        # Obter código do produto
        produto_codigo = codigo_entry.get()
        resultado_label.config(text="==={}===".format(produto_codigo == ''))

        if produto_codigo == "" and len(lista_produtos) > 0:
            resultado_label.config(text="-----Código do produto está vazio-----")

            return
        if produto_codigo == "":
            resultado_label.config(text="-----Código do produto está vazio-----")
            return

        produto_codigo = produto_codigo.split()

        if len(produto_codigo) == 1:
            quantidade = 1
        else:
            quantidade = produto_codigo[1]
        produto_codigo = produto_codigo[0]

        if verificar_prod(produto_codigo):
            lista_produtos.append([produto_codigo, quantidade])
            preco_un = obter_valor_produto(produto_codigo)
            nome_produt = obter_nome_produto(produto_codigo)
            preco_tt = float(preco_un) * float(quantidade)


            text_box.configure(state="normal")  # Habilita a edição
            insert_centered_text(text_box,'{} --- {} x {} ----------------{}'.format(nome_produt,preco_un,quantidade,round(preco_tt,2)))
            text_box.configure(state="disabled")  # Desabilita a edição


            resultado_label.config(text="Produto adicionado")

            total_compra_label = 0
            for prod in lista_produtos:
                total_compra_label += obter_valor_produto(prod[0]) * int(prod[1])
            total_label.config(text="Total: {:.2f} R$".format(total_compra_label) ,font=("Arial", 20))



            codigo_entry.delete(0, tk.END)
        else:
            resultado_label.config(text="ERRO: Produto não cadastrado")
            codigo_entry.delete(0, tk.END)

        # Calcular total de compras
        total_compra = 0
        for prod in lista_produtos:
            total_compra += obter_valor_produto(prod[0]) * int(prod[1])

    # Função para finalizar a venda
    def finalizar(event=None):

        if len(lista_produtos) == 0:
            resultado_label.config(text="---Nota Vazia---")
            return
        try:
            if not int(forma_pagamento_entry.get()) in [1,2,3,4,5]:
                resultado_label.config(text="Opção de pagamento inválida")
                return
        except:
            resultado_label.config(text="Opção de pagamento inválida")
            return
        if forma_pagamento_entry.get() == "":
            resultado_label.config(text="Opção de pagamento inválida!!")
            return


        if (dinheiro_entry.get()) == '' and forma_pagamento_entry.get() == 1:
            resultado_label.config(text="---Nenhum valor recebido---")
            return
        # Obter código do cliente
        cod_cliente = cliente_entry.get() or '00000'

        if verificar_cliente(cod_cliente) == False:
            resultado_label.config(text="Cliente inválido")
            return

        # Obter CPF
        cpf = cpf_entry.get()
        if cpf != '' and not validar_cpf(cpf):
            resultado_label.config(text="CPF inválido")
            return

        # Obter forma de pagamento
        #
        forma_pagamento = int(forma_pagamento_entry.get())

        # Processar o pagamento
        global terminou_pagamento
        pagamento_realizado = False
        valor_pago = 0
        global iniciou_pagamento
        global valor_devido
        if  not iniciou_pagamento:
            valor_devido = float(total_compra)

        if forma_pagamento == 1:

            while not pagamento_realizado:
                try:
                    dinheiro_recebido = (dinheiro_entry.get())
                    #resultado_label.config(text='{} opp {}'.format(valor_devido, dinheiro_recebido))
                    if float(dinheiro_recebido) < float(valor_devido):
                        resultado_label.config(text="valor devido")
                        valor_devido -= float(dinheiro_recebido)
                        iniciou_pagamento = True
                        break
                    else:
                        #resultado_label.config(text='{} - {}'.format(valor_devido,dinheiro_recebido))
                        troco = float(dinheiro_recebido) - float(valor_devido)
                        valor_pago = total_compra
                        pagamento_realizado = True
                        terminou_pagamento = True
                except Exception as e:
                    resultado_label.config(text='valores inválido')
                    return
        elif forma_pagamento in [2, 3]:
            resultado_label.config(text="valor devido")
            pagamento_realizado = True
            terminou_pagamento = True
        elif forma_pagamento == 4:
            resultado_label.config(text="valor devido")
            pagamento_realizado = True
            terminou_pagamento = True
        elif forma_pagamento == 5:
            resultado_label.config(text="valor devido")
            if cod_cliente == '00000':
                resultado_label.config(text="Opção inválida para cliente não cadastrado")
                return
            elif encontrar_credito_cliente(cod_cliente) < valor_devido:
                valor_devido -= float(encontrar_credito_cliente(cod_cliente))
                atualizar_credito_cliente(cod_cliente, 0)
            else:
                atualizar_credito_cliente(cod_cliente, float(encontrar_credito_cliente(cod_cliente)) - float(valor_devido))
                pagamento_realizado = True
                terminou_pagamento = True

        if terminou_pagamento and len(lista_produtos) > 0:


            cliente_compra_id = verificar_cliente(cod_cliente)[0]
            # Registrar a venda no banco de dados
            data_e_hora = pegar_data_e_hora_formato_mysql()
            abrir_conexao()

            if forma_pagamento == 1:
                forma_pagamento = "Dinheiro"
            elif forma_pagamento == 2:
                forma_pagamento = "Cartão de Credito"
            elif forma_pagamento == 3:
                forma_pagamento = "Cartão de Débito"
            elif forma_pagamento == 4:
                forma_pagamento = "Pix"
            elif forma_pagamento == 5:
                forma_pagamento = "Cliente Fidelidade"

            comando_insercao = "INSERT INTO `vendas` (`ID`, `DataHora`, `ClienteID`, `Total`, `FormaPagamento`) VALUES (NULL, '{}', '{}', '{}', '{}');".format(data_e_hora, cliente_compra_id, total_compra, forma_pagamento)
            cursor = conexao.cursor()
            cursor.execute(comando_insercao)
            conexao.commit()
            cursor.close()
            conexao.close()

            # Obter o ID da venda
            id_venda = encontrar_id_venda(data_e_hora, cliente_compra_id, total_compra, forma_pagamento)

            # Registrar os itens da venda no banco de dados
            for prod_it in lista_produtos:
                quantidade_ = prod_it[1]
                id_produto_ = encontrar_id_produto(prod_it[0])
                abrir_conexao()
                comando_insercao = "INSERT INTO `itens_venda` (`id`, `venda_id`, `produto_id`, `quantidade`) VALUES (NULL, '{}', '{}', '{}');".format(id_venda, id_produto_, quantidade_)
                update_query = "UPDATE produtos SET quantidadeEstoque = quantidadeEstoque - {} WHERE codigo_de_produtos	 = {}".format(quantidade_,prod_it[0])
                cursor = conexao.cursor()
                cursor.execute(comando_insercao)
                conexao.commit()


                cursor.execute(update_query)
                conexao.commit()

                cursor.close()
                conexao.close()


            iniciou_pagamento = False
            codigo_entry.delete(0, tk.END)
            cpf_entry.delete(0, tk.END)
            forma_pagamento_entry.delete(0, tk.END)
            cliente_entry.delete(0, tk.END)
            dinheiro_entry.delete(0, tk.END)
            total_label.configure(text="0,0 R$")

            #messagebox.showerror("------", "Venda Concluída")
            terminou_pagamento = False
            lista_produtos.clear()

            try:
                troco = troco
            except:
                troco = 0
            text_fim_venda = '''
-----{}-----
    Cliente: {}
    Total: {:.2f}
    Troco: {:.2f}'''.format(data_e_hora,verificar_cliente(cod_cliente)[1],total_compra,round(troco,2))

            content = "----------------- Mini Mercado do Samuel -----------------\n\n\n"
            text_box.configure(state="normal")  # Habilita a edição
            tr_foco_codigo_prod()

            clear_text(text_box)
            insert_centered_text(text_box, content)
            text_box.configure(state="disabled")  # Desabilita a edição


            resultado_label.config(text="----------   Minimercado Do Nelson   ----------")

#            messagebox.showinfo("Venda Concluída", text_fim_venda)
            show_custom_message('Venda concluído',text_fim_venda)

            resultado_label.config(text="----------   Minimercado Do Nelson   ----------")


        else:
            resultado_label.config(text="Valor devido: {} ".format(round(valor_devido,2)))

    # Criação da interface gráfica
    root = tk.Toplevel()
    root.title("Venda")
    root.geometry("600x600")
    root.attributes("-fullscreen", True)
    root.configure(bg="blue")
    root.option_add('*Label.background', 'orange')

    # Criação dos frames
    main_frame = tk.Frame(root)

    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.configure(bg="orange"
                            "")
    entry_frame = tk.Frame(main_frame)
    entry_frame.grid(row=0, column=0, padx=10, pady=10)
    entry_frame.configure(bg="orange")

    # Código do produto
    codigo_label = tk.Label(entry_frame, text="Código do produto:")
    codigo_label.grid(row=0, column=0)

    codigo_entry = tk.Entry(entry_frame)
    codigo_entry.grid(row=0, column=1)
    codigo_entry.focus_set()

    # Funções de foco
    def tr_foco_cliente(event=None):
        cliente_entry.focus_set()

    def tr_foco_codigo_prod(event=None):
        codigo_entry.focus_set()

    def tr_foco_cpf(event=None):
        cpf_entry.focus_set()

    def tr_foco_forma_de_pagamento(event=None):
        forma_pagamento_entry.focus_set()

    def tr_foco_dinheiro(event=None):
        dinheiro_entry.focus_set()

    # Código do cliente
    cliente_label = tk.Label(entry_frame, text="Código do cliente:")
    cliente_label.grid(row=1, column=0)

    cliente_entry = tk.Entry(entry_frame)
    cliente_entry.grid(row=1, column=1)

    # CPF
    cpf_label = tk.Label(entry_frame, text="CPF:")
    cpf_label.grid(row=2, column=0)

    cpf_entry = tk.Entry(entry_frame)
    cpf_entry.grid(row=2, column=1)

    # Forma de pagamento
    text_forma_de_pagamento = """Forma de pagamento:
    1 - Dinheiro
    2 - Cartão de Crédito
    3 - Cartão de Débito
    4 - Pix
    5 - Saldo cliente fidelidade"""

    forma_pagamento_label = tk.Label(entry_frame, text=text_forma_de_pagamento)
    forma_pagamento_label.grid(row=3, column=0)

    forma_pagamento_entry = tk.Entry(entry_frame)
    forma_pagamento_entry.grid(row=3, column=1)

    # Valor recebido
    dinheiro_label = tk.Label(entry_frame, text="Valor recebido:")
    dinheiro_label.grid(row=4, column=0)

    dinheiro_entry = tk.Entry(entry_frame)
    dinheiro_entry.grid(row=4, column=1)


    # Label de resultado
    resultado_label = tk.Label(entry_frame, text="")
    resultado_label.grid(row=6, column=0, columnspan=2)


    # Eventos de teclado
    codigo_entry.bind("<Return>", processar)
    codigo_entry.bind("<,>", tr_foco_cliente)
    codigo_entry.bind("<Down>", tr_foco_cliente)

    cliente_entry.bind("<Return>", tr_foco_cpf)
    cliente_entry.bind("<Down>", tr_foco_cpf)
    cliente_entry.bind("<Up>", tr_foco_codigo_prod)

    cpf_entry.bind("<Return>", tr_foco_forma_de_pagamento)
    cpf_entry.bind("<Down>", tr_foco_forma_de_pagamento)
    cpf_entry.bind("<Up>", tr_foco_cliente)

    forma_pagamento_entry.bind("<Return>", tr_foco_dinheiro)
    forma_pagamento_entry.bind("<Down>", tr_foco_dinheiro)
    forma_pagamento_entry.bind("<Up>", tr_foco_cpf)

    dinheiro_entry.bind("<Return>", finalizar)
    dinheiro_entry.bind("<Up>", tr_foco_forma_de_pagamento)

    # Frame do texto
    text_frame = tk.Frame(root)
    text_frame.grid(row=0, column=1, sticky="nsew")

    # Widget Text
    text_box = tk.Text(text_frame, height=47, width=130,bg="yellow")
    text_box.config(state="disabled")
    text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Barra de rolagem
    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Vincula a barra de rolagem ao widget Text
    text_box.config(yscrollcommand=scrollbar.set)

    scrollbar.config(command=text_box.yview)

    # Adiciona algum conteúdo ao widget Text
    content = "----------------- Mini Mercado do Samuel -----------------\n\n\n"
    text_box.configure(state="normal")  # Habilita a edição
    insert_centered_text(text_box,content)
    #text_box.insert(tk.END, content)
    text_box.configure(state="disabled")  # Desabilita a edição
    resultado_label.config(text="----------   Minimercado Do Samuel   ----------")

    # Carrega a imagem
    image = Image.open("img/img.png")
    image = image.resize((300, 500))  # Redimensiona a imagem, se necessário

    # Cria um objeto ImageTk para exibir a imagem no widget Label
    photo = ImageTk.PhotoImage(image)

    # Cria um widget Label e exibe a imagem
    image_label = tk.Label(entry_frame, image=photo)
    image_label.grid(row=7, column=0, columnspan=2)



    total_label = tk.Label(entry_frame, text="0,0 R$",bg="red")
    total_label.grid(row=8, column=0, columnspan=2)

    root.focus_force()
    root.mainloop()
#criar_janela_login()


