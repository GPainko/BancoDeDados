import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re

def formatar_cpf(entry):
    # Função para formatar o CPF conforme o usuário digita
    current_text = entry.get()
    if re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", current_text):
        return
    if re.match(r"\d{11}", current_text):
        formatted_text = f"{current_text[:3]}.{current_text[3:6]}.{current_text[6:9]}-{current_text[9:]}"
        entry.delete(0, tk.END)
        entry.insert(0, formatted_text)

def adicionar_cliente():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    endereco = entry_endereco.get()
    numero_cameras = entry_num_cameras.get()

    # Validação do CPF com uso de Regex
    if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
        messagebox.showerror("Erro", "CPF inválido. Por favor, utilize o formato XXX.XXX.XXX-XX.")
        return

    try:
        numero_cameras = int(numero_cameras)
    except ValueError:
        messagebox.showerror("Erro", "Número de câmeras deve ser um número inteiro.")
        return
    
    # Conexão com o banco de dados MySQL
    try:
        conn = mysql.connector.connect(
            host="localhost",       # Ou o IP do seu servidor MySQL
            user="root",     # Substitua com o seu usuário do MySQL
            password="81107984",   # Substitua com a sua senha do MySQL
            database="monitoramento"   # Substitua com o nome do banco de dados no MySQL
        )
        cursor = conn.cursor()
        
        # Comando SQL para inserir os dados
        sql = "INSERT INTO cliente (nome, cpf, localizacao, numero_cameras) VALUES (%s, %s, %s, %s)"
        valores = (nome, cpf, endereco, numero_cameras)
        cursor.execute(sql, valores)
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Cliente registrado com sucesso!")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao adicionar cliente: {err}")
    finally:
        if conn.is_connected():
            conn.close()

# Criação da interface gráfica com tkinter
root = tk.Tk()
root.title("Registrar Cliente")

# Campos de entrada
tk.Label(root, text="Nome:").grid(row=0, column=0, sticky="w")
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="CPF:").grid(row=1, column=0, sticky="w")
entry_cpf = ttk.Entry(root)  # Usando ttk.Entry para a máscara
entry_cpf.grid(row=1, column=1)
entry_cpf.bind('<KeyRelease>', lambda event: formatar_cpf(entry_cpf))  # Adicionando callback de formatação

tk.Label(root, text="Endereço:").grid(row=2, column=0, sticky="w")
entry_endereco = tk.Entry(root)
entry_endereco.grid(row=2, column=1)

tk.Label(root, text="Número de Câmeras:").grid(row=3, column=0, sticky="w")
entry_num_cameras = tk.Entry(root)
entry_num_cameras.grid(row=3, column=1)

# Botão para registrar cliente
btn_registrar = tk.Button(root, text="Registrar", command=adicionar_cliente)
btn_registrar.grid(row=4, column=0, columnspan=2)

# Executa a interface gráfica
root.mainloop()