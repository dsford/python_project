#-*- coding: utf-8 -*-

# Data Split

import os
import sys

import dsford.backup
import dsford.ini
import dsford.search
import dsford.show
import dsford.time



def main():

    print("<작업 준비중...>\n")

    program_start_time = dsford.time.sub_folder_name()

    head_count = [20, 17, 2, 9, 10, 18] # 9는 원래 12이나 코드는 바이트가 아닌 글자수 기준으로 불러오므로 한글 세글자(6바이트)는 3으로 처리하여 3을 뺌

    split_count = [4, 7, 14, 3, 4, 1, 9, 9, 3, 6, 6, 2]

    total_head_count = 76
    total_count = 68

    file_ext = ["txt"]    
    file_list = []
   

    for i in file_ext:

        file_list += dsford.search.ext(".\\", i, 0)


    report_file = open(".\\[작 업 결 과].txt", "w")
    report_file.write("[작 업 결 과]\n\n")
    report_file.write("작업일시 : " + program_start_time + "\n\n")
    
    print("준비 완료\n")
    print("\n<1차 제외 작업>")
    new_file_list = []
    for i, file in enumerate(file_list):
        if os.path.getsize(".\\" + file) <= (total_head_count + total_count):
            
            print("▶" + file + "는 파일 크기가 너무 작습니다.")
            report_file.write(file + "\t\t" + ": 실패(파일 크기가 너무 작습니다.)\n")
            
        else:
            new_file_list.append(file)


    file_list = new_file_list

    print("\n\n<분리 작업 시작>\n")
    for file in file_list:

        print(file)

        ori_txt = open(".\\" + file, "r")

        ori_txt.read(total_head_count)

        is_enter = 0        
        check_chr = ord(ori_txt.read(1))

        
        if not check_chr >= ord("0") and check_chr <= ord("9"):
            print("▶" + "줄바꿈 있는 파일")
            is_enter = 1
            ori_txt.read(2)
            
        else:

            ori_txt.seek(0)
            ori_txt.read(total_head_count)

        
        temp_db_count = len(ori_txt.read())

        row_count, test_count = divmod(temp_db_count, total_count)

        ori_txt.seek(0)

        if not test_count == 0 or os.path.getsize(".\\" + file) <= (total_head_count + total_count):

            print("▶" + "작업할 파일이 아닌 것으로 추정\n")
            report_file.write(file + "\t\t" + ": 실패(데이터 부분의 문자수가 68배수가 아닙니다.)\n")
            ori_txt.close()

        else:         

            print("▶" + "작업 파일로 간주하고 분리 작업 시작")
            new_txt = open(".\\" + "[분리]" + file , "w")

            temp_head_split = []
            for split in head_count:
                temp_head_split.append(ori_txt.read(split))
            new_txt.write(",".join(temp_head_split) + "\n")
                
            if is_enter == 1:
                ori_txt.read(3)
            
            for i in range(row_count):
                temp_split = []
                for split in split_count:
                    temp_split.append(ori_txt.read(split))
                new_txt.write(",".join(temp_split) + "\n")
            
            new_txt.close()
            print("▶" + "분리작업 완료\n")
            report_file.write(file + "\t\t" + ": 성공\n")
            ori_txt.close()

        
    report_file.close()
    print("\n<작업 완료>\n")
    print("프로그램을 종료합니다.")
    os.startfile(".\\[작 업 결 과].txt")

    
if __name__ == '__main__':
    sys.exit(main())
