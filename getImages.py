#Python Script to perform HTTP Get, analyze HTTP content, look for URLs that will have target images, image scrape and download (using image scrape Library)

#TBDs
#Get Active List of Categories from Gutenberg - if static write to db
#Investigate other sources of data and images
#Create website for access to data
#Look into setting up mirror with RasPi and/or Serve via eBook server
#Create master directory and write all images to
#Create Individual Directories for each book and load with images
#Load text and images also to directories above, per book

#Constants - GUTENBERG
CONST_GUTEN_CATEGORY_URL = "http://www.gutenberg.org/browse/loccs/sh"
CONST_GUTEN_URL_PRE_HTTP = "http://www.gutenberg.org"
CONST_GUTEN_URL_PRE_HTTPS = "https://www.gutenberg.org"

#IMPORTS
import os
import sys
import requests #pip install requests
#from BeautifulSoup4 import BeautifulSoup4  # pip install BeautifulSoup4  - code failed TBD
import image_scraper 
from lxml import html
import os #e.g. os.system("arp -a")


class GutenCapture:

    def hello(path):
	    print('Hello')
	

def httpGet (url):

     r = requests.get('https://api.github.com/events')
     r.text

from html.parser import HTMLParser  #pip install HTMLParser, The module is called html.parser in Python 3. So you need to change your import to reflect that new name:

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, print it.
               if name == "href":
                   print (name, "=", value)

def createDir(path):
    # define the name of the directory to be created
    #path = "/tmp/year"

    try:  
       os.mkdir(path)
    except OSError:  
        print ("Creation of the directory %s failed" % path + "(May Exist)")
    else:  
        print ("Successfully created the directory %s " % path)	
		
cwd = os.getcwd()
print ("Current working Directory" + cwd)

#test createDir
cpath = cwd + "/dir"
createDir(cpath)
		


#install: pip install ImageScraper  reference: https://pypi.org/project/ImageScraper/
#usage:  import image_scraper   image_scraper.scrape_images(URL)

#url = 'http://www.gutenberg.org/files/35351/35351-h/35351-h.htm'
url = CONST_GUTEN_CATEGORY_URL
#url = 'http://econpy.pythonanywhere.com/ex/001.html'
#r = requests.get ('https://api.github.com/events')
r = requests.get (url)

# Add code to replace http with CRLF http
# replace code
str = r.text
str = str.replace('http:', chr(13) + '.........http:')
#print (str)
#print (r.text)

#sys.exit()

page = requests.get(url)
webpage = html.fromstring(page.content)

#print (webpage.xpath('//a/@href'))
strP = webpage.xpath('//a/@href') #save xpath result as string
print (strP)
print (type(strP))
intPlen = len(strP)
print (type(intPlen))
print (intPlen)

print ("Elements Found in Collection: ", intPlen)

#sys.exit()

# url example: http://www.gutenberg.org/ebooks/35351
# url target example for image extract: http://www.gutenberg.org/files/35351/35351-h/35351-h.htm   <<<  TBD edit url to match this format - working
#http://www.gutenburg.org/files/34672/34672-h/34672-h.htm
#https://www.gutenberg.org/files/9198/9198-h/9198-h.htm

test = "false"

for each in strP:
    #print(each)
    if (each.find("ebooks") > 0):   #str1.find(str2) find string2 in string1
        if (test == "true"):
            #xslt_content = xslt_content.decode('utf-8').encode('ascii') -->  some content failing, look at passing content as bytes from image scraper docs
            os.system ("image-scraper -s test http://www.gutenberg.org/files/35351/35351-h/35351-h.htm")
            os.system ("image-scraper -s test https://www.gutenberg.org/files/9198/9198-h/9198-h.htm")
			#https://www.gutenberg.org/files/9198/9198-h/9198-h.htm
            break
        #print(urlPre + each)
		#original format: /ebooks/34672
        each = each.replace("/ebooks/","") #leaves just book number e.g. 34762, now replace in format: /files/35351/35351-h/35351-h.htm
        each = "/files/" + each + "/" + each + "-h/" + each + "-h.htm"
		
        path = "/ImageFiles"
        createDir(cwd + path)
        
		#HTTP Call
		#sURL = "image-scraper -s ImageFiles " + CONST_GUTEN_URL_PRE_HTTP + each
        #print('sURL = ' + sURL)
        #os.system (sURL) #note:  Getting some error 404 returns 
		
        #HTTPS Call
        sURL = "image-scraper -s ImageFiles " + CONST_GUTEN_URL_PRE_HTTPS + each
        print('sURL = ' + sURL)
        os.system (sURL) #note:  Getting some error 404 returns 
	
		#image_scraper.scrape_images(sURL)
        #image_scraper.scrape_images (urlPre + each)


#----------------------------------------------------------------------

parser = MyHTMLParser()
#parser.feed(your_html_string)

#print(parser.feed(url))



	