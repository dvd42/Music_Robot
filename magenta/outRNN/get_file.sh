#!/bin/bash

mypath='./magenta/outRNN/'
myfile=$(tail -n 1 ${mypath}log.txt) 


IFS='.'

read -ra ADDR <<< "$myfile"


IFS=''

myfile2="${ADDR[0]}.mp3"
myfile="${ADDR[0]}.mid"

timidity $mypath$myfile -Ow -o - | lame - -b 64 $mypath$myfile2
scp $mypath$myfile2 pi@192.168.43.167:rlp/magenta_audio/
