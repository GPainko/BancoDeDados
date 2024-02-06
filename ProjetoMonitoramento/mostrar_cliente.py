import tkinter as tk
from tkinter import ttk
import mysql.connector

# Conectar ao banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database="monitoramento"
)

# Cursor para executar operações no banco de dados
cursor = db.cursor()

# Função para obter e exibir clientes do banco
def show_clients():
    # Consulta para obter todos os clientes
    cursor.execute("SELECT * FROM cliente")
    results = cursor.fetchall()

    # Limpar a exibição anterior
    for widget in tree.get_children():
        tree.delete(widget)

    # Exibir os clientes na interface gráfica
    for row in results:
        tree.insert("", "end", values=row)

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Visualizador de Clientes do Banco de Dados")

# Botão para mostrar clientes
btn_show_clients = tk.Button(root, text="Mostrar Clientes", command=show_clients)
btn_show_clients.pack(pady=10)

# Treeview para exibir clientes em uma tabela
columns = ("ID", "Nome", "CPF", "Endereço")  # Adapte de acordo com a sua tabela
tree = ttk.Treeview(root, columns=columns, show="headings")

# Definir os cabeçalhos das colunas
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)  # Ajuste a largura das colunas conforme necessário

tree.pack(padx=10, pady=10)

# Rodar a aplicação
root.mainloop()
