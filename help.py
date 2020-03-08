import sys
#from sys import exit

prompt = """Python Help Browser (ctrl-c o ctrl-d para salir)
---------------------------------------------------
Ingrese tema: """

while True:
	try:
	   a = raw_input(prompt)
	   help(a)
        except (KeyboardInterrupt, EOFError):
           sys.exit()

