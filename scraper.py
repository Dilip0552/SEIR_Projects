import requests
from bs4 import BeautifulSoup
import sys
def fetchDetails(url):
    try:
        headers ={"User-Agent":"Mozilla/5.0"}
        resp = requests.get(url,headers=headers)
        sp= BeautifulSoup(resp.text, "html.parser")

        # fetch and print title of the webpage
        if sp.title:
            print("\n---------------------- Title------------------\n",sp.title.text.strip())
        else:
            print("Title not found")

        # fetch and print body of the webpage
        bodyTag = sp.find('body')
        if bodyTag:
            mytext = bodyTag.get_text(separator=" ").strip()
        else:
            mytext = sp.get_text(separator=" ").strip()

        mytext=mytext[:5000]  if len(mytext) > 5000 else mytext
        print("\n-----------------------Body--------------------\n"," ".join(mytext.split()))

        # fetch and print all the links in the webpage to which this webpage is pointing to
        print("\n-----------------------Links--------------------\n ")

        myset=set()
        for l in sp.find_all("a"):
            href_link=l.get("href")
            
            if href_link and "http" in href_link:
                if href_link not in myset:
                    print(href_link)
                    myset.add(href_link)
    except Exception as e:
        print(e)


if len(sys.argv) != 2:
    print("Kindly enter a url in the command line after filename. Ex: python Assignment.py URl")
else:
    page_url = sys.argv[1]
    fetchDetails(page_url)

