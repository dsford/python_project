#-*- coding: utf-8 -*-

# Order Analysis

import os
import re
import sys
import time
import xlrd
import codecs
import shutil
import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font

import dsford.backup
import dsford.ini
import dsford.search
import dsford.show
import dsford.time


# 프로그램 이름
program_name = "Order_Analysis"

# 프로그램 버전
program_ver = "v161001"

# 프로그램 시작 시간
program_start_time = dsford.time.sub_folder_name()

# ini파일 로드
try:
    ini_dict = dsford.ini.load_ini(".\\Order_Report.ini")
except:
    print("Order_Report.ini 파일이 없습니다. 프로그램을 종료합니다.")
    time.sleep(2)
    sys.exit()

# 리포트 관련 리스트
report_file_list = []
report_work_result = []
report_work_note = []
report_only_filename_list = []



# 리포트 폴더 생성     
report_folder = ini_dict["Report"]
if not os.path.isdir(report_folder): 
    os.mkdir(report_folder)

report_file = open(report_folder + "[분석결과] " + program_start_time + ".txt", "w")
report_file.write("[분 석 결 과]\n\n")
report_file.write("분석일시 : " + program_start_time + "\n\n\n")


#카운트 리스트 생성
def make_count_list():
    count_list = []
    for i in range(int(ini_dict["MaxItemsCount"]) + 1):
        count_list.append("")
    return count_list



#번호에서 숫자만 추출
def conv_num(number):
 
    only_num = ini_dict["ExtractNumber"]
  
    num = re.findall(only_num, number)
  
    if len(str(num[0])) == 1:
      if ord(str(num[0])) >= ord("①"):
        num[0] = ord(str(num[0])) - ord("①") + 1
      
    return int(num[0])


#번호, 숫자만 남기고 나머지 지우기
def get_data(ori_text):

    text = re.sub(ini_dict["ItemSplit"], " ", ori_text).strip()
  
    number_pat = ini_dict["Number"]
    count_pat = ini_dict["Count"]

    get_list = []
    temp_list = []
    search_level = 0
  
    for word in text.split(" "):
      new_word = " " + word + " "
    
      temp_num = re.findall(number_pat, new_word)
      temp_cou = re.findall(count_pat, new_word)
         
      if search_level == 0:
        if len(temp_num) > 0 and len(temp_cou) > 0:
          temp_list.append(conv_num(temp_num[0]))
          temp_list.append(int(temp_cou[len(temp_cou) - 1]))
          search_level = 2       
        elif len(temp_num) > 0:        
          temp_list.append(conv_num(temp_num[0]))
          search_level = 1
        

      elif search_level > 0:      
        if len(temp_num) > 0 and len(temp_cou) > 0:
          if search_level == 2:
            get_list.append(temp_list)
            temp_list = []
            temp_list.append(conv_num(temp_num[0]))
            temp_list.append(int(temp_cou[len(temp_cou) - 1]))          
          elif search_level == 1:
            temp_list.append(int(temp_cou[len(temp_cou) - 1]))
            search_level = 2
          
        elif len(temp_num) > 0:
          if search_level == 2:
            get_list.append(temp_list)
            temp_list = []
            temp_list.append(conv_num(temp_num[0]))
            search_level = 1
          
        elif len(temp_cou) > 0:     
          if search_level == 2:  
            temp_list[1] = int(temp_cou[len(temp_cou) - 1])
          elif search_level == 1:
            temp_list.append(int(temp_cou[len(temp_cou) - 1]))
            search_level = 2
          
  
    get_list.append(temp_list)           
            
    #print(get_list)
    
    count_list = make_count_list()
    for i in range(len(get_list)):
        if count_list[get_list[i][0]] == "":
            count_list[get_list[i][0]] = 0
        count_list[get_list[i][0]] = count_list[get_list[i][0]] + get_list[i][1]

    temp_sum = 0
    
    for i in range(1, len(count_list)):
        if not count_list[i] == "":
            temp_sum = temp_sum + count_list[i]

    count_list[0] = temp_sum
     
    return count_list


def num2excelcol(num):
    
    temp = []

    while True:

        num, r = divmod(num, 26)
        # num = 몫으로 변환, r = 나머지
        # A ~ Z 까지 26개 이므로 숫자를 26으로 나눔
    
        if r == 0:
            r = 26
            num -= 1
        # 나머지가 0일 경우 26의 배수라는 의미이므로 Z(26번째)가 되어야 하니 26으로 바꿈
        # 26으로 바꾸는 과정은 다시말해 몫에서 1만큼 빌려온 셈이 되므로 몫을 1 감소시킴

        temp.append(chr(r + 64))
        # ASCII 코드에서 65가 A이고, 나머지는 1부터 시작하기 때문에 r + 64

        if num < 26:
            if not num == 0:
                temp.append(chr(num + 64))
            #몫이 26보다 작으면 더이상 나눌 수 없으므로 문자로 변환
            
            col = []
            for i in range(len(temp)-1,-1,-1):
                col.append(temp[i])
            #문자 순서 반전
            
            return "".join(col)             



# 파일에서 데이터 추출
def data_summary(file):
    
    report_temp = []

    
    only_ext = file.split("\\")[len(file.split("\\")) - 1].split(".")[len(file.split("\\")[len(file.split("\\")) - 1].split("."))-1]

   
    
    if only_ext == "xls":
        report_temp.append("[" + file.split("\\")[len(file.split("\\")) - 1] + "] (ini 설정에 따라 결과물은 새로운 " + ini_dict["ManageXlsDataWrite"] + " 파일로 만들어 집니다.)\n\n")
        

    else:
        report_temp.append("[" + file.split("\\")[len(file.split("\\")) - 1] + "]\n\n")
        
    report_only_filename_list.append(file.split("\\")[len(file.split("\\")) - 1])

    
    #파일 읽기
    wb = xlrd.open_workbook(file)
    ws = wb.sheet_by_index(0)

    #머리글 행 검색
    ncol = ws.ncols
    nrow = ws.nrows
    first_col = 0

    tcol = 0
    trow = 0

    temp_col = []
    temp_row = []

    title_name_db = []

    field_num = 1
    while True:    
        try:
            field = ini_dict["Field" + str(field_num)]
            if not field == "":
                title_name_db.append(field)
            field_num += 1
        except:
            break


    loop_end = 0
    sub_loop_end = 0
    temp_i = 0
    title_name_only = []
    while loop_end == 0:
        temp = ws.row_values(temp_i)
        
        for i in range(len(temp)):
            for j in title_name_db:
                if temp[i] == j:
                    title_name_only.append(j)
                    temp_col.append(i)
                    temp_row.append(temp_i)

                    for k in range(len(temp)):
                        if not temp[k] == "":
                            first_col = k
                            break

                    
                    sub_loop_end = 1
                    
        if sub_loop_end == 1:
            loop_end = 1


            
        if loop_end == 1:
            break
        
        temp_i = temp_i + 1
        
        if temp_i > nrow - 1:
            loop_end = 1
            
            
            report_temp.append("주문관련 머리글 열이 없습니다.\n\n\n\n")
            report_work_result.append("▶ 부적합 : 주문관련 머리글 열이 없습니다.")
            report_temp.append("\n\n")
            report_work_note.append(report_temp)
            
            time.sleep(2)
            return None




    #번호, 숫자 취합 작업

    

    if len(temp_col) > 1:
            
            report_temp.append(" <주문관련 머리글 열 : " + str(len(temp_col)) + "개>\n\n")


            
    for num in range(len(temp_col)):

        err_count = 0
        err_list = []
        
        tcol = temp_col[num]
        trow = temp_row[num]

        
        report_temp.append(" ■ 머리글 열 이름 : " + title_name_only[num] + "\n")
        report_temp.append(" ■ 머리글 열 주소 : " + num2excelcol(tcol + 1) + str(trow + 1) + "\n\n")
        

        
        data = ws.col_values(tcol)

        total_count_list = []
        is_list = 1
        for i in range(trow + 1, len(data)):

            
            if not data[i] == "":

                try:
                    get_data(data[i])
                    
                except:
                    if is_list == 1:
                        report_temp.append(" <부적합 주문정보 목록>\n")
                        is_list = 0
                    report_temp.append("  [" + num2excelcol(tcol + 1) + str(i + 1) + "] " + data[i] + "\n")
                    err_count += 1

        err_list.append(err_count)

        report_temp.append("\n\n\n")

       
    if 0 in err_list:

        report_work_result.append("▶ 적합")

    else:

        report_work_result.append("▶ 부적합 : 주문내용이 형식에 맞지 않습니다.")
    report_temp.append("\n\n")

    report_work_note.append(report_temp)
    print(file.split("\\")[len(file.split("\\")) - 1] + " 분석완료")
    


def main():
    
    os.system("cls")
    print("Order Analysis " + program_ver + "\n\n")
    print("이 프로그램은 아래의 용도로 사용할 수 있습니다.\n")
    print("1. Order Report 사용전 적합한 파일인지 점검")
    print("(현 버전에선 주문정보 유무 및 형식에 대해서만 점검합니다)\n")
    #print("2. Order Report 오류 발생시 문제점 예측\n")
    print("3초 후 분석을 시작합니다.\n\n")

    time.sleep(3)

    #print("ini 파일을 점검합니다.")
    #print("ini 파일 점검을 완료했습니다.\n\n")

    
    # .xlsx .xls 확장자를 가진 파일 목록 생성
    file_ext = []
    ext_num = 1
    while True:    
        try:
            ext = ini_dict["Ext" + str(ext_num)]
            if not ext == "":
                file_ext.append(ext)
            ext_num += 1
        except:
            break

    file_list = []
    full_file_list = []

    for i in file_ext:

        file_list += dsford.search.ext(ini_dict["File"], i, 0)
        full_file_list += dsford.search.ext(ini_dict["File"], i, 1)

    if len(file_list) == 0:
        print("분석할 파일이 존재하지 않습니다.")
        print("프로그램을 종료합니다.")       

        report_file.write("분석할 파일이 존재하지 않습니다.\n")
        report_file.close()

        os.startfile(report_folder + "[분석결과] " + program_start_time + ".txt")
        
        time.sleep(2)
        
        sys.exit()

    print("\n분석 대상 파일 : " + str(len(file_list)) + "개\n")

    for i in file_list:
        report_file_list.append(i)


    for file in full_file_list:
        data_summary(file)

    report_file.write("<분석 결과 요약>\n\n")

    for i in range(len(report_only_filename_list)):
        report_file.write(report_only_filename_list[i] + " " + report_work_result[i] + "\n")

    report_file.write("\n\n\n<상세 분석 결과>\n\n")
    for i in range(len(report_work_note)):

        for j in range(len(report_work_note[i])):

            if j == 1:
                report_file.write(report_work_result[i])
            
            report_file.write(report_work_note[i][j])
                         
            


    report_file.close()
    os.startfile(report_folder + "[분석결과] " + program_start_time + ".txt")
    time.sleep(2)
        
    sys.exit()
    
if __name__ == '__main__':
    sys.exit(main())
