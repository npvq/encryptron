#####################################
#                                   #
#  Encryptron: The Discreet Enigma  #
#                                   #
#####################################
#
# Ver: 0.1-b
version = "Version 0.1-beta"
# Author: npvq
# 2021-08-25
#

from sys import argv, exit
import os
import argparse
import encryptron.codec as cdc
from encryptron import ansi, terminal_run

clipboard = True
try:
    import pyperclip
except ModuleNotFoundError:
    clipboard = False

script_path = os.path.dirname(os.path.abspath(__file__))


# CLI Component
# print("argv: ", argv)
parser = argparse.ArgumentParser('Encryptron', allow_abbrev=False)


parser.add_argument('--version', action='store_true', help='Prints version and exits.')
parser.add_argument('--check-key', action='store', type=str, nargs=1, help='Checks the permutation of a key and exits.')
parser.add_argument('-t', '--terminal', action='store_true', help='Launches feature-complete interactive terminal (beta).')

parser.add_argument('-d', '--decode', action='store_true', help='Switches to decoding mode (encoding mode is default).')
parser.add_argument('-k', '--key', action='store', type=str, nargs=1, help='Stores a key to use for encryption. Takes precedence over --perm.')
parser.add_argument('-p', '--perm', action='store', type=str, nargs=1, help='Stores a hex permutation to use for encryption.')
parser.add_argument('--filter', action='store', type=str, nargs=1, help='Numbers used to mix up code. Options: Tribonacci (default), Fibonacci, Lucas.')

# catch for message
parser.add_argument('message', nargs='*') # at least one present

args = parser.parse_args()
# print(args) # debug

# NEED TO IMPLEMENT methods from codec.py
def main():
    # print("Args: ", args)
    # Preliminary argument parsing
    if args.version:
        print(version)
        exit(0)
    if args.terminal:
        # os.system(script_path+"/crypt terminal")
        terminal_run(version = "Encryptron Terminal "+version)
        exit(0)
    if args.check_key:
        print("Corresponding Permutation: {}".format(cdc.key_to_perm(args.check_key)))
        exit(0)

    # Text processing
    if not args.message:
        print("Message cannot be blank\nTry 'crypt --help'")
        exit(-1)

    args_dict = {}
    if args.filter:
        for k in cdc.num_gen_filters.keys():
            if k.casefold().startswith(args.filter[0].casefold()):
                args_dict['filter'] = k
                break
        else:
            print(ansi(93)+"No filter named \"{}\" was found, using default (tribonacci)...".format(args.filter[0])+ansi(0))
    if args.key:
        args_dict['key'] = args.key[0]
        if args.perm:
            print(ansi(93)+"Since key settings take precedence, the inputted permutation will not be used."+ansi(0))
    if args.perm:
        args_dict['perm'] = args.perm[0]

    if args.decode:
        print("Message: {}".format(cdc.ws_decode(args.message[0], **args_dict)))
    else:
        print("Code: [start]{}[stop]".format(cdc.ws_encode(" ".join(args.message), **args_dict)))



if __name__ == "__main__":
    main()
