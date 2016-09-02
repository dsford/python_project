#-*- coding: utf-8 -*-

# 숫자를 엑셀 열번호로 변경 (1 = A // ... // 26 = Z // 27 = AA // ...)
# openpyxl 등의 엑셀관련 모듈에서 사용하기 위해 작성


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
 

         
#테스트
print(num2col(27))

