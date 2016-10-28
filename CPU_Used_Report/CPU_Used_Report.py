#-*- coding: utf-8 -*-

# CPU_Used_Report

import os
import sys
import time
import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font

import dsford.search


# 프로그램 이름
program_name = "CPU_Used_Report"

base_dir = ".\\"
ext1 = "txt"
pass_line = 6 # 처음 6줄은 데이터와 관련없음

t1 = 18 # 00:00 ~ 08:30 - 업무시간
t2 = 19 # 09:00 ~ 18:00 - 업무시간
t3 = 11 # 18:30 ~ 23:30 - 비업무시간

# 반올림 
round_num = 2

# 엑셀 시작 위치
start_row = 1
start_col = 1


def make_xlsx(data, file_dir):

    wb = openpyxl.Workbook()
    ws = wb.active

    xlsx_file = file_dir[:-3] + "xlsx"


    ws.column_dimensions["A"].width = 15
    ws.column_dimensions["B"].width = 15
    ws.column_dimensions["C"].width = 15
    
    ws.cell(column=start_col, row=start_row, value="년월일")
    ws.cell(column=start_col, row=start_row).alignment=Alignment(horizontal="center",vertical="center")
    ws.cell(column=start_col, row=start_row).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
    ws.cell(column=start_col + 1, row=start_row, value="업무시간평균")
    ws.cell(column=start_col + 1, row=start_row).alignment=Alignment(horizontal="center",vertical="center")
    ws.cell(column=start_col + 1, row=start_row).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
    ws.cell(column=start_col + 2, row=start_row, value="비업무시간평균")
    ws.cell(column=start_col + 2, row=start_row).alignment=Alignment(horizontal="center",vertical="center")
    ws.cell(column=start_col + 2, row=start_row).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
    
    
    for i in range(len(data)):
        ws.cell(column=start_col, row=start_row + i + 1, value=data[i][0])
        ws.cell(column=start_col, row=start_row + i + 1).alignment=Alignment(horizontal="center",vertical="center")
        ws.cell(column=start_col, row=start_row + i + 1).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
        
        ws.cell(column=start_col + 1, row=start_row + i + 1, value=data[i][1])
        ws.cell(column=start_col + 1, row=start_row + i + 1).alignment=Alignment(horizontal="center",vertical="center")
        ws.cell(column=start_col + 1, row=start_row + i + 1).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
        
        
        ws.cell(column=start_col + 2, row=start_row + i + 1, value=data[i][2])
        ws.cell(column=start_col + 2, row=start_row + i + 1).alignment=Alignment(horizontal="center",vertical="center")
        ws.cell(column=start_col + 2, row=start_row + i + 1).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
               
    
    wb.save(filename = xlsx_file)

    return 0


def txt_analysis(txt_file):

    file = open(txt_file, "r")

    # 데이터와 관련 없는 첫 부분 제외
    for i in range(pass_line):
        file.readline()

    # 데이터 가져오기
    ori_db = []
    line_end = 0
    while line_end == 0:
        temp = file.readline().strip()
        if not temp == "":     
            ori_db.append(temp)
        else:
            line_end = 1

    # 오름차순 정렬
    ori_db.sort()

    # "날짜, 시간, 수치" 로 분리(공백 한칸)
    new_db = []
    for db in ori_db:
        new_db.append(db.split(" "))


    used_result = []
    line = 0
    for i in range(len(new_db) // (t1 + t2 + t3)):

        # 일자
        temp_date = new_db[line][0]

        temp_work = []
        temp_nonwork = []

        # 비업무시간 : 00:00 ~ 08:30
        for j in range(t1):
            temp_nonwork.append(float(new_db[line][2]))
            line += 1
            
        # 업무시간 : 09:00 ~ 18:00
        for j in range(t2):
            temp_work.append(float(new_db[line][2]))
            line += 1

        # 비업무시간 : 18:30 ~ 23:30
        for j in range(t3):
            temp_nonwork.append(float(new_db[line][2]))
            line += 1

        # 각 수치 평균
        work_average = round(sum(temp_work)/t2,round_num)
        nonwork_average = round(sum(temp_nonwork)/(t1 + t3),round_num)

        used_result.append([temp_date, work_average, nonwork_average])

    return used_result
        
        
def main():

    print("작업을 시작합니다.\n")

    # .txt 확장자를 가진 파일 목록 생성
    file_list = []
    full_file_list = []

    file_list += dsford.search.ext(base_dir, ext1, 0)
    full_file_list += dsford.search.ext(base_dir, ext1, 1)

    if len(file_list) == 0:
        print(base_dir + "에 txt 파일이 존재하지 않습니다.")
        print("프로그램을 종료합니다.")               
        time.sleep(2)        
        sys.exit()

    print("대상 파일 : " + str(len(file_list)) + "개\n")

    for file in full_file_list:
        data = txt_analysis(file)
        make_xlsx(data, file)
        
    print("모든 작업을 완료했습니다.")
    time.sleep(2)        
    sys.exit()
    
if __name__ == '__main__':
    sys.exit(main())
