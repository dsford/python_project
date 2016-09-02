#-*- coding: utf-8 -*-
import os
import re
import sys
import time
import xlrd
import codecs
import shutil
import xlsxwriter


#프로그램 이름
program_name = "Log_Arrangement"

#프로그램 시작 시간
program_start_time = "%04d-%02d-%02d %02d%02d%02d" % (time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)

#측정용 시간
start_time = 0

#버전
program_version = "v160817"


time_delay = 1


#프로그램 시작전 ini 파일 불러오기    
def load_ini():
    
    ini_file = codecs.open(".\\" + program_name + ".ini", "r", "utf-16")


    ini_dict = {}
    for line in ini_file:
        temp = line.strip()
        if not temp == "" and not temp[0] == "[" and not temp[0] == "#":
            temp = line.strip().replace("==", "=▣")
            temp = temp.split("=")
            temp[1] = temp[1].replace("▣", "=")
            ini_dict[temp[0]] = temp[1]

    ini_file.close()
          
    return ini_dict

    
#대상 파일 검색            
def search(dirname, file_ext):

    file_list = [] 
         
    file_name = os.listdir(dirname)
        
    for file in file_name:
        ext = os.path.splitext(file)[-1]
        if ext == file_ext: 
            file_list.append(file)
            
    return file_list




def get_data(file, full_file):
    
    log_file = open(full_file, "r")

    print("\n대상파일 : " + file + "\n")
    """
    print("로그파일의 일부분을 검사하여 로그파일이 맞는지 확인합니다.")

    
    end_loop = 0
    line_count = 0
    verify_count = 0
    next_while = 0
    while end_loop == 0:
        try:
            line_info = load_ini()["Line" + str(next_while + 1)]

            temp_line = log_file.readline()
            line_count += 1

            if line_info == "N":
                print(11231231)
                print(temp_line)

                if temp_line == "\n" or temp_line == "\r\n":
                    verify_count += 1



            elif line_info == "H":
                
                if temp_line.strip()[0] == load_ini()["StartHeadNum"]:
                    verify_count += 1


                    

            elif line_info == "L":
                
                if temp_line.strip()[0] == load_ini()["LineType"]:
                    verify_count += 1



            elif line_info == "N":
                
                if len(temp_line.strip()) >= int(load_ini()["ItemNum"]):
                    verify_count += 1


            next_while += 1
        except:
            if line_count == verify_count:
                print("\n검증완료")
                print("이 파일을 로그 파일로 간주합니다.")
                end_loop = 1

            else:
                print("로그 파일이 아닙니다. 프로그램을 종료합니다.")
                end_loop = 1
                sys.exit()
                
    """
    print("\n데이터 정리를 시작합니다.")
    
    log_file.seek(0)

    lines = len(log_file.readlines())

    log_file.seek(0)


    end_loop = 0
    line = 0
    tarr = []
    carr = []

    temp_head = []

    ItemNum = int(load_ini()["ItemNum"])
    LastHeadName = load_ini()["LastHeadName"]
    DataCombNum = int(load_ini()["DataCombNum"])
    

    
    for i in range(ItemNum - 1):       
        temp_head.append(str(i))
    temp_head.append(LastHeadName)

    carr.append(temp_head)

    while end_loop == 0:
        temp = log_file.readline()
        line += 1   
     
        if temp[0] == "=":
            temp = log_file.readline().strip()
            line += 1
            for i in range(10):
                temp = temp.replace("  "," ")
            tarr.append(temp)
 
            if len(tarr) == DataCombNum:
                carr.append(" ".join(tarr).split(" "))
                tarr = []
                                        
        if line == lines:
            end_loop = 1           

    log_file.close()
    
    print("데이터 정리 완료")

    return carr




def export_to_xlsx(full_data, export_file_name):

    
    wb = xlsxwriter.Workbook(export_file_name)
    ws = wb.add_worksheet("결과")

    HeadRowColor = load_ini()["HeadRowColor"]
    RowSize = int(load_ini()["RowSize"])
    ColumnSize = int(load_ini()["ColumnSize"])

    
 
    format1 = wb.add_format()
    format1.set_bold()
    format1.set_align("center")
    format1.set_align("vcenter")
    format1.set_pattern(1)
    format1.set_bg_color(HeadRowColor)
    format1.set_top()
    format1.set_bottom()
    format1.set_left()
    format1.set_right()
    format1.set_num_format(0x0)
 
 
    format2 = wb.add_format()
    format2.set_align("center")
    format2.set_align("vcenter")
    format2.set_top()
    format2.set_bottom()
    format2.set_left()
    format2.set_right()
    format2.set_num_format(0x0)

    print("\n")
 
    for i in range(len(full_data)):
        for j in range(len(full_data[i])):
            if not i == 0:
                try:
                    ws.write(i, j, int(full_data[i][j]), format2)
                except:
                    ws.write(i, j, full_data[i][j], format2)
            else:
                try:
                    ws.write(i, j, int(full_data[i][j]), format1)
                except:
                    ws.write(i, j, full_data[i][j], format1)
 
        if i > 0 and i % 1000 == 0:
            
            print(str(i)+"세트 쓰기 완료")

    for i in range(len(full_data)):
        ws.set_row(i, RowSize)

    for i in range(len(full_data[0])):
        ws.set_column(i, ColumnSize)

    print(str(len(full_data) - 1)+"세트 쓰기 완료")
    print("\n모든 세트를 쓰기 완료 했습니다.")
    print("\n파일 저장을 시작합니다.")
    print("저장에는 시간이 다소 소요될 수 있습니다.")
         
    wb.close()  

    


def export_to_txt(full_data, export_file_name):

    txt_file = open(export_file_name, "w")

    for i in range(len(full_data)):
        txt_file.write("\t".join(full_data[i])+"\n")

    txt_file.close()



#경고문
def ShowWarning():
    
    os.system("cls")

    print("\n" + program_name + " " + program_version)
    print("            by D.S.Ford\n\n")

    print("\n[주 의 사 항]\n\n")
    print("이 프로그램은 제한된 정보만을 기준으로 만들었기 때문에\n")
    print("경우에 따라서 오류가 발생하거나 제대로된 결과물을 낼 수 없을 수도 있습니다.\n\n")
    print("따라서 결과물을 100% 신뢰해서는 안 되며, 반드시 직접 확인하셔야 합니다.\n\n\n")
    print("5초 후 프로그램을 시작합니다.")

    time.sleep(5)

    os.system("cls")




def main():


    if load_ini()["ShowWarning"] == "True":
        ShowWarning()
    
                        
    
    #특정 확장자를 가진 파일 목록 생성
        
    base_dir = load_ini()["File"]

    

    file = search(base_dir, "." + load_ini()["FileExt"])


    # 2개 이상 나왔을 경우 처리
    if len(file) > 1:
        
        manage_loop = 0
        while manage_loop == 0:
            os.system("cls")

            print("\n로그 파일 " + str(len(file)) + "개가 발견되었습니다.\n\n")
            
            for i in range(len(file)):
                print("[" + str(i + 1) + "] " + file[i] + "\n")
            print("[X] 프로그램 종료\n")

            manage_select = input("\n작업할 로그 파일에 해당하는 숫자를 입력하고 Enter를 눌러 주세요 : ")

            if manage_select.upper() == "X":
                print("\n프로그램을 종료합니다.")
                time.sleep(time_delay)
                sys.exit()
                
            for i in range(len(file)):
                if manage_select == str(i + 1):
                    file = file[i]
                    print("\n")
                    manage_loop = 1
                    break
                
            if manage_loop == 0:
                print("\n잘못 입력하셨습니다. 1초 후 선택 화면으로 돌아갑니다.")
                time.sleep(time_delay)
    elif len(file) == 1:
        file = file[0]

    else:
        print("\n로그 파일이 없습니다. 프로그램을 종료합니다.")
        time.sleep(time_delay)
        sys.exit()

    # 전체 경로 (openpyxl 전용)
    full_file = os.path.abspath(os.curdir) + "\\" + file


    

    #파일 백업
    if load_ini()["DoFileBackup"] == "True":

        print("파일 백업 여부 : True")

        backup_folder = load_ini()["Backup"]
        if not os.path.isdir(backup_folder): 
            os.mkdir(backup_folder)

        backup_sub_folder = program_start_time
        if not os.path.isdir(backup_folder + '\\' + backup_sub_folder): 
            os.mkdir(backup_folder + '\\' + backup_sub_folder)

        shutil.copy(full_file, backup_folder + '\\' + backup_sub_folder + '\\' + file)

        if backup_folder[0] == ".":
            backup_folder = os.path.abspath(os.curdir) + backup_folder[1:]
        print(backup_folder + '\\' + backup_sub_folder + '\\' + " 에 파일을 백업했습니다.\n\n")

        
    #작업 시작

    start_time = time.time()

    full_data = get_data(file, full_file)
 
        
    print("\n쓰기 작업을 시작합니다.")

    

    export_file_name = full_file[:-(len(load_ini()["FileExt"])+1)] + "_result" + "." + load_ini()["ResultFileExt"]
    export_only_file_name = file[:-(len(load_ini()["FileExt"])+1)] + "_result" + "." + load_ini()["ResultFileExt"]
    
    print("저장 형식 : " + load_ini()["ResultFileExt"])
    print("저장 파일명 : " + export_only_file_name)

    if load_ini()["ResultFileExt"] == "xlsx":
        export_to_xlsx(full_data, export_file_name)

    elif load_ini()["ResultFileExt"] == "txt":
        
        export_to_txt(full_data, export_file_name)


    print("\n파일 저장이 완료되었습니다.")
    print("\n총 소요시간 : " + str(int(time.time() - start_time) + 1) + "초")
    print("\n프로그램을 종료합니다.")
    time.sleep(3)
    sys.exit()



   

if __name__ == '__main__':
    sys.exit(main())
