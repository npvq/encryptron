#!/bin/bash
# Does packaging magic if you're on a Mac (run in root dir of project!)
# Open the DMG disk image inside /packaging
# If it's not at the default path, set it manually via the environment variable
# named ENCPACKPATH

# Packaging folder:
pkg_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# Root dir
root_dir="$(dirname "$pkg_dir")"


if [ -z "${ENCPACKPATH}" ]; then
    ppath="/Volumes/Encryptron" # Default Path
else
    ppath="${ENCPACKPATH}"
fi

if [ ! -d "${ppath}" ]; then
    tput bold; tput setaf 1; echo "Disk Image Not Found."; tput sgr0
    exit 1
fi

if [ ! -f "${pkg_dir}/package_settings.sh" ]; then
    tput bold; tput setaf 1; echo "Package Settings (packaging/package_settings.sh) not found."; tput sgr0
    exit 1
fi

source "${pkg_dir}/package_settings.sh"

printf "root_dir: $root_dir\npkg_dir: $pkg_dir\nppath: $ppath\nProceed?"
read -n 1 -r

echo "Deleting the following files..."

find "${ppath}/.assets" ! -name 'Icon?' -type f -exec rm -v {} +
find "${ppath}/.scripts" ! -name 'Icon?' -type f -exec rm -v {} +
find "${ppath}/.fseventsd" ! -name 'Icon?' -type f -exec rm -v {} +
# rm -v "${ppath}/.assets/"*
# rm -v "${ppath}/.scripts/"*
# Do this to not mess up folder style settings
echo "Dealing with ${ppath}/install ..."
cat "${root_dir}/install" > "${ppath}/install"
echo "Dealing with ${ppath}/README.txt ..."
cat "${root_dir}/README.txt" > "${ppath}/README.txt"

echo "Importing Assets..."
for file in "${asset_files[@]}"
do
    if [ ! -d "$(dirname ${ppath}/.assets/${file})" ]; then
        mkdir -pv "$(dirname ${ppath}/.assets/${file})"
    fi
    cp -v "${root_dir}/assets/${file}" "${ppath}/.assets/${file}"
done

echo "Importing Scripts..."
for file in "${script_files[@]}"
do
    if [ ! -d "$(dirname ${ppath}/.scripts/${file})" ]; then
        mkdir -pv "$(dirname ${ppath}/.scripts/${file})"
    fi
    cp -v "${root_dir}/${file}" "${ppath}/.scripts/${file}"
done

echo "Importing Helper Files..."
for file in "${helper_files[@]}"
do
    if [ ! -d "$(dirname ${ppath}/.scripts/helper/${file})" ]; then
        mkdir -pv "$(dirname ${ppath}/.scripts/helper/${file})"
    fi
    cp -v "${root_dir}/${file}" "${ppath}/.scripts/helper/${file}"
done

echo "Copying Package Settings..."
cp -v "${pkg_dir}/package_settings.sh" ""${ppath}/.scripts/package_settings.sh""

tput bold; tput setaf 2; echo "PACKAGING COMPLETE ✓"; tput sgr0
