import datetime, time
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import timedelta
from flashtext import KeywordProcessor
i = 2
j = 1
auxL = 0
listaC = []
#filtro da table

kp = KeywordProcessor()
kp.add_keyword('expediente')
kp.add_keyword('expedientes')
kp.add_keyword('gráfico')
kp.add_keyword('gráficos')
kp.add_keyword('comunicação')
kp.add_keyword('comunicações')
kp.add_keyword('revista')
kp.add_keyword('revistas')
kp.add_keyword('cartilha')
kp.add_keyword('cartilhas')
kp.add_keyword('capa de processo')
kp.add_keyword('capa de processos')
kp.add_keyword('jornal')
kp.add_keyword('jornais')
kp.add_keyword('folder')
kp.add_keyword('forders')
kp.add_keyword('panfleto')
kp.add_keyword('panfletos')
kp.add_keyword('cartão')
kp.add_keyword('cartais')

#inicialização

path = "C:\\Users\\ian77\\Desktop\\ia\\python\\Nova pasta\\msedgedriver.exe" #caminho do driver
browser  = webdriver.Edge(path)
browser.get('http://comprasnet.gov.br/livre/Pregao/lista_pregao_filtro.asp?Opc=0') #link

#filtro de entrada
today = date.today() + timedelta(days=1) # fazer filtro para remover finais de semana
dateH = datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%d/%m/%Y')
calendario = browser.find_element_by_xpath('//*[@id="dt_abertura"]')
calendario.send_keys(dateH) #inserir data
situacao = browser.find_element_by_xpath('//*[@id="lstSituacao"]/option[text()="Aberto para Proposta"]').click()
confirmar = browser.find_element_by_xpath('//*[@id="ok"]').click()

#busca da lista
window_before = browser.window_handles[0]
window_before_title = "principal"
limite = browser.find_element_by_css_selector('#QtdPregoes')
aux = limite.text.replace('=', '')
totalP = aux.replace('pregões', '')
while i < (int(totalP) + 2):
    preparaUrlC1 = '/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[i]/td[j]/a'
    preparaUrlC1 = preparaUrlC1.replace('i', str(i))
    preparaUrlC1 = preparaUrlC1.replace('j', str(j))
    browser.find_element_by_xpath(preparaUrlC1).click()
    #time.sleep(1)
    window_after = browser.window_handles[1]
    window_after_title = "detalhes"
    browser.switch_to.window(window_after)
    buscar = browser.find_element_by_xpath('html')
    if bool(kp.extract_keywords(buscar.text)):
        keywords_found = kp.extract_keywords(buscar.text)
        keywordaux = keywords_found
        browser.switch_to.window(window_before)
        resultadov1 = browser.find_element_by_xpath(preparaUrlC1)
        preparaUrlC2 = '/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[i]/td[j]'
        preparaUrlC2 = preparaUrlC2.replace('i', str(i))
        preparaUrlC2 = preparaUrlC2.replace('j', '2')
        resultadov2 = browser.find_element_by_xpath(preparaUrlC2)
        listaC.append((resultadov1.text, resultadov2.text, keywordaux))
        
    browser.switch_to.window(window_before)
    i += 1
if listaC != None:
    lista = open(r'C:\Users\ian77\Desktop\ia\python\Nova pasta\lista.txt','w') #caminho para criar o txt
    for auxL in range(len(listaC)):
        lista.write(str(listaC[auxL]) + '\n')
else:
    lista = open(r'C:\Users\ian77\Desktop\ia\python\Nova pasta\lista.txt','w')
    lista.write("não foi encontrado valores")
lista.close()


    
    
    
       
       





    
    








