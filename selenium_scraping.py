#https://github.com/mozilla/geckodriver/releases

from urllib.request import Request,urlopen
import pandas as pd
from tabulate import tabulate
from selenium import webdriver
import time

browser = webdriver.Firefox(executable_path=r'geckodriver.exe')

browser.get('https://www.cartolafcbrasil.com.br/scouts')

times = ['Bahia', 'Flamengo', 'Vasco']

for team in times:
    try:
        #elem = browser.find_element_by_class_name('hidden-xs')
        browser.find_element_by_xpath("//select[@name='ctl00$cphMainContent$drpClubes']/option[text()='" + team + "']").click()
        browser.find_element_by_xpath("//select[@name='ctl00$cphMainContent$drpStatus']/option[text()='[TODOS]']").click()
        botao = browser.find_element_by_id('ctl00_cphMainContent_btnFiltrar')
        botao.click()
        #print('Found <%s> element with that class name!' % (elem.tag_name))
        
    except:
        print('Was not able to find an element with that name.')


    time.sleep(10)
    table = browser.find_element_by_id('ctl00_cphMainContent_gvList')
    table_html = table.get_attribute('outerHTML')
    df = pd.read_html(str(table_html))
    df = df[0]
    
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df.clube = team
    df.preço = df.preço / 100
    df.média = df.média /100
    df.variação = df.variação /100
    df = df.iloc[:,:8]
    print(df)

browser.quit()
