import os
import sys
import subprocess

mode=['3g','4g','5g'] 
#mode=['5g'] 
host=[1] 

#algo=['conventional','bba', 'arbiter','elastic','bba','logistic'] # adaptation algorithm  'elastic','bba','logistic'

algo=['conventional','bba', 'arbiter'] # adaptation algorithm  'elastic','bba','logistic'


#algo=['logistic'] 
net3= ['train', 'ferry','car','bus','metro'] # mobility for 3g

net4=['bus', 'train', 'static','car','pedestrian'] # mobility for 4g

net5=[ 'Static-1','Static-2', 'Static-3', 'Driving-1', 'Driving-2'] # mobility for 5g

prot=['tcp','quic']

sertype=['WSGI']

#video_id=['tos1']
video_id=['raza']

iteration = 3


for it in range(iteration):
    for md in mode:
        if md == '5g':
           for i in net5:
               for vd in video_id:
                   for k in sertype:
                       for l in host:
                           for m in algo:
                                for p in prot:
                                    clear = 'sudo mn -c'
                                    test3 = 'sudo python test3.py '+ str(md)+ ' ' + str(i) + ' ' + str(l)+ ' ' + str(m)+ ' ' + str(p)+ ' ' + str(k)+ ' ' + str(it)+ ' ' + str(vd)
                                    subprocess.run(clear.split(' '))
                                    print(test3)
                                    subprocess.run(test3.split(' '))
        elif md =='4g':
            for i in net4:
                for vd in video_id:
                   for k in sertype:
                       for l in host:
                           for m in algo:
                               for p in prot:
                                    clear = 'sudo mn -c'
                                    test3 = 'sudo python test3.py '+ str(md)+ ' ' + str(i) + ' ' + str(l)+ ' ' + str(m)+ ' ' + str(p)+ ' ' + str(k)+  ' ' + str(it)+ ' ' + str(vd)
                                    subprocess.run(clear.split(' '))
                                    print(test3)
                                    subprocess.run(test3.split(' '))
        else:
            for i in net3:
               for vd in video_id:
                   for k in sertype:
                       for l in host:
                           for m in algo:
                               for p in prot:
                                    clear = 'sudo mn -c'
                                    test3 = 'sudo python test3.py '+ str(md)+ ' ' + str(i) + ' '  + str(l)+ ' ' + str(m)+ ' ' + str(p)+ ' ' + str(k)+  ' ' + str(it)+ ' ' + str(vd)
                                    subprocess.run(clear.split(' '))
                                    print(test3)
                                    subprocess.run(test3.split(' '))
