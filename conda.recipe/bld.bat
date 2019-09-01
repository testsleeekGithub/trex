python setup.py install
if errorlevel 1 exit 1

set MENU_DIR=%PREFIX%\Menu
IF NOT EXIST (%MENU_DIR%) mkdir %MENU_DIR%

copy %SRC_DIR%\img_src\trex.ico %MENU_DIR%\
if errorlevel 1 exit 1
copy %SRC_DIR%\img_src\trex_reset.ico %MENU_DIR%\
if errorlevel 1 exit 1
copy %RECIPE_DIR%\menu-windows.json %MENU_DIR%\trex_shortcut.json
if errorlevel 1 exit 1

del %SCRIPTS%\trex_win_post_install.py
del %SCRIPTS%\trex.bat
