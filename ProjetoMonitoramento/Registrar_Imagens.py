import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import os

# Configure os detalhes de conexão com o banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '81107984',
    'database': 'monitoramento'
}

# Função para inserir imagem e hora no banco de dados
def insert_image(image_path, timestamp):
    # Conexão com o banco de dados
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Lê a imagem e converte para blob
    with open(image_path, 'rb') as f:
        binary_data = f.read()
    
    # Insere os dados na tabela
    query = "INSERT INTO imagens (imagem, horario) VALUES (%s, %s)"
    cursor.execute(query, (binary_data, timestamp))
    conn.commit()
    
    # Fecha a conexão
    cursor.close()
    conn.close()

# Função chamada quando o botão de upload é pressionado
def upload_action():
    # Abre o diálogo para o usuário escolher uma imagem
    file_path = filedialog.askopenfilename()
    if file_path:
        # Armazena a imagem e a hora atual no banco de dados
        current_time = datetime.now()
        insert_image(file_path, current_time)
    
        # Atualiza a imagem na interface gráfica
        load_image(file_path)

# Carrega e exibe a imagem na interface gráfica
def load_image(path):
    img = Image.open(path)
    img.thumbnail((200, 200))  # Redimensiona para uma miniatura
    img = ImageTk.PhotoImage(img)
    
    img_label.configure(image=img)
    img_label.image = img  # Mantenha uma referência!

# Cria a interface gráfica
root = tk.Tk()
root.title("Upload de Imagem")

# Label para exibir a imagem
img_label = tk.Label(root)
img_label.pack()

# Botão de upload
upload_button = tk.Button(root, text="Upload Imagem", command=upload_action)
upload_button.pack()

root.mainloop()