#!/usr/bin/env bash

g=$(pgrep godash)
t=$(pgrep tcpdump)
c=$(pgrep caddy)

go="godash"

#echo $g

#echo $t

#echo $c
a=1

while [ $a -lt 2 ]; do
     num=$(ps -ef| grep  godash| wc -l) 
     echo $num
     if [ $a -eq 2 ]; then
         break
     fi
     if [ $num -eq 1 ]; then
            echo "yo yo"
            sleep 4
            sudo pkill -9 tcpdump && sudo pkill -9 caddy
            a=$((a + 1))
            
     else
         sleep 4
         echo "out"
         echo ps -ef| grep  godash| wc -l
           
     fi
   
done
   

