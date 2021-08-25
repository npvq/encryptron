
██████╗███╗  ██╗ █████╗██████╗██╗   ██╗██████╗██████████████╗  █████╗ ███╗  ██╗
██╔═══╝████╗ ██║██╔═══╝██╔══██╚██╗ ██╔╝██╔══██╚══██╔══██╔══██╗██╔══██╗████╗ ██║
████╗  ██╔██╗██║██║    ██████╔╝╚████╔╝ ██████╔╝  ██║  ██████╔╝██║  ██║██╔██╗██║
██╔═╝  ██║╚████║██║    ██╔══██╗ ╚██╔╝  ██╔═══╝   ██║  ██╔══██╗██║  ██║██║╚████║
██████╗██║ ╚███║╚█████╗██║  ██║  ██║   ██║       ██║  ██║  ██║╚█████╔╝██║ ╚███║
╚═════╝╚═╝  ╚══╝ ╚════╝╚═╝  ╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚══╝
 _        ___         ___             ___        _
/ |      / _ \       / _ \           / _ \      / |
- |     | | | |     | | | |  _____  | |_) )     - |
| |     | | | |     | | | | (_____) |  _ <      | |
| |  _  | |_| |  _  | |_| |         | |_) )  _  | |
|_| (_)  \___/  (_)  \___/          |  __/  (_) |_|
                                    | |
                                    |_|
(v1.0.0-beta.1, revised 2021-08-25)

Instructions:

- Double click the installer, a unix shell script named 'install', to install
  the file
- If you have already installed the Encryptron before (i.e. if you're updating)
  then it will warn you about overwriting files. It's okay to overwrite these
  Files when updating, but pay special attention if these binaries were
  installed for other purposes.
- The script is run using the command 'crypt'

___                             _  _    _ __    _
| __|   _ _      __       _ _   | || |  | '_ \  | |_      _ _    ___    _ _
| _|   | ' \    / _|     | '_|   \_, |  | .__/  |  _|    | '_|  / _ \  | ' \
|___|  |_||_|   \__|_   _|_|_   _|__/   |_|__   _\__|   _|_|_   \___/  |_||_|
_|"""""|_|"""""|_|"""""|_|"""""|_| """"|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'

Usage Guide:

- The '-h' or '--help' option provides a guide to basic usage, it can also be
  accessed if you enter 'crypt' with no arguments (?)
- There is also a beta version of a live terminal in development, which
  supports simplified syntax and better integration for continuous usage.
  This can be accessed using the '-t' or '--terminal' option, and once
  successfully launched you can learn more about it and its syntax by entering
  'help' or 'tutorial'.
- pyperclip can be installed via 'python3 -m pip install pyperclip'

.----------------.  .-----------------. .----------------.
| .--------------. || .--------------. || .--------------. |
| |  _________   | || | ____  _____  | || |     ______   | |
| | |_   ___  |  | || ||_   \|_   _| | || |   .' ___  |  | |
| |   | |_  \_|  | || |  |   \ | |   | || |  / .'   \_|  | |
| |   |  _|  _   | || |  | |\ \| |   | || |  | |         | |
| |  _| |___/ |  | || | _| |_\   |_  | || |  \ `.___.'\  | |
| | |_________|  | || ||_____|\____| | || |   `._____.'  | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
'----------------'  '----------------'  '----------------'
.----------------.  .----------------.  .----------------.
| .--------------. || .--------------. || .--------------. |
| |  _______     | || |  ____  ____  | || |   ______     | |
| | |_   __ \    | || | |_  _||_  _| | || |  |_   __ \   | |
| |   | |__) |   | || |   \ \  / /   | || |    | |__) |  | |
| |   |  __ /    | || |    \ \/ /    | || |    |  ___/   | |
| |  _| |  \ \_  | || |    _|  |_    | || |   _| |_      | |
| | |____| |___| | || |   |______|   | || |  |_____|     | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
'----------------'  '----------------'  '----------------'
.----------------.  .----------------.  .----------------.
| .--------------. || .--------------. || .--------------. |
| |  _________   | || |  _______     | || |     ____     | |
| | |  _   _  |  | || | |_   __ \    | || |   .'    `.   | |
| | |_/ | | \_|  | || |   | |__) |   | || |  /  .--.  \  | |
| |     | |      | || |   |  __ /    | || |  | |    | |  | |
| |    _| |_     | || |  _| |  \ \_  | || |  \  `--'  /  | |
| |   |_____|    | || | |____| |___| | || |   `.____.'   | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
'----------------'  '----------------'  '----------------'
                    .-----------------.
                   | .--------------. |
                   | | ____  _____  | |
                   | ||_   \|_   _| | |
                   | |  |   \ | |   | |
                   | |  | |\ \| |   | |
                   | | _| |_\   |_  | |
                   | ||_____|\____| | |
                   | |              | |
                   | '--------------' |
                    '----------------'

Technical Details:

- A folder ~/.config/encryptron is created in the home directory and the script,
  supporting scripts, and configuration files are located there.
- A symlink called 'crypt' is created and stored in /usr/local/bin. I'm not
  aware of any other program called 'crypt', hopefully there won't be conflicts.
  The program will check if such a file exists and warn the user about it. This
  warning also exists when updating.
- NOTE: This is a pre-release developmental version of the script. Also, as of
  this version, there is no package management system for this project.

We hope you enjoy, and should you encounter any installation issues, bugs, or
feature requests, please visit our github page:

                     https://github.com/npvq/encryptron
  __
 /  `                       _/_
/--  ____  _. __  __  , _   /  __  __ ____
(___,/ / <_(__/ (_/ (_/_/_)_<__/ (_(_)/ / <_
                    / /
                   ' '
