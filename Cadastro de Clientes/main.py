import sys
import sqlite3
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QListWidget, QMessageBox


class CadastroCliente(QMainWindow):
    def __init__(self):
        super().__init__()

        #Configurações da janela principal
        self.setWindowTitle('Cadastro de clientes')
        self.setGeometry(100, 100, 400, 600)

        #Widget central da janela para receber os elementos de layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        #Widgets do layout
        self.lbl_nome = QLabel('Nome')
        self.txt_nome = QLineEdit()
        self.lbl_sobrenome = QLabel('Sobrenome')
        self.txt_sobrenome = QLineEdit()
        self.lbl_email = QLabel('E-mail')
        self.txt_email = QLineEdit()

        #Widgets do layout referente às interações com os clientes da lista
        self.btn_salvar = QPushButton('Salvar')
        self.btn_editar = QPushButton('Editar')
        self.btn_remover = QPushButton('Remover')

        #Define as cores dos botões
        self.btn_salvar.setStyleSheet("background-color: lightgreen;"
                                      "border-radius: 5px;"
                                      "border: 2px solid green;"
                                      )
        self.btn_editar.setStyleSheet("background-color: #F1EB9C;"
                                      "border-radius: 5px;"
                                      "border: 2px solid orange;"
                                      )
        self.btn_remover.setStyleSheet("background-color: #FFA8A8;"
                                       "border-radius: 5px;"
                                       "border: 2px solid red;"
                                       )

        #Widget de lista para demonstrar os clientes já cadastrados
        self.lst_clientes = QListWidget()
        self.lst_clientes.itemClicked.connect(self.selecionar_cliente)

        #Adiciona os widgets ao layout
        self.layout.addWidget(self.lbl_nome)
        self.layout.addWidget(self.txt_nome)
        self.layout.addWidget(self.lbl_sobrenome)
        self.layout.addWidget(self.txt_sobrenome)
        self.layout.addWidget(self.lbl_email)
        self.layout.addWidget(self.txt_email)
        self.layout.addWidget(self.lst_clientes)
        self.layout.addWidget(self.btn_salvar)
        self.layout.addWidget(self.btn_editar)
        self.layout.addWidget(self.btn_remover)

        #Cria o banco de dados
        self.criar_banco()

        #Preenche a lista de clientes
        self.carregar_clientes()

        #Valida cliente selecionado
        self.cliente_selecionado = None

        #Ações para interação com banco de dados
        self.btn_salvar.clicked.connect(self.salvar_cliente)
        self.btn_editar.clicked.connect(self.editar_cliente)
        self.btn_remover.clicked.connect(self.validar_remocao)
    def criar_banco(self):
        conexao = sqlite3.connect('cadastro_clientes.db')
        cursor = conexao.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clientes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    sobrenome TEXT,
                    email TEXT
                    )
        ''')
        conexao.close()

    def salvar_cliente(self):
        nome = self.txt_nome.text()
        sobrenome = self.txt_sobrenome.text()
        email = self.txt_email.text()

        if nome and sobrenome and email:
            conexao = sqlite3.connect('cadastro_clientes.db')
            cursor = conexao.cursor()

            if self.cliente_selecionado is None:
                cursor.execute('''
                    INSERT INTO clientes(nome, sobrenome, email)
                    VALUES (?, ?, ?)
                ''', (nome, sobrenome, email))

            else:
                cursor.execute('''
                    UPDATE clientes
                    SET nome = ?, sobrenome = ?, email = ?
                    WHERE ID = ?
                ''', (nome, sobrenome, email, self.cliente_selecionado['id']))

            conexao.commit()
            conexao.close()

            #Limpar os campos após o insert do cliente
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.cliente_selecionado = None
            self.carregar_clientes()

        else:
            QMessageBox.warning(self,'Aviso', 'Preencha todos os dados')


    def carregar_clientes(self):
        self.lst_clientes.clear()    #para não duplicar/triplicar... as informações
        conexao = sqlite3.connect('cadastro_clientes.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome, sobrenome, email FROM clientes')
        clientes = cursor.fetchall()
        conexao.close()

        for cliente in clientes:
            id_cliente, nome, sobrenome, email = cliente
            self.lst_clientes.addItem(f'{id_cliente} | {nome} {sobrenome} | {email}')


    def selecionar_cliente(self, item):
        self.cliente_selecionado = {
            'id': item.text().split()[0],
            'nome': self.txt_nome.text(),
            'sobrenome': self.txt_sobrenome.text(),
            'email': self.txt_email.text()
        }

    def editar_cliente(self):
        if self.btn_editar.text() == 'Editar':
            if self.cliente_selecionado is not None:
                conexao = sqlite3.connect('cadastro_clientes.db')
                cursor = conexao.cursor()
                cursor.execute('SELECT nome, sobrenome, email FROM clientes WHERE id = ?', self.cliente_selecionado['id'])
            cliente = cursor.fetchone()
            conexao.close()

            if cliente:
                nome, sobrenome, email = cliente
                self.txt_nome.setText(nome)
                self.txt_sobrenome.setText(sobrenome)
                self.txt_email.setText(email)
                self.btn_editar.setText('Cancelar')
        else:
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.btn_editar.setText('Editar')

    def validar_remocao(self):
        if self.cliente_selecionado is not None:
            mensagem = QMessageBox()
            mensagem.setWindowTitle('Confirmação')
            mensagem.setText('Tem certeza que deseja remover o cliente?')
            #Define o texto dos botões de confirmação para sim e não
            botao_sim = mensagem.addButton('Sim', QMessageBox.YesRole)
            botao_nao = mensagem.addButton('Não', QMessageBox.NoRole)
            #Define o icone como questionamento
            mensagem.setIcon(QMessageBox.Question)
            mensagem.exec()

            if mensagem.clickedButton() == botao_sim:
                self.remove_cliente()

    def remove_cliente(self):
        if self.cliente_selecionado is not None:
            conexao = sqlite3.connect('cadastro_clientes.db')
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM clientes WHERE id = ?',
                           self.cliente_selecionado['id'])
            conexao.commit()
            conexao.close()
            self.carregar_clientes()
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.cliente_selecionado = None


if __name__== '__main__':
    app = QApplication(sys.argv)
    window = CadastroCliente()
    window.show()
    sys.exit(app.exec())