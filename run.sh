#!/bin/bash
# Call a python script as many times as needed to treat a text file

c=1
for i in {1..500}; # limit client number by 10
do
    STRING="Python execute script called $i times"
    PYTHON="python3"
    CLIENT="client.py"
    echo $STRING;
    $PYTHON "$CLIENT" "usr"$i &
    
done