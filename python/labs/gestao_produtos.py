"""
Programa para gestão do catálogo de produtos. Este programa permite:
    - Lista o catálogo
    - Pesquisar por alguns campos 
    - Eliminar um registo do catálogo
    - Guardar o catálogo em ficheiro
"""

from decimal import Decimal as dec
import subprocess
import sys
from typing import TextIO

CSV_DEFAULT_DELIM = ','
DEFAULT_INDENTATION = 3

################################################################################
##
# PRODUTOS E CATÁLOGO
##
################################################################################

PRODUCT_TYPES = {
    'AL': 'Alimentação',
    'DL': 'Detergente p/ Loiça',
    'FRL': 'Frutas e Legumes'
}

# id    : > 0 e tem que ter cinco digitos
# nome
# tipo
# quantidade
# preco


class Produto:
    def __init__(
            self,
            id_: int,
            nome: str,
            tipo: str,
            quantidade: int,
            preco: dec,
    ):
        if id_ < 0 or len(str(id_)) != 5:
            raise InvalidProdAttribute(
                f'{id_=} inválido (deve ser > 0 e ter 5 dígitos)')
        if not nome:
            raise InvalidProdAttribute('Nome vazio')
        if tipo not in PRODUCT_TYPES:
            raise InvalidProdAttribute(
                f'Tipo de produto ({tipo}) desconhecido')
        if quantidade < 0:
            raise InvalidProdAttribute('Quantidade deve ser >= 0')
        if preco < 0:
            raise InvalidProdAttribute('Preço deve ser >= 0')

        self.id = id_
        self.nome = nome
        self.tipo = tipo
        self.quantidade = quantidade
        self.preco = preco
    #:

    def __str__(self):
        cls_name = self.__class__.__name__
        return f'{cls_name}[id_= {self.id}  nome = "{self.nome}" tipo = "{self.tipo}"]'
    #:

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'{cls_name}(id_={self.id}, nome={self.nome}, tipo={self.tipo}, '\
            f'quantidade={self.quantidade}, preco={self.preco})'

    # Com Iva
    def com_iva(self, taxa_iva: dec) -> dec:
        return self.preco * (1 + taxa_iva/100)
    #:
#:


class InvalidProdAttribute(ValueError):
    pass
#:


def main() -> None:
    prod1 = Produto(30987, 'pão de milho', 'AL', 2, dec('1'))
    # prod2 = Produto(356, 'AJAX')

    print(prod1)
    print(f"Preço com IVA (13%): {prod1.com_iva(dec('13'))}")

    # print(f"prod1 {prod1.nome}")    # console.log(`prod1 ${prod1.nome}`)
    # print(f"prod2 {prod2.nome}")
#:


if __name__ == '__main__':
    main()
#:
