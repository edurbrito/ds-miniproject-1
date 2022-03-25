#!/bin/sh

if [[ -f ./env/bin/python3 ]]
then
echo "Installing the requirements..."
./env/bin/pip3 install -r ./requirements.txt
echo "Starting the server..."
./env/bin/python3 ./src/server.py
else 
echo "Creating a virtual env..."
python3 -m venv env
echo "Installing the requirements..."
./env/bin/pip3 install -r ./requirements.txt
echo "Starting the server..."
./env/bin/python3 ./src/server.py
fi