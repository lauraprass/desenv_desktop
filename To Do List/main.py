import sys
from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QListWidget, QVBoxLayout, QWidget, QInputDialog
from PySide6.QtCore import Qt

class AppListaTarefas(QWidget):
    def __init__(self):
        super().__init__()


        self.tarefas = []

        #Configuração da janela principal
        self.setWindowTitle('To do List')
        self.setGeometry(100, 100, 400, 600)

        #Widgets da interface
        self.txt_tarefa = QLineEdit()
        self.btn_adicionar = QPushButton('Adicionar')
        self.btn_adicionar.setStyleSheet("background-color: lightgreen;"
                                         "border-radius: 5px;"
                                         "border: 2px solid green;")

        self.btn_adicionar.clicked.connect(self.adicionar_tarefa)

        self.btn_concluir = QPushButton('Concluir')
        self.btn_concluir.setStyleSheet("background-color: lightblue;"
                                        "border-radius: 5px;"
                                        "border: 2px solid blue;")

        self.btn_concluir.clicked.connect(self.concluir_tarefa)

        self.btn_editar = QPushButton('Editar')
        self.btn_editar.setStyleSheet("background-color: yellow;"
                                      "border-radius: 5px;"
                                      "border: 2px solid orange;")

        self.btn_editar.clicked.connect(self.editar_tarefa)

        self.btn_remover = QPushButton('Remover')
        self.btn_remover.setStyleSheet("background-color: lightcoral;"
                                       "border-radius: 5px;"
                                       "border: 2px solid red;")

        self.btn_remover.clicked.connect(self.remover_tarefa)

        self.lst_tarefa = QListWidget()

        #Configuração do layout
        layout = QVBoxLayout()
        layout.addWidget(self.txt_tarefa)
        layout.addWidget(self.btn_adicionar)
        layout.addWidget(self.btn_concluir)
        layout.addWidget(self.btn_editar)
        layout.addWidget(self.btn_remover)
        layout.addWidget(self.lst_tarefa)

        self.setLayout(layout)

    def adicionar_tarefa(self):
        #Função para adicionar tarefa à lista QList
        tarefa = self.txt_tarefa.text()
        if tarefa:
            self.lst_tarefa.addItem(tarefa)
            self.txt_tarefa.clear()

    def concluir_tarefa(self):
        #Função para marcar o checkbox como checado e desativar a edição do checkbox
        item_selecionado = self.lst_tarefa.currentItem()
        if item_selecionado:
            item_selecionado.setFlags(item_selecionado.flags() | Qt.ItemIsUserCheckable)
            item_selecionado.setCheckState(Qt.Checked)
            item_selecionado.setFlags(~Qt.ItemIsSelectable)
            item_selecionado.setFlags(~Qt.ItemIsEnabled)

            # Operador de bit wise AND &, OR | XOR ^, NOT ~


    def remover_tarefa(self):
        #Função para remover a tarefa da lista
        item_selecionado = self.lst_tarefa.currentItem()
        if item_selecionado:
            self.lst_tarefa.takeItem(self.lst_tarefa.row(item_selecionado))



    def editar_tarefa(self):
        item_selecionado = self.lst_tarefa.currentItem()
        if item_selecionado:
            novo_texto, ok = QInputDialog.getText(self, 'Editar tarefa', 'Editar a tarefa', text=item_selecionado.text())
            if ok and novo_texto:
                item_selecionado.setText(novo_texto)

if __name__ == '__main__':
    app = QApplication()
    app_lista_tarefas = AppListaTarefas()
    app_lista_tarefas.show()
    sys.exit(app.exec())
