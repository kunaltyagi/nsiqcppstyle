#! /bin/bash

x=$PWD
SOURCE="${BASH_SOURCE[0]}"

while [ -h "$SOURCE" ]; do
    # resolve $SOURCE until the file is no longer a symlink
    DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
    # if $SOURCE was a relative symlink, we need to resolve it
    # relative to the path where the symlink file was located
done

DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

# Add an alias for the purpose of calling the main script by name
echo 'alias nsiqcppstyle="'$DIR'/nsiqcppstyle $@"' >> ~/.bashrc
echo '' >> ~/.bashrc

if [ $? -ne 0 ]; then
    echo "Something went terribly wrong"
else
    echo "Installed nsiqcppstyle for only the current user successfully ("$USER")"
    echo "Please take care not to move this folder someplace else"
fi

# Go back to the original directory (if any changes were made)
cd $x
