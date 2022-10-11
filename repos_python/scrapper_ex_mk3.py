import time   
import warnings  
warnings.filterwarnings('ignore')  # 경고무시 

import pandas as pd  
import numpy as np  
import chromedriver_autoinstaller  
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# HRD- 페이지 진입
path = chromedriver_autoinstaller.install( )
driver = webdriver.Chrome(path)
driver.get("https://www.hrd.go.kr/hrdp/ti/ptiao/PTIAO0100L.do")
time.sleep(2)

# 빈리스트 만들기
name_list = []
local_list = []
title_list = []
period_list = []

#더조은 검색어 입력
#검색어
searchAgency = driver.find_element(By.ID,"keyword")
searchAgency.send_keys("더조은컴퓨터")
#개강일자 조회
searchStDate = driver.find_element(By.ID,"startDate")
searchStDate.send_keys(Keys.CONTROL + "a")
searchStDate.send_keys(Keys.DELETE)
searchStDate.send_keys("20220501")
searchEndDate = driver.find_element(By.ID,"endDate")
searchEndDate.send_keys(Keys.CONTROL + "a")
searchEndDate.send_keys(Keys.DELETE)
searchEndDate.send_keys("20220601")
#조회조건 입력 후 엔터
searchAgency.send_keys(Keys.RETURN)

try:
    for j in range(2,11):
        for i in range(1,11):
            # 기관명
            name_select = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) >div.title > a >p.zone"
            name = driver.find_element(By.CSS_SELECTOR, name_select)
            name = name.text
            name_list.append(name)

            # 위치
            local_select = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.title > a > p.school"
            local = driver.find_element(By.CSS_SELECTOR, local_select)
            local = local.text
            local_list.append(local)

            # 과정명
            title_select = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.content > p > a"
            title = driver.find_element(By.CSS_SELECTOR, title_select)
            title = title.get_attribute('title')
            title = title.replace(" 새창","")
            title_list.append(title)
            
            # 훈련기간
            period_select = f'#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.content > div > dl:nth-child(2) > dd'
            period = driver.find_element(By.CSS_SELECTOR, period_select)
            period = period.text
            period_list.append(period)
            
        driver.find_element(By.LINK_TEXT, str(j)).click()
        time.sleep(2)
except:
    print("오류발생")
    pass
    

# 리스트 길이가 같아야 변환 가능하니 확인
print(len(name_list), len(local_list), len(title_list), len(period_list))

df = pd.DataFrame({'name':name_list, 'local':local_list, 'title':title_list, 'period':period_list})
df.to_csv("K-digital_ex3.csv", encoding='utf-8-sig', index=False)





