
import datetime, time, os
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import timedelta
from flashtext import KeywordProcessor


kp = KeywordProcessor()
#filtro da table
def filtroDeBusca(kp):
    with open(os.path.abspath('filtro.txt'),'r', encoding='utf-8') as file:   
        for linha in file:
            for palavra in linha.split():         
                kp.add_keyword(palavra)
    return kp
#inicialização
def busca():
    filtroDeBusca(kp)
    i = 2
    j = 1
    auxL = 0
    listaC = []
    
    path = os.path.abspath('msedgedriver.exe') #caminho do driver
    browser  = webdriver.Edge(path)
    try:
        browser.get('http://comprasnet.gov.br/livre/Pregao/lista_pregao_filtro.asp?Opc=0') #link
    except Exception:
        lista = open(os.path.abspath('lista.txt'),'w')
        lista.write("O site está indisponivel")
    try:
        today = date.today() + timedelta(days=1) # fazer filtro para remover finais de semana
        dateH = datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%d/%m/%Y')
        calendario = browser.find_element(By.XPATH,'//*[@id="dt_abertura"]')
        calendario.send_keys(dateH) #inserir data
        situacao = browser.find_element(By.XPATH,'//*[@id="lstSituacao"]/option[text()="Aberto para Proposta"]').click()
        confirmar = browser.find_element(By.XPATH,'//*[@id="ok"]').click()
        window_before = browser.window_handles[0]
        window_before_title = "principal"
    except Exception:
        lista = open(os.path.abspath('lista.txt'),'w')
        lista.write("O site está com problemas")
    limite = browser.find_element(By.CSS_SELECTOR,'#QtdPregoes')
    aux = limite.text.replace('=', '')
    totalP = aux.replace('licitações', '')
    
    while i < (int(totalP) + 2):
        preparaUrlC1 = '/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[i]/td[j]/a'
        preparaUrlC1 = preparaUrlC1.replace('i', str(i))
        preparaUrlC1 = preparaUrlC1.replace('j', str(j))
        browser.find_element(By.XPATH,preparaUrlC1).click()
        #time.sleep(1)
        window_after = browser.window_handles[1]
        window_after_title = "detalhes"
        browser.switch_to.window(window_after)
        buscar = browser.find_element(By.XPATH,'html')
        if bool(kp.extract_keywords(buscar.text)):
            keywords_found = kp.extract_keywords(buscar.text)
            keywordaux = keywords_found
            browser.switch_to.window(window_before)
            resultadov1 = browser.find_element(By.XPATH,preparaUrlC1)
            preparaUrlC2 = '/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[i]/td[j]'
            preparaUrlC2 = preparaUrlC2.replace('i', str(i))
            preparaUrlC2 = preparaUrlC2.replace('j', '2')
            resultadov2 = browser.find_element(By.XPATH,preparaUrlC2)
            listaC.append((resultadov1.text, resultadov2.text, keywordaux))
            
        browser.switch_to.window(window_before)
        i += 1
        
    if listaC != []:
        lista = open(os.path.abspath('lista.txt'),'w') #caminho para criar o txt
        
        for auxL in range(len(listaC)):
            lista.write(str(listaC[auxL]) + '\n')
    else:
        if(totalP == 0):
            lista = open(os.path.abspath('lista.txt'),'w')
            lista.write("Não há pregoes para serem buscados amanhã")
        else:
            lista = open(os.path.abspath('lista.txt'),'w')
            lista.write("não foi encontrado pregões")
        
    lista.close()
    browser.quit()

#busca()



    


