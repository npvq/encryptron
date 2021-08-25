# encryptron
A fun CLI for "encrypting" sneaky messages.

# Synopsis

This was a project I made with my friends for fun. We were writing simple python scripts to "encrypt" our messages and hide it from one another on Discord. I came across [this site](https://emptycharacter.com/) which has a list of Unicode empty characters. The list had 16 different invisible characters, so I thought "why not encode Ascii characters into pairs of unicode space characters?" and that is what we did. After writing up the script, we met a roadblock: one of the sixteen whitespace characters, `U+00A0`, the no-break space is converted into regular spaces by Discord, presumably to prevent website/domain name fraud. The fix was pretty easy, we just had to find another unicode character to replace it. We found the invisible comma/separator `U+2063` and the empty Braille pattern `U+2800`, and decided to go with the former.

While making the project, I wondered if I could make an accompanied "CLI" to make the script easier to use. The organization of this project is a little messy, but it's just a proof of concept. The CLI works like any other executable (using `argparse`), but it also has a terminal mode, in which a "terminal" is loaded up that uses a non-shell and more specific/efficient syntax. The mechanisms of the *Encryptron* are mostly explained by its own terminal's [help file](encryptron/terminal_help). One other thing to note is that I use the term `crypt` to mean `encrypted text` throughout the documentation because I didn't want to have to type the latter a lot. Almost all of the ASCII Art used were generated using [this site](https://patorjk.com/software/taag).

During this project I had the opportunity to mess with Disk Images on MacOS (you'll see when you download the installer), and I also had fun messing with ANSI escapes, which culminated in an unrelated file in this repository called `minecraft` :rofl:.

I think the real value (if any) of this project, other than the fun and learning experience, is the stuff in `encryptron/codec.py`. If you have any ideas about improving it, go right ahead! I'll be very happy about pull requests of any type.

# Packaging

While there is a proper way to distribute python packages and apps, the *Encryptron* is very small and only uses one non-default (i.e. not shipped with python) package *optionally* for its terminal: `pyperclip`, so I've decided to resort to writing a simple install script that just checks if there exists a python 3 installation that is newer than `3.6` and then copies everything to a directory (hopefully without requiring admin privileges), and after that, creating a symlink from the main script `crypt` to `/usr/local/bin/script`. The main script sets up `PYTHONPATH` so the and calls `main.py` so the program can function normally. The `README.txt` file in this repository is for the disk image.

The target directory is `~/.config/encryptron` be default, since most users have a `~/.config` directory, it wouldn't bother the user too much (and the install script has write permissions there without requiring the user password.) The target directory is stored in `packaging/package_settings.sh`, which is copied into the `.scripts` folder of the disk image by the package preparation script `packaging/package.sh`.

I packaged all this into a MacOS Disk Image. With minor modifications this should also work on any Linux distribution. Compatibility with Windows is beyond the scope of this project, but I suppose that all features except for the terminal should be able to run on Windows. The packaging process for future updates is streamlined by the `packaging/package.sh` script. A list of files (scripts, assets, and installation helper files) to be moved into the Disk Image (except `install` and `README.txt` which are selected by default) are stored in `packaging/package_settings.sh`, which is used and put into `.scripts` on the Disk Image by `packaging/package.sh` and then used by `install` during the user-end installation.

The file structure of the Disk Image is as follows:
- The `install` script
- The `README.txt` file
- The `.assets` directory containing art/icons (and background image) for the install drive
- The `.scripts` directory containing all the scripts to be installed.
    - There is a special subfolder called `helper` containing scripts that will only be used during the installation process. This is mostly so that I don't mix up which scripts I need to copy.
- And the `.fseventd` directory because MacOS loves it so much

### How to package

After populating a folder with the necessary scripts, use the Disk Utility app to create a read/write drive from that folder. Then, modify the folder stylistically, and after that, go back to Disk Utility and convert the drive to a read-only drive.

Update: Packaging has now been made easier with the advent of a new packaging script `packaging/package.sh` that largely automates the packaging process. This makes it easier to package updates.

### Basic Version Control

The only locations in which the version number is present are
- At the top of `main.py`
- In a comment at the top of `install`
- And in `README.txt`

# TODOS

- [ ] Add style to the help and tutorial docs using ANSI escape codes.
- [ ] Fix issue with up/down arrows. (info: interactive mode seems to be a potential fix.)
- [ ] Get Config up and working. Customization will be implemented gradually.
- [x] !!! Write installation/packaging scripts.
