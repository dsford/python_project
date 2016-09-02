PATH %SystemRoot%\system32\

SET ProgName=DePatcher.py 
SET Option=-t2h
SET CurrentPath=%CD%
SET InputFolder=^[Input^]
SET Extension=txt
SET Get_List=TXT_List.tmp

CD %InputFolder%
FOR /f %%a in ('DIR *.%Extension% /b')  DO ECHO %%a >> %Get_List%
MOVE %Get_List% %CurrentPath%
CD..

FOR /f  %%b in ('type %Get_List%') do (
	 %ProgName% %Option% %%b)

DEL %Get_List%