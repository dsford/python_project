PATH %SystemRoot%\system32\

SET ProgName=DePatcher.py 
SET Option1=-c
SET Option2=1
SET CurrentPath=%CD%
SET InputFolder=^[Input^]
SET Extension=txt
SET Get_List=TXT_List.tmp

CD %InputFolder%
FOR /f %%a in ('DIR *.%Extension% /b')  DO ECHO %%a >> %Get_List%
MOVE %Get_List% %CurrentPath%
CD..

FOR /f  %%b in ('type %Get_List%') do (
	 %ProgName% %Option1%  %%b %Option2%)

DEL %Get_List%