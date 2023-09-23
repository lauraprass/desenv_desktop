from infra.repository.filme_repository import FilmeRepository
from infra.configs.connection import DBConnectionHandler

repo = FilmeRepository()
data_base = DBConnectionHandler()

# Persistimos os dados na base
repo.insert('Barbie', 'Comédia', 2023)
repo.insert('Spawn', 'Ação', 1997)

# Consultamos e printamos todos os dados da base
filmes = repo.select_all()
print(filmes)

# Atualizamos um filme através do ID
repo.update(2, 'Spawn - Soldado do inferno', 'Ação', 1997)

# Consultamos o filme através do ID
filme = repo.select_one(2)
print(filme)

#Removemos um registro através do id
id = len(filmes)
repo.delete(id)