from mininet.node import Controller, RemoteController
from mininet.link import TCLink
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
#from mininet.net import Mininet
#from mininet.node import Host
#from mininet.cli import CLI
from mininet.log import setLogLevel, info
from multiprocessing import Process
from collections import OrderedDict
import os
import time
import  random
import sys
import json


station = []

def topology():

    mod = str(sys.argv[1]) # network type
    print("-------------------------------")
    print("Network Trace Type : "+ str(mod) +'\n')

    nett = str(sys.argv[2]) # mobility
    print("-------------------------------")
    print("Network Trace Mobility : "+ str(nett) +'\n')

  
    host = int(sys.argv[3]) # num of host
    print("-------------------------------")
    print("Number of Total Host : "+ str(host) +'\n')

    algo = str(sys.argv[4]) # name of adaptation algorithm
    print("-------------------------------")
    print("ABS Algorithm : "+ str(algo) +'\n')
   
    prot = str(sys.argv[5]) # name of protocol
    print("-------------------------------")
    print("Protocol : "+ str(prot) +'\n')
    
    sertype = str(sys.argv[6]) # name of server
    print("-------------------------------")
    print("Server : "+ str(sertype) +'\n')
    
    fol = int(sys.argv[7]) # Iteration of experiment
    print("-------------------------------")
    print("Total iteration : "+ str(fol) +'\n')
    
    v_id = str(sys.argv[8]) # Video content type
    print("-------------------------------")
    print("Video name : "+ str(v_id) +'\n')


###################################
    "Create a network."
    net = Mininet_wifi()
    #net = Mininet()


    info("*** Creating client-nodes\n")
    for i in range(host):
        m='sta%s' % (i+1)
        j=i+1
        station.insert(i, net.addStation(m, ip='10.0.0.2%s/24'%(j)))
        #station.insert(i, net.addHost(m, ip='10.0.0.2%s/24'%(j)))

    info("*** Creating AP-node\n")
    ap1 = net.addAccessPoint('ap1', ssid="simpletopo", mode="g", channel="5")

    info("*** Creating server-node\n")
    server = net.addHost('server',ip='10.0.0.1/24')
    
    info("*** Creating cross_traffic-nodes\n")
    dc = net.addHost('dc',ip='10.0.0.80/24')
    ds = net.addHost('ds',ip='10.0.0.81/24')

    info("*** Creating Switch-node\n")
    s2 = net.addSwitch('s2')
    #s1 = net.addSwitch('s1')
    
    info("*** Creating controller-node\n")
    c0 = net.addController('c0')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()


    info("*** Associating clients and AP\n")
    for i in range(host):
        m='sta%s' % (i+1)
        net.addLink(m, ap1)
    
    info("*** Associating AP and switch\n")    
    net.addLink(s2, ap1, 1, 10)  # initial link parameter default according to mininet
    
    info("*** Associating switch and server\n")
    net.addLink(server, s2, bw=1000)
    print("\n ")
    
    info("*** Associating cross_traffic sender and receiver\n")
    net.addLink(dc, ap1)
    net.addLink(ds, s2)
   
    
    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    s2.start([c0])


##############################

    time.sleep(5)
    print("\n ")
    
    #info("*** Running CLI\n")
    #CLI(net)
    #print net.get('ap1')
    #print net['s3']
    
    os.system('cd /home/dash/testbed/goDASH/godash/files && sudo rm -R *')

    fol1=str(v_id)
    fol2=str(fol+1)
    folder = 'iteration_' + str(fol2)+ '_video_' + str(v_id)+'_mode_'+(mod)+ '_net_' + str(nett) +'_host_'+ str(host)+ '_algo_' + str(algo)+ '_protocol_' + str(prot)+'_server_' + str(sertype)

    
    #os.system('mkdir -p /home/dash/testbed/Data/Raw/'+fol+'/'+ folder)
    os.system('mkdir -p /media/sf_vm/'+fol1+'/'+fol2+'/'+ folder)
    
    
    os.system('cd /home/dash/testbed/goDASH/godash/config && sudo rm -R *')
    


    
    with open('/home/dash/testbed/goDASHbed/config/configure.json') as json_file:
        test_dict = json.load(json_file, object_pairs_hook=OrderedDict)
        
    test_dict['adapt']=algo
    
    if prot=='tcp':
       test_dict['quic']='off'
       test_dict['url']='https://www.godashbed.org/x264/full/tearsofsteel_enc_x264_dash.mpd'
    else:
       test_dict['quic']='on'
       test_dict['url']='https://www.godashbed.org:4444/x264/full/tearsofsteel_enc_x264_dash.mpd'
       
    test_dict['serveraddr']='off'
    
    json.dump(test_dict, open('/home/dash/testbed/goDASH/godash/config/configure.json',"w"))
    
    st=[]
    for i in range(host):
        m1='sta%s'%(i+1)
        m2=net[m1]
        st.insert(i, m2)

    switch2=net['s2']
    server=net['server']
    ap= net['ap1']
    #switch1= net['s1']
    dc=net['dc']
    ds=net['ds']
    
    if mod=='3g':
       bt=3
    elif mod=='4g':
       bt=4
    else:
       bt=5
    

    return st, switch2, server,  ap, host , algo, nett, mod, prot, dc, ds, sertype, fol1, bt, fol2



# server settings


def server(sr, prot, sertype):
	
	if sertype=='WSGI':
		if prot=='quic':
			sr.cmd('cd /home/dash/testbed/goDASHbed && sudo systemctl stop apache2.service && caddy start --config ./caddy-config/TestbedTCP/CaddyFilev2QUIC --adapter caddyfile')
			print("......WSGI(caddy) server and quic protocol.....")
		else:
			sr.cmd('cd /home/dash/testbed/goDASHbed && sudo systemctl stop apache2.service && caddy start --config ./caddy-config/TestbedTCP/CaddyFilev2TCP --adapter caddyfile')
			print("......WSGI(caddy) server  and tcp protocol.....")

	elif sertype == 'ASGI':
		if prot == 'quic':
			print(sr.cmd('cd /home/dash/testbed/goDASHbed && sudo systemctl stop apache2.service &&  hypercorn hypercorn_goDASHbed_quic:app &'))
			print('......ASGI(hypercorn) server and quic protocol.....')
		else:
			print(sr.cmd('cd /home/dash/testbed/goDASHbed && sudo systemctl stop apache2.service && hypercorn hypercorn_goDASHbed:app &'))
			print('......ASGI(hypercorn) server and tcp protocol.....')
        
                
# pcap capture                
def pcap(mod, host, algo, nett, prot, sertype, fol1, fol2):
	print("Pcap capturing ap1-eth10 ..........\n")
	#os.system('sudo tcpdump -i ap1-eth10  -U -w  /media/sf_vm/'+str(fol1)+'/'+str(fol2)+'/iteration_' + str(fol2)+ '_video_' + str(fol1)+'_mode_'+(mod)+ '_net_' + str(nett) +'_host_'+ str(host)+ '_algo_' + str(algo)+ '_protocol_' + str(prot)+'_server_' + str(sertype)+'/iteration_' + str(fol2)+ '_video_' + str(fol1)+'_mode_'+(mod)+ '_net_' + str(nett) +'_host_'+ str(host)+ '_algo_' + str(algo)+ '_protocol_' + str(prot)+'_server_' + str(sertype)+'_ap.pcap')




#tc script and kill process

def netcon(mod, nett, host):
	print(str(mod)+ "-"+str(nett)+"  traces.............\n")
	os.system('sudo ./ta1.sh %s %s %d'%(mod, nett,host))


# run godash player

def player(mod, client, host, algo, nett, prot, sertype,fol1,fol2):


     client.cmd('cd /home/dash/testbed/goDASH/godash && ./godash -config ./config/configure.json >/media/sf_vm/'+str(fol1)+'/'+str(fol2)+'/iteration_' + str(fol2)+ '_video_' + str(fol1)+'_mode_'+(mod)+ '_net_' + str(nett) +'_host_'+ str(host)+ '_algo_' + str(algo)+ '_protocol_' + str(prot)+'_server_' + str(sertype)+'/iteration_' + str(fol2)+ '_video_' + str(fol1)+'_mode_'+(mod)+ '_net_' + str(nett) +'_host_'+ str(host)+ '_algo_' + str(algo)+ '_protocol_' + str(prot)+'_server_' + str(sertype)+'.txt && echo ....Streaming done_' + str(client))

        




def ditgr(s):
    time.sleep(1.5)
    print(s.cmd('cd /home/dash/testbed/D-ITG-2.8.1-r1023/bin  && multiport=off && bursty=off && ./ITGRecv'))

#def ditgs(c):
    #print(c.cmd('cd /home/dash/testbed/D-ITG-2.8.1-r1023/bin && ./ITGSend -T UDP -a 10.0.0.81 -c 500 -C 100 -t 180000 -l sender.log -x receiver.log && pkill ITGRecv'))

def ditgs(c,bt):
    time.sleep(1.5)
    #print(c.cmd('cd /home/dash/testbed/D-ITG-2.8.1-r1023/bin && ./ITGSend script_file'+str(bt)+' -l sender.log -x receiver.log'))
    print(c.cmd('cd /home/dash/testbed/D-ITG-2.8.1-r1023/bin &&  multiport=off && bursty=off && ./ITGSend script_file'+str(bt)+' -l sender.log -x receiver.log && sudo pkill ITGRecv && ./kill.sh && echo Streaming done...............'))




if __name__ == '__main__':
    setLogLevel( 'info' )

    #station, switch, ser, ap, host, algo, nett, doc, num, mod, prot, dc, ds =  topology()
    station, switch, ser, ap, host, algo, nett, mod, prot, dc, ds, st, fol1, bt, fol2 =  topology()

    a=True;b=False;c=False;d=False; e=False; f=False;g=False; h=False;


    if a:
       n=Process(target=pcap, args=(mod,host,algo,nett,prot,st,fol1,fol2,))
       n.start()
       b=True  

    if b:
       xx=Process(target=ditgr, args=(ds,))
       xx.start()
       c=True

    if c:
       zz=Process(target=ditgs, args=(dc,bt,))
       zz.start()
       d=True

    if d:
       y=Process(target=server, args=(ser,prot, st,))
       y.start()
       e=True

    if e:
       nn=Process(target=netcon, args=(mod,nett, host,))
       nn.start()
       f=True
    if f:
       #print 'dashc'
       for k in range(host):
           print('Start streaming......')
           q = Process(target=player, args=(mod,station[k],host,algo,nett,prot,st,fol1,fol2))
           q.start()
           q.join
       
