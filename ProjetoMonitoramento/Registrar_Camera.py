import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Função para conectar ao banco de dados MySQL
def connect_to_db():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            user='root',  
            password='81107984',  
            database='monitoramento'  
        )
    except Exception as e:
        messagebox.showerror("Erro de conexão", f"Ocorreu um erro ao conectar ao banco de dados:\n{e}")
    return connection

# Função para inserir dados no banco de dados
def insert_data(registro, cliente_id, local):
    connection = connect_to_db()
    if connection is not None:
        try:
            cursor = connection.cursor()
            sql_insert_query = """
            INSERT INTO camera (registro, cliente_id, localinstalada)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql_insert_query, (registro, cliente_id, local))
            connection.commit()
            messagebox.showinfo("Sucesso", "Registro inserido com sucesso no banco de dados!")
        except Exception as e:
            messagebox.showerror("Erro de inserção", f"Ocorreu um erro ao inserir os dados:\n{e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Função chamada quando o botão de registro é pressionado
def on_register_button_click():
    registro = registro_entry.get()
    cliente = cliente_entry.get()
    local = local_entry.get()
    
    # Valida se o registro é composto somente por números
    if not registro.isdigit():
        messagebox.showwarning("Entrada inválida", "O campo 'registro' deve conter apenas números.")
        return
    
    if cliente and local:
        insert_data(registro, cliente, local)
    else:
        messagebox.showwarning("Entrada inválida", "Todos os campos são obrigatórios.")

# Configuração da interface gráfica 
app = tk.Tk()
app.title('Registro de Câmeras')
app.geometry('300x150')

# Campo de entrada para o registro
tk.Label(app, text='Registro').grid(row=0, column=0)
registro_entry = tk.Entry(app)
registro_entry.grid(row=0, column=1)

# Campo de entrada para o nome do cliente
tk.Label(app, text='Cliente ID').grid(row=1, column=0)
cliente_entry = tk.Entry(app)
cliente_entry.grid(row=1, column=1)

# Campo de entrada para o local da instalação
tk.Label(app, text='Local').grid(row=2, column=0)
local_entry = tk.Entry(app)
local_entry.grid(row=2, column=1)

# Botão de registro
register_button = tk.Button(app, text='Registrar', command=on_register_button_click)
register_button.grid(row=3, column=0, columnspan=2)

app.mainloop()