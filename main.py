import codes.pdv22
import tkinter as tk
from PIL import ImageTk, Image





def clientes__0():
    import codes.clientes
    codes.clientes.criar_janela_clientes()

def compras__0():
    import codes.compras
    codes.compras.criar_janela_compras()

def fornecedores__0():
    import codes.fornecedores
    codes.fornecedores.criar_janela_fornecedores()

def produtos__0():
    import codes.produtos
    codes.produtos.criar_janela_produtos()

def usuarios__0():
    import codes.usuarios
    codes.usuarios.criar_janela_usuarios()

def vendas__0():
    import codes.vendas
    codes.vendas.criar_janela_vendas()

def pdv__0():
    import pdv22
    codes.pdv22.criar_janela_login()


root__0 = tk.Tk()
root__0.title("Executar Funções")
root__0.geometry('800x600')
root__0.minsize(800, 600)  # Define o tamanho mínimo da janela
root__0.configure(bg="orange")

# Carrega a imagem
image_0 = Image.open("img/sistem_comercios.png")
image_0 = image_0.resize((600, 90))  # Redimensiona a imagem, se necessário

# Cria um objeto ImageTk para exibir a imagem no widget Label
photo_0 = ImageTk.PhotoImage(image_0)


# Cria um widget Label e exibe a imagem
image_label_0 = tk.Label(root__0, image=photo_0)
image_label_0.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
image_label_0.configure(bg="orange")

# Crie um frame para os botões
button_frame_0 = tk.Frame(root__0)
button_frame_0.grid(row=1, column=0, columnspan=4)
button_frame_0.configure(bg="orange")
# Crie os botões
button1 = tk.Button(button_frame_0, text="Clientes", command=clientes__0, width=30, height=6)
button2 = tk.Button(button_frame_0, text="Compras", command=compras__0, width=30, height=6)
button3 = tk.Button(button_frame_0, text="Fornecedores", command=fornecedores__0, width=30, height=6)
button4 = tk.Button(button_frame_0, text="Usuários", command=usuarios__0, width=30, height=6)
button5 = tk.Button(button_frame_0, text="Vendas", command=vendas__0, width=30, height=6)
button6 = tk.Button(button_frame_0, text="Produtos", command=produtos__0, width=30, height=6)
button7 = tk.Button(button_frame_0, text="PDV", command=codes.pdv22.criar_janela_login, width=30, height=6)

# Posicione os botões usando o layout grid
button1.grid(row=0, column=0, padx=5, pady=5)
button2.grid(row=0, column=1, padx=5, pady=5)
button3.grid(row=0, column=2, padx=5, pady=5)
button4.grid(row=1, column=0, padx=5, pady=5)
button5.grid(row=1, column=1, padx=5, pady=5)
button6.grid(row=1, column=2, padx=5, pady=5)
button7.grid(row=2, column=1, padx=5, pady=5)

# Configure o peso das linhas e colunas para expandir e centralizar os elementos
root__0.grid_rowconfigure(0, weight=1)
root__0.grid_rowconfigure(1, weight=1)
root__0.grid_columnconfigure(0, weight=1)
root__0.grid_columnconfigure(1, weight=1)
root__0.grid_columnconfigure(2, weight=1)

# Configure o peso das linhas e colunas do frame dos botões para centralizá-los verticalmente
button_frame_0.grid_rowconfigure(0, weight=1)
button_frame_0.grid_rowconfigure(1, weight=1)
button_frame_0.grid_rowconfigure(2, weight=1)

root__0.mainloop()
