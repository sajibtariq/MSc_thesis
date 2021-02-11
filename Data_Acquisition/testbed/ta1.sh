#!/usr/bin/env bash
mod=$1
net=$2
host=$3

a=1
b=1
v=1


while true; do
    array=()
    j=1
    cut -d, -f 1,2 --output-delimiter=' ' /home/dash/testbed/goDASHbed/Band_data/Band_data/$mod/$net.csv | while read col1 ; do
    
    array[$j]=$col1
    ban=$(bc<<<"scale=3; ${array[j]}*$host")
    echo $ban
    if [ $v -eq 1 ]; then

         #sudo  tc qdisc add dev s1-eth10 handle 1:0 root htb default 1 && tc class add dev s1-eth10 parent 1:0 classid 1:1 htb rate  "$(bc<<<"scale=2; $ban/1")"kbit ceil "$(bc<<<"scale=2; $ban/1")"kbit && echo  "second" $SECONDS  "band" "$(bc<<<"scale=2; $ban/1")"kbit

         sudo  tc qdisc add dev s2-eth1 handle 1:0 root htb default 1 && tc class add dev s2-eth1 parent 1:0 classid 1:1 htb rate "$(bc<<<"scale=2; $ban/1")"kbit ceil "$(bc<<<"scale=2; $ban/1")"kbit &&  echo  "second" $SECONDS"band" "$(bc<<<"scale=2; $ban/1")"kbit

         sleep 4

         v=0

    else

         #sudo tc qdisc del dev s1-eth10 root &&  sudo tc qdisc add dev s1-eth10 handle 1:0 root htb default 1 && tc class add dev s1-eth10 parent 1:0 classid 1:1 htb rate "$(bc<<<"scale=2; $ban/1")"kbit ceil "$(bc<<<"scale=2; $ban/1")"kbit &&  echo  "second" $SECONDS  "band" "$(bc<<<"scale=2; $ban/1")"kbit

         sudo tc qdisc del dev s2-eth1 root  &&  sudo  tc qdisc add dev  s2-eth1 handle 1:0 root htb default 1 && tc class add dev s2-eth1 parent 1:0 classid 1:1 htb rate "$(bc<<<"scale=2; $ban/1")"kbit ceil "$(bc<<<"scale=2; $ban/1")"kbit &&  echo  "second" $SECONDS  "band" "$(bc<<<"scale=2; $ban/1")"kbit

        sleep 4

    j=$((j + 1))
    fi

    num=$(ps -ef| grep  godash| wc -l) 
  
         
    if [ $num -eq 1 ]; then
     #       sleep 1
      #      sudo chmod 777 -R /home/dash/testbed/Data/Raw/
             #echo  "Streaming done..."
        #    echo  "Stop pcap capturing..."
         #   echo  "Stop server...."
            
            #sudo pkill -9 tcpdump
            sudo pkill -9 caddy
            #sudo pkill -9 hypercorn
            #cd /home/dash/testbed/D-ITG-2.8.1-r1023/bin/ && ./ITGDec receiver.log 
            #pkill ITGRecv
            b=$((b + 1))

            break
    fi

done
    if [ $b -eq 2 ]; then
          break
    else  
          num=$(ps -ef| grep  godash| wc -l) 
          if [ $num -eq 1 ]; then
                  # sleep 1
                   #sudo chmod 777 -R /home/dash/testbed/Data/Raw/
                   #echo  "Streaming done..."
                   #echo  "Stop pcap capturing..."
                   #echo  "Stop server...."
            
                   #sudo pkill -9 tcpdump
                   sudo pkill -9 caddy
                   #sudo pkill -9 hypercorn
                   #cd /home/dash/testbed/D-ITG-2.8.1-r1023/bin/ && ./ITGDec receiver.log 
                   #pkill ITGRecv
                   break
          fi
    fi

done

