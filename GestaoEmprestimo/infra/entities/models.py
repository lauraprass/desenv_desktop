from __future__ import annotations
from typing import List
from sqlalchemy import Column, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from infra.config.base import Base

association_table = (
    "emprestimos",
    Base.metadata,
    Column("funcionario_id", ForeignKey("funcionarios.id"), primary_key=True),
    Column("uniforme_id", ForeignKey("uniformes.id"), primary_key=True),
    Column("data_emprestimo", DateTime, nullable=False),
    Column("data_devolucao", DateTime)
)

class Funcionario(Base):
    __tablename__ = 'funcionarios'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    cpf: Mapped[str] = mapped_column(nullable=False, unique=True)
    uniformes: Mapped[List[Uniforme]] = relationship(secondary=association_table, back_populates='funcionarios', lazy=False)

    def __repr__(self):
        return f'Funcionario [nome= {self.nome}, cpf={self.cpf}]'

class Uniforme(Base):
    __tablename__ = 'uniformes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    funcinarios: Mapped[List[Funcionario]] = relationship(secondary=association_table, back_populates='uniformes', lazy=False)

    def __repr__(self):
        return f'Uniforme[nome = {self.nome}]'