#!/usr/bin/python3
#-*-coding:utf-8-*-

import os

#check correct Attach procedure & errors for all the UEs
#os.system('python multiple_attach_1-1.py ue0.log 1')
os.system('python multiple_attach_1-1.py amari.log 5')

#check content of SIB1 message
os.system('python sib1.py ue0.log')

#check content of SIB2 message
os.system('python sib2.py ue0.log')

#check correct transition from RRC CONNECTED to RRC IDLE
os.system('python connected2idle_1-2.py ue0.log 1')

#check if any paging messages are present in script
os.system('python paging_1-3.py ue0.log 5')

#check if any paging messages are present in script
os.system('python paging_1-4.py ue0.log 5')

#check if there is a cyclical release of resources
os.system('python resource_sharing_2-1.py ue0.log')
