#-*- coding: utf-8 -*-
# backup.py
import os
import shutil


def backup(backup_folder, backup_sub_folder_name, file_name, full_file_dir):

    if not os.path.isdir(backup_folder):
        os.mkdir(backup_folder)

    if not os.path.isdir(backup_folder + "\\" + backup_sub_folder_name):
        os.mkdir(backup_folder + "\\" + backup_sub_folder_name)


    shutil.copy(full_file_dir, backup_folder + '\\' + backup_sub_folder_name + '\\' + file_name)
    



# backup(backup_folder, backup_sub_folder_name, file_name, full_file_dir)
# 작업할 파일을 백업 폴더에 백업
# backup_folder : 백업 폴더 경로
# backup_sub_folder_name : 백업 폴더 내에 생성할 폴더 이름
# file_name : 파일 이름
# full_file_dir : 파일의 전체 경로

