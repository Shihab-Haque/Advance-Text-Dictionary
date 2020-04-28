# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 00:06:34 2020

@author: Tech Land
"""


import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import sys

from urllib.request import urlopen, Request
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#starting option
start=input('Press s to write your paragraph or press f to read a text file:  ')
if start=='s':
    sen=input('write your paragraph: ')
elif start=='f':
    try:
        fname=input('Put the file in the same folder first, then enter name of the file: ')
        fh=open(fname)
        sen=fh.read()
    except:
        print('wrong file name')
        sys.exit()
       
else:
    print('wrong input')
    sys.exit()
    
wordlist=sen.split()
c=0
for word in wordlist:
    if word=='.' or word==',' or word==':' or word=='-' or word==';':
        del wordlist[c]
    c=c+1


results={'noun':[],'pronoun':[],'adjective':[],'adverb':[],'verb':[],'preposition':[]}


#using google search
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
serviceurl="https://www.google.com/search?" # url format for searching anything

for word in wordlist:
    parms={'q':word+' meaning'}
    reg_url =serviceurl + urllib.parse.urlencode(parms)
    req = Request(url=reg_url, headers=headers) 
    html = urlopen(req,context=ctx).read()
    
    soup = BeautifulSoup(html, "html.parser")
    tags=soup('span')
    s=0
    types=['noun','verb','adjective','adverb','pronoun','preposition','article']
    for tag in tags:
        if len(tag.contents)<1: continue
    
        if tag.contents[0] in types:
           #print('word=',word," Word type: ",tag.contents[0])
           temp1=tag.contents[0]
           
           
           s=1
    
        try:
            if s==1 and len(tag.contents[0].split())>=3:
               #print('meaning: ',tag.contents[0])
                if not ':' in tag.contents[0]:
                    results[temp1].append({word:tag.contents[0]})
                    break
        except: continue
fh.close()
    
    
#writing results to a text file
d=input('If you want to write the resukts to a file press y ,otherwise press n :')
if d=='y':
    rfile=input('give a name to your results text file,put .txt after the name: ')
    rfh=open(rfile,'a')
    for k in results.keys():
        line='List of '+ str(k)+'; total number= '+str(len(results[k]))+'\n'
        rfh.write(line)
        for wrds in results[k]:
            for k,v in wrds.items():
                meaning=k+' : '+v+'\n'
                rfh.write(meaning)
            
            #rfh.write(str(wrds.items()))
            rfh.write('\n')
            
        #rfh.write(str(results[k]))
        rfh.write('\n')
    rfh.close()
    print('execution finished')
elif d=='n':
    print('execution finished')
else:
    print('wrong input,execution finished')
    