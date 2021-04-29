#gui import
import PySimpleGUI as sg

#funções import
import datetime, time, os
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import timedelta
from flashtext import KeywordProcessor
from os import path
from ComprasNetFilter import busca, filtroDeBusca

kp = KeywordProcessor()
browser = webdriver.Edge
def carregaFiltro(filtro):
    try:
        filtroDeBusca(kp)
    except Exception as e:
            sg.popup_quick_message(f'excessão {e}','Não foi encontrado nenhum filtro', keep_on_top=True)
            arquivoF = open("filtro.txt","w+")
            arquivoF.close()
    return filtro

def exibir():
    sg.theme('SystemDefaultForReal')
    layout = [ [sg.Output(size=(60,10))],
               [sg.Button('Fechar')]
    ]
    #window = sg.Window("Exibição", layout)
    return sg.Window('Exibição', layout, finalize=True)
    
        

def Menu():
    filtro = path.join(path.dirname(__file__), r'filtro.txt')
    carregaFiltro(filtro)
    sg.theme('SystemDefaultForReal')

    layout = [  [sg.Text('Configuração do filtro')],
                [sg.Text('Digite uma palavra'), sg.InputText(key='-INPUT-')],
                [sg.Button('Adicionar no filtro'), sg.Button('Remover do filtro')],
                [sg.Text('Funções do filtro')],
                [sg.Button('Buscar'), sg.Button('Exibir palavras do filtro'), sg.Button('Sair')]]

            
    return sg.Window('Filtro do ComprasNet', layout, finalize=True)

window1, window2, window3 = Menu(), None, None

while True:
    window, event, values = sg.read_all_windows()
    if window == window1 and event == sg.WIN_CLOSED or event == 'Sair':
        break
    if window == window2 and event == sg.WIN_CLOSED or event == 'Fechar':
        window2.close()
    if window == window3 and event == sg.WIN_CLOSED or event == 'Fechar':
        window2.close()
    if window == window1 and event == 'Exibir palavras do filtro':
        window2 = exibir()
        arquivoF = open("filtro.txt", "r", encoding='utf-8')
        print(arquivoF.read())
        arquivoF.close()
    if window == window1 and event == 'Adicionar no filtro':
        palavra_chave = values['-INPUT-']
        if(palavra_chave not in kp):
            arquivoF = open("filtro.txt", "r", encoding='utf-8')
            conteudo = arquivoF.read()
            print(arquivoF.read())
            print()
            arquivoF.close()
            arquivoF = open("filtro.txt", "w", encoding='utf-8')
            kp.add_keyword(palavra_chave)
            arquivoF.write(palavra_chave + ' ' + conteudo)
            arquivoF.close()
    if window == window1 and event == 'Remover do filtro':
        palavra_chave = values['-INPUT-']
        with open(os.path.abspath('filtro.txt'),'r', encoding='utf-8') as file:   
            for linha in file:
                for palavra in linha.split():
                    if(palavra == palavra_chave):
                        linha = linha.replace(palavra,'')
                        kp.remove_keyword(palavra_chave)
                        print("removido")
        arquivoF = open("filtro.txt", "w", encoding='utf-8')
        arquivoF.write(linha)
        arquivoF.close()
    if window == window and event == 'Buscar':
        busca()
        window2 = exibir()
        arquivoL = open("lista.txt", "r")
        print(arquivoL.read())
        arquivoL.close()
    
window.close()       


