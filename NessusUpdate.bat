@echo off &Title Nessus Update 

:Menu
CLS
echo.
echo ============================
echo +       Nessus Update      +
echo +                          +
echo +    1  全部更新           +
echo +    2  更新插件           +
echo +    3  使用代理           +
echo +    4  关闭代理           +
echo +    0  退出               +
echo ============================

set /p choose=请输入编号：

if "%choose%"=="1" GOTO UpdateAll
if "%choose%"=="2" GOTO UpdatePlugins
if "%choose%"=="3" GOTO StartProxy
if "%choose%"=="4" GOTO CloseProxy
if "%choose%"=="0" GOTO Close

:UpdateAll
"C:\Program Files\Tenable\Nessus\nessuscli.exe" update --all
pause
goto Menu

:UpdatePlugins
"C:\Program Files\Tenable\Nessus\nessuscli.exe" update --plugins-only
pause
goto Menu

:StartProxy
netsh winhttp set proxy proxy-server="socks=localhost:1080" bypass-list="localhost"
pause
goto Menu

:CloseProxy
netsh winhttp reset proxy
pause
goto Menu

:Close
pause
exit