#!/usr/bin/env python2.7

import urllib2
import os
import sys
from queue import Queue
import requests
import getopt
import threading
from termcolor import colored
import time

threading.Lock()
q=Queue()
tim=0
def usage():
    print colored("========================================================================\n","green")
    print colored("\t\t\tWeb FUZZ by @luffy27\n","green")
    print colored("\t\t\t\tv1.1\n","green")
    print colored("=======================================================================\n","green")
    print colored("-u for the url/ --url\n","red")
    print colored("-e for extention --ext\n","red")
    print colored("-w for wordlist --word\n","red")
    print colored("-t for no of threads --thread(use -t 0 if u dont want multi-threading)","red")
    
def main():
    print("-h or --help for help options")
    try:
        opts,args=getopt.getopt(sys.argv[1:],"u:e:w:t:h",["url","ext","wordlist","thread","help"])
    except:
        print("fuck")
    url=""
    ext=""
    wlist=""
    global thr
    thr=0
    for o,a in opts:
        if o in ("--help","-h"):
            usage()
        elif o in ("--url","-u"):
            url=str(a)
        elif o in ("--ext","-e"):
            ext=str(a)
        elif o in ("-w","--wordlist"):
            wlist=str(a)
        elif o in ("--thread","-t"):
            thr=sys.argv[-1]
    if(thr==0 and wlist!=""):
        f=open(wlist,"r")
        words=f.readlines()    
        word=list()
        for w1 in words:
            w1=w1.rstrip()
            q.put(str(w1))
        f.close()
        bruteit(url,ext,wlist,thr)
    elif(thr!=0 and wlist!=""):
        f=open(wlist,"r")
        words=f.readlines()
        word=list()
        for w1 in words:
            w1=w1.rstrip()
            q.put(str(w1))
        f.close()
        trd(url,ext,wlist,thr)   
        
def trd(url,ext,wlist,thr):
    try:
        
        for i in range(int(thr)):
            t=threading.Thread(target=bruteit,args=(url,ext,wlist))
            t.start()
    except Exception as e:
        print(e)
        
def bruteit(u,e,w):
    try:
        while not q.empty():   
            lst=str(q.get())
            req=requests.get(u+lst)
            if req.status_code==200 or req.status_code==302:
                    print(str(req.status_code)+":"+lst)
            req1=requests.get(u+lst+"."+e)
            if req1.status_code==200 or req1.status_code==302:
                print(str(req1.status_code)+":"+lst+"."+e)
    except Exception as err:
        print("fuck not wroking\n",err)


        
main()

