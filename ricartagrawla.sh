#! /bin/sh

re='^[+-]?[0-9]+([.][0-9]+)?$'
if ! [[ "$1" =~ $re ]] || [ -z "$1" -o $1 -lt 1 ]; then
printf "Usage:  ricartagrawla.sh [N]\n\tN\tnumber of processes (N > 0)\n"
exit 1
fi

if [[ -f ./env/bin/python3 ]]
then
echo "Installing the requirements..."
./env/bin/pip3 install -r ./requirements.txt
echo "Starting the program..."
./env/bin/python3 ./src $1
else 
echo "Creating a virtual env..."
python3 -m venv env
echo "Installing the requirements..."
./env/bin/pip3 install -r ./requirements.txt
echo "Starting the program..."
./env/bin/python3 ./src $1
fi