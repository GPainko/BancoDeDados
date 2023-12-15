import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import io

config = {
    'user': 'root',
    'password': '81107984',
    'host': 'localhost',
    'database': 'monitoramento',
    'raise_on_warnings': True,
}

# Conexão com o banco de dados
try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    messagebox.showerror("Database Connection Error", f"An error occurred: {err}")
    exit(1)

# Query para buscar as imagens
query = "SELECT imagem FROM imagens" 

class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Viewer")

        # Navegação entre imagens
        self.image_index = 0
        self.images = self.load_images()
        
        if not self.images:
            messagebox.showerror("No Images", "There are no images to display.")
            return
        
        self.displayed_image_label = tk.Label(self)
        self.displayed_image_label.pack()

        self.prev_button = tk.Button(self, text="Previous", command=self.show_prev_image)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self, text="Next", command=self.show_next_image)
        self.next_button.pack(side=tk.RIGHT)

        self.update_image()

    def load_images(self):
        images = []
        cursor = cnx.cursor()
        cursor.execute(query)
        for (image_blob,) in cursor:
            image_stream = io.BytesIO(image_blob)
            image = Image.open(image_stream)
            images.append(image)
        cursor.close()
        return images

    def update_image(self):
        image = ImageTk.PhotoImage(self.images[self.image_index])
        self.displayed_image_label.config(image=image)
        self.displayed_image_label.image = image  # Keep a reference!

    def show_next_image(self):
        if self.image_index < len(self.images) - 1:
            self.image_index += 1
            self.update_image()

    def show_prev_image(self):
        if self.image_index > 0:
            self.image_index -= 1
            self.update_image()


if __name__ == '__main__':
    app = ImageApp()
    app.mainloop()
    cnx.close()