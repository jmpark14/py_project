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

options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

driver = webdriver.Chrome(options=options)
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

#상세 페이지 들어가서 데이터 추출


#2. 수강후기 버튼 클릭
#driver.find_element(By.ID, "infoTab4").click()
#3. 데이터 추출
#빈리스트 만들기
review_list = []
test_list = []
curj_list = []
reviewNum_list = []
#데이터 추출
try:
    # 페이지 순회
    for j in range(2,11):
        # 상세페이지 진입 순회
        for i in range(1,11):
            
            # 상세페이지 진입
            # 1. 과정클릭
            title_click = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.content > p > a"
            driver.find_element(By.CSS_SELECTOR, title_click).click()
            time.sleep(1)
            
            # 2. 탭이동
            # j가 2부터 시작하지만 현재 페이지는 1
            driver.switch_to.window(driver.window_handles[i+((j-2)*10)])
            
            # 만족도/후기 버튼 클릭            
            review_click = f"#infoTab4 > button"
            driver.find_element(By.CSS_SELECTOR, review_click).click()
            
            # 3. 현제 URL 추출
            reviewNum = driver.find_elements(By.CLASS_NAME, "ment").size()
            if reviewNum == "":
                reviewNum = "0"                
            reviewNum_list.append(reviewNum)            
            """
            test = driver.current_url
            test_list.append(test)
            curj_list.append(j)
            """
            # 4. 목록탭으로 이동                
            driver.switch_to.window(driver.window_handles[0])            
        
        # 4. 목록탭으로 이동                
        driver.switch_to.window(driver.window_handles[0])    
        driver.find_element(By.LINK_TEXT, str(j)).click()
        time.sleep(2)
except:
    pass

# 리스트 길이가 같아야 변환 가능하니 확인
print(len(reviewNum_list))

df = pd.DataFrame({'reviewNum_list':reviewNum_list})
df.to_csv("K-digital_ex4_1.csv", encoding='utf-8-sig', index=False)





