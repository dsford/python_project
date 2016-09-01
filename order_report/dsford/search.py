#-*- coding: utf-8 -*-
# search.py
import os


def ext(dirname, file_ext, is_full_dir):

    file_list = []
    file_ext = "." + file_ext         
    file_name = os.listdir(dirname)
        
    for file in file_name:
        ext = os.path.splitext(file)[-1]
        
        if ext == file_ext:
            if is_full_dir == 1:
                if dirname == ".\\":
                    full_dir = os.path.abspath(os.curdir) + "\\" + file
                else:
                    full_dir = os.path.abspath(dirname) + "\\" + file

                file_list.append(full_dir)
                
            else:
                file_list.append(file)

            
    return file_list

# ext(dirname, file_ext, is_full_dir)
# 확장자로 지정 폴더의 파일 검색(하위 폴더는 검색하지 않음)
# dirname : 검색할 폴더 경로
# file_ext : 확장자 ex) "txt"
# is_full_dir : 전체 경로를 나타낼지 여부 (맞다면 1)
# 결과는 리스트 형태로 반
