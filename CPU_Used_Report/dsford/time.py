#-*- coding: utf-8 -*-
# time.py
import time


def sub_folder_name():

    return "%04d-%02d-%02d %02d시%02d분%02d초" % (time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)




# sub_folder_name()
# 백업 폴더 내 폴더 이름을 시간으로 정한 것
# "YYYY-MM-DD HH시MM분SS초" 형식으로 반환
