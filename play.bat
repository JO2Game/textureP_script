rem @echo off
COLOR 06
python tp_script.pyc -isClear="True"

set DIR=%~dp0

set tPath="D:/Program Files/CodeAndWeb/TexturePacker/bin/TexturePacker.exe"

set replacePath=%DIR%../"Resources/Image/"

rem 注意目录最后不要加斜杠
set oPath=%DIR%../"Resources/Image/baseui/starCraftUI"
python tp_script.pyc -tp=%tPath% -op=%oPath% -replacePath=%replacePath% -isDir="True" -isAnySize="False"

set oPath=%DIR%../"Resources/Image/baseui/starCraftUIEX"
python tp_script.pyc -tp=%tPath% -op=%oPath% -replacePath=%replacePath% -isDir="True" -isAnySize="True"

set oPath=%DIR%../"Resources/Image/hd"
python tp_script.pyc -tp=%tPath% -op=%oPath% -replacePath=%replacePath% -isDir="True" -isAnySize="False"
set oPath=%DIR%../"Resources/Image/ld"
python tp_script.pyc -tp=%tPath% -op=%oPath% -replacePath=%replacePath% -isDir="True" -isAnySize="False"


set oPath=%DIR%../"Resources/Image/download/download_atlas"
python tp_script.pyc -tp=%tPath% -op=%oPath% -replacePath=%replacePath% -isDir="True" -isAnySize="False"
set oPath=%DIR%../"Resources/Image/download/download_atlasEX"
python tp_script.pyc -tp=%tPath% -op=%oPath% -replacePath=%replacePath% -isDir="True" -isAnySize="True"

rem copy

xcopy "%DIR%../Resources/Image/baseui/starCraftView" "%DIR%ExportDir/baseui/starCraftView\" /e
xcopy "%DIR%../Resources/Image/download/download_single" "%DIR%ExportDir/download/download_single\" /e

pause