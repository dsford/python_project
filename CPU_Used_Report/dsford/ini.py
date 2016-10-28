#-*- coding: utf-8 -*-
# ini.py
import codecs


# [ini 파일의 기본 규칙]
# ini 파일은 utf-16 형식으로 인코딩한 파일로 한다.
# 첫 문자가 "[", "#" 는 가져오지 않는다.
# "명칭=옵션" 의 형식 
# 옵션이 숫자라면 숫자형식 그대로 사용하면 된다.


def load_ini(ini_file_dir):

    ini_file = codecs.open(ini_file_dir, "r", "utf-16")

    ini_dict = {}

    for line in ini_file:
        temp = line.strip()
        if not temp == "" and not temp[0] == "[" and not temp[0] == "#":
            temp = line.strip().replace("==", "=▣")
            temp = temp.split("=")
            temp[1] = temp[1].replace("▣", "=")

            try:
                ini_dict[temp[0]] = int(temp[1])
            except:
                ini_dict[temp[0]] = temp[1]

    ini_file.close()
          
    return ini_dict
    

# load_ini(ini_file_dir)
# ini 파일에서 각종 정보를 가져옴
# ini_file_dir : ini 파일의 전체 경로
# 딕셔너리 형태로 반환



def make_ini(ini_file_dir):

    ini_file = codecs.open(ini_file_dir, "w", "utf-16")

    ini_file.write("# .ini 파일 양식 입니다.\r\n")
    ini_file.write("# 첫 문자가 \"[\" 나 \"#\"는 불러오지 않습니다.\r\n")
    ini_file.write("# \"명칭=옵션\" 형식으로 작성해야 합니다.\r\n")
    ini_file.write("\r\n")
    ini_file.write("[Test]\r\n")
    ini_file.write("Test=1\r\n")

    ini_file.close()


# make_ini(ini_file_dir)
# ini 파일 양식 생성
# ini_file_dir : ini 파일의 전체 경로



    
    
