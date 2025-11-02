#32230144_고건우 : 420~444(수정 전), 706~711, 807~833
#김시우 : 60~110, 168~171, (수정 전 카테고리에 없는 옷 종류 및 온도 설정 코드 (PPT와 발표 참고 부탁드립니다))
#32231594_박기쁨 : 60~154(김시우님께서 초안 작성, 이후 본인이 수정 및 추가 (역할분담은 PPT와 발표 참고 부탁드립니다)), 168~171, 185~238, 419, 421, 428~654, 663, 665, 680, 682
#32222946_윤예원 : 44~58,157~165,177~183,193,194,206,207,219,220,232,233,241~416,422~424,499~502,553~556,607~610,646~649,661~704,718~732,749~804,816~828
#32233421 이은지 : 20~42

import tkinter as tk
from tkinter import messagebox
import time

import datetime
import ssl
import re
import urllib
# 파이썬이 url을 가져올 수 있게 하는 라이브러리
from bs4 import BeautifulSoup
# 데이터를 파이썬이 읽을 수 있는 형태로 변환 html형태로 변환 후 문서의 구조에 따라 데이터를 가져올 수 있도록 돕는 라이브러리
import urllib.request as req

Weather = None

# 네이버에서 서울의 기온을 크롤링하여 가져오는 함수
def GetWeather():
    # https에 필요한 ssl 인증서 확인을 무시하기 위해 SSL 컨텍스트를 생성해 https문서를 열람할 수 있게 한다.
    context = ssl._create_unverified_context()
    # 네이버의 서울 날씨 웹페이지에 접속한다.
    webpage = urllib.request.urlopen(
        'https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8%EB%82%A0%EC%94%A8',
        context=context)
    # 지정한 url을 파이썬이 대신 열어서 해당 html파일을 복사(파싱)해온다.
    soup = BeautifulSoup(webpage, 'html.parser')
    # temperature_text클래스이면서 div태그 안에 담겨있는 현재기온 값(temps) 받아오기
    temps = soup.find('div', 'temperature_text')
    # 찾은 요소에서 텍스트를 추출하고, 공백을 제거한다.
    temps = str(temps.text.strip())
    # 현재 기온
    global Weather
    # \d+.\d+:숫자들과 숫자들 사이에 어떤 문자가 와 있는 경우를 추출한다.
    # re.findall: String에서 패턴에 해당하는 내용을 찾아서 리스트로 리턴한다.
    # [0]으로 리스트의 첫 번째 요소, 즉 숫자 패턴의 첫 번째 부분 선택, float로 선택된 숫자를 부동소수점으로 변환.
    # 즉, 문자열 temps에서 기온(실수)만 가져온다.
    Weather = float(re.findall('\d+.\d+', temps)[0])

closet_Top = []  # 상의 옷장 리스트
closet_Low = []  # 하의 옷장 리스트
closet_Outer = []  # 겉옷 옷장 리스트
closet_Axcessory = []  # 악세서리 옷장 리스트
return_closet = {}
custom_closet_Top = []  # 카테고리에 없는 상의 옷장 리스트
custom_closet_Low = []  # 카테고리에 없는 하의 옷장 리스트
custom_closet_Outer = []  # 카테고리에 없는 겉옷 옷장 리스트
custom_closet_Axcessory = []  # 카테고리에 없는 악세서리 옷장 리스트
custom_return_closet = {}

year = None  # 년, 일, 요일, 월 전역변수
day = None
day_of_the_week = None
Month = None

# 상의 추천 함수
def get_recommendation_top():
    global Weather
    recommended_top = []  # 상의 추천 함수의 리턴 값을 담을 리스트
    clothing_type = []  # 현재 기온에 맞는 상의 타입(카테고리)을 저장할 리스트

    # 기온에 맞는 상의 분류
    if Weather <= 16:
        clothing_type = ["맨투맨", "가디건", "후드티", "니트"]
    elif 16 < Weather <= 19:
        clothing_type = ["맨투맨", "가디건"]
    elif 19 < Weather <= 22:
        clothing_type = ["긴팔", "셔츠", "블라우스"]
    elif 22 < Weather <= 27:
        clothing_type = ["반팔"]
    elif 28 < Weather:
        clothing_type = ["민소매", "반팔"]

    # 기온에 맞는 상의 보유 여부 확인 및 리턴 값(리스트)에 추가
    for clothing in closet_Top:
        if clothing["category"] in clothing_type:  # 현재 기온에 맞는 상의 타입과 일치하는 상의를 보유하고 있다면
            recommended_top.append(clothing)  # 상의 추천 함수의 리턴 값(리스트)에 옷 추가

    # 추천 상의(리스트) 리턴
    return recommended_top

# 하의 추천 함수
def get_recommendation_bot():
    global Weather
    recommended_bot = []  # 하의 추천 함수의 리턴 값을 담을 리스트
    clothing_type = []  # 현재 기온에 맞는 하의 타입(카테고리)을 저장할 리스트

    # 기온에 맞는 하의 분류
    if Weather <= 4:
        clothing_type = ["기모바지"]
    elif 4 < Weather <= 8:
        clothing_type = ["청바지"]
    elif 8 < Weather <= 22:
        clothing_type = ["면바지", "슬랙스", "청바지", "치마"]
    elif 22 < Weather <= 27:
        clothing_type = ["반바지", "면바지", "치마"]
    elif 27 < Weather:
        clothing_type = ["반바지", "치마"]

    # 기온에 맞는 하의 보유 여부 확인 및 리턴 값(리스트)에 추가
    for clothing in closet_Low:
        if clothing["category"] in clothing_type:  # 현재 기온에 맞는 하의 타입과 일치하는 하의를 보유하고 있다면
            recommended_bot.append(clothing)  # 하의 추천 함수의 리턴 값(리스트)에 옷 추가

    # 추천 하의(리스트) 리턴
    return recommended_bot

# 겉옷 추천 함수
def get_recommendation_out():
    global Weather
    recommended_out = []  # 겉옷 추천 함수의 리턴 값을 담을 리스트
    clothing_type = []  # 현재 기온에 맞는 겉옷 타입(카테고리)을 저장할 리스트

    # 기온에 맞는 겉옷 분류
    if Weather <= 4:
        clothing_type = ["패딩"]
    elif 4 < Weather <= 19:
        clothing_type = ["가죽자켓", "코트"]
    elif 8 < Weather <= 11:
        clothing_type = ["자켓", "코트", "점퍼"]
    elif 11 < Weather <= 16:
        clothing_type = ["자켓", "청자켓"]
    elif 16 < Weather <= 19:
        clothing_type = ["바람막이"]

    # 기온에 맞는 겉옷 보유 여부 확인 및 리턴 값(리스트)에 추가
    for clothing in closet_Outer:
        if clothing["category"] in clothing_type:  # 현재 기온에 맞는 겉옷 타입과 일치하는 겉옷을 보유하고 있다면
            recommended_out.append(clothing)  # 겉옷 추천 함수의 리턴 값(리스트)에 옷 추가

    # 추천 겉옷(리스트) 리턴
    return recommended_out

# 액세서리 추천 함수
def get_recommendation_acc():
    global Weather
    recommended_acc = []  # 액세서리 추천 함수의 리턴 값을 담을 리스트
    clothing_type = []  # 현재 기온에 맞는 액세서리 타입(카테고리)을 저장할 리스트

    # 기온에 맞는 액세서리 분류
    if Weather <= 4:
        clothing_type = ["목도리", "장갑"]

    # 기온에 맞는 액세서리 보유 여부 확인 및 리턴 값(리스트)에 추가
    for clothing in closet_Axcessory:
        if clothing["category"] in clothing_type:  # 현재 기온에 맞는 액세서리 타입과 일치하는 액세서리를 보유하고 있다면
            recommended_acc.append(clothing)  # 액세서리 추천 함수의 리턴 값(리스트)에 옷 추가

    # 추천 액세서리(리스트) 리턴
    return recommended_acc

#추천한 코디 출력 함수
def recommend_coordi():
    global year  # 년도 전역변수
    global day  # 일 전역변수
    global day_of_the_week  # 요일 전역변수
    global Month  # 달 전역변수

    recommend__coordi = tk.Toplevel(root)  # 새로운 윈도우 창 띄우기
    recommend__coordi.title("코디 추천")  # 창 이름
    T = tk.Text(recommend__coordi, height=(10 + len(closet_Top) + len(closet_Low) + len(closet_Outer) + len(closet_Axcessory)+ len(custom_closet_Top)+len(custom_closet_Low)+len(custom_closet_Outer)+len(custom_closet_Axcessory)),width=60)  # 텍스트 위젯 생성

    GetWeather()  # 기온 함수 호출
    recommended_top = get_recommendation_top()
    recommended_bot = get_recommendation_bot()
    recommended_out = get_recommendation_out()
    recommended_acc = get_recommendation_acc()
    custom_recommended_Top = get_recommendation_custom_Top() #카테고리에 없는 상의 추천 리스트
    custom_recommended_Low = get_recommendation_custom_Low() #카테고리에 없는 하의 추천 리스트
    custom_recommended_Outer = get_recommendation_custom_Outer() #카테고리에 없는 겉옷 추천 리스트
    custom_recommended_Axcessory = get_recommendation_custom_Axcessory() #카테고리에 없는 액세서리 추천 리스트

    calendar()  # 날짜 함수 호출
    date = "[ " + year + "년" + Month + day + "일" + day_of_the_week + " ]"
    T.insert(tk.END, date)  # 날짜 출력
    T.insert(tk.END, "\n")
    temp = "[ 기온 : " + str(Weather) + " ]"
    T.insert(tk.END, temp)  # 기온 출력
    T.insert(tk.END, "\n")

    # 상의 추천
    if recommended_top or (custom_recommended_Top != []):
        T.insert(tk.END, "추천 상의:\n")
        i = 1
        for clothing in recommended_top:
            T.insert(tk.END, f"{i}.  {clothing['design']} {clothing['category']}")
            T.insert(tk.END, "\n")
            i += 1
        for n in range(len(custom_recommended_Top)) : #반복문으로 카테고리에 없는 상의 추천 리스트의 요소들 출력
            T.insert(tk.END, '현재 기온에는 %s %s도 적합합니다.\n'%(custom_recommended_Top[n]["design"], custom_recommended_Top[n]["category"]))
    else:
        T.insert(tk.END, "현재 계절과 기온에 맞는 상의가 없습니다.\n")

    # 하의 추천
    if recommended_bot or (custom_recommended_Low != []):
        T.insert(tk.END, "추천 하의:\n")
        i = 1
        for clothing in recommended_bot:
            T.insert(tk.END, f"{i}. {clothing['design']} {clothing['category']}")
            T.insert(tk.END, "\n")
            i += 1
        for n in range(len(custom_recommended_Low)) : #반복문으로 카테고리에 없는 하의 추천 리스트의 요소들 출력
            T.insert(tk.END, '현재 기온에는 %s %s도 적합합니다.\n'%( custom_recommended_Low[n]["design"], custom_recommended_Low[n]["category"]))
    else:
        T.insert(tk.END, "현재 계절과 기온에 맞는 하의가 없습니다.\n")

    # 겉옷 추천
    if recommended_out or (custom_recommended_Outer != []):
        T.insert(tk.END, "추천 겉옷:\n")
        i = 1
        for clothing in recommended_out:
            T.insert(tk.END, f"{i}.  {clothing['design']} {clothing['category']}")
            T.insert(tk.END, "\n")
            i += 1
        for n in range(len(custom_recommended_Outer)) : #반복문으로 카테고리에 없는 상의 겉옷 리스트의 요소들 출력
            T.insert(tk.END, '현재 기온에는 %s %s도 적합합니다.\n' % (custom_recommended_Outer[n]["design"],custom_recommended_Outer[n]["category"]))
    else:
        T.insert(tk.END, "현재 계절과 기온에 맞는 겉옷이 없습니다.\n")

    # 액세서리 추천
    if recommended_acc or (custom_recommended_Axcessory != []):
        T.insert(tk.END, "추천 액세서리:\n")
        i = 1
        for clothing in recommended_acc:
            T.insert(tk.END, f"{i}. {clothing['design']} {clothing['category']}")
            T.insert(tk.END, "\n")
            i += 1
        for n in range(len(custom_recommended_Axcessory)) : #반복문으로 카테고리에 없는 액세서리 추천 리스트의 요소들 출력
            T.insert(tk.END, '현재 기온에는 %s %s도 적합합니다.\n' % (custom_recommended_Axcessory[n]["design"],custom_recommended_Axcessory[n]["category"]))
    else:
        T.insert(tk.END, "현재 계절과 기온에 맞는 액세서리가 없습니다.\n")

    T.pack()
    recommend__coordi.mainloop()

#카테고리에 없는 상의 추천 함수
def get_recommendation_custom_Top () :
    global Weather #기온 전역변수
    custom_recommended_Top = [] #기온 범위에 들어가는 카테고리에 없는 상의들을 저장할 리스트

    for i in range(len(custom_closet_Top)) : #반복문으로 카테고리에 없는 상의들을 저장한 리스트의 모든 요소들을 가져옴
        if (Weather-2) <= float(custom_closet_Top[i]["temperature"]) <= (Weather+2) : #temperature키의 value값(카테고리에 없는 옷을 받을 때 옷에 적합한 온도를 문자열로 받았기 때문에 형변환)이 범위에 들어가면
            custom_recommended_Top.append(custom_closet_Top[i]) #그 요소를 카테고리에 없는 상의 추천 리스트에 추가한다.

    return custom_recommended_Top #카테고리에 없는 상의 추천 리스트를 리턴

#카테고리에 없는 하의 추천 함수
def get_recommendation_custom_Low():
    global Weather #기온 전역변수
    custom_recommended_Low = [] #기온 범위에 들어가는 카테고리에 없는 하의들을 저장할 리스트

    for i in range(len(custom_closet_Low)): #반복문으로 카테고리에 없는 하의들을 저장한 리스트의 모든 요소들을 가져옴
        if (Weather - 2) <= float(custom_closet_Low[i]["temperature"]) <= (Weather + 2): #temperature키의 value값(카테고리에 없는 옷을 받을 때 옷에 적합한 온도를 문자열로 받았기 때문에 형변환)이 범위에 들어가면
            custom_recommended_Low.append(custom_closet_Low[i]) #그 요소를 카테고리에 없는 하의 추천 리스트에 추가한다.

    return custom_recommended_Low #카테고리에 없는 하의 추천 리스트를 리턴

#카테고리에 없는 겉옷 추천 함수
def get_recommendation_custom_Outer():
    global Weather #기온 전역변수
    custom_recommended_Outer = [] #기온 범위에 들어가는 카테고리에 없는 겉옷들을 저장할 리스트

    for i in range(len(custom_closet_Outer)): #반복문으로 카테고리에 없는 겉옷들을 저장한 리스트의 모든 요소들을 가져옴
        if (Weather - 2) <= float(custom_closet_Outer[i]["temperature"]) <= (Weather + 2): #temperature키의 value값(카테고리에 없는 옷을 받을 때 옷에 적합한 온도를 문자열로 받았기 때문에 형변환)이 범위에 들어가면
            custom_recommended_Outer.append(custom_closet_Outer[i]) #그 요소를 카테고리에 없는 겉옷 추천 리스트에 추가한다.

    return custom_recommended_Outer #카테고리에 없는 겉옷 추천 리스트를 리턴

#카테고리에 없는 액세서리 추천 함수
def get_recommendation_custom_Axcessory():
    global Weather #기온 전역변수
    custom_recommended_Axcessory = [] #기온 범위에 들어가는 카테고리에 없는 액세서리들을 저장할 리스트

    for i in range(len(custom_closet_Axcessory)): #반복문으로 카테고리에 없는 액세서리들을 저장한 리스트의 모든 요소들을 가져옴
        if (Weather - 2) <= float(custom_closet_Axcessory[i]["temperature"]) <= (Weather + 2): #temperature키의 value값(카테고리에 없는 옷을 받을 때 옷에 적합한 온도를 문자열로 받았기 때문에 형변환)이 범위에 들어가면
            custom_recommended_Axcessory.append(custom_closet_Axcessory[i]) #그 요소를 카테고리에 없는 액세서리 추천 리스트에 추가한다.

    return custom_recommended_Axcessory #카테고리에 없는 액세서리 추천 리스트를 리턴

# 오늘의 날짜 출력 함수
def calendar():
    global year  # 년도 전역변수
    global day  # 일 전역변수
    global day_of_the_week  # 요일 전역변수
    global Month  # 월 전역변수

    t1 = time.asctime()  # 현재 날짜와 시간을 문자열 형태로 가져오기
    t2 = t1.split()  # 문자열 나누기
    year = t2[4]  # 년도
    day = t2[2]  # 날짜

    if (t2[0] == 'Mon'): day_of_the_week = " 월요일"
    if (t2[0] == 'Tue'): day_of_the_week = " 화요일"
    if (t2[0] == 'Wed'): day_of_the_week = " 수요일"
    if (t2[0] == 'Thu'): day_of_the_week = " 목요일"
    if (t2[0] == 'Fri'): day_of_the_week = " 금요일"
    if (t2[0] == 'Sat'): day_of_the_week = " 토요일"
    if (t2[0] == 'Sun'): day_of_the_week = " 일요일"  # 요일 변환

    if (t2[1] == 'Jan'): Month = " 1월 "
    if (t2[1] == 'Feb'): Month = " 2월 "
    if (t2[1] == 'Mar'): Month = " 3월 "
    if (t2[1] == 'Apr'): Month = " 4월 "
    if (t2[1] == 'May'): Month = " 5월 "
    if (t2[1] == 'Jun'): Month = " 6월 "
    if (t2[1] == 'Jul'): Month = " 7월 "
    if (t2[1] == 'Aug'): Month = " 8월 "
    if (t2[1] == 'Sep'): Month = " 9월 "
    if (t2[1] == 'Oct'): Month = " 10월 "
    if (t2[1] == 'Nov'): Month = " 11월 "
    if (t2[1] == 'Dec'): Month = " 12월 "  # 월 변환

def categorizing():  # cloth_enter함수에서 변경한 전역 변수 return_closet값을 받아 카테고리에 따라 옷장 별로 분류
    global return_closet  # return_closet 전역변수
    if return_closet["category"] in ["맨투맨", "가디건", "후드티", "니트", "긴팔", "셔츠", "블라우스", "반팔", "민소매"]: closet_Top.append(
        return_closet)
    if return_closet["category"] in ["기모바지", "청바지", "면바지", "슬랙스", "치마", "반바지"]: closet_Low.append(return_closet)
    if return_closet["category"] in ["패딩", "가죽자켓", "코트", "자켓", "점퍼", "청자켓", "바람막이"]: closet_Outer.append(return_closet)
    if return_closet["category"] in ["목도리", "장갑"]: closet_Axcessory.append(return_closet)

def custom_categorizing() : # custom_cloth함수에서 옷 정보 입력 및 삭제 함수에서 변경한 전역 변수 custom_return_closet값을 받아 카테고리에 따라 옷장 별로 분류
    if custom_return_closet["type"] == "상의" : custom_closet_Top.append(custom_return_closet)
    if custom_return_closet["type"] == "하의": custom_closet_Low.append(custom_return_closet)
    if custom_return_closet["type"] == "겉옷": custom_closet_Outer.append(custom_return_closet)
    if custom_return_closet["type"] == "액세서리": custom_closet_Axcessory.append(custom_return_closet)

# 옷장 속 상의 출력 함수
def cloth_info_print_Top():
    cloth_info_print__Top = tk.Toplevel(root)  # 새로운 윈도우 창 띄우기
    cloth_info_print__Top.title("상의")  # 창 이름
    T = tk.Text(cloth_info_print__Top, height=(3 + len(closet_Top) + len(custom_closet_Top)), width=60)  # 텍스트 위젯 생성

    if (closet_Top == [] and custom_closet_Top == []):  # 옷장에 상의가 1개도 없을 경우
        T.insert(tk.END, "옷장에 상의가 없습니다.")
    else:  # 옷장에 상의가 있을 경우 → 리스트의 길이만큼 옷장 속 상의 딕셔너리들 출력
        for i in range(len(closet_Top)):
            T.insert(tk.END,'%s %s\n' % (closet_Top[i]["design"], closet_Top[i]["category"]))
        for i in range(len(custom_closet_Top)) :
            T.insert(tk.END, '%s %s\n'%(custom_closet_Top[i]["design"], custom_closet_Top[i]["category"]))

    T.pack()
    cloth_info_print__Top.mainloop()

# 옷장 속 하의 출력 함수
def cloth_info_print_Low():
    cloth_info_print__Low = tk.Toplevel(root)  # 새로운 윈도우 창 띄우기
    cloth_info_print__Low.title("하의") #창 이름
    T = tk.Text(cloth_info_print__Low, height=(3 + len(closet_Low)), width=60)  # 텍스트 위젯 생성

    if (closet_Low == [] and custom_closet_Low == []):  # 옷장에 하의가 1개도 없을 경우
        T.insert(tk.END, "옷장에 하의가 없습니다.")
    else:  # 옷장에 하의가 있을 경우 → 리스트의 길이만큼 옷장 속 하의 딕셔너리들 출력
        for i in range(len(closet_Low)):
            T.insert(tk.END,
                     '%s %s\n' % (closet_Low[i]["design"], closet_Low[i]["category"]))
            for i in range(len(custom_closet_Low)):
                T.insert(tk.END, '%s %s\n' % (
                custom_closet_Low[i]["design"], custom_closet_Low[i]["category"]))

    T.pack()
    cloth_info_print__Low.mainloop()

# 옷장 속 겉옷 출력 함수
def cloth_info_print_Outer():
    cloth_info_print__Outer = tk.Toplevel(root)  # 새로운 윈도우 창 띄우기
    cloth_info_print__Outer.title("겉옷") #창 이름
    T = tk.Text(cloth_info_print__Outer, height=(3 + len(closet_Outer)), width=60)  # 텍스트 위젯 생성

    if (closet_Outer == [] and custom_closet_Outer == []):  # 옷장에 겉옷이 1개도 없을 경우
        T.insert(tk.END, "옷장에 겉옷이 없습니다.")
    else:  # 옷장에 겉옷이 있을 경우 → 리스트의 길이만큼 옷장 속 겉옷 딕셔너리들 출력
        for i in range(len(closet_Outer)):
            T.insert(tk.END,
                     '%s %s\n' % (closet_Outer[i]["design"], closet_Outer[i]["category"]))
            for i in range(len(custom_closet_Outer)):
                T.insert(tk.END, '%s %s\n' % (
                custom_closet_Outer[i]["design"], custom_closet_Outer[i]["category"]))

    T.pack()
    cloth_info_print__Outer.mainloop()

# 옷장 속 악세서리 출력 함수
def cloth_info_print_Axcessory():
    cloth_info_print__Axcessory = tk.Toplevel(root)  # 새로운 윈도우 창 띄우기
    cloth_info_print__Axcessory.title("악세서리") #창 이름
    T = tk.Text(cloth_info_print__Axcessory, height=(3 + len(closet_Axcessory)), width=60)  # 텍스트 위젯 생성

    if (closet_Axcessory == [] and custom_closet_Axcessory == []):  # 옷장에 악세서리가 1개도 없을 경우
        T.insert(tk.END, "옷장에 악세서리가 없습니다.")
    else:  # 옷장에 악세서리가 있을 경우 → 리스트의 길이만큼 옷장 속 악세서리 딕셔너리들 출력
        for i in range(len(closet_Axcessory)):
            T.insert(tk.END, '%s %s\n' % (
            closet_Axcessory[i]["design"], closet_Axcessory[i]["category"]))
            for i in range(len(custom_closet_Top)):
                T.insert(tk.END, '%s %s\n' % (
                custom_closet_Axcessory[i]["design"], custom_closet_Axcessory[i]["category"]))

    T.pack()
    cloth_info_print__Axcessory.mainloop()

# 옷장 정보 출력 버튼함수
def closet_info():
    cloth_info = tk.Toplevel(root)  # 새로운 윈도우 창 띄우기
    cloth_info.title("옷장 정보")  # 창 이름
    cloth_info.geometry("200x310")  # 창 크기

    tk.Button(cloth_info, text="상의", command=cloth_info_print_Top, font=(20), fg="purple", bg="#FFFACD").pack(pady=10, ipadx=7, ipady=10)  # 상의 옷장 출력 버튼
    tk.Button(cloth_info, text="하의", command=cloth_info_print_Low, font=(20), fg="purple", bg="#FFFACD").pack(pady=10, ipadx=7, ipady=10)  # 하의 옷장 출력 버튼
    tk.Button(cloth_info, text="겉옷", command=cloth_info_print_Outer, font=(20), fg="purple", bg="#FFFACD").pack(pady=10, ipadx=7, ipady=10)  # 겉옷 옷장 출력 버튼
    tk.Button(cloth_info, text="액세서리", command=cloth_info_print_Axcessory, font=(20), fg="purple", bg="#FFFACD").pack(pady=10, ipadx=7, ipady=10)  # 악세서리 옷장 출력 버튼

    cloth_info.mainloop()

# 옷 정보 입력 및 삭제함수
S = None   # 기존의 category_entry 역할 변수
def cloth_enter():
    global S
    cloth__enter = tk.Toplevel(root)  # 새로운 윈도우 창 띄우기
    cloth__enter.title("옷 정보 입력")  # 창 이름
    cloth__enter.geometry("400x350")  # 창 크기

    tk.Label(cloth__enter, text="카테고리", font=(20), fg='purple').pack()  # 카테고리 입력받기

    ##### 버튼과 라디오버튼 코드

    # 상의 버튼
    button1 = tk.Button(cloth__enter, text="상의", command=lambda: show_radio_buttons_top("상의"))
    button1.pack()
    # 하의 버튼
    button2 = tk.Button(cloth__enter, text="하의", command=lambda: show_radio_buttons_bot("하의"))
    button2.pack()
    # 겉옷 버튼
    button3 = tk.Button(cloth__enter, text="겉옷", command=lambda: show_radio_buttons_out("겉옷"))
    button3.pack()
    # 액세서리 버튼
    button4 = tk.Button(cloth__enter, text="액세서리", command=lambda: show_radio_buttons_acc("액세서리"))
    button4.pack()
    # 출력값을 띄워줄 라벨 추가
    output_label = tk.Label(cloth__enter, text="", font=(20), fg='blue')
    output_label.pack()

    def show_radio_buttons_top(selected_option):
        global S
        # 새로운 창 열기
        radio_window = tk.Toplevel(root)
        radio_window.title("카테고리 선택")
        radio_window.geometry("300x400")

        tk.Label(radio_window, text="상의 종류를 선택하세요:", font=(16)).pack()

        # 라디오 버튼 생성
        selected_radio = tk.StringVar()

        radio1 = tk.Radiobutton(radio_window, text="맨투맨", variable=selected_radio, value="맨투맨")
        radio1.pack()

        radio2 = tk.Radiobutton(radio_window, text="가디건", variable=selected_radio, value="가디건")
        radio2.pack()

        radio3 = tk.Radiobutton(radio_window, text="후드티", variable=selected_radio, value="후드티")
        radio3.pack()

        radio4 = tk.Radiobutton(radio_window, text="니트", variable=selected_radio, value="니트")
        radio4.pack()

        radio5 = tk.Radiobutton(radio_window, text="긴팔", variable=selected_radio, value="긴팔")
        radio5.pack()

        radio6 = tk.Radiobutton(radio_window, text="셔츠", variable=selected_radio, value="셔츠")
        radio6.pack()

        radio7 = tk.Radiobutton(radio_window, text="블라우스", variable=selected_radio, value="블라우스")
        radio7.pack()

        radio8 = tk.Radiobutton(radio_window, text="반팔", variable=selected_radio, value="반팔")
        radio8.pack()

        radio9 = tk.Radiobutton(radio_window, text="민소매", variable=selected_radio, value="민소매")
        radio9.pack()

        radio10 = tk.Radiobutton(radio_window, text= "카테고리에 없는 옷", variable = selected_radio, value = "기타")
        radio10.pack()

        # 확인 버튼 생성
        confirm_button = tk.Button(radio_window, text="확인",
                                   command=lambda: update_output_label(selected_option, selected_radio.get()))
        S = selected_radio.get()
        confirm_button.pack()

        def update_output_label(selected_option, radio_option):
            global S
            # 선택된 옵션을 출력 라벨에 업데이트
            output_label.config(text=f"{selected_option}: {radio_option}")
            S = selected_radio.get()
            if (S == "기타"): #'카테고리에 없는 옷' 버튼을 클릭했을 경우 기존 창들을 모두 지우고 카테고리에 없는 옷을 입력받을 함수를 불러온다.
                radio_window.destroy()
                cloth__enter.destroy()
                custom_cloth()
            else : #카테고리를 입력받았을 경우 창을 지운다.
                radio_window.destroy()

    def show_radio_buttons_bot(selected_option):
        global S
        # 새로운 창 열기
        radio_window = tk.Toplevel(root)
        radio_window.title("카테고리 선택")
        radio_window.geometry("300x400")

        tk.Label(radio_window, text="하의 종류를 선택하세요:", font=(16)).pack()

        # 라디오 버튼 생성
        selected_radio = tk.StringVar()

        radio1 = tk.Radiobutton(radio_window, text="기모바지", variable=selected_radio, value="기모바지")
        radio1.pack()

        radio2 = tk.Radiobutton(radio_window, text="청바지", variable=selected_radio, value="청바지")
        radio2.pack()

        radio3 = tk.Radiobutton(radio_window, text="면바지", variable=selected_radio, value="면바지")
        radio3.pack()

        radio3 = tk.Radiobutton(radio_window, text="슬랙스", variable=selected_radio, value="슬랙스")
        radio3.pack()

        radio4 = tk.Radiobutton(radio_window, text="청바지", variable=selected_radio, value="청바지")
        radio4.pack()

        radio5 = tk.Radiobutton(radio_window, text="치마", variable=selected_radio, value="치마")
        radio5.pack()

        radio6 = tk.Radiobutton(radio_window, text="반바지", variable=selected_radio, value="반바지")
        radio6.pack()

        radio7 = tk.Radiobutton(radio_window, text="카테고리에 없는 옷", variable=selected_radio,  value="기타")
        radio7.pack()

        # 확인 버튼 생성
        confirm_button = tk.Button(radio_window, text="확인",
                                   command=lambda: update_output_label(selected_option, selected_radio.get()))
        S = selected_radio.get()
        confirm_button.pack()

        def update_output_label(selected_option, radio_option):
            global S
            # 선택된 옵션을 출력 라벨에 업데이트
            output_label.config(text=f"{selected_option}: {radio_option}")
            S = selected_radio.get()
            if (S == "기타"): #'카테고리에 없는 옷' 버튼을 클릭했을 경우 기존 창들을 모두 지우고 카테고리에 없는 옷을 입력받을 함수를 불러온다.
                radio_window.destroy()
                cloth__enter.destroy()
                custom_cloth()
            else : #카테고리를 입력받았을 경우 창을 지운다.
                radio_window.destroy()

    def show_radio_buttons_out(selected_option):
        global S
        # 새로운 창 열기
        radio_window = tk.Toplevel(root)
        radio_window.title("카테고리 선택")
        radio_window.geometry("300x400")

        tk.Label(radio_window, text="겉옷 종류를 선택하세요:", font=(16)).pack()

        # 라디오 버튼 생성
        selected_radio = tk.StringVar()

        radio1 = tk.Radiobutton(radio_window, text="패딩", variable=selected_radio, value="패딩")
        radio1.pack()

        radio2 = tk.Radiobutton(radio_window, text="코트", variable=selected_radio, value="코트")
        radio2.pack()

        radio3 = tk.Radiobutton(radio_window, text="가죽자켓", variable=selected_radio, value="가죽자켓")
        radio3.pack()

        radio4 = tk.Radiobutton(radio_window, text="자켓", variable=selected_radio, value="자켓")
        radio4.pack()

        radio5 = tk.Radiobutton(radio_window, text="청자켓", variable=selected_radio, value="청자켓")
        radio5.pack()

        radio6 = tk.Radiobutton(radio_window, text="점퍼", variable=selected_radio, value="점퍼")
        radio6.pack()

        radio7 = tk.Radiobutton(radio_window, text="바람막이", variable=selected_radio, value="바람막이")
        radio7.pack()

        radio8 = tk.Radiobutton(radio_window, text="카테고리에 없는 옷", variable=selected_radio, value="기타")
        radio8.pack()

        # 확인 버튼 생성
        confirm_button = tk.Button(radio_window, text="확인",
                                   command=lambda: update_output_label(selected_option, selected_radio.get()))
        S = selected_radio.get()
        confirm_button.pack()

        def update_output_label(selected_option, radio_option):
            global S
            # 선택된 옵션을 출력 라벨에 업데이트
            output_label.config(text=f"{selected_option}: {radio_option}")
            S = selected_radio.get()
            if (S == "기타"): #'카테고리에 없는 옷' 버튼을 클릭했을 경우 기존 창들을 모두 지우고 카테고리에 없는 옷을 입력받을 함수를 불러온다.
                radio_window.destroy()
                cloth__enter.destroy()
                custom_cloth()
            else : #카테고리를 입력받았을 경우 창을 지운다.
                radio_window.destroy()

    def show_radio_buttons_acc(selected_option):
        global S
        # 새로운 창 열기
        radio_window = tk.Toplevel(root)
        radio_window.title("카테고리 선택")
        radio_window.geometry("300x200")

        tk.Label(radio_window, text="액세서리 종류를 선택하세요:", font=(16)).pack()

        # 라디오 버튼 생성
        selected_radio = tk.StringVar()

        radio1 = tk.Radiobutton(radio_window, text="목도리", variable=selected_radio, value="목도리")
        radio1.pack()

        radio2 = tk.Radiobutton(radio_window, text="장갑", variable=selected_radio, value="장갑")
        radio2.pack()

        radio3 = tk.Radiobutton(radio_window, text="카테고리에 없는 옷", variable=selected_radio, value="기타")
        radio3.pack()

        # 확인 버튼 생성
        confirm_button = tk.Button(radio_window, text="확인",
                                   command=lambda: update_output_label(selected_option, selected_radio.get()))
        S = selected_radio.get()
        confirm_button.pack()

        def update_output_label(selected_option, radio_option):
            global S
            # 선택된 옵션을 출력 라벨에 업데이트
            output_label.config(text=f"{selected_option}: {radio_option}")
            S = selected_radio.get()
            if (S == "기타"): #'카테고리에 없는 옷' 버튼을 클릭했을 경우 기존 창들을 모두 지우고 카테고리에 없는 옷을 입력받을 함수를 불러온다.
                radio_window.destroy()
                cloth__enter.destroy()
                custom_cloth()
            else : #카테고리를 입력받았을 경우 창을 지운다.
                radio_window.destroy()


    #####

    tk.Label(cloth__enter, text="디자인 및 색상", font=(20), fg='purple').pack()  # 디자인 및 색상 입력받기
    design_entry = tk.Entry(cloth__enter)
    design_entry.pack()

    # 옷 정보를 옷장에 저장하는 함수
    def save_info():
        global return_closet  # return_closet 전역변수(입력받은 옷 정보들을 저장해서 옷장에 분류해서 넣을 때 필요한 변수)
        global S
        return_closet = {}  # return_closet 초기화
        category = S  # 카테고리 받아오기
        design = design_entry.get()  # 디자인 및 색상 받아오기

        return_closet = {"design": design, "category": category}  # return_closet 딕셔너리에 카테고리, 디자인 및 색상 저장

        if not category or not design:  # 카테고리, 디자인 및 색상 중 1개라도 입력되지 않았으면 오류 메시지 출력
            messagebox.showerror("오류", "카테고리, 디자인 및 색상은 모두 입력되어야 합니다.")
        else: #카테고리, 디자인, 색상이 모두 입력되었을 경우 저장되었다는 메시지 출력
            messagebox.showinfo("성공", "옷 정보가 저장되었습니다.")
            cloth__enter.destroy() #창 지우기
            categorizing()  # 옷을 카테고리에 따라 분류하는 함수 호출

    # 옷 정보를 옷장에서 삭제하는 함수
    def delete_info():
        global return_closet  # return_closet 전역변수(입력받은 옷 정보들을 저장해서 옷장 속 옷들과 비교할 때 필요한 변수)
        global S
        return_closet = {}  # return_closet 초기화
        category = S  # 카테고리 받아오기
        design = design_entry.get()  # 디자인 및 색상 받아오기

        return_closet = {"design": design, "category": category}  # return_closet 딕셔너리에 카테고리, 디자인 및 색상 저장

        if (return_closet not in closet_Top not in closet_Low not in closet_Outer not in closet_Axcessory):
            messagebox.showinfo(" ", "삭제할 옷이 존재하지 않습니다.")  # 옷 정보와 일치하는 옷이 없을 때는 삭제할 옷이 없다는 메시지 출력
        if return_closet in closet_Top:  # 상의 옷장에 있으면 상의 옷장 속 동일한 요소 삭제
            closet_Top.remove(return_closet)
            messagebox.showinfo(" ", "옷 정보가 삭제되었습니다.")  # 옷 정보가 삭제되었다는 메시지 출력
            cloth__enter.destroy()
        if return_closet in closet_Low:  # 하의 옷장에 있으면 하의 옷장 속 동일한 요소 삭제
            closet_Low.remove(return_closet)
            messagebox.showinfo(" ", "옷 정보가 삭제되었습니다.")  # 옷 정보가 삭제되었다는 메시지 출력
            cloth__enter.destroy()
        if return_closet in closet_Outer:  # 겉옷 옷장에 있으면 겉옷 옷장 속 동일한 요소 삭제
            closet_Outer.remove(return_closet)
            messagebox.showinfo(" ", "옷 정보가 삭제되었습니다.")  # 옷 정보가 삭제되었다는 메시지 출력
            cloth__enter.destroy()
        if return_closet in closet_Axcessory:  # 악세서리 옷장에 있으면 악세서리 옷장 속 동일한 요소 삭제
            closet_Axcessory.remove(return_closet)
            messagebox.showinfo(" ", "옷 정보가 삭제되었습니다.")  # 옷 정보가 삭제되었다는 메시지 출력
            cloth__enter.destroy()

    save_button = tk.Button(cloth__enter, text="저장", command=save_info, font=(20), bg='#D1B2FF')  # 저장 버튼
    save_button.place(x=135, y=300)
    delete_button = tk.Button(cloth__enter, text="삭제", command=delete_info, font=(20), bg='#D1B2FF')  # 삭제 버튼
    delete_button.place(x=205, y=300)

    cloth__enter.mainloop()

# 카테고리에 없는 옷 정보를 받아오는 함수
def custom_cloth():
    custom_clothing_temperature_window = tk.Toplevel(root) #새로운 윈도우 창 띄우기
    custom_clothing_temperature_window.title("옷 종류와 온도 설정") #창 이름

    type_radio = tk.StringVar()  #옷 종류를 받아올 변수 생성
    tk.Label(custom_clothing_temperature_window, text="옷 종류를 선택해 주세요").pack()

    # 상의 라디오 버튼
    button1 = tk.Radiobutton(custom_clothing_temperature_window, text="상의", variable=type_radio,value="상의")
    button1.pack()
    # 하의 라디오 버튼
    button2 = tk.Radiobutton(custom_clothing_temperature_window, text="하의", variable=type_radio,value="하의")
    button2.pack()
    # 겉옷 라디오 버튼
    button3 = tk.Radiobutton(custom_clothing_temperature_window, text="겉옷", variable=type_radio,value="겉옷")
    button3.pack()
    # 액세서리 라디오 버튼
    button4 = tk.Radiobutton(custom_clothing_temperature_window, text="액세서리", variable=type_radio,value="액세서리")
    button4.pack()

    tk.Label(custom_clothing_temperature_window, text="카테고리", font=(20), fg='purple').pack() #카테고리 받아오기
    custom_category = tk.Entry(custom_clothing_temperature_window)
    custom_category.pack()

    tk.Label(custom_clothing_temperature_window, text="온도", font=(20), fg='purple').pack() #온도 받아오기
    temperature_entry = tk.Entry(custom_clothing_temperature_window)
    temperature_entry.pack()

    tk.Label(custom_clothing_temperature_window, text="디자인 및 색상").pack() #디자인 및 색상 받아오기
    custom_design = tk.Entry(custom_clothing_temperature_window)
    custom_design.pack()


    # 목록에 없는 옷 종류 어느 온도에 입을 것인지 직접 설정할 수 있는 기능 추가
    #카테고리에 없는 옷 정보를 저장하는 함수
    def set_custom_clothing_temperature():
        global custom_return_closet #custom_return_closet 전역변수(입력받은 옷 정보들을 저장해서 옷장에 분류해서 넣을 때 필요한 변수)
        # 사용자가 입력한 옷 카테고리를 가져옴
        category = custom_category.get()
        # 사용자가 입력한 온도를 가져옴
        temperature = temperature_entry.get()
        type = type_radio.get() #옷 종류 받아오기
        design = custom_design.get() #디자인 및 색상 받아오기


        # 사용자가 입력한 옷 정보와 온도를 딕셔너리에 저장
        custom_return_closet = {"type" : type, "category": category, "design": design, "temperature": temperature}

        if not type or not category or not temperature or not design: #종류,카테고리,디자인 및 색상,온도 중 한 개라도 입력되지 않았을 경우 오류 메시지 출력
            messagebox.showerror("오류", "종류, 카테고리, 디자인 및 색상, 온도를 모두 입력해주세요.")
        else: #모든 정보가 입력되었을 경우 저장되었다는 메시지 출력
            messagebox.showinfo("성공","옷 정보가 저장되었습니다.")
            custom_clothing_temperature_window.destroy()  # 창 지우기
            custom_categorizing() #옷 분류 함수 호출

    #카테고리에 없는 옷 정보를 삭제하는 함수
    def delete_custom_clothing_temperature() :
        global custom_return_closet #custon_return_closet 전역변수(입력받은 옷 정보들을 저장해서 옷장 속 옷들과 비교할 때 필요한 변수)
        category = custom_category.get() #카테고리 받아오기
        temperature = temperature_entry.get() #온도 받아오기
        type = type_radio.get() #옷 종류 받아오기
        design = custom_design.get() #디자인 및 색상 받아오기

        #사용자가 입력한 옷 정보와 온도를 딕셔너리에 저장
        custom_return_closet = {"type" : type, "category": category, "design": design, "temperature" : temperature}

        if(custom_return_closet not in custom_closet_Top not in custom_closet_Low not in custom_closet_Outer not in custom_closet_Axcessory):
            #옷 정보와 일치하는 옷이 없을 때는 삭제할 옷이 없다는 메시지 출력
            messagebox.showinfo(" ","삭제할 옷이 존재하지 않습니다.")
        if return_closet in custom_closet_Top : #상의 옷장에 있으면 상의 옷장 속 동일한 요소 삭제
            custom_closet_Top.remove(custom_return_closet)
            messagebox.showinfo(" ","옷 정보가 삭제되었습니다.") #삭제되었다는 메시지 출력
            custom_clothing_temperature_window.destroy() #창 지우기
        if return_closet in custom_closet_Low: #하의 옷장에 있으면 하의 옷장 속 동일한 요소 삭제
            custom_closet_Low.remove(custom_return_closet)
            messagebox.showinfo(" ", "옷 정보가 삭제되었습니다.") #삭제되었다는 메시지 출력
            custom_clothing_temperature_window.destroy() #창 지우기
        if return_closet in custom_closet_Outer: #겉옷 옷장에 있으면 겉옷 옷장 속 동일한 요소 삭제
            custom_closet_Outer.remove(custom_return_closet)
            messagebox.showinfo(" ", "옷 정보가 삭제되었습니다.") #삭제되었다는 메시지 출력
            custom_clothing_temperature_window.destroy() #창 지우기
        if return_closet in custom_closet_Axcessory: #액세서리 옷장에 있으면 액세서리 옷장 속 동일한 요소 삭제
            custom_closet_Axcessory.remove(custom_return_closet)
            messagebox.showinfo(" ", "옷 정보가 삭제되었습니다.") #삭제되었다는 메시지 출력
            custom_clothing_temperature_window.destroy() #창 지우기

    set_custom_clothing_temperature_button = tk.Button(custom_clothing_temperature_window, text="저장",
                                                       command=set_custom_clothing_temperature, font=(20), bg='#D1B2FF') #저장 버튼
    set_custom_clothing_temperature_button.pack()
    delete_custom_clothing_temperature_button = tk.Button(custom_clothing_temperature_window, text = "삭제", command = delete_custom_clothing_temperature, font = (20), bg = '#D1B2FF') #삭제 버튼
    delete_custom_clothing_temperature_button.pack()
    custom_clothing_temperature_window.mainloop()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()  # 메인 윈도우 창
root.geometry("800x600")  # 창 크기를 크게 조절

cloth_enter_btn = tk.Button(root, text="옷 정보 입력 및 삭제", command=cloth_enter,
                            font="Helvetica 20 bold italic", fg="#8A2BE2", bg="#FFFACD")  # 옷 정보 입력 및 삭제 버튼
cloth_enter_btn.place(relx=0.5, rely=0.2, anchor="center")  # 가로 중앙 정렬

cloth_info_btn = tk.Button(root, text="옷장 정보", command=closet_info, font="Helvetica 20 bold italic", fg="#8A2BE2",bg="#FFFACD")  # 옷장 정보 출력 버튼
cloth_info_btn.place(relx=0.5, rely=0.5, anchor="center")  # 가로 중앙 정렬

cloth_recommend_btn = tk.Button(root, text="코디 추천", command=recommend_coordi,
                                font="Helvetica 20 bold italic", fg="#8A2BE2", bg="#FFFACD")  # 코디 추천 버튼
cloth_recommend_btn.place(relx=0.5, rely=0.8, anchor="center")  # 가로 중앙 정렬

# 창을 화면 중앙에 배치
center_window(root, 800, 600)

root.mainloop()
