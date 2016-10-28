#-*- coding: utf-8 -*-
# show.py
import os
import time

def warning(program_name, delay_time):

    program_version = "v%02d%02d%02d" % (time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)

    
    os.system("cls")

    print("\n" + program_name + " " + program_version)
    temp_len = len(program_name + " " + program_version) - 11
    temp_string = ""
    for i in range(temp_len):
        temp_string = temp_string + " "
        
    print(temp_string + "by D.S.Ford\n\n")

    print("\n[주 의 사 항]\n\n")
    print("이 프로그램은 제한된 정보만을 기준으로 만들었기 때문에\n")
    print("경우에 따라서 오류가 발생하거나 제대로된 결과물을 낼 수 없을 수도 있습니다.\n\n")
    print("따라서 결과물을 100% 신뢰해서는 안 되며, 반드시 직접 확인하셔야 합니다.\n\n\n")
    print(str(delay_time) + "초 후 프로그램을 시작합니다.")

    time.sleep(delay_time)

    os.system("cls")
   


# warning(program_name, delay_time)
# 프로그램 시작 전 경고문구를 보여줍니다.
# program_name : 프로그램 이름
# program_version : 프로그램 버전, YYMMDD(날짜) 형식으로 사용

