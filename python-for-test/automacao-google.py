# -*- coding: utf-8 -*-
import webbrowser

"""
Automação simples para abrir o Google e listar as bibliotecas usadas.
"""

BIBLIOTECAS_USADAS = ['webbrowser']


def abrir_google():
    url = 'https://www.google.com'
    webbrowser.open(url)
    print(f'Abrindo: {url}')


def listar_bibliotecas():
    print('Bibliotecas usadas no processo:')
    for lib in BIBLIOTECAS_USADAS:
        print(f'- {lib}')


if __name__ == '__main__':
    abrir_google()
    listar_bibliotecas()
