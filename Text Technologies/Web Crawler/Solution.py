
## Importing the required libraries
import robotparser
import urllib
import re
from savefile import *
import urlparse
import heapq
## Setting up the counter for the number of new, duplicate and faulty url
Duplicatelinkscount = 1
newlinks = 1
faultycount = 1
count = 1
##Seed Link
link = "http://ir.inf.ed.ac.uk/tts/1152699/1152699.html"

parsedlink = urlparse.urlparse(link)
pfinder=robotparser.RobotFileParser()
pfinder.set_url(parsedlink.scheme+'://'+parsedlink.netloc+'/robots.txt')
pfinder.read()

folder=re.split('[\w_.-]*$',parsedlink.path)
#Creating HeapQ
Q = []
L = []
##Pushing the seed link into Q
heapq.heappush(Q,link)
nextlink=link
nparsedlink = urlparse.urlparse(nextlink)
if not ((parsedlink.netloc) is (nparsedlink.netloc)):
    print "External Link"
else:
    pass

while (len(Q)>0):
    if not (pfinder.can_fetch('TTS', nextlink)):
        print ("faulty", nextlink)
        faultycount = faultycount+1 # Increase the faultylink counter if the link is not accessible or external
        
        
    else:
        data = urllib.urlopen(nextlink).read() # reading the html file
        remctag1 = re.search('<!-- CONTENT -->(.*)<!-- /CONTENT -->', data) #Data inside the content tag
	#saveToFile(remctag1.group(1),'content.txt')
	if (remctag1 != None):	
		saveToFile(remctag1.group(1), 'content'+(str)(count)+'.html')
		count = count+1
	else:
		pass
        if remctag1:
            rematag1 = re.findall('\<a.*?href="(.*?)"', remctag1.group(1)) #Anchor tags
            if rematag1:
                for x in rematag1:
                    c = parsedlink.scheme+'://'+parsedlink.netloc+folder[0]+x
                    print c
                    
                    b = Q
                    #print b
                    d = L
                    #print d
                    if (c in b or c in L): #If the link is already present in both Q and L
                        print('Duplicate')
                        Duplicatelinkscount = Duplicatelinkscount+1 # Increment the duplicate count by 1
                        print Duplicatelinkscount            
                        pass
                    else:# If not new link. Push into Q
                        print (c)
                        #saveToFile(c,parsedlink.path,)
                        newlinks = newlinks+1
                        #print newlinks
                        print('New URL')
                        heapq.heappush(Q,c) 
            else:
                pass
        else:
            pass
    
    L.append(nextlink) #Add the processed link into L
    Q.remove(nextlink) # Remove the processed link from Q since it has been added to L
    if (len(Q)==0):
        break
    else:
        nextval=heapq.nlargest(1,Q)#Fetching the largest value in heapQ
        nextlink=nextval[0]# Extracting the link alone without[]


print(L)
saveToFile(L,'finalL.txt')
saveToFile(Q,'finalQ.txt')
print ("Qlength",len(L))
print ("duplicate", Duplicatelinkscount)
#print newlinks
print("newurl", newlinks)
print ("faultycount", faultycount)
total = Duplicatelinkscount+newlinks+faultycount
print ("totalcount", total)
