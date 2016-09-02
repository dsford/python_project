PATH %SystemRoot%\system32\

SET ProgName=DePatcher.py 
SET Option=-uptf
SET CurrentPath=%CD%
SET InputFolder=^[Input^]
SET Extension=PAC
SET Get_List=PAC_List.tmp

CD %InputFolder%
FOR /f %%a in ('DIR *.%Extension% /b')  DO ECHO %%a >> %Get_List%
MOVE %Get_List% %CurrentPath%
CD..

FOR /f  %%b in ('type %Get_List%') do (
	 %ProgName% %Option% %%b)

DEL %Get_List%