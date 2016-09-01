#-*- coding: utf-8 -*-
import os
import re
import sys
import time
import xlrd
import codecs
import shutil
import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font


#프로그램 이름
program_name = "Order_Report"

#프로그램 시작 시간
program_start_time = "%04d-%02d-%02d %02d%02d%02d" % (time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)


#버전
program_version = "v160726"

#리포트 관련 리스트
report_file_list = []
report_work_result = []
report_work_note = []
        

#ini파일 생성(초기화용)
def make_ini():

    ini_head = ["General",
                "Folder",
                "File",
                "HeaderRow",
                "Patterns",
                "Control",
                "ETC"]

    ini_general = ["ShowWarning=True", 
                   "ShowReadme=False", 
                   "ShowReport=True",
                   "DoFileBackup=True", 
                   "DoMakeLog=False"
                   ]

    ini_folder = ["File=.\\",
                  "Report=.\\Report\\",
                  "Backup=.\\Backup\\",
                  "Log=.\\Log\\",
                  "EntItemsDB=.\\EntDB\\"
                  ]
    
    ini_file = ["Ext1=.xlsx",
                "Ext2=.xls",
                "Ext3=",
                "Ext4=",
                "Ext5="]
    
    ini_headrow = ["Field1=상품명",
                   "Field2=상품정보",
                   "Field3=상품정보(상세)",
                   "Field4=상품정보 (상세)",
                   "Field5=주문옵션",
                   "Field6=",
                   "Field7=",
                   "Field8=", 
                   "Field9="]

    ini_patterns = ["ItemSplit=(\\n|\\r\\n|/)", 
                    "Number=\\D(\\d+[.)]|옵션\\d+|선택\\d+|[①-⑳])\\D"
                    "Count=\\D(\\d+)[개]\\D",
                    "ExtractNumber=(\\d+|[①-⑳])"
                    ]
    
    ini_control = ["Mode=Auto",
                   "MaxItemsCount=26",
                   "ManageDataOrderBy=TotalToCase",
                   "ManageXlsDataWrite=Excel",
                   "ManageHeaderRowMultipleResult=Last"
                    ]
    
    ini_etc = []

    ini_sub = [ini_general, ini_folder, ini_file, ini_headrow, ini_patterns, ini_control, ini_etc]


    ini_file = codecs.open(".\\" + program_name + ".ini", "w", "utf-16")


    for i in range(len(ini_head)):        
        ini_file.write("[" + ini_head[i] + "]\r\n")

        for sub in ini_sub[i]:
            ini_file.write(sub + "\r\n")

        ini_file.write("\r\n\r\n")
            
       
    ini_file.close()


#프로그램 시작전 ini 파일 불러오기    
def load_ini():
    
    ini_file = codecs.open(".\\" + program_name + ".ini", "r", "utf-16")


    ini_dict = {}
    for line in ini_file:
        if not line.strip() == "" and not line.strip()[0] == "[":
            temp = line.strip().split("=")
            ini_dict[temp[0]] = temp[1]

    ini_file.close()


            
    return ini_dict

    
#대상 파일 검색            
def search(dirname, file_ext):

    file_list = [] 

    for file_ext in file_ext:           
        file_name = os.listdir(dirname)
        
        for file in file_name:
            ext = os.path.splitext(file)[-1]      
            if ext == file_ext: 
                file_list.append(file)
            
    return file_list



#카운트 리스트 생성
def make_count_list():
    count_list = []
    for i in range(int(load_ini()["MaxItemsCount"]) + 1):
        count_list.append("")
    return count_list



#번호에서 숫자만 추출
def conv_num(number):
 
    only_num = load_ini()["ExtractNumber"]
  
    num = re.findall(only_num, number)
  
    if len(str(num[0])) == 1:
      if ord(str(num[0])) >= ord("①"):
        num[0] = ord(str(num[0])) - ord("①") + 1
      
    return int(num[0])


#번호, 숫자만 남기고 나머지 지우기
def get_data(ori_text):

    text = re.sub(load_ini()["ItemSplit"], " ", ori_text).strip()
  
    number_pat = load_ini()["Number"]
    count_pat = load_ini()["Count"]

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



#xlsx파일에 직접 테이블 기록
def write_xlsx(wb2, ws2, file, ncol, trow, total_count_list, new_max_order_count, ManageDataOrderBy):
                         

    if ManageDataOrderBy == "TotalToCase":
        for i in range(new_max_order_count + 1):
            if not i == 0:
                ws2.cell(column=ncol + 1 + i, row=trow + 1, value="옵션" + str(i))
            else:
                ws2.cell(column=ncol + 1 + i, row=trow + 1, value="합계")
            ws2.cell(column=ncol + 1 + i, row=trow + 1).alignment=Alignment(horizontal="center",vertical="center")
            ws2.cell(column=ncol + 1 + i, row=trow + 1).font = Font(bold=True)
            ws2.cell(column=ncol + 1 + i, row=trow + 1).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
            ws2.cell(column=ncol + 1 + i, row=trow + 1).fill = PatternFill(fill_type="solid", start_color="FFFFFF00")

        for i in range(len(total_count_list)):
            for j in range(new_max_order_count + 1):
                if not total_count_list[i][j] == "":
                    ws2.cell(column=ncol + 1 + j, row=trow + 2 + i, value=int(total_count_list[i][j]))
                #else:
                    #ws2.cell(column=ncol + 1 + j, row=trow + 2 + i, value=total_count_list[i][j])
                ws2.cell(column=ncol + 1 + j, row=trow + 2 + i).alignment=Alignment(horizontal="center",vertical="center")
                ws2.cell(column=ncol + 1 + j, row=trow + 2 + i).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))

                if j == 0:
                    ws2.cell(column=ncol + 1 + j, row=trow + 2 + i).font = Font(bold=True)
                    ws2.cell(column=ncol + 1 + j, row=trow + 2 + i).fill = PatternFill(fill_type="solid", start_color="808080")
                    
        wb2.save(filename = file)

        print("\n" + file.split("\\")[len(file.split("\\")) - 1] + "에 대한 작업을 완료했습니다.\n")
        print("처리할 다른 파일이 남아있다면 2초 후 다시 시작합니다.\n")
        time.sleep(2)
        if load_ini()["ShowReport"] == "True":
            report_work_result.append("성공")
            report_work_note .append("")

    elif ManageDataOrderBy == "CaseToTotal":
        for i in range(new_max_order_count + 1):
            if not i == new_max_order_count:
                ws2.cell(column=ncol + 1 + i, row=trow + 1, value="옵션" + str(i + 1))
            else:
                ws2.cell(column=ncol + 1 + i, row=trow + 1, value="합계")
            ws2.cell(column=ncol + 1 + i, row=trow + 1).alignment=Alignment(horizontal="center",vertical="center")
            ws2.cell(column=ncol + 1 + i, row=trow + 1).font = Font(bold=True)
            ws2.cell(column=ncol + 1 + i, row=trow + 1).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
            ws2.cell(column=ncol + 1 + i, row=trow + 1).fill = PatternFill(fill_type="solid", start_color="FFFFFF00")


        for i in range(len(total_count_list)):
            for j in range(1, new_max_order_count + 1):
                if not total_count_list[i][j] == "":
                    ws2.cell(column=ncol + j, row=trow + 2 + i, value=int(total_count_list[i][j]))
                #else:
                    #ws2.cell(column=ncol + j, row=trow + 2 + i, value=total_count_list[i][j])
                ws2.cell(column=ncol + j, row=trow + 2 + i).alignment=Alignment(horizontal="center",vertical="center")
                ws2.cell(column=ncol + j, row=trow + 2 + i).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))

            if not total_count_list[i][0] == "":
                ws2.cell(column=ncol + new_max_order_count + 1, row=trow + 2 + i, value=int(total_count_list[i][0]))
            ws2.cell(column=ncol + new_max_order_count + 1, row=trow + 2 + i).alignment=Alignment(horizontal="center",vertical="center")
            ws2.cell(column=ncol + new_max_order_count + 1, row=trow + 2 + i).border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
            ws2.cell(column=ncol + new_max_order_count + 1, row=trow + 2 + i).font = Font(bold=True)
            ws2.cell(column=ncol + new_max_order_count + 1, row=trow + 2 + i).fill = PatternFill(fill_type="solid", start_color="808080")

                    
        wb2.save(filename = file)

    
        print("\n" + file.split("\\")[len(file.split("\\")) - 1] + "에 대한 작업을 완료했습니다.\n")
        print("처리할 다른 파일이 남아있다면 2초 후 다시 시작합니다.\n")
        time.sleep(2)
        if load_ini()["ShowReport"] == "True":
            report_work_result.append("성공")
            report_work_note .append("")

    else:
        os.system("cls")
        print("\nManageDataOrderBy 옵션이 올바르지 않습니다.")
        print("프로그램을 종료합니다. ini파일을 확인해 주세요.")
        time.sleep(2)
        if load_ini()["ShowReport"] == "True":
            report_file.write("ManageDataOrderBy 설정이 올바르지 않습니다.\n")
            report_file.close()
            os.startfile(report_folder + program_start_time + ".txt")
                
        sys.exit()





#파일에서 데이터 추출
def data_summary(file):
    

    print(file.split("\\")[len(file.split("\\")) - 1] + "작업 시작")
    
    #파일 읽기
    wb = xlrd.open_workbook(file)
    ws = wb.sheet_by_index(0)

    #머리글 행 검색
    ncol = ws.ncols
    nrow = ws.nrows

    tcol = 0
    trow = 0

    temp_col = []
    temp_row = []

    title_name_db = []
    for i in range(9):
        if not load_ini()["Field" + str(i + 1)] == "":
            title_name_db.append(load_ini()["Field" + str(i + 1)])
        

    loop_end = 0
    sub_loop_end = 0
    temp_i = 0
    while loop_end == 0:
        temp = ws.row_values(temp_i)
        
        for i in range(len(temp)):
            for j in title_name_db:
                if temp[i] == j:
                    temp_col.append(i)
                    temp_row.append(temp_i)
                    sub_loop_end = 1
                    
        if sub_loop_end == 1:
            loop_end = 1

            if len(temp_col) == 1:
                tcol = temp_col[0]
                trow = temp_row[0]
                

            else:                

                ManageHeaderRowMultipleResult = load_ini()["ManageHeaderRowMultipleResult"]
                
                if  ManageHeaderRowMultipleResult == "Ahead":
                    tcol = temp_col[0]
                    trow = temp_row[0]
                    
                elif ManageHeaderRowMultipleResult == "Last":
                    tcol = temp_col[len(temp_col) - 1]
                    trow = temp_row[len(temp_row) - 1]

                elif ManageHeaderRowMultipleResult == "Select":

                    manage_loop = 0
                    while manage_loop == 0:
                        os.system('cls')
                        print("\n대상파일 : " + file.split("\\")[len(file.split("\\")) - 1])
                        print(str(len(temp_col)) + "개의 머리글 행이 검색되었습니다.\n\n\n")

                    
                        for i in range(len(temp_col)):
                            temp_db = ws.col_values(temp_col[i])

                            print("[" + str(i + 1) + "]    " + temp_db[int(len(temp_db) / 2) + 1][:50] + "\n\n")

                        print("[X]    프로그램 종료(파일이 여러개면 다음 파일로 넘어갑니다.)\n\n")
                            
                        manage_select = input("\n데이터가 있는 항목의 숫자를 입력하고 Enter를 눌러 주세요 : ")
                        
                        if manage_select.upper() == "X":
                            report_work_result.append("실패")
                            report_work_note .append("사용자가 임의로 작업 종료")
                            return None
                                               
                              
                        for i in range(len(temp_col)):
                            if manage_select == str(i + 1): 
                                tcol = temp_col[i]
                                trow = temp_row[i]
                                manage_loop = 1
                                os.system('cls')
                                break
                        
                        if manage_loop == 0:
                            os.system('cls')
                            print("\n잘못 입력하셨습니다. 1초 후 선택 화면으로 돌아갑니다.")
                            time.sleep(1)

            
        if loop_end == 1:
            break
        temp_i = temp_i + 1
        if temp_i > nrow - 1:
            loop_end = 1
            
            print("\n대상파일 : " + file.split("\\")[len(file.split("\\")) - 1] + "\n")
            print("주문관련 머리글 행이 없습니다. 파일을 확인해 주세요.\n")
            print("처리할 다른 파일이 남아있다면 2초 후 다시 시작합니다.\n")

            report_work_result.append("실패")
            report_work_note .append("주문관련 머리글 행 없음")
            
            time.sleep(2)
            return None


    #번호, 숫자 취합 작업
    data = ws.col_values(tcol)

    total_count_list = []
    for i in range(1, len(data)):
        if data[i] == "":
            total_count_list.append(make_count_list())
        else:
            total_count_list.append(get_data(data[i]))

    temp_max = 1
    for i in range(len(total_count_list)):
        for j in range(1, len(total_count_list[i])):
            if not total_count_list[i][j] == "":
                temp_max = max(temp_max, j)

    new_max_order_count = temp_max
                

    #파일쓰기 작업

    ManageDataOrderBy = load_ini()["ManageDataOrderBy"]

    if file[-4:] == "xlsx":

        wb2 = openpyxl.load_workbook(file)
        ws2 = wb2.active
    
        write_xlsx(wb2, ws2, file, ncol, trow, total_count_list, new_max_order_count, ManageDataOrderBy)

    elif file[-3:] == "xls":

        print("\n대상파일 : " + file.split("\\")[len(file.split("\\")) - 1])
        print("해당 파일은 .xls 이므로 정해둔 설정에 따라 파일을 따로 생성합니다.")
        
        ManageXlsDataWrite = load_ini()["ManageXlsDataWrite"]

        if ManageXlsDataWrite == "Excel":

            
            
            wb2 = openpyxl.Workbook()
            ws2 = wb2.active

            new_file = file[:-4] + "_Report.xlsx"
        
            write_xlsx(wb2, ws2, new_file, 0, trow, total_count_list, new_max_order_count, ManageDataOrderBy)

    
        elif ManageXlsDataWrite == "Txt":

            txt_file = open(file[:-3] + "txt", "w")


            if ManageDataOrderBy == "TotalToCase":
                for i in range(new_max_order_count + 1):
                    if i == 0:
                        txt_file.write("합계" + "\t")
                    else:
                        txt_file.write("옵션" + str(i) + "\t")
                txt_file.write("\r\n")

                for i in range(len(total_count_list)):
                    for j in range(new_max_order_count + 1):
                        txt_file.write(str(total_count_list[i][j]) + "\t")
                    txt_file.write("\r\n")

                txt_file.close()
                print(file.split("\\")[len(file.split("\\")) - 1][:-3] + "txt" + "파일을 생성했습니다.\n")
                report_work_result.append("성공")
                report_work_note .append(file.split("\\")[len(file.split("\\")) - 1][:-3] + "txt" + "로 생성")

            elif ManageDataOrderBy == "CaseToTotal":
                for i in range(new_max_order_count + 1):
                    if not i == new_max_order_count:
                        txt_file.write("옵션" + str(i + 1) + "\t")
                    else:
                        txt_file.write("합계" + "\t")
                txt_file.write("\r\n")

                for i in range(len(total_count_list)):
                    for j in range(1, new_max_order_count + 1):
                        txt_file.write(str(total_count_list[i][j]) + "\t")
                    txt_file.write(str(total_count_list[i][0]) + "\t")
                    txt_file.write("\r\n")

                txt_file.close()
                print("\n" + file.split("\\")[len(file.split("\\")) - 1][:-3] + "txt" + "에 대한 작업을 완료했습니다.\n")
                report_work_result.append("성공")
                report_work_note .append(file.split("\\")[len(file.split("\\")) - 1][:-3] + "txt" + "로 생성")

            else:
                os.system("cls")
                print("\nManageDataOrderBy 옵션이 올바르지 않습니다.")
                print("프로그램을 종료합니다. ini파일을 확인해 주세요.")
                time.sleep(2)
                if load_ini()["ShowReport"] == "True":
                    report_file.write("ManageDataOrderBy 설정이 올바르지 않습니다.\n")
                    report_file.close()
                    os.startfile(report_folder + program_start_time + ".txt")
                
                sys.exit()
            
        else:
                os.system("cls")
                print("\nManageXlsDataWrite 설정이 올바르지 않습니다.\n")
                print("프로그램을 종료합니다. ini파일을 확인해 주세요.")           
                time.sleep(2)
                if load_ini()["ShowReport"] == "True":
                    report_file.write("ManageXlsDataWrite 설정이 올바르지 않습니다.\n")
                    report_file.close()
                    os.startfile(report_folder + program_start_time + ".txt")
                
                sys.exit()

    else:
        os.system("cls")
        print("\nManageDataOrderBy 옵션이 올바르지 않습니다.\n")
        print("프로그램을 종료합니다. ini파일을 확인해 주세요.")
        time.sleep(2)
        if load_ini()["ShowReport"] == "True":
            report_file.write("ManageDataOrderBy 설정이 올바르지 않습니다.\n")
            report_file.close()
            os.startfile(report_folder + program_start_time + ".txt")
                
        sys.exit()                      




#자동 작업
def auto_mode(file_list, full_file_list):

    if load_ini()["ManageHeaderRowMultipleResult"] == "Select":
        
         print("작동 모드 : 반자동 (사용자가 입력해야 할 작업이 있을 수 있습니다.)\n ")

    else:

        print("작동 모드 : 자동 (미리 정해둔 설정대로 작업합니다.)\n\n")


    print("\n5초 후 작업을 시작합니다.\n")
    time.sleep(5)


    for file in full_file_list:
        data_summary(file)

    
        
    


    

#수동 작업
def manual_mode(file_list, full_file_list):

    print("manual")



#경고문
def ShowWarning():
    
    os.system("cls")

    print("\nOrder Report " + program_version)
    print("         by D.S.Ford\n\n")

    print("\n[주 의 사 항]\n\n")
    print("이 프로그램은 제한된 정보만을 기준으로 만들었기 때문에\n")
    print("경우에 따라서 오류가 발생하거나 제대로된 결과물을 낼 수 없을 수도 있습니다.\n\n")
    print("따라서 결과물을 100% 신뢰해서는 안 되며, 반드시 직접 확인하셔야 합니다.\n\n\n")
    print("5초 후 프로그램을 시작합니다.")

    time.sleep(5)

    os.system("cls")



#리포트 폴더 생성
if load_ini()["ShowReport"] == "True":
        
    print("리포트 파일 생성 여부 : True")
        
    report_folder = load_ini()["Report"]
    if not os.path.isdir(report_folder): 
        os.mkdir(report_folder)

    report_file = open(report_folder + program_start_time + ".txt", "w")
    report_file.write("[작 업 결 과]\n\n")
    report_file.write("작업일시 : " + program_start_time + "\n\n")
    print(program_start_time + ".txt" + "파일을 생성했습니다.\n")





def main():


    if load_ini()["ShowWarning"] == "True":
        ShowWarning()
    
                        
    
    #특정 확장자를 가진 파일 목록 생성
    file_ext = []
    for i in range(5):
        if not load_ini()["Ext" + str(i + 1)] == "":
            file_ext.append(load_ini()["Ext" + str(i + 1)])

    base_dir = load_ini()["File"]

    file_list = search(base_dir, file_ext)

    
    if base_dir[0] == ".":
        base_dir = os.path.abspath(os.curdir) + base_dir[1:]



    if len(file_list) == 0:
        print(base_dir + "에 대상 파일이 존재하지 않습니다.")
        print("프로그램을 종료합니다.")       

        if load_ini()["ShowReport"] == "True":
            report_file.write(base_dir + " 에 대상 파일이 존재하지 않습니다.\n")
            report_file.close()

            os.startfile(report_folder + program_start_time + ".txt")

        time.sleep(2)
        
        sys.exit()

            
    full_file_list = []
    print("\n대상 파일 : " + str(len(file_list)) + "개")
    for file in file_list:
        full_file_list.append(base_dir + file)
        report_file_list.append(file)
        print("  " + file)
    print("\n")
    
    

    #파일 백업
    if load_ini()["DoFileBackup"] == "True":

        print("파일 백업 여부 : True")

        backup_folder = load_ini()["Backup"]
        if not os.path.isdir(backup_folder): 
            os.mkdir(backup_folder)

        backup_sub_folder = program_start_time
        if not os.path.isdir(backup_folder + '\\' + backup_sub_folder): 
            os.mkdir(backup_folder + '\\' + backup_sub_folder)

        for i in range(len(file_list)):
            shutil.copy(full_file_list[i], backup_folder + '\\' + backup_sub_folder + '\\' + file_list[i])

        if backup_folder[0] == ".":
            backup_folder = os.path.abspath(os.curdir) + backup_folder[1:]
        print(backup_folder + '\\' + backup_sub_folder + '\\' + " 에 파일을 백업했습니다.\n\n")
        

    #모드에 따라 실행 (오토 / 수동) // 수동은 일단 보류
    if load_ini()["Mode"] == "Auto":
        auto_mode(file_list, full_file_list)
    else:
        manual_mode(file_list, full_file_list)
        

    print("\n\n모든 작업이 완료되었습니다.")
    if load_ini()["ShowReport"] == "True":
        for i in range(len(report_file_list)):
            report_file.write("  " + report_file_list[i] + " : " + report_work_result[i])
            if not report_work_note[i] == "":
                report_file.write(" // " + report_work_note[i])
            report_file.write("\n")
                
        report_file.close()

        os.startfile(report_folder + program_start_time + ".txt")
        

if __name__ == '__main__':
    sys.exit(main())
