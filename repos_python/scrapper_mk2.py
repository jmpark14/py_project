from lib2to3.pgen2 import driver
import time
from turtle import pd
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
#path = chromedriver_autoinstaller.install()
#driver = webdriver.Chrome(path)
#driver.get("https://www.hrd.go.kr/")
driver.get("https://www.hrd.go.kr/hrdp/ti/ptiao/PTIAO0100L.do")
time.sleep(2)

#driver.find_element_by_link_text("#K-Digital Training").click()
#driver.find_element(By.ID, "topMenu2___").click()

page_title = ''
name_list = []
local_list = []
title_list = []
period_list = []

try:    
    for j in range(2,11):
        for i in range(1,11):
            #name_select = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) >div.title > a >p.zone"
            name_select = f"#contentArea > div.detailListWrap > ul > li:nth-child(1) > div.content > p > a "
            name = driver.find_element_by_css_selector(name_select)
            name = name.text
            name_list.append(name)
            """
            local_select = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.title > a > p.school"
            local = driver.find_element_by_css_selector(local_select)
            local = local.text
            local_list.append(local)

            title_select = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.content > p > a"
            title = driver.find_element_by_css_selector(title_select)
            title = title.get_attribute('title')
            title = title.replace(" 새창","")
            title_list.append(title)
            
            period_select = f'#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.content > div > dl:nth-child(2) > dd'
            period = driver.find_element_by_css_selector(period_select)
            period = period.text
            period_list.append(period)
            """
            
        driver.find_element_by_link_text(str(j)).click()
        time.sleep(2)
except:
    pass

#print(len(name_list), len(local_list), len(title_list), len(period_list))
print(len(name_list))

if len(name_list) > 0:
    #df = pd.DataFrame({'name':name_list, 'local':local_list, 'title':title_list, 'period':period_list})
    df = pd.DataFrame({'name':name_list})
    df.to_csv("K-digital.csv", encoding='utf-8-sig', index=False)