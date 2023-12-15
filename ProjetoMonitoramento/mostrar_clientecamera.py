import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import mysql.connector

# Configure a conexão do banco de dados aqui
db_config = {
    'user': 'root',
    'password': '81107984',
    'host': 'localhost',
    'database': 'monitoramento'
}

# Consulta SQL para sua view
SQL_QUERY = 'SELECT * FROM view_cliente_com_cameras'

# Classe da Aplicação
class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setWindowTitle('Resultados da View MySQL')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()
        
    def initUI(self):
        # Configuração do layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QVBoxLayout(central_widget)

        # Tabela para exibir os resultados da view
        self.table_widget = QTableWidget()
        lay.addWidget(self.table_widget)

        # Carrega os resultados do banco de dados
        self.loadResultsFromDB()

    def loadResultsFromDB(self):
        try:
            # Conecta ao banco de dados
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(SQL_QUERY)

            # Obtém os resultados
            results = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]

            # Configura a tabela
            self.table_widget.setRowCount(len(results))
            self.table_widget.setColumnCount(len(column_names))
            self.table_widget.setHorizontalHeaderLabels(column_names)

            # Preenche a tabela com os resultados
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        except mysql.connector.Error as e:
            print(f'Erro ao conectar ao MySQL: {e}')
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MyApp()
    mainWin.show()
    sys.exit(app.exec_())