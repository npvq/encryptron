# Specific Terminal for Encryptron

# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html (doesn't work, breaks terminal)
import os
from sys import stdout
from time import sleep
from random import randint
clipboard_import = True
try:
    import pyperclip
except ModuleNotFoundError:
    clipboard_import = False

import encryptron.codec as cdc


ansi = lambda *args : "\u001b[" + ";".join([str(i) for i in args]) + "m"
script_dir = os.path.dirname(os.path.abspath(__file__))

_ascii_escape = {'n': '\n', 'r': '\r', 't': '\t', 'b': '\b', 'f': '\f',
                 'v': '\v', '0': '\0'}
def parse_cmd(line):
    line = list(line)
    cmd = ['']
    in_quotes = False
    while len(line):
        char = line.pop(0)
        if char == "\\":
            if len(line):
                p = line.pop(0)
                cmd[-1] += _ascii_escape.get(p, p) # adds next character, no questions asked
            else:
                # usually trailing "\" block newlines. But we cannot have multi-line expressions
                pass
            continue
        if char == '\"':
            in_quotes = not in_quotes
            continue
        if char == " " and not in_quotes:
            if len(cmd[-1]):
                cmd.append('')
            continue
        cmd[-1] += char
    if not len(cmd[-1]):
        cmd.pop()
    return cmd


cmd_history = []
HISTORY_MAX_SIZE = 1000
HISTORY_QUEUE_SIZE = 20
def _check_nonzero(lst):
    for i in lst:
        if i:
            return True
    return False

def highlight(search, text):
    mark = [ansi(47), ansi(103)] # off, on
    map = [0]*(len(text)+1)
    for term in search:
        i = text.find(term)
        while i != -1:
            for j in range(len(term)):
                map[i+j] = 1
            i = text.find(term, i+len(term))
    outstr = ""
    for i in range(len(text)):
        outstr += text[i]
        if map[i] != map[i+1]:
            outstr += mark[map[i+1]]
    return (_check_nonzero(map), ansi(30,(103 if map[0] else 47))+outstr)

def search_history(*args):
    if not args:
        n = max(len(cmd_history)-HISTORY_QUEUE_SIZE+1, 1)
        for tup in cmd_history[-HISTORY_QUEUE_SIZE:]:
            m = str(n)
            m += (4-len(m))*' '
            print(m+" "+ansi(30,47)+tup[1]+ansi(0))
            n += 1
    else:
        for n in range(len(cmd_history)):
            b, t = highlight(args, cmd_history[n][1])
            if b:
                m = str(n+1)
                m += (4-len(m))*' '
                print(m+" "+t+ansi(0))



def cmd_not_found(*args):
    print("That command does not exist! Please type 'help <cmd>' or 'tutorial' for help")


def exit_term(*args, ctrl_c=False):
    if ctrl_c:
        print("")
    stdout.write("Exiting the Terminal")
    sleep(0.1)
    for i in range(2):
        stdout.flush()
        stdout.write('.')
        sleep(0.2)
    stdout.flush()
    stdout.write('.\n')
    return True

# def suspend_term(*args):
#     os.system("bg "+os.environ["ENCTERM_ID"])

clipboard_mode = False
def copy(*args):
    global clipboard_mode
    if args:
        if args[0].casefold() in ['0', 'false', 'off']:
            clipboard_mode = False
        elif args[0].casefold() in ['1', 'true', 'on']:
            if not clipboard_import:
                print(ansi(93)+"copy: Cannot set Clipboard Mode to True because the `pyperclip` package has not been installed."+ansi(0))
                return
            clipboard_mode = True
        else:
            print(ansi(31)+"copy: Invalid Input"+ansi(0))
            return
        # print("Clipboard Mode set to {}".format(ansi(1,(92 if clipboard_mode else 31))+str(clipboard_mode)+ansi(0)))
        print("Clipboard Mode turned {}".format( (ansi(1,92)+"On" if clipboard_mode else ansi(1,31)+"Off") + ansi(0) ))
    else:
        print("Clipboard Mode: {}".format( (ansi(1,92)+"On" if clipboard_mode else ansi(1,31)+"Off") + ansi(0) ) )

help_pages = {}
def _help_doc_parse(docs):
    lines = []
    for line in docs.strip().split('\n'):
        if line.startswith("~>"):
            line = ansi(7) + line[2:] + ansi(0)
        lines.append(line)
    return '\n'.join(lines)

def initialize_help():
    with open(script_dir+"/terminal_help", 'r') as e:
        page = e.read()
        for section in page.split("%%%%%%%%%%")[:-1]:
            tag, docs = section.strip().split('\n',1)
            docs = _help_doc_parse(docs)
            for entry in tag.strip().split(','):
                help_pages[entry] = docs

def help(*args):
    if not args:
        print("help: Please enter a command to search. Try 'help list' or 'tutorial'.")
        return
    cmd = args[0]
    if cmd not in help_pages.keys():
        print("help: The help page for the command {} was not found. Try 'help list' or 'tutorial'.".format(cmd))
    print(help_pages[cmd], end="\n\n")


def tutorial(*args):
    # os.system('clear||cls') # clears screen: unix/windows
    os.system(f'less "{os.path.dirname(os.path.abspath(__file__))}/terminal_tutorial"')


def check_key(*args):
    if args:
        key = args[0]
        perm = cdc.key_to_perm(key)
        print("Checking key \"{}\"...\nThe key permutation is {}".format(ansi(4)+key+ansi(0), perm))
        if perm == "0123456789abcdef":
            print("check-key: "+ansi(3,93)+"Warning: This key is defective"+ansi(0))
        if clipboard_mode and len(args) > 1 and args[-1] == "cc":
            pyperclip.copy(perm)
            print("Copied to Clipboard!")
    elif clipboard_mode:
        key = pyperclip.paste()
        if key:
            perm = cdc.key_to_perm(key)
            print("Checking key \"{}\"...\nThe key permutation is {}".format(ansi(4)+key+ansi(0), perm))
            if perm == "0123456789abcdef":
                print("check-key: "+ansi(3,93)+"Warning: This key is defective"+ansi(0))
            if len(args) > 1 and args[-1] == "cc":
                pyperclip.copy(perm)
                print("Copied to Clipboard!")
        else:
            print(ansi(31)+"check-key: No Key Entered."+ansi(0))
    else:
        print(ansi(31)+"check-key: No Key Entered."+ansi(0))
        return


def check_perm(*args):
    if args:
        perm = args[0]
        print("Checking permutation \"{}\"...\nThe key permutation is {}".format(perm, (ansi(1,4,92)+"Valid") if cdc.check_hex_perm(perm) else (ansi(1,4,31)+"Invalid")) + ansi(0))
    elif clipboard_mode:
        perm = pyperclip.paste()
        if perm:
            print("Checking permutation \"{}\"...\nThe key permutation is {}".format(perm, (ansi(1,4,92)+"Valid") if cdc.check_hex_perm(perm) else (ansi(1,4,31)+"Invalid")) + ansi(0))
        else:
            print(ansi(31)+"check-perm: No Permutation Entered."+ansi(0))
    else:
        print(ansi(31)+"check-perm: No Permutation Entered."+ansi(0))

def encode(*args):
    args = list(args)
    if not args:
        print(ansi(31)+"encode: Missing Key"+ansi(0))
        return
    key = args.pop(0)
    if key == 'wp':
        encode_wp(*args)
        return
    if len(key) == 1 and ord(key) % 17 == 0:
        key = None
        print(ansi(1,7)+"(NO KEY){} ".format(ansi(0)), end='')
    filter = ""
    if args and args[0].startswith("-f="):
        tmp = args.pop(0).split("=")[1].casefold()
        for k in cdc.num_gen_filters.keys():
            if k.startswith(tmp):
                filter = k
        if not filter:
            print(ansi(93)+"encode: No filter named \"{}\" was found, using default...".format(tmp)+ansi(0))
    copy_res = False
    if clipboard_mode and args and args[-1] == "cc":
        args.pop()
        copy_res = True
    if args:
        outstr = cdc.ws_encode(" ".join(args), filter=filter, key=key)
    elif clipboard_mode:
        c = pyperclip.paste()
        if not len(c):
            print(ansi(31)+"encode: Message from Clipboard is Empty"+ansi(0))
            return
        outstr = cdc.ws_encode(c, filter=filter, key=key)
    else:
        print(ansi(31)+"encode: Message Empty"+ansi(0))
        return
    print("Message Encoded:\n[START]"+ansi(7)+outstr+ansi(0)+"[STOP]")
    if copy_res:
        pyperclip.copy(outstr)
        print("Copied to Clipboard!")


def encode_wp(*args): # with permutation instead of key
    args = list(args)
    if not args:
        print(ansi(31)+"encode: Missing Permutation"+ansi(0))
        return
    perm = args.pop(0)
    if not cdc.check_hex_perm(perm):
        print(ansi(31)+"encode: Invalid Permutation (use check-perm to verify)"+ansi(0))
        return
    filter = ""
    if args and args[0].startswith("-f="):
        tmp = args.pop(0).split("=")[1]
        for k in cdc.num_gen_filters.keys():
            if k.startswith(tmp):
                filter = k
        if not filter:
            print(ansi(93)+"encode: No filter named \"{}\" was found, using default...".format(tmp)+ansi(0))
    copy_res = False
    if clipboard_mode and args and args[-1] == "cc":
        args.pop()
        copy_res = True
    if args:
        outstr = cdc.ws_encode(" ".join(args), filter=filter, perm=perm)
    elif clipboard_mode:
        c = pyperclip.paste()
        if not len(c):
            print(ansi(31)+"encode: Message from Clipboard is Empty"+ansi(0))
            return
        outstr = cdc.ws_encode(c, filter=filter, perm=perm)
    else:
        print(ansi(31)+"encode: Message Empty"+ansi(0))
        return
    print("Message Encoded:\n[START]"+ansi(7)+outstr+ansi(0)+"[STOP]")
    if copy_res:
        pyperclip.copy(outstr)
        print("Copied to Clipboard!")


def decode(*args):
    args = list(args)
    if not args:
        print(ansi(31)+"decode: Missing Key"+ansi(0))
        return
    key = args.pop(0)
    if key == 'wp':
        decode_wp(*args)
        return
    if len(key) == 1 and ord(key) % 17 == 0:
        key = None
        print(ansi(1,7)+"(NO KEY){} ".format(ansi(0)), end='')
    filter = ""
    if args and args[0].startswith("-f="):
        tmp = args.pop(0).split("=")[1]
        for k in cdc.num_gen_filters.keys():
            if k.startswith(tmp):
                filter = k
        if not filter:
            print(ansi(93)+"encode: No filter named \"{}\" was found, using default...".format(tmp)+ansi(0))
    copy_res = False
    if clipboard_mode and args and args[-1] == "cc":
        args.pop()
        copy_res = True
    if args:
        if len(args) > 1:
           print("decode: "+ansi(3,93)+"Only part of the string was recorded. Are you sure you used quotes around the crypt?"+ansi(0))
        outstr = cdc.ws_decode(args[0], filter=filter, key=key)
    elif clipboard_mode:
        c = pyperclip.paste()
        if not len(c):
            print(ansi(31)+"decode: Message from Clipboard is Empty"+ansi(0))
            return
        outstr = cdc.ws_decode(c, filter=filter, key=key)
    else:
        print(ansi(31)+"decode: Message Empty"+ansi(0))
        return
    print("Message Decoded:\n"+ansi(7)+outstr+ansi(0))
    if copy_res:
        pyperclip.copy(outstr)
        print("Copied to Clipboard!")


def decode_wp(*args):
    args = list(args)
    if not args:
        print(ansi(31)+"encode: Missing Permutation"+ansi(0))
        return
    perm = args.pop(0)
    if not cdc.check_hex_perm(perm):
        print(ansi(31)+"encode: Invalid Permutation (use check-perm to verify)"+ansi(0))
        return
    filter = ""
    if args and args[0].startswith("-f="):
        tmp = args.pop(0).split("=")[1]
        for k in cdc.num_gen_filters.keys():
            if k.startswith(tmp):
                filter = k
        if not filter:
            print(ansi(93)+"encode: No filter named \"{}\" was found, using default...".format(tmp)+ansi(0))
    copy_res = False
    if clipboard_mode and args and args[-1] == "cc":
        args.pop()
        copy_res = True
    if args:
        if len(args) > 1:
           print("decode: "+ansi(3,93)+"Only part of the string was recorded. Are you sure you used quotes around the crypt?"+ansi(0))
        outstr = cdc.ws_decode(args[0], filter=filter, perm=perm)
    elif clipboard_mode:
        c = pyperclip.paste()
        if not len(c):
            print(ansi(31)+"decode: Message from Clipboard is Empty"+ansi(0))
            return
        outstr = cdc.ws_decode(c, filter=filter, perm=perm)
    else:
        print(ansi(31)+"decode: Message Empty"+ansi(0))
        return
    print("Message Decoded:\n"+ansi(7)+outstr+ansi(0))
    if copy_res:
        pyperclip.copy(outstr)
        print("Copied to Clipboard!")

# These functions shoult not return anything, they should directly interact
# with CLI. And if they return 'True', the session ends.
cmd_table = {
    "tutorial": tutorial,
    "help": help,
    'd': decode,
    'e': encode,
    'x': exit_term,
    'exit': exit_term,
    'copy': copy,
    'ckey': check_key,
    'check-key': check_key,
    'p': check_perm,
    'check-perm': check_perm,
    # 'sus': suspend_term,
    'history': search_history
}

# Vanity

# https://stackoverflow.com/a/34325723/14387133
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

logostr = """██████╗███╗  ██╗ █████╗██████╗██╗   ██╗██████╗██████████████╗  █████╗ ███╗  ██╗
██╔═══╝████╗ ██║██╔═══╝██╔══██╚██╗ ██╔╝██╔══██╚══██╔══██╔══██╗██╔══██╗████╗ ██║
████╗  ██╔██╗██║██║    ██████╔╝╚████╔╝ ██████╔╝  ██║  ██████╔╝██║  ██║██╔██╗██║
██╔═╝  ██║╚████║██║    ██╔══██╗ ╚██╔╝  ██╔═══╝   ██║  ██╔══██╗██║  ██║██║╚████║
██████╗██║ ╚███║╚█████╗██║  ██║  ██║   ██║       ██║  ██║  ██║╚█████╔╝██║ ╚███║
╚═════╝╚═╝  ╚══╝ ╚════╝╚═╝  ╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚══╝"""

subtitlestr = """                     ____ ____ ____ ____ ____ ____ ____ ____
                    ||T |||e |||r |||m |||i |||n |||a |||l ||
                    ||__|||__|||__|||__|||__|||__|||__|||__||
                    |/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|"""

def printlogo(colorscheme=1): # color scheme: 1 to 6
    lines = logostr.split('\n')
    assert len(lines) == 6
    clr = 16 + 6*(colorscheme-1)
    for line in lines:
        print(ansi(38,5,clr),end='')
        clr += 1
        for _ in range(5):
            substr, line = (line[:13], line[13:]) # 80/6 = 13 R 2
            print(substr + ansi(38, 5, clr),end='')
            clr += 1
        print(line+ansi(0)) # with newline at the end
        clr += 30  # 36 - 6

# Main loop

def run(version=""):
    global cmd_history
    initialize_help()
    os.system('clear')
    printlogo(colorscheme = randint(1,6))
    print(subtitlestr+"\n\n")

    # loading bar
    items = list(range(0, 20))
    os.system("tput civis")
    for item in progressBar(items, prefix = 'Loading... ', suffix = 'Complete', length = 50):
        # could potentially be used to make actual progress!
        sleep((21-item)/80)
    os.system("tput cnorm")
    print("\n"+version+"\n")
    # Main Loop
    while True:
        try:
            line = input("(?) ").strip()
        except KeyboardInterrupt:
            exit_term(ctrl_c=True)
            break
        if not line:
            print("Empty Line...")
            continue
        cmd = parse_cmd(line)

        # History related commands
        if cmd[0] in ['!!']:
            if cmd_history:
                cmd = cmd_history[-1][0]
            else:
                print(ansi(31)+"No comamnd history. Failed to fetch previous command."+ansi(0))
        elif cmd[0].startswith('!'):
            try:
                n = int(cmd[0][1:])
            except ValueError:
                print(ansi(31)+"Invalid history search:".format(cmd[0][1:])+ansi(0))
            if 0 < n <= len(cmd_history):
                print(ansi(30,47)+cmd_history[n-1][1]+ansi(0))
                cmd = cmd_history[n-1][0]
                if cmd_history[n-1][1] != cmd_history[-1][1]: # no repeats
                    cmd_history.append(cmd_history[n-1])
                    # if len(cmd_history) > HISTORY_MAX_SIZE: # TODO: implement this later (term sliding problem)
                    #     cmd_history.pop(0)
            else:
                print(ansi(31)+"History command out of range: {}. History size: {}. Check `history`.".format(n, len(cmd_history))+ansi(0))
        else:
            if (not cmd_history) or cmd_history[-1][1] != line: # no repeats
                cmd_history.append((cmd, line))
                # if len(cmd_history) > HISTORY_MAX_SIZE:
                #     cmd_history.pop(0)

        query = cmd[0].casefold()
        if cmd_table.get(query, cmd_not_found)(*(cmd[1:])):
            break
    # Assuming no error, we break out way out of here (interactive python) – discontinued for now.
    # os.system("kill "+str(os.getpid())+" 2>&1 /dev/null") #suicide!


if __name__ == "__main__":
    run(version = "Encryptron Terminal: Test Build.")
