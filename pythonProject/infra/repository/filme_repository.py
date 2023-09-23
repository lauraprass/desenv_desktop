from infra.configs.connection import DBConnectionHandler
from infra.entities.filme import Filme

class FilmeRepository:

    def select_all(self):
        with DBConnectionHandler() as db:
            filmes = db.session.query(Filme).all()
            return filmes

    def select_one(self, id):
        with DBConnectionHandler() as db:
            if id:
                filme = db.session.query(Filme).filter(Filme.id == id).first()
            else:
                filme = db.session.query(Filme).first()
            return filme

    def insert(self, titulo, genero, ano):
        with DBConnectionHandler() as db:
            filme = Filme(titulo=titulo, genero=genero, ano=ano)
            db.session.add(filme)
            db.session.commit()

    def update(self, id, titulo, genero, ano):
        with DBConnectionHandler() as db:
            db.session.query(Filme).filter(Filme.id == id).update(
                {
                    'titulo': titulo,
                    'genero': genero,
                    'ano': ano
                }
            )

    def delete(self, id):
        with DBConnectionHandler() as db:
            db.session.query(Filme).filter(Filme.id == id).delete()
            db.session.commit()
