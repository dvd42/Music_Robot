#!/bin/bash

mypath='./magenta/outRNN/'
myfile=$(tail -n 1 ${mypath}log.txt) 


IFS='.'

read -ra ADDR <<< "$myfile"


IFS=''

myfile2="${ADDR[0]}.mp3"
myfile="${ADDR[0]}.mid"
myfile3="${ADDR[0]}cut.mp3"

timidity $mypath$myfile -Ow -o - | lame - -b 64 $mypath$myfile2
ffmpeg -ss 00:00:05 -i $mypath$myfile2 $mypath$myfile3 -y
lame --scale 30 $mypath$myfile3 $mypath$myfile2'a'
scp $mypath$myfile2'a' pi@192.168.43.167:rlp/magenta_audio/

