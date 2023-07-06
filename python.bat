
@echo off
REM This is the one to use on the box
C:\Program Files\Thermo-Calc\2021a\python\python.exe "%~1" %*

REM This is the one to use to test on your local machine...in cmd prompt type "where python" to find the path to your python.exe
REM "C:\Users\live\AppData\Local\Programs\Python\Python39\python.exe" "%~1" %*

pause
