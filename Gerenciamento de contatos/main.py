import sys
import sqlite3
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox


class GerenciamentoContatos(QMainWindow):
    def __init__(self):
        super().__init__()

        #Configurações da janela principal
        self.setWindowTitle('Gerenciamento de contatos')
        self.setGeometry(100, 100, 400, 500)

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
        self.lbl_telefone = QLabel('Telefone')
        self.txt_telefone = QLineEdit()

        #Widgets do layout referente às interações com os clientes da lista
        self.btn_salvar = QPushButton('Salvar')
        self.btn_editar = QPushButton('Editar')
        self.btn_remover = QPushButton('Remover')

        #Define as cores dos botões
        self.btn_salvar.setStyleSheet("background-color: #BFD3C1;"
                                      "border-radius: 5px;"
                                      )
        self.btn_editar.setStyleSheet("background-color: #FFD2B5;"
                                      "border-radius: 5px;"
                                      )
        self.btn_remover.setStyleSheet("background-color: #EFC7C2;"
                                       "border-radius: 5px;"
                                       )

        #Widget de lista para demonstrar os clientes já cadastrados
        self.lst_contatos = QListWidget()
        self.lst_contatos.itemClicked.connect(self.selecionar_contato)

        #Adiciona os widgets ao layout
        self.layout.addWidget(self.lbl_nome)
        self.layout.addWidget(self.txt_nome)
        self.layout.addWidget(self.lbl_sobrenome)
        self.layout.addWidget(self.txt_sobrenome)
        self.layout.addWidget(self.lbl_email)
        self.layout.addWidget(self.txt_email)
        self.layout.addWidget(self.lbl_telefone)
        self.layout.addWidget(self.txt_telefone)
        self.layout.addWidget(self.lst_contatos)
        self.layout.addWidget(self.btn_salvar)
        self.layout.addWidget(self.btn_editar)
        self.layout.addWidget(self.btn_remover)

        #Cria o banco de dados
        self.criar_banco()

        #Preenche a lista de clientes
        self.carregar_contatos()

        #Valida cliente selecionado
        self.contato_selecionado = None

        #Ações para interação com banco de dados
        self.btn_salvar.clicked.connect(self.salvar_contato)
        self.btn_editar.clicked.connect(self.editar_contato)
        self.btn_remover.clicked.connect(self.validar_remocao)
    def criar_banco(self):
        conexao = sqlite3.connect('cadastro_contatos.db')
        cursor = conexao.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS contatos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    sobrenome TEXT,
                    email TEXT,
                    telefone TEXT
                    )
        ''')
        conexao.close()

    def salvar_contato(self):
        nome = self.txt_nome.text()
        sobrenome = self.txt_sobrenome.text()
        email = self.txt_email.text()
        telefone = self.txt_telefone.text()

        if nome and sobrenome and email and telefone:
            conexao = sqlite3.connect('cadastro_contatos.db')
            cursor = conexao.cursor()

            if self.contato_selecionado is None:
                cursor.execute('''
                    INSERT INTO contatos(nome, sobrenome, email, telefone)
                    VALUES (?, ?, ?, ?)
                ''', (nome, sobrenome, email, telefone))

            else:
                cursor.execute('''
                    UPDATE contatos
                    SET nome = ?, sobrenome = ?, email = ?, telefone = ?
                    WHERE ID = ?
                ''', (nome, sobrenome, email, telefone, self.contato_selecionado['id']))

            conexao.commit()
            conexao.close()

            #Limpar os campos após o insert do cliente
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.txt_telefone.clear()
            self.contato_selecionado = None
            self.carregar_contatos()

        else:
            QMessageBox.warning(self,'Aviso', 'Preencha todos os dados')


    def carregar_contatos(self):
        self.lst_contatos.clear()    #para não duplicar/triplicar... as informações
        conexao = sqlite3.connect('cadastro_contatos.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome, sobrenome, email, telefone FROM contatos')
        contatos = cursor.fetchall()
        conexao.close()

        for contato in contatos:
            id_contato, nome, sobrenome, email, telefone = contato
            self.lst_contatos.addItem(f'{id_contato} | {nome} {sobrenome} | {email} | {telefone}')


    def selecionar_contato(self, item):
        self.contato_selecionado = {
            'id': item.text().split()[0],
            'nome': self.txt_nome.text(),
            'sobrenome': self.txt_sobrenome.text(),
            'email': self.txt_email.text(),
            'telefone': self.txt_telefone.text()
        }

    def editar_contato(self):
        if self.btn_editar.text() == 'Editar':
            if self.contato_selecionado is not None:
                conexao = sqlite3.connect('cadastro_contatos.db')
                cursor = conexao.cursor()
                cursor.execute('SELECT nome, sobrenome, email, telefone FROM contatos WHERE id = ?', self.contato_selecionado['id'])
            contato = cursor.fetchone()
            conexao.close()

            if contato:
                nome, sobrenome, email, telefone = contato
                self.txt_nome.setText(nome)
                self.txt_sobrenome.setText(sobrenome)
                self.txt_email.setText(email)
                self.txt_telefone.setText(telefone)
                self.btn_editar.setText('Cancelar')
        else:
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.txt_telefone.clear()
            self.btn_editar.setText('Editar')

    def validar_remocao(self):
        if self.contato_selecionado is not None:
            mensagem = QMessageBox()
            mensagem.setWindowTitle('Confirmação')
            mensagem.setText('Tem certeza que deseja remover o contato?')
            #Define o texto dos botões de confirmação para sim e não
            botao_sim = mensagem.addButton('Sim', QMessageBox.YesRole)
            botao_nao = mensagem.addButton('Não', QMessageBox.NoRole)
            #Define o icone como questionamento
            mensagem.setIcon(QMessageBox.Question)
            mensagem.exec()

            if mensagem.clickedButton() == botao_sim:
                self.remove_contato()

    def remove_contato(self):
        if self.contato_selecionado is not None:
            conexao = sqlite3.connect('cadastro_contatos.db')
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM contatos WHERE id = ?',
                           self.contato_selecionado['id'])
            conexao.commit()
            conexao.close()
            self.carregar_contatos()
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.txt_telefone.clear()
            self.contato_selecionado = None


if __name__== '__main__':
    app = QApplication(sys.argv)
    window = GerenciamentoContatos()
    window.show()
    sys.exit(app.exec())