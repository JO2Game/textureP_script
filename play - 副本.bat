rem @echo off
set tPath="D:/Program Files/CodeAndWeb/TexturePacker/bin/TexturePacker.exe"
set oPath="E:/of_proj/StarCraft_plan/Image/starCraftUI"

set a1=%1
if "%a1%"=="" (
	python tp_script.pyc -tp=%tPath% -op=%oPath% -isDir="False"
)else if "%a1%"=="-h" (
	python tp_script.pyc -tp=%tPath%
)

