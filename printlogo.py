from sys import argv
from random import randint

logostr = """██████╗███╗  ██╗ █████╗██████╗██╗   ██╗██████╗██████████████╗  █████╗ ███╗  ██╗
██╔═══╝████╗ ██║██╔═══╝██╔══██╚██╗ ██╔╝██╔══██╚══██╔══██╔══██╗██╔══██╗████╗ ██║
████╗  ██╔██╗██║██║    ██████╔╝╚████╔╝ ██████╔╝  ██║  ██████╔╝██║  ██║██╔██╗██║
██╔═╝  ██║╚████║██║    ██╔══██╗ ╚██╔╝  ██╔═══╝   ██║  ██╔══██╗██║  ██║██║╚████║
██████╗██║ ╚███║╚█████╗██║  ██║  ██║   ██║       ██║  ██║  ██║╚█████╔╝██║ ╚███║
╚═════╝╚═╝  ╚══╝ ╚════╝╚═╝  ╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚══╝"""

ansi = lambda *args : "\u001b[" + ";".join([str(i) for i in args]) + "m"

argv.pop(0)
cs = 0
if argv:
    try:
        cs = int(argv[0])
    except IndexError:
        cs = ranint(1, 6)
else:
    cs = randint(1, 6)

lines = logostr.split('\n')
assert len(lines) == 6
clr = 16 + 6*(cs-1)
for line in lines:
    print(ansi(38,5,clr),end='')
    clr += 1
    for _ in range(5):
        substr, line = (line[:13], line[13:]) # 80/6 = 13 R 2
        print(substr + ansi(38, 5, clr),end='')
        clr += 1
    print(line+ansi(0)) # with newline at the end
    clr += 30  # 36 - 6
