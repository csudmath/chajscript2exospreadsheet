EXCEL = /cygdrive/c/Program\ Files/Microsoft\ Office/root/Office16/EXCEL.EXE

compile: exolist.py
		python exolist.py

view: compile
	$(EXCEL) output.xlsx &
