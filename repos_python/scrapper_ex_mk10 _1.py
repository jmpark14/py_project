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
period_list_1 = []  # 훈련 기간(기간)
period_list_2 = []  # 훈련 기간(회차)
tType_list = []     # 훈련 유형
review_list = []    # 수강후기 
prelocal_list = []  # 위치 자르기 위한 리스트(주소+연락처)
reviewNum_list = []

# 빈리스트 만들기2 - 테스트, 미사용
test_list = []      # URL출력 테스트
sati_list = []      # 만족도 평점 test
review_val_list = []

#더조은 검색어 입력
#검색어
searchAgency = driver.find_element(By.ID,"keyword")     # 검색어 입력부분 선택
searchAgency.send_keys("더조은")                        # 검색어 입력
#개강일자 조회
searchStDate = driver.find_element(By.ID,"startDate")   # 개강일자 시작일 입력부분 선택
searchStDate.send_keys(Keys.CONTROL + "a")              # 기입력된 개강일자 선택
searchStDate.send_keys(Keys.DELETE)                     # 기입력된 개강일자 삭제
searchStDate.send_keys("20220501")                      # 개강일자 시작일 입력
searchEndDate = driver.find_element(By.ID,"endDate")    # 개강일자 종료일 입력부분 선택
searchEndDate.send_keys(Keys.CONTROL + "a")             # 기입력된 개강일자 선택
searchEndDate.send_keys(Keys.DELETE)                    # 기입력된 개강일자 삭제
searchEndDate.send_keys("20220601")                     # 개강일자 시작일 입력
#조회조건 입력 후 엔터
searchAgency.send_keys(Keys.RETURN)                     # 엔터키 입력 
time.sleep(1)

#데이터 추출
try:
    # 페이지 순회
    for j in range(2,4):
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
            
            # 만족도/후기 버튼 클릭            
            review_click = f"#infoTab4 > button"
            driver.find_element(By.CSS_SELECTOR, review_click).click()
            time.sleep(1)
            
            # 테스트 추출
            #test = driver.current_url
            #test_list.append(test)
            
            reviewNums = driver.find_elements(By.CLASS_NAME, 'ment')
            reviewNum = len(reviewNums)
            #reviewNum_list.append(reviewNum)  
            # 후기 개수 추출 성공
            # 후기 개수만큼 반복하여 후기 추출 예정 
            
            for k in range (reviewNum):
                
                # 스크롤 맨위로 이동
                driver.execute_script('window.scrollTo(0,0)')
                
                # 훈련기관 정보로 이동                
                trTab2_click = f"#contentArea > div > div.tabListArea > ul > li:nth-child(2) > button"
                driver.find_element(By.CSS_SELECTOR, trTab2_click).click()
                time.sleep(0.5)
                
                # 훈련기관 홈페이지
                local_select = f"#section2 > div.infoDetailBox > div > div > div.content > div.infoList > ul > li:nth-child(5) > span.con > a"
                local_tmp = driver.find_element(By.CSS_SELECTOR, local_select)
                
                local_tmp = local_tmp.text
                local_kn = "kn" in local_tmp
                local_jr = "jr" in local_tmp
                local_jg = "jg" in local_tmp                
                local_ic = "ic" in local_tmp
                local_gd = "gd" in local_tmp
                local_gr = "gr" in local_tmp
                local_nw = "nw" in local_tmp
                local_bu = "bu" in local_tmp
                local_is = "is" in local_tmp
                local_cc = "cc" in local_tmp
                local_kj = "kj" in local_tmp
                local_us = "us" in local_tmp
                local_gh = "tjoeunart.com" in local_tmp
                local_dg = "dg" in local_tmp
                local_bs = "bs" in local_tmp
                local_bd = "bd" in local_tmp
                
                if local_kn:
                    local = "강남"
                elif local_jr:
                    local = "종로"
                elif local_jg:
                    local = "종각"
                elif local_ic:
                    local = "신촌"
                elif local_gd:
                    local = "천호"
                elif local_gr:
                    local = "구로"
                elif local_nw:
                    local = "노원"
                elif local_bu:
                    local = "인천"
                elif local_is:
                    local = "일산"
                elif local_cc:
                    local = "춘천"
                elif local_kj:
                    local = "광주"
                elif local_us:
                    local = "울산"
                elif local_gh:
                    local = "김해"
                elif local_dg:
                    local = "대구"
                elif local_bs:
                    local = "부산"
                elif local_bd:
                    local = "부전"
                else:
                    local = local_tmp.text
                
                local_list.append(local)
                
                # 훈련과정 정보로 이동                
                trTab1_click = f"#contentArea > div > div.tabListArea > ul > li:nth-child(1) > button"
                driver.find_element(By.CSS_SELECTOR, trTab1_click).click()
                time.sleep(0.5)
                
                # 만족도/후기 버튼 클릭            
                review_click = f"#infoTab4 > button"
                driver.find_element(By.CSS_SELECTOR, review_click).click()
                time.sleep(0.5)
                
            # 목록탭으로 이동
            driver.switch_to.window(driver.window_handles[0])
        
        #driver.switch_to.window(driver.window_handles[0]) 
        #time.sleep(1)   
        driver.find_element(By.LINK_TEXT, str(j)).click()
        time.sleep(2)
except:
    pass

# 리스트 길이가 같아야 변환 가능하니 확인
#print(len(name_list), len(local_list), len(title_list), len(score_list), len(tType_list), len(period_list_1), len(period_list_2), len(review_list))
#print(len(name_list), len(title_list), len(score_list), len(period_list_1), len(period_list_2), len(review_list), len(review_val_list))
print(len(local_list))

# 결과값 데이터 프레임 정의
#df = pd.DataFrame({'name_list':name_list, 'local_list':local_list, 'title_list':title_list, 'score_list':score_list, 'tType_list':tType_list, 'period_list_1':period_list_1, 'period_list_2':period_list_2, 'review_list':review_list})
#df = pd.DataFrame({'name_list':name_list, 'title_list':title_list, 'score_list':score_list, 'period_list_1':period_list_1, 'period_list_2':period_list_2, 'review_list':review_list, 'review_val_list':review_val_list})
df = pd.DataFrame({'local_list':local_list})

# 파일명에 들어갈 날짜 및 형식 정의
fileName = dt.datetime.now().strftime("%Y%m%d")

# csv로 파일 추출
df.to_csv("HRD-NET_MK10_"+fileName+".csv", encoding='utf-8-sig', index=False)





