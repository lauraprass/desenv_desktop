from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infra.configs.base import Base


class DBConnectionHandler:
    def __init__(self):
        # Definimos o dialeto e o path do arquivo de banco de dados
        self.__connection_string = 'sqlite:///locadora.db'
        # Criamos uma instância de engine e passamos para a variavel privada em engine
        self.__engine = self.__create_database_engine()
        self.create_table()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string, echo=True)
        return engine

    def create_table(self):
        engine = create_engine(self.__connection_string)
        # Utilizamos o metadata.create_all para percorrer o projeto e verificar quais classes herdam Base e criar
        # as tabelas e suas colunas
        Base.metadata.create_all(engine)
        print('Tabelas criadas com sucesso!')

    def get_engine(self):
        return self.__engine

    # Funções "mágicas" que executam algo no momento em que a classe é instanciada e quando ela é finalizada
    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        print('Abrindo conexão')
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Encerrando conexão')
        self.session.close()
