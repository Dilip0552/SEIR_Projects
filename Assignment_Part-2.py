import requests
from bs4 import BeautifulSoup
import re
import sys

# function to fetch words from a particular website 
def fetchWordsFromBody(url):
    try:
        headers ={"User-Agent":"Mozilla/5.0"}
        resp = requests.get(url, headers=headers)
        sp= BeautifulSoup(resp.text, "html.parser")
        bodyTag=sp.find("body")
        targetContent = bodyTag if bodyTag else sp
        mytext=targetContent.get_text(separator=" ").lower().strip()
        txt = " ".join(mytext.split())
        words = re.findall(r'\w+', txt)
        return words
    except Exception as e:
        print(e)
    return []


# function to find simhash of a webpage
def findSimhash(url):
    wordFreq={}
    lst = [0]*64
    words=fetchWordsFromBody(url)
    if len(words)==0:
        print("0 words collected")
    for word in words:
        if word in wordFreq:
            wordFreq[word] = wordFreq[word] + 1
        else:
            wordFreq[word] = 1

    for w in wordFreq:

        f = wordFreq[w]

        p=53
        m=2**64
        hash=0
        power=1;
        for c in w:  
            hash=(hash+ord(c)*power)%m
            power = (power*p)%m
        
        for i in range(64):
            if (hash >> i) & 1:
                lst[i] += f
            else:
                lst[i] -= f
    sh=0
    for i in range(64):
        if lst[i]>0:
            sh = sh | (1<<i)
    return sh

if len(sys.argv) != 3:
    print("Kindly enter two urls in the command line after filename. Ex: python Assignment.py URL1 URL2")
else:
    url1=sys.argv[1]
    url2=sys.argv[2]
    h1=findSimhash(url1)
    h2=findSimhash(url2)
    print(f"Simhash of [{url1}] : {h1}")
    print(f"Simhash of [{url2}] : {h2}")

    # comparing bits of two webpages
    temp1 = h1
    temp2 = h2
    commonBits= 0

    for i in range(64):
        bit1= temp1%2
        bit2=temp2%2
        
        if bit1==bit2:
            commonBits=commonBits+1
        temp1 =temp1 //2
        temp2 = temp2// 2

    print(f"Common bits: {commonBits} (out of total 64)")