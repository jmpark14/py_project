import time   
import warnings  
warnings.filterwarnings('ignore')  # 경고무시 

import pandas as pd  
import numpy as np  
import datetime as dt
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
score_list = []
title_list = []
period_list = []
period_list_1 = []
period_list_2 = []
tType_list = []

#더조은 검색어 입력
#검색어
searchAgency = driver.find_element(By.ID,"keyword")
searchAgency.send_keys("더조은")
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
review_list = []    # 수강후기 
test_list = []      # URL출력 테스트
sati_list = []      # 만족도 평점 test
prelocal_list = []  # 위치 자르기 위한 리스트(주소+연락처)
#데이터 추출
try:
    # 페이지 순회
    for j in range(2,5):
        # 상세페이지 진입 순회
        for i in range(1,11):
            # 위치
            local_select = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.title > a > p.school"
            local = driver.find_element(By.CSS_SELECTOR, local_select)
            local = local.text
            #local_list.append(local)
            prelocal_list = local.split('(')            
            local_list.append(prelocal_list[0].replace("\n", ""))
            
            # 훈련유형
            tType_select = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.content > ul > ul > img"
            tType = driver.find_element(By.CSS_SELECTOR, tType_select)
            tType = tType.get_attribute('alt')            
            tType_list.append(tType)
            
            #상세페이지 진입                
            #1. 과정명 클릭
            title_click = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.content > p > a"
            driver.find_element(By.CSS_SELECTOR, title_click).click()
            
            #2. 새로 나타나는 탭으로 이동
            #driver.switch_to.window(driver.window_handles[i]) #<-코드는 1-10탭만 반복해버림
            # j가 2부터 시작하지만 현재 페이지는 1
            driver.switch_to.window(driver.window_handles[i+((j-2)*10)])
            
            #만족도/후기 버튼 클릭            
            review_click = f"#infoTab4 > button"
            driver.find_element(By.CSS_SELECTOR, review_click).click()
            
            test = driver.current_url
            test_list.append(test)
            
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
            
            # 수강후기 긁어오기 - 1줄만 작동
            review_select = f"#tbodyEpilogue > dd:nth-child(3) > p"
            review = driver.find_element(By.CSS_SELECTOR, review_select)
            review = review.text                        
            review_list.append(review)
            
            # 수강후기 탭 페이지 만족도 점수 데이터 스크랩 여부 테스트 - 정상작동
            """
            sati_select = f"#infoDiv > div:nth-child(1) > dl > dd > span.num"
            sati = driver.find_element(By.CSS_SELECTOR, sati_select)
            sati = sati.text
            sati_list.append(sati)
            """
            # 목록탭으로 이동
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
        
        driver.switch_to.window(driver.window_handles[0])    
        driver.find_element(By.LINK_TEXT, str(j)).click()
        time.sleep(2)
except:
    pass

# 리스트 길이가 같아야 변환 가능하니 확인
print(len(name_list), len(title_list), len(score_list), len(period_list_1), len(period_list_2), len(local_list), len(review_list), len(tType_list))

# 결과값 데이터 프레임 정의
df = pd.DataFrame({'title_list':title_list, 'tType_list':tType_list, 'local_list':local_list, 'name_list':name_list, 'score_list':score_list, 'period_list_1':period_list_1, 'period_list_2':period_list_2, 'review_list':review_list})

# 파일명에 들어갈 날짜 및 형식 정의
fileName = dt.datetime.now().strftime("%Y%m%d")

# csv로 파일 추출
df.to_csv("HRD-NET_"+fileName+".csv", encoding='utf-8-sig', index=False)





