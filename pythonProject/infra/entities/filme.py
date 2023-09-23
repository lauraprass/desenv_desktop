from sqlalchemy import Column, String, Integer
from infra.configs.base import Base

# Criamos uma classe filme herdando Base (declarative_base)
class Filme(Base):
    # Definimos o nome da tabela
    __tablename__ = 'filmes'

    # Definimos os atributos e seus tipos de dados que serão criados na base
    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String(100), nullable=False)
    genero = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)

    # Sobrescrevemos a função mágica que ocorre para apresentação dos dados do objeto desta classe
    def __repr__(self):
        return f'Filme [Titulo = {self.titulo}, Ano = {self.ano}]\n'
