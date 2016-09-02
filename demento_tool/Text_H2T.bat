PATH %SystemRoot%\system32\

SET ProgName=DePatcher.py 
SET Option=-h2t
SET CurrentPath=%CD%
SET InputFolder=^[Input^]
SET Extension1=BIN
SET Extension2=text
SET Get_List=Text_List.tmp

CD %InputFolder%
FOR /f %%a in ('DIR *.%Extension1% *.%Extension2% /b')  DO ECHO %%a >> %Get_List%
MOVE %Get_List% %CurrentPath%
CD..

FOR /f  %%b in ('type %Get_List%') do (
	 %ProgName% %Option% %%b)

DEL %Get_List%