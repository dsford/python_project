#-*- coding: utf-8 -*-
import os
import re
import sys
import glob
import time
import random
import codecs
import shutil
import binascii
import webbrowser
from colorama import init, Fore, Back, Style

init(autoreset=True)

#기본 폴더 & 확장자
if len(sys.argv) > 1:
        input_folder = './[Input]/'
        output_folder = './[Result]/'
        cvm_folder = './Data/'
        info_folder = './Info/'
        font_folder = './Font/'
        table_k_folder = './Table(k)/'
        table_j_folder = './Table(j)/'
        table_m_folder = './Table(m)/'
        patch_folder = './Patch/'
        
else:
        input_folder = './Patch/temp/'
        output_folder = './Patch/temp/'
        cvm_folder = './Data/'
        info_folder = './Patch/temp/'
        font_folder = './Patch/temp/'
        #table_k_folder = './Table(k)/'
        #table_j_folder = './Table(j)/'
        #table_m_folder = './Table(m)/'
        patch_folder = './Patch/'       


        
patch_ext = 'dsfp'
patch_ver= 1
program_title = '디멘토(Demento)'
console_type = 'Play Station 2'
patch_maker = '총괄 : D.S.Ford | 번역 : 팀 한글날'
use_magic_code = 1
        

if not os.path.isdir(output_folder):
        os.mkdir(output_folder)







#Detool.py -t
def export_cvm_info():
    
    #output_folder = './[Result]/'

    #if not os.path.isdir(output_folder):
        #os.mkdir(output_folder)
        
    cvm_folder = './Data/'
    
    cvm_file = open(cvm_folder + '/' + 'DATA.CVM', 'rb')
    cvm_info = open(output_folder + '/' + 'DATA.txt', 'w')
    cvm_table_info = open(output_folder + '/' + 'DATA_table_info.txt', 'w')

    
    cvm_info.write('\n\n----------[0xA800~]--------------\n\n')
    cvm_info.write('[NAME_SIZE]' + '    ' + '[NAME_ID]' + '    '  + '[ETC]' +  '    ' +  '[NAME]' + '\n' )

    cvm_file.seek(43008)

    count_off = 0
    while count_off == 0:
        name_size = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        zero1 = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        
        name_id = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        zero2 = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        
        etc_hex = ''
        for i in range(4):
            etc_hex = etc_hex + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()

        temp_name = ''
        for i in range(int(name_size, 16)):
            temp_name = temp_name + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
            
       
        
        last_pos = cvm_file.tell()
        check_zero = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        if check_zero == '00':
            temp_name = temp_name + check_zero
        else:
            cvm_file.seek(last_pos)

        
        
        cvm_info.write(name_size + zero1 + '    '  + name_id + zero2 + '    ' + etc_hex + ' ' + temp_name +'    '+ codecs.decode(temp_name,'hex_codec').decode('utf-8') + '\n')


        last_pos = cvm_file.tell()
        check_end = binascii.hexlify(cvm_file.read(8)).decode('utf-8').upper()
        if check_end == '0000000000000000':
            count_off = 1
        else:
            cvm_file.seek(last_pos)

    #B800~

    cvm_info.write('\n\n----------[0xB800~]--------------\n\n')
    cvm_info.write('[NAME_SIZE]' + '    ' +'[ETC_1]'+'  ' + '[NAME_ID]' + '    '  + '[ETC_2]' +  '    ' +  '[NAME]' + '\n')

    cvm_file.seek(47104)

    count_off = 0
    while count_off == 0:
        name_size = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        zero1 = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        
        etc_hex = ''
        for i in range(3):
            etc_hex = etc_hex + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
            
        name_id = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        zero2 = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        
        etc_hex2 = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()       

        temp_name = ''
        for i in range(int(name_size, 16)):
            temp_name = temp_name + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        last_pos = cvm_file.tell()
        check_zero = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        if check_zero == '00':
            temp_name = temp_name + check_zero
        else:
            cvm_file.seek(last_pos)

        cvm_info.write(name_size + zero1 + '    '  + etc_hex + '    ' + name_id + zero2 + '    ' + etc_hex2 + ' ' + temp_name +'    '+ codecs.decode(temp_name,'hex_codec').decode('utf-8') + '\n')
        
        last_pos = cvm_file.tell()
        check_end = binascii.hexlify(cvm_file.read(8)).decode('utf-8').upper()
        if check_end == '0000000000000000':
            count_off = 1
        else:
            cvm_file.seek(last_pos)

    #C800~

    check_class = []
    class_name = []
    class_pos = []

    cvm_info.write('\n\n----------[0xC800~]--------------\n\n')
    cvm_info.write('[TABLE_SIZE]	[FILE_START(L)] [FILE_START(B)] [FILE_SIZE(L)] [FILE_SIZE(B)] [ETC]	[NAME_SIZE] [NAME]' + '\n')

    cvm_file.seek(51200)

    count_off = 0
    while count_off == 0:
        
        table_size = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        zero1 = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()

        class_pos.append(cvm_file.tell())

        file_start1 = ''
        for i in range(4):
            file_start1 = file_start1 + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()

        file_start2 = ''
        for i in range(4):
            file_start2 = file_start2 + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        if int(file_start2, 16) < 234:
            check_class.append('[Fold] ')
        else:
            check_class.append('[File] ')

        file_size1 = ''
        for i in range(4):
            file_size1 = file_size1 + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()

        file_size2 = ''
        for i in range(4):
            file_size2 = file_size2 + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
            
        etc_hex1 = ''
        for i in range(8):
            etc_hex1 = etc_hex1 + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()

        etc_hex2 = ''
        for i in range(6):
            etc_hex2 = etc_hex2 + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        
        name_size = binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        
        temp_name = ''
        for i in range(int(table_size, 16) - (2 + 4 + 4 + 4 + 4 + 8 + 6 + 1)):
            temp_name = temp_name + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
        class_name.append(codecs.decode(temp_name,'hex_codec').decode('utf-8').replace(';1',''))

        cvm_info.write(table_size + zero1 + '    '  + file_start1 + file_start2 + '    ' + file_size1 + file_size2 +' ' + etc_hex1 + '    ' + etc_hex2 + ' '+name_size+'   ' + temp_name +'    '+ codecs.decode(temp_name,'hex_codec').decode('utf-8') + '\n')
        
        last_pos = cvm_file.tell()
        check_end = binascii.hexlify(cvm_file.read(8)).decode('utf-8').upper()
        
        if check_end == '0000000000000000':
            if last_pos + 1 < 484538:
                cvm_file.seek(last_pos + (2048 - last_pos % 2048))
                cvm_info.write('\n\n----------['+ hex(cvm_file.tell()).replace('L','') +'~]--------------\n\n')
            else:
                count_off = 1
        else:
            cvm_file.seek(last_pos)


    for i in range(len(class_name)):
        cvm_table_info.write(check_class[i] + ' '+ class_name[i] + ' '+ str(class_pos[i]).replace('L','')+'\n')

            
    return 0

            
#Detool.py -u
def unpack_to_cvm():

    os.system('cls')

    print('\nDATA.CVM 파일 해제를 시작합니다.\n\n')

    #output_folder = './[Result]/'
    #info_folder = './Info/'
    #cvm_folder = './Data/'
    
    cvm_file = open(cvm_folder + '/' + 'DATA.CVM', 'rb')
    cvm_info = open(info_folder  + '/' + 'CVM_Info.bin', 'r')
    

    unpack_folder_name = cvm_folder + '/UnpackCVM/'
    if not os.path.isdir(unpack_folder_name):
        os.mkdir(unpack_folder_name)

    print('기본정보 수집중...', end='\r')

    info_split = re.compile('(?P<type>.+)[;](?P<name>.+)[;](?P<pos>\d+)')

    data_type = [] #Make, Fold, File, Root, Head
    data_name = []
    data_pos = [] #Fold => In File Numbers, Head => Header Size // pos = pos + 2(table_index_size)
    
    with cvm_info as info:
        for line in info:
            data_type.append(re.match(info_split, line).group('type'))
            data_name.append(re.match(info_split, line).group('name'))
            data_pos.append(int(re.match(info_split, line).group('pos')))

    print('기본정보 수집중... 완료\n')

    print('파일 해제 시작...\r')
    count_off = 0
    i_counter = 0
    this_folder_name = ''
    while count_off == 0:
        if data_type[i_counter] == 'Make':
            print('                                        ', end='\r')    
            print(Fore.YELLOW + data_name[i_counter] + Fore.WHITE + ' (' + str(i_counter + 1) + '/2943)', end='\r')
            make_folder_name = unpack_folder_name + '/' + data_name[i_counter]
            if not os.path.isdir(make_folder_name):
                os.mkdir(make_folder_name)
            i_counter += 1
            
        elif data_type[i_counter] == 'Fold':
            
            this_folder_name = unpack_folder_name + '/' + data_name[i_counter] + '/'
            i_counter += 1

        elif data_type[i_counter] == 'File':
            print('                                        ', end='\r') 
            print(Fore.CYAN + data_name[i_counter] + Fore.WHITE + ' (' + str(i_counter + 1) + '/2943)', end='\r')
            temp_file = open(this_folder_name + data_name[i_counter], 'wb')
                
            cvm_file.seek(data_pos[i_counter] + 4)
            temp_start = ''
            for j in range(4):
                temp_start = temp_start + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
            file_start = int(temp_start, 16) * 2048 + 6144

            cvm_file.seek(data_pos[i_counter] + 12)
            temp_size = ''
            for j in range(4):
                temp_size = temp_size + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
            file_size = int(temp_size, 16)

            
            cvm_file.seek(file_start)
            temp_file.write(cvm_file.read(file_size))
            temp_file.close()
            i_counter += 1
                
        elif data_type[i_counter] == 'Root':
            print('                                        ', end='\r')     
            print(Fore.CYAN + data_name[i_counter] + Fore.WHITE + ' (' + str(i_counter + 1) + '/2943)', end='\r')
            temp_file = open(unpack_folder_name + '/' + data_name[i_counter], 'wb')

            cvm_file.seek(data_pos[i_counter] + 4)
            temp_start = ''
            for j in range(4):
                temp_start = temp_start + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
            file_start = int(temp_start, 16) * 2048 + 6144


            cvm_file.seek(data_pos[i_counter] + 12)
            temp_size = ''
            for j in range(4):
                temp_size = temp_size + binascii.hexlify(cvm_file.read(1)).decode('utf-8').upper()
            file_size = int(temp_size, 16)

            cvm_file.seek(file_start)
            temp_file.write(cvm_file.read(file_size))
            temp_file.close()
                
            i_counter += 1
                
        else:
            print('파일 해제 완료')
            print('\n')
            print('헤더 영역을 추출합니다...', end='\r')

            cvm_file.seek(0)
            cvm_header = open(unpack_folder_name + '/' + data_name[i_counter], 'wb')
            cvm_header.write(cvm_file.read(data_pos[i_counter]))
            cvm_header.close()

            count_off = 1
            
    print('헤더 영역을 추출합니다... 완료\n')
    print('DATA.CVM 파일의 해제가 완료되었습니다.\n')
    time.sleep(1)

    return 0


#Detool.py -r
def repack_to_folder():
    
    os.system('cls')

    print('\nDATA.CVM 파일 리팩을 시작합니다.\n\n')
    #output_folder = './[Result]/'
    #info_folder = './Info/'
    #cvm_folder = './Data/'
    
    print('기본정보 수집중...', end='\r')
    repack_cvm = open('./' + 'DATA.CVM', 'wb')   
    cvm_info = open(info_folder + '/' + 'CVM_Info.bin', 'r')
    repack_folder_name = cvm_folder + '/UnpackCVM/'
    

    info_split = re.compile('(?P<type>.+)[;](?P<name>.+)[;](?P<pos>\d+)')

    data_type = [] #Make, Fold, File, Root, Head
    data_name = []
    data_pos = [] #Fold => In File Numbers, Head => Header Size // pos = pos + 2(table_index_size)
    data_size = []
    data_add_zero = []
     
    with cvm_info as info:
        for line in info:
            data_type.append(re.match(info_split, line).group('type'))
            data_name.append(re.match(info_split, line).group('name'))
            data_pos.append(int(re.match(info_split, line).group('pos')))

            if re.match(info_split, line).group('type') ==  'Make':
                data_size.append(0)
                data_add_zero.append(0)

            elif re.match(info_split, line).group('type') ==  'Fold':
                this_folder_name = repack_folder_name + '/' + re.match(info_split, line).group('name') + '/'
                data_size.append(0)
                data_add_zero.append(0)

            elif re.match(info_split, line).group('type') ==  'File':
                data_size.append(os.path.getsize(this_folder_name + re.match(info_split, line).group('name')))
                if os.path.getsize(this_folder_name + re.match(info_split, line).group('name')) % 2048 == 0:
                    data_add_zero.append(0)
                else:
                    data_add_zero.append(2048 - os.path.getsize(this_folder_name + re.match(info_split, line).group('name')) % 2048)

            elif re.match(info_split, line).group('type') ==  'Root':
                this_folder_name = repack_folder_name + '/'
                data_size.append(os.path.getsize(this_folder_name + re.match(info_split, line).group('name')))
                if os.path.getsize(this_folder_name + re.match(info_split, line).group('name')) % 2048 == 0:
                    data_add_zero.append(0)
                else:
                    data_add_zero.append(2048 - os.path.getsize(this_folder_name + re.match(info_split, line).group('name')) % 2048)
                
            else:
                data_size.append(0)
                data_add_zero.append(0)
        
    print('기본정보 수집중... 완료\n')
    
    print('헤더 영역을 생성합니다...', end='\r')
    only_data_name = []
    only_data_pos = []
    only_data_size = []
    only_data_add_zero = []   

    for i in range(len(data_type)):
        if data_type[i] == 'File' or data_type[i] == 'Root':
            only_data_name.append(data_name[i])
            only_data_pos.append(data_pos[i])
            only_data_size.append(data_size[i])
            only_data_add_zero.append(data_add_zero[i])
            
    cvm_header = open(repack_folder_name + data_name[len(data_name) - 1], 'r+b')
    #first_file_pos = 485376
    temp_pos = 0
    for i in range(len(only_data_name)):        
        if not i == 0:
            temp_pos = temp_pos + only_data_size[i - 1] + only_data_add_zero[i - 1]
        else:
            temp_pos = 485376
            
        temp_pos2 = int((temp_pos - 6144) / 2048)
        
        temp_hex = str('0x' + '%.2x' % temp_pos2)[2:].zfill(8).upper()
        re_info1 = temp_hex[6:8] + temp_hex[4:6] + temp_hex[2:4] + temp_hex[0:2] + temp_hex
        temp_size = str('0x' + '%.2x' % only_data_size[i])[2:].zfill(8).upper()
        re_info2 = temp_size[6:8] + temp_size[4:6] + temp_size[2:4] + temp_size[0:2] + temp_size

        cvm_header.seek(only_data_pos[i])
        cvm_header.write(binascii.unhexlify(re_info1 + re_info2))
        

    cvm_header.close()
    print('헤더 영역을 생성합니다... 완료\n')


    print('DATA.CVM 파일을 생성하는 중입니다...\r')
    cvm_header = open(repack_folder_name + data_name[len(data_name) - 1], 'rb')
    repack_cvm.write(cvm_header.read())
    cvm_header.close()

    
    file_count = 0
    for i in range(len(data_type) - 1):
        if data_type[i] == 'Fold':
            this_folder_name = repack_folder_name + '/' + data_name[i] + '/'

        elif data_type[i] == 'File':
            file_count += 1
            print('                                        ', end='\r')  
            print(Fore.CYAN + data_name[i] + Fore.WHITE + ' (' + str(file_count) + '/' + str(len(only_data_name)) + ')', end='\r')
            temp_file = open(this_folder_name + data_name[i], 'rb')
            repack_cvm.write(temp_file.read())

            if not data_add_zero[i] == 0:
                for j in range(data_add_zero[i]):
                    repack_cvm.write(binascii.unhexlify('00'))
                    
            temp_file.close()

        elif data_type[i] == 'Root':
            file_count += 1
            print('                                        ', end='\r') 
            print(Fore.CYAN + data_name[i] + Fore.WHITE + ' (' + str(file_count) + '/' + str(len(only_data_name)) + ')', end='\r')
            this_folder_name = repack_folder_name
            temp_file = open(this_folder_name + data_name[i], 'rb')
            repack_cvm.write(temp_file.read())

            if not data_add_zero[i] == 0:
                for j in range(data_add_zero[i]):
                    repack_cvm.write(binascii.unhexlify('00'))
                    
            temp_file.close()
            
        else:
            temp_else = 0
            
    
    repack_cvm.close()

    repack_cvm = open('./DATA.CVM', 'r+b')
    repack_cvm_size = os.path.getsize('./DATA.CVM')
    repack_cvm_size_hex = str('0x' + '%.2x' % repack_cvm_size)[2:].zfill(8).upper()
    repack_cvm.seek(32)
    repack_cvm.write(binascii.unhexlify(repack_cvm_size_hex))
    repack_cvm.close()
    

    print('DATA.CVM 파일의 생성이 완료되었습니다.\n')
    time.sleep(1)
    
    return 0


#Detool.py -h2t ???.BIN(???.text)
def text_h2t(text_file):

    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    #table_j_folder = './Table(J)/'
    
    bin_file = open(input_folder + '/' + text_file, 'rb')

    export_folder = output_folder
    if not os.path.isdir(export_folder):
        os.mkdir(export_folder)


    #대사 개수 확인

    index_num2 = binascii.hexlify(bin_file.read(1)).decode('utf-8')
    index_num1 = binascii.hexlify(bin_file.read(1)).decode('utf-8')
    index_num = int(index_num1 + index_num2, 16) + 1 # 0~ N 까지이므로 +1

    


    pos_info = [] # 대사 시작위치  정보
    real_text_pos_info = [] # 중복대사 제거 시작위치 정보 
    text_num_info = [] # 대사번호 부여
    text_num = 0
    for i in range(index_num):

        temp_hex2 = binascii.hexlify(bin_file.read(1)).decode('utf-8')
        temp_hex1 = binascii.hexlify(bin_file.read(1)).decode('utf-8')
        temp_hex = int(temp_hex1 + temp_hex2, 16)

        pos_info.append(temp_hex)

        if i == 0:
            real_text_pos_info.append(pos_info[i])
            text_num_info.append(text_num)
            text_num += 1
            
        if i > 0:
            for j in range(i - 1):
                if pos_info[j] == temp_hex:
                    text_num_info.append(text_num_info[j])
                    break
            else:
                real_text_pos_info.append(pos_info[i])
                text_num_info.append(text_num)
                text_num += 1


    real_text_pos_info.append(os.path.getsize(input_folder + '/' + text_file))


     
    #대사 길이 확인
    text_size_info = []
    for i in range(len(real_text_pos_info) - 1):
        text_size_info.append(real_text_pos_info[i + 1] - real_text_pos_info[i])

   

    #대사 추출
    bin_text = codecs.open(export_folder + '/' + os.path.splitext(text_file)[0].upper() + '.txt', 'w', 'utf-16')
    
    m_dict = {}

    tbl_split = re.compile('(?P<code>.+)[=](?P<char>.+)[\r]')
    
    with codecs.open(table_j_folder + '/' + os.path.splitext(text_file)[0] + '.table', 'r', 'utf-16') as dict_file:
        for line in dict_file:
            m_dict[re.match(tbl_split, line).group('code')] = re.match(tbl_split, line).group('char')
   
    text_num = 0
    for i in range(len(pos_info)):
        if text_num == text_num_info[i]:
            bin_file.seek(real_text_pos_info[text_num])
            temp_text = ''
            
            text_size = 0
            while text_size < text_size_info[text_num]:
                temp_code = ''
                this_code = binascii.hexlify(bin_file.read(1)).decode('utf-8').upper()
                temp_code = this_code
                text_size += 1
                
                if this_code == '1A' or this_code == '1B' or this_code == '1C' or this_code == '1D':
                    that_code =  binascii.hexlify(bin_file.read(1)).decode('utf-8').upper()
                    temp_code = this_code + that_code
                    text_size += 1

                temp_text = temp_text + m_dict[temp_code]

            bin_text.write(temp_text + '\r\n')
            text_num += 1
                    
                
        else:
            bin_text.write('★' + str(text_num_info[i]).zfill(4) + '\r\n') #줄의 첫글자가 ★이면 뒤에 4자리 숫자는 대사번호가 가지는 포인터를 가짐

    bin_file.close()
    bin_text.close()
    


    return 0
    '''
    bin_file = open(input_folder + '/' + text_file, 'rb')

    export_folder = output_folder
    if not os.path.isdir(export_folder):
        os.mkdir(export_folder)

    
    bin_text = codecs.open(export_folder + '/' + os.path.splitext(text_file)[0].upper() + '.txt', 'w', 'utf-16')
    
    m_dict = {}

    tbl_split = re.compile('(?P<code>.+)[=](?P<char>.+)[\r]')
    
    with codecs.open(table_j_folder + '/' + os.path.splitext(text_file)[0] + '.table', 'r', 'utf-16') as dict_file:
        for line in dict_file:
            m_dict[re.match(tbl_split, line).group('code')] = re.match(tbl_split, line).group('char')


    temp_point = ''
    for i in range(2):
        bin_file.seek(1 - i)
        temp_point = temp_point +  binascii.hexlify(bin_file.read(1)).decode('utf-8')
        

    p_num = int(temp_point, 16) + 1

    p_off = []
    for i in range(p_num):
        t_p = ''
        for j in range(2):
            bin_file.seek(2 * i + 3 - j)
            t_p = t_p +  binascii.hexlify(bin_file.read(1)).decode('utf-8')
            
        p_off.append(int(t_p, 16))

    split_codes = []
    
    for i in range(len(p_off)):
        temp_codes = ''
        bin_file.seek(p_off[i])
        
        loop_out = 0
        while loop_out == 0:
            this_code =  binascii.hexlify(bin_file.read(1)).decode('utf-8').upper()
            temp_codes = temp_codes + this_code

            if this_code == '00':
                split_codes.append(temp_codes)
                loop_out = 1

                    
            if this_code == '1A' or this_code == '1B' or this_code == '1C' or this_code == '1D':
                that_code =  binascii.hexlify(bin_file.read(1)).decode('utf-8').upper()
                temp_codes = temp_codes + that_code

             
    conv_text = []
    for i in range(len(split_codes)):
        split_counter = 0
        stop_counter = 0
        while stop_counter == 0:
            temp_char1 = split_codes[i][2 * split_counter : 2 * (split_counter + 1)].upper()

            if temp_char1 == '1A' or temp_char1 == '1B' or temp_char1 == '1C' or temp_char1 == '1D':
                split_counter += 1
                temp_char2 = split_codes[i][2 * split_counter : 2 * (split_counter + 1)].upper()
                bin_text.write(m_dict[temp_char1 + temp_char2])
            else:
                bin_text.write(m_dict[temp_char1])

            if split_counter == (len(split_codes[i]) / 2) - 1:
                stop_counter = 1
            split_counter += 1
            
        bin_text.write('\r\n')

    '''
    




    
#Detool.py -t2h ???.txt
def text_t2h(t_file):

    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    #table_k_folder = './Table(k)/'
 

    text_file = codecs.open(input_folder + '/' + t_file, 'r', 'utf-16')

    export_folder = output_folder
    if not os.path.isdir(export_folder):
        os.mkdir(export_folder)

    if t_file[:2] == 'ST':
        bin_file = open(export_folder + '/' + os.path.splitext(t_file)[0].upper() + '.text', 'wb')
    else:
        bin_file = open(export_folder + '/' + os.path.splitext(t_file)[0].upper() + '.BIN', 'wb')

    m_dict = {}

    tbl_split = re.compile('(?P<code>.+)[=](?P<char>.+)[\r]')
    
    with codecs.open(table_k_folder + '/' + os.path.splitext(t_file)[0] + '.table', 'r', 'utf-16') as dict_file:
        for line in dict_file:
            m_dict[re.match(tbl_split, line).group('char')] = re.match(tbl_split, line).group('code')


    #test_file=codecs.open(export_folder + './aaaa.txt','w','utf-16')
    #test_file.write(str(m_dict))
    #test_file.close()

    #0x0 - 0x1 = pointer //  = p_num = text_num - 1

    text_num = len(text_file.readlines())
    temp_text_num_hex = str('0x' + '%.2x' % (text_num - 1))[2:].zfill(4)
    text_num_hex = temp_text_num_hex[2:4] + temp_text_num_hex[0:2]

    #text_line = text(n) + \r\n(2)
    text_file.seek(0)
    line_string_num = []
    line_num = [] #대사번호
    line_count = 0
    for i in range(text_num):
        temp_readline = text_file.readline()
        if temp_readline[0] == '★':
            line_string_num.append(0)
            line_num.append(int(temp_readline[1:5]))

        else:
            line_string_num.append(len(temp_readline) - 2)
            line_num.append(line_count)
            line_count += 1
                    


    #text_change
    text_file.seek(0)
    text_to_hex = []
    text_len = []
    for i in range(text_num):
        this_text = text_file.readline()
        c2h = ''
        total_count = 0

        if this_text[0] == '★':
            continue

        while not total_count == line_string_num[i]:
            this_char = this_text[total_count]
            total_count += 1
            
            if this_char == '{':
                count_off = 0
                while count_off == 0:
                    temp_char = this_text[total_count]
                    this_char = this_char + temp_char
                    total_count += 1
                    if temp_char == '}':
                        count_off = 1

            c2h = c2h + m_dict[this_char]
        text_to_hex.append(c2h)
        text_len.append(int(len(c2h) / 2))

    new_line_string_num = []
    for i in range(len(line_string_num)):
        if not line_string_num[i] == 0:
            new_line_string_num.append(line_string_num[i])

    #text_hader_make

    text_header = []
    text_header.append(text_num_hex)

    first_pos = 2 + 2 * text_num
    
    text_pos = []
    temp_pos = 0

    
    
    line_count = 0
    for i in range(len(line_num)):
        if not i == 0:
            if line_num[i] == line_count:
                temp_pos = temp_pos + text_len[line_count - 1]
                temp_hex = str('0x' + '%.2x' % temp_pos)[2:].zfill(4)
                text_header.append(temp_hex[2:4] + temp_hex[0:2])
                line_count += 1
            else:
                text_header.append(text_header[line_num[i] + 1])
            
        else:
            temp_pos = first_pos
            temp_hex = str('0x' + '%.2x' % temp_pos)[2:].zfill(4)
            text_header.append(temp_hex[2:4] + temp_hex[0:2])
            line_count += 1

        
    for i in range(len(text_header)):
        bin_file.write(binascii.unhexlify(text_header[i]))
    for i in range(len(text_to_hex)):
        bin_file.write(binascii.unhexlify(text_to_hex[i]))

    
    return 0


#Detool.py -up ST_???.PAC
def unpack_pac(pac):

    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    
    
    pac_file = open(input_folder + '/' + pac, 'rb')
    pac_size = os.path.getsize(input_folder + '/' + pac)

    unpack_folder_name = output_folder + '/UnpackPACs/' + os.path.splitext(pac)[0].upper()
    if not os.path.isdir(unpack_folder_name):
        os.mkdir(unpack_folder_name)


    #le pointer 17 // if not data no.xx = pointer is 00 00 00 00
    pac_point = []
    for i in range(17):
        temp_pos = ''
        for j in range(4):
            temp_pos = temp_pos + binascii.hexlify(pac_file.read(1)).decode('utf-8').upper()
        re_pos = temp_pos[6:8] + temp_pos[4:6] + temp_pos[2:4] + temp_pos[0:2]
        pac_point.append(int(re_pos, 16))

    re_pac_point = []
    real_split_num = []
    for i in range(17):
        if not pac_point[i] == 0:
            re_pac_point.append(pac_point[i])
            real_split_num.append(i + 1)
    re_pac_point.append(pac_size + 1)



    #Split File Info
    
    #01 - 
    #02 - 
    #03 - 
    #04 - 
    #05 - Image(?) (GBA 8bpp) 
    #06 - ???
    #07 - Image(?) (GBA 4bpp)
    #08 - ???
    #09 - Image(?) (GBA 8bpp) 
    #10 - Image (24Bit RGB)
    #11 - Text
    #12 - Font (Chinese)
    #13 -
    #14 -
    #15 -
    #16 -
    #17 -
    
    for i in range(len(real_split_num)):
        temp_pac = open(unpack_folder_name + '/' + os.path.splitext(pac)[0].upper() + '.' + str(real_split_num[i]).zfill(2), 'wb')
        pac_file.seek(re_pac_point[i])

        temp_pac.write(pac_file.read(re_pac_point[i + 1] - re_pac_point[i]))
        temp_pac.close()

    return 0

            
#Detool.py -uptf ST_???.PAC
def unpack_pac_only_tf(pac):

    #input_folder = './[Input]/'
    #output_folder = './[Result]/'

  
    pac_file = open(input_folder + '/' + pac, 'rb')
    pac_size = os.path.getsize(input_folder + '/' + pac)

    unpack_folder_name = output_folder + '/UnpackPACs/'
    if not os.path.isdir(unpack_folder_name):
        os.mkdir(unpack_folder_name)

       
    pac_point = []
    for i in range(17):
        temp_pos = ''
        for j in range(4):
            temp_pos = temp_pos + binascii.hexlify(pac_file.read(1)).decode('utf-8').upper()
        re_pos = temp_pos[6:8] + temp_pos[4:6] + temp_pos[2:4] + temp_pos[0:2]
        pac_point.append(int(re_pos, 16))

    re_pac_point = []
    real_split_num = []
    for i in range(17):
        if not pac_point[i] == 0:
            re_pac_point.append(pac_point[i])
            real_split_num.append(i + 1)
    re_pac_point.append(pac_size + 1)


    for i in range(len(real_split_num)):

        if real_split_num[i] == 11:
            temp_pac = open(unpack_folder_name + '/' + pac[:-3].upper() + 'text', 'wb')
            pac_file.seek(re_pac_point[i])

            temp_pac.write(pac_file.read(re_pac_point[i + 1] - re_pac_point[i]))
            temp_pac.close()

        if real_split_num[i] == 12:
            temp_pac = open(unpack_folder_name + '/' + pac[:-3].upper() + 'font', 'wb')
            pac_file.seek(re_pac_point[i])

            temp_pac.write(pac_file.read(re_pac_point[i + 1] - re_pac_point[i]))
            temp_pac.close()

    return 0


#Detool.py -rptf
def repack_pac_only_tf():

    os.system('cls')

    print('\nPAC 리팩 작업 시작합니다.\n\n')
    print('기본정보 수집중...', end='\r')

    

    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    #info_folder = './Info/'

    info_split = re.compile('(?P<type>.+)[;](?P<name>.+)')

    
    data_name = []
    data_dir = []

    pac_info = open(info_folder + '/' + 'PAC_Info.bin', 'r')

    with pac_info as info:
        for line in info:
            
            if re.match(info_split, line).group('type') == 'Fold':
                main_dir = './Data/UnpackCVM/' + re.match(info_split, line).group('name') + '/'
                
            else:
                
                sub_dir = re.match(info_split, line).group('name')                
                data_dir.append(main_dir + sub_dir)                
                data_name.append(sub_dir[:-3])


    new_data_name = []
    new_data_dir = []
    for i in range(len(data_name)):
        if os.path.isfile(input_folder + '/' + data_name[i] + 'text') and os.path.isfile(input_folder + '/' + data_name[i] + 'font'):
            new_data_name.append(data_name[i])
            new_data_dir.append(data_dir[i])

    print('기본정보 수집중... 완료\n')


    print('PAC파일 리팩 시작...\r')
    for i in range(len(new_data_name)):
        print('                              ', end='\r')
        print(Fore.CYAN + new_data_name[i][:-1] + Fore.WHITE + ' (' + str(i + 1) + '/' + str(len(new_data_name)) +')', end='\r')
        
        pac_file = open(new_data_dir[i], 'rb')
        pac_file_text = open(input_folder + '/' + new_data_name[i] + 'text', 'rb')
        pac_file_font = open(input_folder + '/' + new_data_name[i] + 'font', 'rb')
        pac_size = os.path.getsize(new_data_dir[i])
        pac_text_size = os.path.getsize(input_folder + '/' + new_data_name[i] + 'text')
        pac_font_size = os.path.getsize(input_folder + '/' + new_data_name[i] + 'font')                              

    
        pac_point = []
        for j in range(17):
            temp_pos = ''
            for k in range(4):
                temp_pos = temp_pos + binascii.hexlify(pac_file.read(1)).decode('utf-8').upper()
            re_pos = temp_pos[6:8] + temp_pos[4:6] + temp_pos[2:4] + temp_pos[0:2]
            pac_point.append(int(re_pos, 16))

        re_pac_point = []
        real_split_num = []
        for j in range(17):
            if not pac_point[j] == 0:
                re_pac_point.append(pac_point[j])
                real_split_num.append(j + 1)
        re_pac_point.append(pac_size + 1)



        #pac read index 1 ~ 10
        pac_file.seek(0)
    
        temp_pac_data1 = pac_file.read(pac_point[10])

        temp_pac_data2_size = 0
        for j in range(len(real_split_num)):
            if real_split_num[j] == 12:
                pac_file.seek(re_pac_point[j + 1])
                break
               
        temp_pac_data2 = pac_file.read()
        pac_file.close()
        

        new_pac_file = open(new_data_dir[i], 'wb')
        new_pac_file.write(temp_pac_data1)
      
    
        new_pac_file.write(pac_file_text.read())

        text_add_zero = 16 - pac_text_size % 16
        if text_add_zero == 16:
            text_add_zero = 0
        for j in range(text_add_zero):
            new_pac_file.write(binascii.unhexlify('00'))

        pac_text_size += text_add_zero

    
        new_pac_file.write(pac_file_font.read())
        new_pac_file.write(temp_pac_data2)
        new_pac_file.close()

        new_pac_file = open(new_data_dir[i], 'r+b')


        re_pac_size = []
        new_pac_point = re_pac_point
        for j in range(len(re_pac_point) - 1):
            re_pac_size.append(re_pac_point[j + 1] - re_pac_point[j])


        for j in range(len(real_split_num)):
        
            if real_split_num[j] == 11:
                new_text_size = pac_text_size - re_pac_size[j]
            
        
            if real_split_num[j] == 12:
                new_font_size = pac_font_size - re_pac_size[j]
                new_pac_point[j] += new_text_size


            if real_split_num[j] > 12:
                if not re_pac_point[j] == 0:
                    new_pac_point[j] += (new_text_size + new_font_size)

        
        for j in range(len(real_split_num)):
            if real_split_num[j] > 11:
                if not re_pac_point[j] == 0:
                    new_pac_file.seek(real_split_num[j] * 4 - 4)
                    temp_new_pos = str('0x' + '%.2x' % new_pac_point[j])[2:].zfill(8)
                    new_pos = temp_new_pos[6:8] + temp_new_pos[4:6] + temp_new_pos[2:4] + temp_new_pos[0:2]
                    new_pac_file.write(binascii.unhexlify(new_pos))
        new_pac_file.close()

    print('모든 파일의 리팩이 완료되었습니다.\n')
    time.sleep(1)

    return 0


#DeTool.py -c ???.txt 1/0 (1 = base_chars will del)
def check_used_chars(text_file, del_num):

    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    #info_folder = './Info/'
    #font_folder = './Font/'
                    

    text_ori = codecs.open(input_folder + '/' + text_file, 'r', 'utf-16')
    data = text_ori.read().replace('\r','').replace('\n','').replace('★','')

    #if not os.path.isdir(output_folder):
        #os.mkdir(output_folder)

    

    result = codecs.open(output_folder + '/' + text_file[:-3].upper() + 'chars', 'w', 'utf-16')
    
    m_dict = []
    tbl_split = re.compile('(?P<code>.+)[=](?P<char>.+)[\r]')
    with codecs.open(font_folder + '/' + 'Base_Chars.bin', 'r', 'utf-16') as dict_file:
        for line in dict_file:
            m_dict.append(re.match(tbl_split, line).group('char'))

    
    if os.path.isfile(input_folder + '/' + 'MSG_BASE.chars.bin'):       
        temp_file = codecs.open(input_folder + '/' + 'MSG_BASE.chars.bin', 'r', 'utf-16')
        base_char_data = temp_file.readline().replace('\r','').replace('\n','').replace('★','')
        for i in range(len(base_char_data)):
            data = data.replace(base_char_data[i],'')
            if i > 160: #i가 161일때 => 162번째 글자부터
                result.write(base_char_data[i])
    
    if del_num == '1':
        for i in range(len(m_dict)):
            data = data.replace(m_dict[i],'')
   

    temp_result = []
    count_end = 0
    while count_end == 0:
        if not len(data) == 0: 
            temp_result.append(data[0])
            data = data.replace(data[0],'')

        if len(data) == 0:
            count_end = 1

    temp_result.sort()
    result.write(''.join(temp_result) + '\r\n')
    result.write(str(len(''.join(temp_result))))
    if del_num == '1':
        result.write('\r\n(Base Chars Was Deleted!!!)')
    result.close()

    return 0


#DeTool.py -mt ???.chars 1/0 (1 = big, 0 = small)
def making_table(check_char_file, font_type):

    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    #info_folder = './Info/'
    #font_folder = './Font/'
    #table_m_folder = './Table(m)/'



    temp_kana_char_file = codecs.open(input_folder + '/' + 'MSG_BASE.chars', 'r', 'utf-16')
    kana_data = temp_kana_char_file.readline().replace('\r','').replace('\n','')
    
    kana_table = codecs.open(table_m_folder + '/' + 'BASE_Kana.table', 'r', 'utf-16' )
    
    make_kana_table_file = codecs.open(input_folder + '/' + 'BASE_Kana.table', 'w', 'utf-16' )
    
     
    for i in range(min(161, len(kana_data))):
        make_kana_table_file.write(kana_table.readline().replace('\r','').replace('\n','') + kana_data[i] + '\r\n')
    make_kana_table_file.close()
    kana_table.close()

    

    temp_char_file = codecs.open(input_folder + '/' + check_char_file, 'r', 'utf-16')
    char_data = temp_char_file.readline().replace('\r','').replace('\n','')

    if font_type == '1':
        base_table = codecs.open(table_m_folder + '/' + 'SUB_Base.table', 'r', 'utf-16' )
        sub_table = codecs.open(table_m_folder + '/' + 'SUB_Sub.table', 'r', 'utf-16' )
    else :
        base_table = codecs.open(table_m_folder + '/' + 'PAC_Base.table', 'r', 'utf-16' )
        sub_table = codecs.open(table_m_folder + '/' + 'PAC_Sub.table', 'r', 'utf-16' )



        

    #if not os.path.isdir(output_folder):
        #os.mkdir(output_folder)

    make_table_file = codecs.open(output_folder + '/' + check_char_file[:-5].upper() + 'table', 'w', 'utf-16' )
    
    make_table_file.write(base_table.read())
    
    make_kana_table_file = codecs.open(input_folder + '/' + 'BASE_Kana.table', 'r', 'utf-16' )
    make_table_file.write(make_kana_table_file.read())
    make_kana_table_file.close()
    
    for i in range(len(char_data)):
        make_table_file.write(sub_table.readline().replace('\r','').replace('\n','') + char_data[i] + '\r\n')

    make_table_file.close()
    

    return 0


#DeTool.py -mf ???.chars 1/0 (1 = big, 0 = small, 2 = kana 3= Big + Layer1 0x00 = 01)
def making_font(check_used_chars_file, font_type):

    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    #info_folder = './Info/'
    #font_folder = './Font/'

    char_file = codecs.open(input_folder + '/' + check_used_chars_file, 'r', 'utf-16')
    char_data = char_file.readline().replace('\r','').replace('\n','')
    if check_used_chars_file == 'MSG_BASE.chars':
        if len(char_data) > 161:
            char_data = char_data[:161]
    char_file.close()

    
    kor_chars_file = codecs.open(font_folder + '/' + 'Kor_2350_Chars.bin', 'r', 'utf-16')
    kor_chars = kor_chars_file.readline().replace('\r','').replace('\n','')
    kor_chars_file.close()
    
    kor_chars_dict = {}
    for i in range(len(kor_chars)):
        kor_chars_dict[kor_chars[i]] = i
        
    

    kor_chars_font = open(font_folder + '/' + 'Base_Kor_Font.bin', 'rb')

    if font_type == '1' or font_type == '3':
        base_font = open(font_folder + '/' + 'Big_Font.bin', 'rb')
    elif font_type == '0':
        base_font = open(font_folder + '/' + 'Small_Font.bin', 'rb')
    else:
        base_font = open(font_folder + '/' + 'Small_Kana_Font.bin', 'rb')

    
        


    #if not os.path.isdir(output_folder):
        #os.mkdir(output_folder)


    if check_used_chars_file[:2].upper() == 'ST':
        make_font = open(output_folder + '/' + check_used_chars_file[:-5].upper() + 'font', 'wb')
    else:
        make_font = open(output_folder + '/' + check_used_chars_file[:-5].upper() + 'TEX', 'wb')

    make_font.write(base_font.read())

    if check_used_chars_file == 'ST_085.chars':
        add_font = open(font_folder + '/' + 'Small_085_Font_Add.bin', 'rb')
        make_font.write(add_font.read())
        add_font.close()
    
    base_font.close()
    make_font.close()
    

    if check_used_chars_file[:2].upper() == 'ST':
        make_font = open(output_folder + '/' + check_used_chars_file[:-5].upper() + 'font', 'r+b')
    else:
        make_font = open(output_folder + '/' + check_used_chars_file[:-5].upper() + 'TEX', 'r+b')
    

    char_num = []
    for i in range(len(char_data)):
        char_num.append(kor_chars_dict[char_data[i]])
    

    if font_type == '1' or font_type == '3':
        font_header = 48
        chars_per_row = 32
        column_byte = 4096
        next_shift = 256
    else:
        font_header = 32
        chars_per_row = 16
        column_byte = 2048
        next_shift = 128

    skip_char = 0
    for i in range(len(char_data)):

        if i == 89:
            skip_char += 3
        if i == 89 + 37:
            skip_char += 5
        if i == 89 + 37 + 272:
            skip_char += 1
        if i == 89 + 37 + 272 + 12:
            skip_char += 1
        if i == 89 + 37 + 272 + 12 + 6:
            skip_char += 1
        if i == 89 + 37 + 272 + 12 + 6 + 2:
            skip_char += 1
        if i == 89 + 37 + 272 + 12 + 6 + 2 + 31:
            skip_char += 1
        if i == 89 + 37 + 272 + 12 + 6 + 2 + 31 + 50:
            font_header = 1072
        if i == 89 + 37 + 272 + 12 + 6 + 2 + 31 + 50 + 66:
            skip_char += 3


        #시작pos = 48 + (N // 32)*4096 + {(N % 32)-1}*8
        #file.seek(시작pos + 256*i)
    
        #시작pos = 32 + (N // 16)*2048 + {(N % 16)-1}*8
        #file.seek(시작pos + 128*i)
        
        
        if font_type == '0' or font_type == '1' or font_type == '3':
            write_pos = font_header + ((i + skip_char) // chars_per_row) * column_byte + ((i + skip_char) % chars_per_row) * 8
        else:
            write_pos = font_header + ((i + 91) // chars_per_row) * column_byte + ((i + 91) % chars_per_row) * 8

        
        
        make_font.seek(write_pos)
        kor_chars_font.seek(128 * char_num[i])
        
        for j in range(16):
            
            make_font.write(kor_chars_font.read(8))
            make_font.seek(write_pos + (next_shift * j))

    if font_type == '3':
        make_font.seek(0)
        make_font.write(binascii.unhexlify('01'))
        
    make_font.close()
    kor_chars_font.close()
            

    return 0


#DeTool.py -co
def chars_overview():

    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    #info_folder = './Info/'
    #font_folder = './Font/'

    
    #if not os.path.isdir(output_folder):
        #os.mkdir(output_folder)
        
                    

    file_list = []
    chars_num = []
    with codecs.open(info_folder + '/' + 'Chars_Overview.bin', 'r', 'utf-16') as info:
        for line in info:
            file_list.append(line.replace('\r','').replace('\n',''))
            
            if os.path.isfile(input_folder + '/' + line.replace('\r','').replace('\n','')):
                temp_open = codecs.open(input_folder + '/' + line.replace('\r','').replace('\n',''), 'r', 'utf-16')
                chars_num.append(len(temp_open.readline().replace('\r','').replace('\n','')))
                temp_open.close()
            else:
                chars_num.append('None')

    

    
    base_char_file = codecs.open(input_folder + '/' + 'MSG_BASE.chars', 'r', 'utf-16')
    base_char_num = len(base_char_file.readline().replace('\r','').replace('\n',''))
    first_base_char_num = base_char_num
    if base_char_num > 161:        
        base_char_num = base_char_num - 161
    else:
        base_char_num = 0
    base_char_file.close()
    

    check_possiblilty = []
    check_max = []
    for i in range(len(file_list)):
        if file_list[i] == 'MSG_SUB.chars':
            possiblilty_num = 752
        elif file_list[i] == 'MSG_BASE.chars':
            possiblilty_num = 161
        else:
            possiblilty_num = 248
            
        check_max.append(possiblilty_num)
        
        if not chars_num[i] == 'None':
            if chars_num[i] < possiblilty_num:
                check_possiblilty.append('OK')
            else:
                check_possiblilty.append('Bad')                    
                   
        else:
            check_possiblilty.append('')

    info_file = codecs.open(output_folder + '/' + '[Chars_Overview].txt', 'w', 'utf-16')
    info_file.write('<Chars Files Overview>\r\n\r\n[Chars];[MAX];[Num];[Possibility]\r\n')
    none_file_info = '\r\n-------------------------------\r\n\r\n<None Chars Files>\r\n\r\n'
    for i in range(len(file_list)):

        if file_list[i][:-6] == 'MSG_BASE':
            info_file.write(file_list[i][:-6] + ' : 총' + str(first_base_char_num) + '자로, ' + str(base_char_num) + '자 만큼 다른폰트에 사용해야함' + '\r\n')

        elif file_list[i][:-6] == 'MSG_SUB':
            info_file.write(file_list[i][:-6] + ';' + str(check_max[i]) + ';' + str(chars_num[i]) + ';' + check_possiblilty[i] + '\r\n')   
            
        elif not chars_num[i] == 'None':
            info_file.write(file_list[i][:-6] + ';' + str(check_max[i]) + ';' + str(chars_num[i]) + ';' + check_possiblilty[i] + '\r\n')            
        
        else:
            none_file_info += file_list[i][:-6] + '\r\n'
            
    info_file.write(none_file_info)
       
    info_file.close()
          

    return 0


#DeTool.py -mcd
def making_chars_db():
    
    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    #info_folder = './Info/'
    chars_db_name = 'Chars_DB.bin'

    #if not os.path.isdir(output_folder):
        #os.mkdir(output_folder)

    chars_db = codecs.open(output_folder + '/' + chars_db_name, 'w', 'utf-16')
                    
 
    with codecs.open(info_folder + '/' + 'Chars_Overview.bin', 'r', 'utf-16') as info:
        for line in info:           
            if os.path.isfile(input_folder + '/' + line.replace('\r','').replace('\n','')):
                temp_open = codecs.open(input_folder + '/' + line.replace('\r','').replace('\n',''), 'r', 'utf-16')
                chars_db.write(temp_open.readline().replace('\r','').replace('\n','') + '\r\n')
                temp_open.close()

    chars_db.close()


#DeTool.py -mp
def making_patch():

    #patch_ext = 'dsfp'
    
    #input_folder = './[Input]/'
    #output_folder = './[Result]/'
    #info_folder = './Info/'
    #font_folder = './Font/'

    patch_name = 'DementoHan' + time.strftime('%y%m%d') + '.' + patch_ext
    patch_add_list = 'Patch_Add_List.bin'

    #if not os.path.isdir(output_folder):
        #os.mkdir(output_folder)

    



    #chars_db.bin글자정보  + st_000.text&msg_base.bin 대사
    #Font폴더 // Base_Kor_Font.bin + Big_Font.bin + Kor_2350_Chars.bin + Small_085_Font_Add.bin + Small_Font.bin + (Small_Kana_Font.bin)
    #Info폴더 // Chars_Overview.bin + CVM_Info.bin + PAC_Info.bin

    #순서 : info font chars_db 텍스트

    file_name = []
    file_size = []
    

    info_fold = ['Chars_Overview.bin', 'CVM_Info.bin', 'PAC_Info.bin', 'Patch_Add_List.bin']
    for i in range(len(info_fold)):
        file_name.append(info_fold[i])
        file_size.append(os.path.getsize(info_folder + '/' + info_fold[i]))
        
    
    font_fold = ['Base_Kor_Font.bin', 'Big_Font.bin', 'Kor_2350_Chars.bin', 'Small_085_Font_Add.bin', 'Small_Font.bin', 'Small_Kana_Font.bin']
    for i in range(len(font_fold)):
        file_name.append(font_fold[i])
        file_size.append(os.path.getsize(font_folder + '/' + font_fold[i]))
        
   
    with codecs.open(info_folder + '/' + patch_add_list, 'r', 'utf-16') as info:
        for line in info:           
            if os.path.isfile(input_folder + '/' + line.replace('\r','').replace('\n','')):
                file_name.append(line.replace('\r','').replace('\n',''))
                file_size.append(os.path.getsize(input_folder + '/' + line.replace('\r','').replace('\n','')))


    data_add_zero = []
    for i in range(len(file_size)):
        data_add_zero.append(16 - file_size[i] % 16)
        

    #[헤더생성] 
    #확인문자 00버전 제작일자 파일크기
    #길이(1) + 제목(UTF-16 길이는 HEX길이로) + 길이(1) + 기종 00(add 16) + 길이(2) + 패치제작자

    check_str = patch_ext.upper().encode('ascii')
    check_ver = binascii.unhexlify(str('0x'+'%.2x'% patch_ver)[2:].zfill(8))
    cheack_date = binascii.unhexlify(str('0x'+'%.2x'% int(time.strftime('%y%m%d')))[2:].zfill(8))
    check_file_size_temp = binascii.unhexlify('00000000')
    
    program_title_hex = program_title.encode('utf-16')[2:]
    program_title_hex_len = binascii.unhexlify(str('0x'+'%.2x'% len(program_title_hex))[2:].zfill(2))
    console_type_hex = console_type.encode('ascii')
    console_type_hex_len = binascii.unhexlify(str('0x'+'%.2x'% len(console_type_hex))[2:].zfill(2))
    patch_maker_hex = patch_maker.encode('utf-16')[2:]
    patch_maker_hex_len = binascii.unhexlify(str('0x'+'%.2x'% len(patch_maker_hex))[2:].zfill(4))
    head_add_zero1 = 16 - (4 + 4 + 4 + 4 + 1 + len(program_title_hex) + 1 + len(console_type_hex) + 2 + len(patch_maker_hex)) % 16



    #파일개수(2)
    file_num = binascii.unhexlify(str('0x'+'%.2x'% len(file_name))[2:].zfill(4))
    file_num_add_zero = 16 - len(file_num) % 16
    
    #개수당 정보길이(1)
    #포인터(4)
    #파일크기(4)
    #파일명(N)
    #addzero

    

    file_name_hex = []
    file_size_hex = []
    info_per_num = []
    info_per_num_hex = []
    head_add_zero2 = []
    for i in range(len(file_name)):
        file_name_hex.append(file_name[i].encode('ascii'))
        file_size_hex.append(binascii.unhexlify(str('0x'+'%.2x'% file_size[i])[2:].zfill(8)))       
        info_per_num.append(4 + 4 + len(file_name_hex[i]))
        info_per_num_hex.append(binascii.unhexlify(str('0x'+'%.2x'% info_per_num[i])[2:].zfill(2)))
        head_add_zero2.append(16 - (1 + 4 + 4 + len(file_name_hex[i])) % 16)



    # 파일 데이터 // 헤더길이(고정) + 데이터 + data_add_zero 
    data_pos = []

    header_total_size = 4 + 4 + 4 + 4 + 1 + len(program_title_hex) + 1 + len(console_type_hex) + 2 + len(patch_maker_hex) + head_add_zero1 + 2 + file_num_add_zero
    for i in range(len(file_name)):
        header_total_size += 1 + 4 + 4 + len(file_name_hex[i]) + head_add_zero2[i]
    
    only_herder_size = header_total_size

    for i in range(len(file_name)):
        if not i == 0:
            header_total_size += file_size[i - 1] + data_add_zero[i - 1]
        data_pos.append(binascii.unhexlify(str('0x'+'%.2x'% header_total_size)[2:].zfill(8)))





    #패치 쓰기
    patch_file = open(patch_folder + '/' + patch_name, 'wb')

    patch_file.write(check_str + check_ver + cheack_date + check_file_size_temp + program_title_hex_len + program_title_hex + console_type_hex_len + console_type_hex + patch_maker_hex_len + patch_maker_hex)

    if head_add_zero1 > 0:
        for i in range(head_add_zero1):
            patch_file.write(binascii.unhexlify('00'))
    
    patch_file.write(file_num)
    if file_num_add_zero > 0:
        for i in range(file_num_add_zero):
            patch_file.write(binascii.unhexlify('00'))
    
    for i in range(len(file_name)):
        patch_file.write(info_per_num_hex[i] + data_pos[i] + file_size_hex[i] + file_name_hex[i])
        if head_add_zero2[i] > 0:
            for j in range(head_add_zero2[i]):
                patch_file.write(binascii.unhexlify('00'))



    for i in range(len(file_name)):
        if i < len(info_fold):
            temp_file = open(info_folder + '/' + file_name[i], 'rb')
        elif i > len(info_fold) - 1 and i < len(info_fold) + len(font_fold):
            temp_file = open(font_folder + '/' + file_name[i], 'rb')
        else:
            temp_file = open(input_folder + '/' + file_name[i], 'rb')
            
        patch_file.write(temp_file.read())
        temp_file.close()
        if data_add_zero[i] > 0:
            for j in range(data_add_zero[i]):
                patch_file.write(binascii.unhexlify('00'))
      
    
    patch_file.close()

    #magic_code
    if use_magic_code == 1:
        patch_file = open(patch_folder + '/' + patch_name, 'r+b')

        temp_code = [i for i in range(256)]
        random.shuffle(temp_code)
    
        magic_code = {}
        for i in range(256):
            magic_code[i] = temp_code[i]

    
        patch_file = open(patch_folder + '/' + patch_name, 'r+b')
        patch_file.seek(16)


        for i in range(os.path.getsize(patch_folder + '/' + patch_name) - 16):
            split_data_read = int(binascii.hexlify(patch_file.read(1)).decode('utf-8').upper(),16)

            patch_file.seek(-1, 1)
            new_num = split_data_read + magic_code[patch_file.tell() % 256]
            if new_num > 255:
                new_num = new_num - 256
       
            patch_file.write(binascii.unhexlify(str('0x'+'%.2x'% new_num)[2:].zfill(2)))
   

        for i in range(256):
            patch_file.write(binascii.unhexlify(str('0x'+'%.2x'% magic_code[i])[2:].zfill(2)))
    
        patch_file.close()
    
    patch_file = open(patch_folder + '/' + patch_name, 'r+b')
    patch_file.seek(12)
    patch_file_size = binascii.unhexlify(str('0x'+'%.2x'% os.path.getsize(patch_folder + '/' + patch_name))[2:].zfill(8))
    patch_file.write(patch_file_size)
    patch_file.close()    

    #readme.txt 추가
    if os.path.isfile(input_folder + '/' + '[readme].txt'):
        patch_file = open(patch_folder + '/' + patch_name, 'ab')
        readme_file = open(input_folder + '/' + '[readme].txt', 'rb')
        patch_file.write(readme_file.read())
        patch_file.close()
        readme_file.close()
        
    return 0


def main_title():

    os.system('cls')
    
    print('\n')
    
    print(Back.BLUE + Fore.WHITE + '┌────────────────┐\r')
    print(Back.BLUE + Fore.WHITE + '│                                │\r')
    print(Back.BLUE + Fore.WHITE + '│[PS2] Demento 한글 패쳐 Ver1.0  │\r')
    print(Back.BLUE + Fore.WHITE + '│                                │\r')
    print(Back.BLUE + Fore.WHITE + '│                    2000.00.00  │\r')
    print(Back.BLUE + Fore.WHITE + '│                                │\r')
    print(Back.BLUE + Fore.WHITE + '└────────────────┘')

    print('\r')
    print(Fore.CYAN + '총괄 : D.S.Ford | 번역 : 팀 한글날')


def warning_word():

    main_title()
    
    print('\n■ 주의 사항\r')
    print('   본 패쳐와 패치의 상업적인 이용을 금합니다.\r')
    print('   본 패쳐와 패치는 한식구에서만 배포를 허용합니다.\r')
    print('   패치를 적용한 파일 등의 공유를 금합니다.\n')
    check_agree = input('   위 사항에 동의하십니까? (Yes/No) : ')

    if not (check_agree.upper() == 'Y' or check_agree.upper() == 'YES'):
        sys.exit()




def help_screen():

    os.system('cls')

    print('\n<< 도움말 >>\n')

    print(' 본 패쳐는 Demento의 파일 중 '+ Fore.GREEN + 'DATA.CVM 파일만 패치'+ Fore.WHITE + '하는 프로그램입니다.\r')
    print('이후 과정은 '+ Fore.YELLOW + '[3] 이후 과정 도움말'+ Fore.WHITE + ' 항목을 참고하시기 바랍니다.\n\n')

    print('■ 필요한 것\r')
    print('  Demento DVD 이미지 파일(이하 ISO)\r')
    print('  Demento 한글 패치 파일\r')
    print('  WinRAR\n')

    print('■ 패치 전 준비\r')
    print('  1. ISO파일을 열어 '+ Fore.GREEN + 'DATA.CVM'+ Fore.WHITE + ' 파일을 '+ Fore.YELLOW + 'Data'+ Fore.WHITE + ' 폴더에 풀어줍니다.\r')
    print('  2. 패치 파일은 '+ Fore.YELLOW + 'Patch'+ Fore.WHITE + ' 폴더에 넣어줍니다.\n\n')

    input('  다음 화면으로 넘기시려면 Enter키를 눌러 주세요.')
    os.system('cls')
    
    
    print('\n<< 메인 화면 설명 >>\n')
    print('  ' + Fore.CYAN + '[1] 도움말\r')
    print('   : 도움말을 확인합니다.\n')
    print('  ' + Fore.CYAN + '[2] 패치 작업\r')
    print('   : 작업과정 중 DATA.CVM 파일을 풀어주는 과정이 있습니다.\r')
    print('     패치 완료 이후 생성된 폴더나 파일 등을 건들지 않았다면\r')
    print('     이후 패치가 업데이트 되었을 땐 '+ Fore.CYAN + '파일 추출 생략'+ Fore.WHITE + '으로 진행하시면 됩니다.\n')
    
    print('  ' + Fore.CYAN + '[3] 이후 과정 도움말\r')
    print('  : 패치된 DATA.CVM 파일을 포함, ISO 리빌드 과정에 대한 설명입니다.\r')
    print('    이 작업은 '+ Fore.RED + '패쳐로 할 수 없는 작업'+ Fore.WHITE + '이니 직접 해주셔야 합니다.\n')
    
    print('  ' + Fore.CYAN + '[4] 패치 정보\r')
    print('  : 패치 파일의 정보를 확인합니다.\n')
    
    print('  ' + Fore.CYAN + '[5] 작업 종료\r')
    print('  : 프로그램을 종료합니다.\n\n')
    
    input('  메인 화면으로 돌아갑니다. Enter키를 눌러 주세요.')

    #main_title()
    load_work_case_word()  


def after_work_screen():

    os.system('cls')

    print('\n<< 이후 과정 도움말 >>\n')

    print('■ 필요한 것\r')
    print('  Demento DVD 이미지 파일(이하 ISO)\r')
    print('  WinRAR (http://www.rarlab.com/download.htm)\r')
    print('  Xpert v2.0 (http://xpert2.blogspot.com)\r')
    print('  패치한 DATA.CVM 파일\n\n')

    print('[1] WinRAR 다운로드 페이지로 이동\n')
    print('[2] Xpert v2.0 다운로드 페이지로 이동 (FIREDROP)\n')
    print('[3] 다음 화면으로 이동\n')
    print('[4] 메인 화면으로 이동\n')

    while 1:
        check_work_num = input('원하는 항목의 번호를 입력하시고 Enter키를 눌러 주세요 : ')
        
        if check_work_num == '1':
            webbrowser.open("http://www.rarlab.com/download.htm")

        elif check_work_num == '2':
            webbrowser.open("https://firedrop.com/95fb260de283d6e9")
                        
        elif check_work_num == '3':

            os.system('cls')
            
            print('\n<< ISO 리빌드 작업 >>\n')

            print('* 6번 이후 과정 중에 아이콘이 안 눌러지면 Xpert를 재실행 하고,\r')
            print('  3번까지 진행 후 해당 과정을 계속 진행하시면 됩니다.\r')
            print('* 6~7번의 과정은 ' + Fore.MAGENTA + '더미파일'+ Fore.WHITE + '을 지우는 과정이니 생략 가능합니다.\r')
            print('* Xpert에서 불러오는 ISO는 무조건 ' + Fore.RED + '원본'+ Fore.WHITE + '입니다.\n')
           
            print('1. Xpert를 실행합니다.\r')
            print('2. Xpert-Plugins에서 ' + Fore.GREEN + 'PS2 CdDvd5 |PSP UMD ISO Shrinker v1.04 *.ISO'+ Fore.WHITE + '를 선택합니다.\r')
            print('3. 폴더 아이콘(B 써있는 폴더 아이콘)를 누르고 ' + Fore.RED + '원본 ISO'+ Fore.WHITE + '를 선택합니다.\n')
            
            print('4. 좌측 상단 첫번째 아이콘(' + Fore.CYAN + '1. Extract LBA'+ Fore.WHITE + ')을 누릅니다.\r')
            #print('5. 좌측 상단 두번째 아이콘(' + Fore.CYAN + '2. Extract File'+ Fore.WHITE + ')을 누른다.\n')
            print('5. WinRAR로 ISO를 같은 폴더 안에 ' + Fore.YELLOW + '@파일명.ISO'+ Fore.WHITE + ' 폴더를 만들어 풀어줍니다.\r')
            print('   ex) ' + Fore.CYAN + 'AAA.ISO'+ Fore.WHITE + '이면 ' + Fore.YELLOW + '@AAA.ISO' + Fore.WHITE + '폴더에 풀어줍니다.\n')

            print('6. Tool - Relinker 누른 후, Open버튼을 누르고 ' + Fore.GREEN + '파일명.ISO-LSN.TXT'+ Fore.WHITE + '를 선택합니다.\r')
            print('7. Load버튼을 누른 아래 파일 목록 중 ' + Fore.MAGENTA + '00DUMMY, 01DUMMY, 02DUMMY'+ Fore.WHITE + '항목에 체크,\r')
            print('   우클릭 - ' + Fore.GREEN + 'Replace Selected File(s) With Dummy'+ Fore.WHITE + '를 누르고 EXIT버튼을 누릅니다.\n')

            print('8. ' + Fore.RED + '패치한 DATA.CVM'+ Fore.WHITE + ' 파일을 ' + Fore.YELLOW + '@파일명'+ Fore.WHITE + ' 폴더에 덮어 씌웁니다.\r')
            print('9. 좌측 상단 세번째 아이콘(' + Fore.CYAN + '3. Rebuild File'+ Fore.WHITE + ')을 누릅니다.\r')
            print('10. 좌측 상단 네번째 아이콘(' + Fore.CYAN + '4. Rebuild LBA'+ Fore.WHITE + ')을 누릅니다.\n')

            input('  메인 화면으로 돌아갑니다. Enter키를 눌러 주세요.')
            
            break
            
        elif check_work_num == '4':
            break 
            
        else:
            print('\n번호를 잘못 입력하셨습니다!!!')
            
    #main_title()
    load_work_case_word()      


def check_patch():

    #patch_folder = './Patch/'
    #patch_ext = 'dsfp'
    
    os.system('cls')

    print('\n<< 패치 파일 확인 >>\n\n')

    
    file_list = []
    for file in glob.glob(patch_folder + '/' + '*.' + patch_ext):
        file_list.append(file[8:])

        
    if len(file_list) == 0:
        print('패치 파일이 없습니다. 다시 확인해 주세요.\n')
        time.sleep(1)
        load_work_case_word()
        

    elif len(file_list) > 1:
        while 1:
            os.system('cls')

            print('\n<< 패치 파일 확인 >>\n')
            print('\n' + str(len(file_list)) + '개의 패치 파일이 존재 합니다.\n')
            for i in range(len(file_list)):
                print('[' + str(i + 1) + '] ' + file_list[i])
            print('\n')


            patch_file_num = input('사용할 패치 파일의 번호를 입력해 주세요 : ')

            count_num = 0
            for i in range(len(file_list)):
                if str(i + 1) == patch_file_num:
                    count_num += 1

            if count_num == 1:
                patch_file_name = file_list[int(patch_file_num) - 1]
                break
            else:
                os.system('cls')
                print('\n잘못 입력하셨습니다. 다시 입력해 주세요.\n')
                time.sleep(0.5)
                       
    else:
        patch_file_name = file_list[0]


    if not len(file_list) == 0:
        print(Fore.CYAN + patch_file_name + Fore.WHITE + ' 파일을 선택합니다.\n\n1초 후 다음 화면으로 넘어갑니다.\n')
        time.sleep(1)
        os.system('cls')  
        return patch_file_name
        

    else:
        patch_file_name = ''
        os.system('cls')  
        return patch_file_name



def get_magic_code(patch_file_name):

    #patch_folder = './Patch/'

    patch_file = open(patch_folder + '/' + patch_file_name, 'rb')

    patch_file.seek(12)
    patch_size = int(binascii.hexlify(patch_file.read(4)).decode('utf-8').upper(),16)
    

    patch_file.seek(patch_size - 256)
    magic_code = {}
    for i in range(256):
        magic_code[i] = int(binascii.hexlify(patch_file.read(1)).decode('utf-8').upper(),16)

    return magic_code
    

def extract_patch_file(patch_file_name):

    #patch_folder = './Patch/'
    
    patch_file = open(patch_folder + '/' + patch_file_name, 'rb')
    if not os.path.isdir(patch_folder + '/' + 'temp'):
        os.mkdir(patch_folder + '/' + 'temp')

    #매직코드
    if use_magic_code == 1:
        new_patch_file = open(patch_folder + '/temp/' + 'temp.bin', 'wb')

        magic_code = get_magic_code(patch_file_name)


        patch_file.seek(0)
        
        new_patch_file.write(patch_file.read(12))
        patch_size_only = patch_file.read(4)
        patch_size_only_conv = int(binascii.hexlify(patch_size_only).decode('utf-8').upper(),16)
        new_patch_file.write(patch_size_only)
        #new_patch_file.write(patch_file.read(16))

        patch_file.seek(16)
    
        for i in range(patch_size_only_conv - 16 - 256):
            split_data_read = int(binascii.hexlify(patch_file.read(1)).decode('utf-8').upper(),16)

            patch_file.seek(-1, 1)
            new_num = split_data_read - magic_code[patch_file.tell() % 256]
            if new_num < 0:
                new_num = new_num + 256        
            new_patch_file.write(binascii.unhexlify(str('0x'+'%.2x'% new_num)[2:].zfill(2)))        
            patch_file.seek(1, 1)

        patch_file.close()
        new_patch_file.close()

        new_patch_file = open(patch_folder + '/temp/' + 'temp.bin', 'rb')
    else:
        patch_file.close()
        new_patch_file = open(patch_folder + '/' + patch_file_name, 'rb')
        

    new_patch_file.seek(16)
    
    program_title_len = int(binascii.hexlify(new_patch_file.read(1)).decode('utf-8').upper(),16)
    new_patch_file.read(program_title_len)
    console_type_len = int(binascii.hexlify(new_patch_file.read(1)).decode('utf-8').upper(),16)
    new_patch_file.read(console_type_len)
    patch_maker_len = int(binascii.hexlify(new_patch_file.read(2)).decode('utf-8').upper(),16)
    new_patch_file.read(patch_maker_len)
    new_patch_file.read(16 - new_patch_file.tell() % 16)

    file_num = int(binascii.hexlify(new_patch_file.read(2)).decode('utf-8').upper(),16)
    new_patch_file.read(14)
   
    
    file_name = []
    file_size = []
    data_pos = []
    for i in range(file_num):
        info_per_num = int(binascii.hexlify(new_patch_file.read(1)).decode('utf-8').upper(),16)
        data_pos.append(int(binascii.hexlify(new_patch_file.read(4)).decode('utf-8').upper(),16))
        file_size.append(int(binascii.hexlify(new_patch_file.read(4)).decode('utf-8').upper(),16))
        file_name.append(new_patch_file.read(info_per_num - 4 - 4).decode('ascii'))
        new_patch_file.read(16 - new_patch_file.tell() % 16)



    for i in range(file_num):
        temp_file = open(patch_folder + '/' + 'temp' + '/' + file_name[i], 'wb')
        new_patch_file.seek(data_pos[i])
        temp_file.write(new_patch_file.read(file_size[i]))
        temp_file.close()

    
    new_patch_file.close()
       

    

def patch_prog():

    patch_file_name = check_patch()

    if not patch_file_name == '':
        while 1:
            print('\n<< 패치 방식 선택 >>\n\n')
            print('[1] 전체 과정\n')
            print('[2] 파일 추출 생략\n')
            print('[3] 메인 화면으로 이동\n')

        
            check_work_num = input('원하는 항목의 번호를 입력하시고 Enter키를 눌러 주세요 : ')
        
            if check_work_num == '1' or check_work_num == '2':

                print('\n패치 파일을 분석중입니다. 잠시만 기다려 주세요.\n')

                extract_patch_file(patch_file_name) #추출작업
                
                if check_work_num == '1':
                    unpack_to_cvm() #패치파일 해제

                os.system('cls')

                print('\n폰트 파일 생성을 시작합니다.\n\n')

                
                print('기본정보 수집중...', end='\r')
                chars_file_name = []
                with codecs.open(input_folder + '/' + 'Chars_Overview.bin', 'r', 'utf-16') as info:
                    for line in info:
                        chars_file_name.append(line.replace('\r','').replace('\n',''))
                        
                chars_db = []
                with codecs.open(input_folder + '/' + 'Chars_DB.bin', 'r', 'utf-16') as info:
                    for line in info:
                        chars_db.append(line.replace('\r','').replace('\n',''))

                for i in range(len(chars_db)):
                    temp_open = codecs.open(output_folder + '/' + chars_file_name[i], 'w', 'utf-16')
                    temp_open.write(chars_db[i] + '\r\n')
                    temp_open.close()
                    
                print('기본정보 수집중... 완료\n')

                print('폰트 생성 시작... \r')
                
                for i in range(len(chars_file_name)):
                    print('                              ', end='\r')
                    print(Fore.CYAN + chars_file_name[i][:-6] + Fore.WHITE + ' (' + str(i + 1) + '/' + str(len(chars_file_name)) + ')', end='\r')

                    
                    if chars_file_name[i][:2].upper() == 'ST':
                        font_type = '0'
                    if chars_file_name[i] == 'MSG_BASE.chars':
                        font_type = '2'
                    if chars_file_name[i] == 'MSG_END.chars':
                        font_type = '0'
                    if chars_file_name[i] == 'MSG_SUB.chars':
                        font_type = '1'
                    
                    making_font(chars_file_name[i], font_type) #폰트 생성

                print('폰트 생성이 완료되었습니다.\n')
                time.sleep(1)

        
                repack_pac_only_tf() #PAC 리팩
                
                os.system('cls')

                
                print('\n기타 파일 복사를 시작합니다.\n\n')

                target_file = ['MSG_BASE.BIN', 'MSG_BASE.TEX', 'MSG_END.BIN', 'MSG_END.TEX', 'MSG_SUB.BIN', 'MSG_SUB.TEX']
                target_folder = cvm_folder + '/UnpackCVM/SUBSCR/'

                for i in range(len(target_file)): #기본 파일 복붙
                    print('                              ', end='\r')
                    print(Fore.CYAN + target_file[i] + Fore.WHITE + ' (' + str(i + 1) + '/' + str(len(target_file)) + ')', end='\r')
                    temp_file_open = open(target_folder + target_file[i], 'wb')
                    new_file_open = open(input_folder + target_file[i], 'rb')
                    temp_file_open.write(new_file_open.read())
                    temp_file_open.close()
                    new_file_open.close()

                print('모든 파일의 복사가 완료되었습니다.\n')

                time.sleep(1)                
                
                repack_to_folder()

                shutil.rmtree(input_folder, ignore_errors=True) #temp폴더 제거

                time.sleep(1)

                
                
                load_work_case_word()
                


            elif check_work_num == '3':
                break
            
            else:
                time.sleep(0.5)
                print('\n잘못 입력하셨습니다. 다시 입력해 주세요.')
                                        
            
    

def patch_file_info():

    #patch_folder = './Patch/'
    #output_folder = './Patch/temp/'

    patch_file_name = check_patch()

    patch_file = open(patch_folder + '/' + patch_file_name, 'rb')
    
    patch_file.seek(12)
    patch_size = int(binascii.hexlify(patch_file.read(4)).decode('utf-8').upper(),16)
    
    if not os.path.getsize(patch_folder + '/' + patch_file_name) == patch_size:
        patch_file.seek(patch_size)
        readme_file = open(patch_folder + '/' + patch_file_name[:-5] + '_Readme.txt', 'wb')
        readme_file.write(patch_file.read())
        patch_file.close()
        readme_file.close()

        os.system('notepad.exe ' + patch_folder + '/' + patch_file_name[:-5] + '_Readme.txt')
        load_work_case_word()
        
    else:
        print("\n이 패치 파일에는 패치 정보가 없습니다.\n\n메인 화면으로 돌아갑니다.\n")
        time.sleep(1)

        load_work_case_word()

      


def open_console_mode():
    
    os.system('cls')
    
    print(Back.BLUE + Fore.WHITE + '┌───────────┐\r')
    print(Back.BLUE + Fore.WHITE + '│                      │\r')
    print(Back.BLUE + Fore.WHITE + '│C O N S O L   M O D E │\r')
    print(Back.BLUE + Fore.WHITE + '│                      │\r')
    print(Back.BLUE + Fore.WHITE + '└───────────┘')

    print('\n')

    print('[1] aaa\n')
    print('[2] aaa\n')
    print('[3] aaa\n')
    print('[4] aaa\n')
    print('[5] aaa\n')


    while 1:
        check_work_num = input('원하는 항목의 번호를 입력하시고 Enter키를 눌러 주세요 : ')
        
        if check_work_num == '1': 
            pass
                        
        elif check_work_num == '2': #패치
            pass
            
        elif check_work_num == '3': #이후 과정
            pass
            

        elif check_work_num == '4': #패치 정보
            pass
                        
        elif check_work_num == '5': 
            pass

        else:
            print('\n번호를 잘못 입력하셨습니다!!!')
    



def load_work_case_word():

    main_title()

    print('\n')

    print('[1] 도움말 (반드시 먼저 읽어 주세요)\n')
    print('[2] 패치 작업\n')
    print('[3] 이후 과정 도움말 (직접 하셔야 할 작업)\n')
    print('[4] 패치 정보\n')
    print('[5] 작업 종료\n')
    
    print('\n')
    
    while 1:
        check_work_num = input('원하는 항목의 번호를 입력하시고 Enter키를 눌러 주세요 : ')
        
        if check_work_num == '1': #도움말
            help_screen()
                        
        elif check_work_num == '2': #패치
            patch_prog()
            
        elif check_work_num == '3': #이후 과정
            after_work_screen()
            

        elif check_work_num == '4': #패치 정보
            patch_file_info()
                        
        elif check_work_num == '5': 
            os.system('cls')
            sys.exit()

        elif check_work_num.upper() == 'CONSOLE': #콘솔모드
            
            os.system('cls')
            print('\n콘솔 모드로 전환합니다.')
            time.sleep(1)
            open_console_mode()
            
        else:
            #os.system('cls')
            print('\n번호를 잘못 입력하셨습니다!!!')
            time.sleep(1)
            
        break










def main():

    if len(sys.argv) > 1:
        if sys.argv[1] == '-t':
            export_cvm_info()
            
    
        elif sys.argv[1] == '-u':
            unpack_to_cvm()

        elif sys.argv[1] == '-r':
            repack_to_folder()

        elif sys.argv[1] == '-h2t':
            text_h2t(sys.argv[2])

        elif sys.argv[1] == '-t2h':
            text_t2h(sys.argv[2])

        elif sys.argv[1] == '-up':
            unpack_pac(sys.argv[2])

        elif sys.argv[1] == '-uptf':
            unpack_pac_only_tf(sys.argv[2])

        elif sys.argv[1] == '-rptf':
            repack_pac_only_tf()

        elif sys.argv[1] == '-c':
            check_used_chars(sys.argv[2], sys.argv[3])

        elif sys.argv[1] == '-mt':
            making_table(sys.argv[2], sys.argv[3])

        elif sys.argv[1] == '-mf':
            making_font(sys.argv[2], sys.argv[3])

        elif sys.argv[1] == '-co':
            chars_overview()
            
        elif sys.argv[1] == '-mcd':
            making_chars_db()
            
        elif sys.argv[1] == '-mp':
            making_patch()

        elif sys.argv[1] == '-fi':
            patch_file_info()


    if len(sys.argv) > 1:
        sys.exit()
    

    warning_word()

    while 1:
        load_work_case_word()
    

    

            

    

   

if __name__ == '__main__':
    sys.exit(main())
    
