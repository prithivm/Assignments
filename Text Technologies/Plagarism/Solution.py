'''
Created on 7 Nov 2011

@author: prithiv
'''
def readFile(filename):
    f = open(filename, 'r')
    try:
        content = f.read()
    finally:
        f.close()
    return content

def saveToFile(data, filename):
    d = dict()
    string = ''
    array = []
    s = set(array)    
    f = open(filename, 'w')
    try:
        if type(data) == type(string):
            f.write(data)
        if type(data) == type(array):
            for d in data:
                f.write(str(d) + '\n')
        if type(data) == type(s):
            data = list(data)            
            for d in data:
                f.write(str(d) + '\n')
        if type(data) == type(d):
            sortedData = sorted(data.items(), key=itemgetter(0))
            for sd in sortedData:
                f.write(str(sd) + '\n')
    finally:
        f.close()
        
import os
import re
import glob
import md5
import heapq
from heapq import merge
allfiles = []
path = '/home/prithiv/TTS3/1152699'
#path='train'
listoffiles = os.listdir(path)
n = len(listoffiles)
#iary = {}
#ibin = {}
exactduplicate = []
duplicatecount = 0
nonduplicatecount = 0
for i in range(0 , n-1):
    icontent = readFile(path+'/'+listoffiles[i])
    ix = re.sub('(.+)?:'+ '\n'+ '(.*)' , ' ', icontent)
    allfiles.append(ix)
for i in range(0 , n-1):
    for j in range(i+1 , n-1):
        ix = allfiles[i]
        jx = allfiles[j]
        if ix == jx:
            exactduplicate.append(listoffiles[i].replace('.txt','')+'-'+listoffiles[j].replace('.txt',''))
            duplicatecount = duplicatecount+1
        else:
            nonduplicatecount = nonduplicatecount+1
saveToFile(exactduplicate,'exactduplicates.txt')
print exactduplicate
print "Exact Duplicates Count", duplicatecount

iary = {}
ibin_all={}

for i in range(n):
    ibin = {}
    ifile = readFile(path+'/'+listoffiles[i])
    itext = re.sub('(.+)?:'+ '\n'+ '(.*)' , ' ', ifile)
    iword_list = itext.split(None)
    iword_freq = {}
    for word in iword_list:
        if word not in iword_freq:
            iword_freq[word] = iword_list.count(word)
            hexa = (md5.md5(word).hexdigest())
            iy = bin(int(hexa, 16))[2:].zfill(128)
            ibin[word] = iy
    print i        
    iary[listoffiles[i]] = iword_freq
    ibin_all[listoffiles[i]]=ibin
    #print ibin_all[listoffiles[i]]
        
    
#print ibin

fingerprint = {}
for i in iary:
    fprint=[0]*128
    for x in iary[i]:
        for j in range(128):
            #print ibin_all[i][x][j]
            if ibin_all[i][x][j]=='0':
                
                fprint[j]+=(int)(iary[i][x])*(-1)
            else:
                fprint[j]+=(int)(iary[i][x])*(+1)
    for j in range(128):
        if fprint[j]>0:
            fprint[j]=1
        else:
            fprint[j]=0
    fingerprint[i]=fprint
    print 'HERE!!!'
    print i
   
duplicateitems = []
print 'HAMMMING'
nearduplicate = []
for i in range(n):
    a=fingerprint[listoffiles[i]]
    for j in range(i+1,n):
        
        b=fingerprint[listoffiles[j]]
        assert len(a)==len(b)
        hd=sum(ch1!=ch2 for ch1,ch2 in zip(a,b))
        if hd<5:
            print listoffiles[i],listoffiles[j]
            nearduplicate.append(listoffiles[i].replace('.txt','')+'-'+listoffiles[j].replace('.txt',''))
saveToFile(nearduplicate,'nearduplicates.txt')

duplicateitems = list(merge(exactduplicate, nearduplicate))
saveToFile(duplicateitems,'DuplicateItems.txt')