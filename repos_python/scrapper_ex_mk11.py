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
trainNum_list = []

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
                # 회차 추출
                period_select = f"#section1 > div > div.box > div.info > div.content > div > ul > li:nth-child(7) > span.con"
                period = driver.find_element(By.CSS_SELECTOR, period_select)
                period = period.text
                period_list = period.split('(')
                trainNum = period_list[1].replace("회차)","")
                trainNum_text = trainNum
                trainNum = int(trainNum)
                
                
                # 회차 선택 및 클릭  : 회차선택 드롭박스 선택 시, 역순으로 정렬되어 있어서 알맞는 옵션을 선택하기 어려운 상황
                # 선택   
                # trainNum_select_click = f"#srchTracseTme"       
                # dropdown = driver.find_element(By.CSS_SELECTOR, trainNum_select_click)
                dropdown_var = driver.find_element(By.XPATH, '//*[@id="srchTracseTme"]')
                dropdown = Select(dropdown_var)
                dropdown.select_by_value({trainNum_text})
                time.sleep(0.2)
                trainNum_click = f"#srchTracseTme > option:nth-child({trainNum_text})"
                driver.find_element(By.CSS_SELECTOR, trainNum_click).click()
                time.sleep(0.2)
                # 보기
                trainNum_view_click = f"#section1-4 > div.searchBox > fieldset > dl > button"
                driver.find_element(By.CSS_SELECTOR, trainNum_view_click).click()
                time.sleep(1)
                
                # 수강후기 
                review_select_tmp = f"#tbodyEpilogue > dd > p"
                review_tmp = driver.find_element(By.CSS_SELECTOR, review_select_tmp)
                review_tmp = review_tmp.text
                review_val = review_tmp.find("등록된 후기")
                review_val_list.append(review_val)
                
                if review_val == -1:
                    review_select = f"#tbodyEpilogue > dd:nth-child({k+3}) > p"
                else:
                    review_select = f"#tbodyEpilogue > dd > p"
                
                review = driver.find_element(By.CSS_SELECTOR, review_select)
                review = review.text
                """
                # 수강후기 - 수강후기 내 부정적 키워드 필터링                
                if "불만" in review:
                    continue                
                """
                review_list.append(review)
                
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
                #period_select = f"#section1 > div > div.box > div.info > div.content > div > ul > li:nth-child(7) > span.con"
                #period = driver.find_element(By.CSS_SELECTOR, period_select)
                #period = period.text
                #period_list = period.split('(')
                period_list_1.append(period_list[0])
                period_list_2.append(period_list[1].replace("회차)","")) 
                
                # 훈련유형
                tType_select = f"#section1 > div > div.box > div.info > div.content > div > ul > li:nth-child(14) > span.con"
                tType = driver.find_element(By.CSS_SELECTOR, tType_select)
                tType = tType.text
                tType_list.append(tType)                
                
                # 스크롤 맨위로 이동
                driver.execute_script('window.scrollTo(0,0)')
                
                # 훈련기관 정보로 이동                
                trTab2_click = f"#contentArea > div > div.tabListArea > ul > li:nth-child(2) > button"
                driver.find_element(By.CSS_SELECTOR, trTab2_click).click()
                time.sleep(0.5)
                
                # 훈련기관 홈페이지
                local_select = f"#section2 > div.infoDetailBox > div > div > div.content > div.infoList > ul > li:nth-child(5) > span.con > a"
                local_tmp = driver.find_element(By.CSS_SELECTOR, local_select)
                #local = driver.find_element(By.CSS_SELECTOR, local_select)
                
                local_tmp = local_tmp.text                
                
                if "kn" in local_tmp:
                    local = "강남"
                elif "jr" in local_tmp:
                    local = "종로"
                elif "jg" in local_tmp:
                    local = "종각"
                elif "ic" in local_tmp:
                    local = "신촌"
                elif "sc" in local_tmp:
                    local = "서초"
                elif "gd" in local_tmp:
                    local = "천호"
                elif "gr" in local_tmp:
                    local = "구로"
                elif "nw" in local_tmp:
                    local = "노원"
                elif "bu" in local_tmp:
                    local = "인천"
                elif "is" in local_tmp:
                    local = "일산"
                elif "cc" in local_tmp:
                    local = "춘천"
                elif "kj" in local_tmp:
                    local = "광주"
                elif "us" in local_tmp:
                    local = "울산"
                elif "tjoeunart.com" in local_tmp:
                    local = "김해"
                elif "dg" in local_tmp:
                    local = "대구"
                elif "bs" in local_tmp:
                    local = "부산"
                elif "bd" in local_tmp:
                    local = "부전"
                else:
                    local = local_tmp
                    
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
print(len(name_list), len(local_list), len(title_list), len(score_list), len(tType_list), len(period_list_1), len(period_list_2), len(review_list))
#print(len(name_list), len(title_list), len(score_list), len(period_list_1), len(period_list_2), len(review_list), len(trainNum_list), len(review_val_list))

# 결과값 데이터 프레임 정의
df = pd.DataFrame({'name_list':name_list, 'local_list':local_list, 'title_list':title_list, 'score_list':score_list, 'tType_list':tType_list, 'period_list_1':period_list_1, 'period_list_2':period_list_2, 'review_list':review_list})
#df = pd.DataFrame({'name_list':name_list, 'title_list':title_list, 'score_list':score_list, 'period_list_1':period_list_1, 'period_list_2':period_list_2, 'review_list':review_list, 'trainNum_list':trainNum_list, 'review_val_list':review_val_list})

# 파일명에 들어갈 날짜 및 형식 정의
fileName = dt.datetime.now().strftime("%Y%m%d")

# csv로 파일 추출
df.to_csv("HRD-NET_MK11_1_"+fileName+".csv", encoding='utf-8-sig', index=False)





