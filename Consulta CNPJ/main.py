import sys
import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Consuta CNPJ')
        self.setGeometry(100, 100, 600, 500)

        #Componentes de interface
        self.lbl_cnpj = QLabel('CNPJ')
        self.txt_cnpj = QLineEdit()
        self.btn_consultar = QPushButton('Consultar CNPJ')
        self.lbl_resultado = QLabel()


        #Componentes a serem preenchidos com a resposta da consulta
        self.lbl_empresa = QLabel('Nome da empresa')
        self.txt_empresa = QLineEdit()
        self.lbl_abertura = QLabel('Data da abertura')
        self.txt_abertura = QLineEdit()
        self.lbl_situacao = QLabel('Situação')
        self.txt_situacao = QLineEdit()
        self.lbl_tipo = QLabel('Tipo')
        self.txt_tipo = QLineEdit()
        self.lbl_endereco = QLabel('Endereço:')
        self.lbl_logradouro = QLabel('Logradouro')
        self.txt_logradouro = QLineEdit()
        self.lbl_numero = QLabel('Número')
        self.txt_numero = QLineEdit()
        self.lbl_bairro = QLabel('Bairro')
        self.txt_bairro = QLineEdit()
        self.lbl_municipio = QLabel('Município')
        self.txt_municipio = QLineEdit()
        self.lbl_estado = QLabel('Estado')
        self.txt_estado = QLineEdit()
        self.lbl_cep = QLabel('Cep')
        self.txt_cep = QLineEdit()
        self.btn_limpar_campos = QPushButton('Limpar campos')

        #Criação e inserção dos widgets ao layout

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_cnpj)
        layout.addWidget(self.txt_cnpj)
        layout.addWidget(self.btn_consultar)
        layout.addWidget(self.lbl_resultado)
        layout.addWidget(self.lbl_empresa)
        layout.addWidget(self.txt_empresa)
        layout.addWidget(self.lbl_abertura)
        layout.addWidget(self.txt_abertura)
        layout.addWidget(self.lbl_situacao)
        layout.addWidget(self.txt_situacao)
        layout.addWidget(self.lbl_tipo)
        layout.addWidget(self.txt_tipo)
        layout.addWidget(self.lbl_endereco)
        layout.addWidget(self.lbl_logradouro)
        layout.addWidget(self.txt_logradouro)
        layout.addWidget(self.lbl_numero)
        layout.addWidget(self.txt_numero)
        layout.addWidget(self.lbl_bairro)
        layout.addWidget(self.txt_bairro)
        layout.addWidget(self.lbl_municipio)
        layout.addWidget(self.txt_municipio)
        layout.addWidget(self.lbl_estado)
        layout.addWidget(self.txt_estado)
        layout.addWidget(self.lbl_cep)
        layout.addWidget(self.txt_cep)
        layout.addWidget(self.btn_limpar_campos)

        self.btn_consultar.clicked.connect(self.consulta_cnpj)
        self.btn_limpar_campos.clicked.connect(self.limpa_campos)

        #Definição do widget a ser demonstrado na janela
        widget_central = QWidget()
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

    def consulta_cnpj(self):
        cnpj = self.txt_cnpj.text().replace('-', '').replace('/', '').replace('.', '')
        if self.valida_cnpj(cnpj):
            dados = self.obter_dados_cnpj(cnpj)
            if dados:
                self.preenche_dados(dados)
        else:
            self.lbl_resultado.setText('CNPJ Inválido')

    def preenche_dados(self, dados):
        self.txt_empresa.setText(dados.get('nome', ''))
        self.txt_abertura.setText(dados.get('abertura', ''))
        self.txt_situacao.setText(dados.get('situacao', ''))
        self.txt_tipo.setText(dados.get('tipo', ''))
        self.txt_logradouro.setText(dados.get('logradouro', ''))
        self.txt_numero.setText(dados.get('numero', ''))
        self.txt_bairro.setText(dados.get('bairro', ''))
        self.txt_municipio.setText(dados.get('municipio', ''))
        self.txt_estado.setText(dados.get('uf', ''))
        self.txt_cep.setText(dados.get('cep', ''))

    def obter_dados_cnpj(self, cnpj):
        url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
        try:
            resposta = requests.get(url)

            if resposta.status_code == 200:
                return resposta.json()
        except Exception as e:
            self.lbl_resultado.setText(f'Erro ao consultar CNPJ. Erro {e}.')



    def valida_cnpj(self, cnpj):
        return cnpj.isnumeric() and len(cnpj) == 14


    def limpa_campos(self):
        self.txt_cnpj.clear()
        self.txt_empresa.clear()
        self.txt_abertura.clear()
        self.txt_situacao.clear()
        self.txt_tipo.clear()
        self.txt_logradouro.clear()
        self.txt_numero.clear()
        self.txt_bairro.clear()
        self.txt_municipio.clear()
        self.txt_estado.clear()
        self.txt_cep.clear()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())