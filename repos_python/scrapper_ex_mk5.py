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
# 블루투스 오류 해결
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get("https://www.hrd.go.kr/hrdp/ti/ptiao/PTIAO0100L.do")
time.sleep(2)

# 빈리스트 만들기
name_list = []
local_list = []
score_list = []
title_list = []
period_list = []
period_list_1 = []
period_list_2 = []

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

#상세 페이지 들어가서 데이터 추출


#2. 수강후기 버튼 클릭
#driver.find_element(By.ID, "infoTab4").click()
#3. 데이터 추출
#빈리스트 만들기
review_list = []
test_list = []
#데이터 추출
try:
    # 페이지 순회
    for j in range(2,5):
        # 상세페이지 진입 순회
        for i in range(1,11):
            
            #1. 상세페이지 진입(*** 상세페이지 진입이 안되고 있음. 블로그 내용 참조)            
            for k in range(0,1):
                test = driver.current_url
                test_list.append(test)
                
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)               
                
            title_click = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.content > p > a"
            driver.find_element(By.CSS_SELECTOR, title_click).click()
            driver.switch_to.window(driver.window_handles[i])
            
            #만족도/후기 버튼 클릭            
            review_click = f"#infoTab4 > button"
            driver.find_element(By.CSS_SELECTOR, review_click).click()
            
            # 훈련기관명
            name_list.append(driver.find_element(By.CLASS_NAME, 'add').text)
            
            # 과정명
            title_select = f"#section1 > div > div.box > div.info > div.title > h4"
            title = driver.find_element(By.CSS_SELECTOR, title_select)
            title = title.text            
            title = title.replace(" 모집마감","")
            title_list.append(title)
            
            # 평가점수
            score_select = f"#section1 > div > div.box > div.info > div.content > div > ul > li:nth-child(2) > span.con > div > span"
            score = driver.find_element(By.CSS_SELECTOR, score_select)
            score = score.get_attribute('style')
            score = score.replace("width: ","")
            score = score.replace("%;","")
            score_list.append(score)
            
            # 훈련기간
            period_select = f'#section1 > div > div.box > div.info > div.content > div > ul > li:nth-child(7) > span.con'
            period = driver.find_element(By.CSS_SELECTOR, period_select)
            period = period.text
            period_list = period.split('(')
            period_list_1.append(period_list[0])
            period_list_2.append(period_list[1].replace(")",""))            
            
            # 수강후기 긁어오기 - 작동안됨            
            review = driver.find_elements(By.CLASS_NAME, 'ment')
            review = review.text                        
            review_list.append(review)
            
            # 훈련기관 위치 - 작동안됨
            """
            train_click = f"#contentArea > div > div.tabListArea > ul > li.on > button"
            driver.find_element(By.CSS_SELECTOR, train_click).click()            
            local_select = f"#section2 > div.infoDetailBox > div > div > div.title > ul > li > span.con"
            local = driver.find_element(By.CSS_SELECTOR, local_select)
            local = local.text
            local_list.append(local)
            """            
            
            #time.sleep(2)
            
        driver.find_element(By.LINK_TEXT, str(j)).click()
        time.sleep(2)
except:
    pass

# 리스트 길이가 같아야 변환 가능하니 확인
print(len(name_list), len(title_list), len(test_list), len(score_list), len(period_list_1), len(period_list_2), len(review_list))

df = pd.DataFrame({'test_list':test_list, 'title_list':title_list, 'name_list':name_list, 'score_list':score_list, 'period_list_1':period_list_1, 'period_list_2':period_list_2, 'review_list':review_list})
df.to_csv("HRD-NET_ex.csv", encoding='utf-8-sig', index=False)





