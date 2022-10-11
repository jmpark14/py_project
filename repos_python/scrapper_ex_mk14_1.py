import time   
import warnings
from xml.etree.ElementTree import tostring  
warnings.filterwarnings('ignore')  # 경고무시 

import pandas as pd  
import numpy as np  
import datetime as dt
import chromedriver_autoinstaller  
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


# 크롬 드라이버 세팅(경로 자동, 업데이트 자동)
path = chromedriver_autoinstaller.install( )
driver = webdriver.Chrome(path)
# 블루투스 오류 해결
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# 실제 사용자인척 하는 통신값 삽입
options.add_argument("disable-gpu")     # 가속 사용 x
options.add_argument("lang=ko_KR")      # 가짜 플러그인 탑재
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정
#options.add_argument('headless')        # 브라우저를 보이지 않게 해줌
#options.add_argument('--blink-settings=imagesEnabled=false') # 이미지 사용 안함

driver = webdriver.Chrome(options=options)

# HRD- 페이지 진입
driver.get("https://www.hrd.go.kr/hrdp/ti/ptiao/PTIAO0100L.do")
time.sleep(2)

# 빈리스트 만들기 - 사용
name_list = []      # 훈련기관 명
local_list = []     # 훈련 기관 위치
score_list = []     # 과정 평가점수
title_list = []     # 과정명
period_list = []    # 훈련 기간
period_list_1 = []  # 훈련 기간(개강일)
period_list_1_1 = []# 훈련 기간(종강일)
period_list_2 = []  # 훈련 기간(회차)
tType_list = []     # 훈련 유형
tType_code_list = []     # 훈련 유형 코드(더조은)
review_list = []    # 수강후기 
prelocal_list = []  # 위치 자르기 위한 리스트(주소+연락처)
reviewNum_list = []
ncs_list = []
ncs_code_list = []

# 빈리스트 만들기2 - 테스트, 미사용
test_list = []      # URL출력 테스트
sati_list = []      # 만족도 평점 test
review_val_list = []
trainNum_list = []
trainNum_select = []

limit_date_list = []
today_date_list = []

#더조은 검색어 입력
#검색어
searchAgency = driver.find_element(By.ID,"keyword")     # 검색어 입력부분 선택
searchAgency.send_keys("더조은")                        # 검색어 입력
#개강일자 조회
searchStDate = driver.find_element(By.ID,"startDate")   # 개강일자 시작일 입력부분 선택
searchStDate.send_keys(Keys.CONTROL + "a")              # 기입력된 개강일자 선택
searchStDate.send_keys(Keys.DELETE)                     # 기입력된 개강일자 삭제
searchStDate.send_keys("20220401")                      # 개강일자 시작일 입력
searchEndDate = driver.find_element(By.ID,"endDate")    # 개강일자 종료일 입력부분 선택
searchEndDate.send_keys(Keys.CONTROL + "a")             # 기입력된 개강일자 선택
searchEndDate.send_keys(Keys.DELETE)                    # 기입력된 개강일자 삭제
searchEndDate.send_keys("20220430")                     # 개강일자 종료일 입력
#조회조건 입력 후 엔터
searchAgency.send_keys(Keys.RETURN)                     # 엔터키 입력 
time.sleep(1)

#데이터 추출
try:
    # 페이지 순회
    for j in range(2,3):
        # 페이지 별 목록 순회
        for i in range(1,11):
            
            # 상세페이지 진입                
            #1. 과정명 클릭
            title_click = f"#contentArea > div.detailListWrap > ul > li:nth-child({i}) > div.content > p > a"
            driver.find_element(By.CSS_SELECTOR, title_click).click()
            time.sleep(1) 
            
            #2. 새로 나타나는 탭으로 이동            
            # j가 2부터 시작하지만 현재 페이지는 1
            # 페이지가 다음 페이지로 넘어갔을때 첫번째 탭이 아닌 다음 탭 선택 로직
            driver.switch_to.window(driver.window_handles[i+((j-2)*10)])
            
            # 종강일이 현재 날짜보다 뒤라면 건너뛰기            
            period_select = f"#section1 > div > div.box > div.info > div.content > div > ul > li:nth-child(7) > span.con"
            period = driver.find_element(By.CSS_SELECTOR, period_select)
            period = period.text
            period_list = period.split('(')
            period_list_1_tmp = period_list[0].split(' ~')
            limit_date = period_list_1_tmp[1]
            limit_date = period_list_1_tmp[1].replace('-','')
            today_date = dt.date.today().strftime('%Y%m%d')
            
            limit_date_list.append(limit_date)
            today_date_list.append(today_date)
            
            # 목록탭으로 이동
            driver.switch_to.window(driver.window_handles[0])
            
        #driver.switch_to.window(driver.window_handles[0])
        #time.sleep(1)
        driver.find_element(By.LINK_TEXT, str(j)).click()
        time.sleep(2)
except:
    pass

# 리스트 길이가 같아야 변환 가능하니 확인
print(len(limit_date_list), len(today_date_list))

# 결과값 데이터 프레임 정의
df = pd.DataFrame({'limit_date_list':limit_date_list, 'today_date_list':today_date_list})

# 파일명에 들어갈 날짜 및 형식 정의
fileName = dt.datetime.now().strftime("%Y%m%d")

# csv로 파일 추출
df.to_csv("HRD-NET_MK14_1_"+fileName+".csv", encoding='utf-8-sig', index=False)






