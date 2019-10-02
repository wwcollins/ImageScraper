#Python Script to perform HTTP Get, analyze HTTP content, look for URLs that will have target images, image scrape and download (using image scrape Library)

#TBDs
#Get Active List of Categories from Gutenberg - if static write to db
#Investigate other sources of data and images
#Create website for access to data
#Look into setting up mirror with RasPi and/or Serve via eBook server
#Create master directory and write all images to - done
#Create Individual Directories for each book and load with images
#Load text and images also to directories above, per book - book download code created
#Move all code to OO Python Library
# IN PROGRESS:  Create a log file for all books, number of images and other relevant information
# Create an Ebook of Ebooks on the fly including a Table of Contents and Content and Reference Section
# JQuery Book formation for reading each book?
# Use AI to analyze photos from imagescraper?  Could be another module, leverage another module such as Clarifai...
# 

#Constants - GUTENBERG
CONST_GUTEN_CATEGORY_URL = "https://www.gutenberg.org/browse/loccs/sh" #Browse By Library of Congress Class: Agriculture: Aquaculture, Fisheries, Angling
CONST_GUTEN_CATEGORY_URL_NAME = "Class: Agriculture: Aquaculture, Fisheries, Angling"
CONST_GUTEN_URL_PRE_HTTP = "http://www.gutenberg.org"
CONST_GUTEN_URL_PRE_HTTPS = "https://www.gutenberg.org"
CONST_WGET_EBOOK_DOWNLOAD_PATH= "/EBOOKS"
CONST_LOG_PATH= "/LOGS"

#IMPORTS
from bs4 import BeautifulSoup
import os
import sys
import requests #pip install requests
#from BeautifulSoup4 import BeautifulSoup4  # pip install BeautifulSoup4  - code failed TBD
import image_scraper #https://pypi.org/project/ImageScraper/
from lxml import html
import os #e.g. os.system("arp -a")
import wget # pip install wget
#fileUrl = 'http://speedtest.ftp.otenet.gr/files/test10Mb.db'; import wget; file_name = wget.download(fileUrl)

class GutenCapture:

     def main():
        print ("Class Main")
		
     #TBD - Continue to Export code blocks to this class then migrate to imporatble library
     def GetImages(categoryPath, outpath): #Get data using os.system with imagescraper
        outpath = "ImageFiles"
        try:
            #sURL = "image-scraper -s " + outpath + " + CONST_GUTEN_URL_PRE_HTTP + each
            sURL = "image-scraper -s " + outpath + CONST_GUTEN_URL_PRE_HTTP + categoryPath
            print('ImageScraper sURL = ' + sURL)
            os.system (sURL) #note:  Getting some error 404 returns 
        except:
            print ("Error in ImageScraper Encountered")
         



def httpGet (url):
     r = requests.get('https://api.github.com/events')
     return (r.text)

from html.parser import HTMLParser  #pip install HTMLParser, The module is called html.parser in Python 3. So you need to change your import to reflect that new name:

class HTMLParser_Tags(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, print it.
               if name == "href":
                   print (name, "=", value)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)
				   

class HTMLParser_Get_Title(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        if tag == "title":
            print ("Analyzing ", tag)
 	    # Check the list of defined attributes.
            for name, value in attrs:
                   print (name, "=", value)
    
 

print("Starting HTMLParser_Get_Title")

parser = HTMLParser_Get_Title()
parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')
			
			
print("Eval of BeautifulSoup")
html_doc = '<html><head><title>Test</title></head><body><h1>Parse me!</h1></body></html>'
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())
print (soup.title.string)
soup.close
			
#sys.exit()		

def write2File(filePath, file, text):
    print ("Hello")
    file = open(file, “w”)
    file.write(“This is a test”) 
    file.write(“To add more lines.”)

    file.close()
    
def getCWD()
    cwd = os.getcwd()
    print ("Current working Directory = " + cwd)
    return cwd
 

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
#cpath = cwd + "/dir"
#createDir(cpath)

#install: pip install ImageScraper  reference: https://pypi.org/project/ImageScraper/
#usage:  import image_scraper   image_scraper.scrape_images(URL)

#url = 'http://www.gutenberg.org/files/35351/35351-h/35351-h.htm'
url = CONST_GUTEN_CATEGORY_URL
#url = 'http://econpy.pythonanywhere.com/ex/001.html'
#r = requests.get ('https://api.github.com/events')
#r = requests.get (url)

#Add code to replace http with CRLF http
#replace code
#str = r.text

#str = str.replace('http:', chr(13) + '.........http:')
#print (str)
#print (r.text)

#sys.exit()

page = requests.get(url)
webpage = html.fromstring(page.content)

#print (webpage.xpath('//a/@href'))
strP = webpage.xpath('//a/@href') #save xpath result as string
print ("List Elements found in Collection ...........................")
print (strP) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#print (type(strP))
intPlen = len(strP)
#print (type(intPlen))
#print (intPlen)

print ("Number of Elements Found in Collection: ", intPlen)

#sys.exit()

# url example: http://www.gutenberg.org/ebooks/35351
# url target example for image extract: http://www.gutenberg.org/files/35351/35351-h/35351-h.htm   <<<  TBD edit url to match this format - working
#http://www.gutenburg.org/files/34672/34672-h/34672-h.htm
#https://www.gutenberg.org/files/9198/9198-h/9198-h.htm

test = "false"

#Use Beautiful Soup as well as ImageScraper
print("Analyzing Data From " + CONST_GUTEN_CATEGORY_URL_NAME)
for each in strP:
    print("Each = " + each)
	eList = []
    if (each.find("ebooks") > 0):   #str1.find(str2) find string2 in string1
        if (test == "true"):
            #xslt_content = xslt_content.decode('utf-8').encode('ascii') -->  some content failing, look at passing content as bytes from image scraper docs
            os.system ("image-scraper -s test http://www.gutenberg.org/files/35351/35351-h/35351-h.htm")
            os.system ("image-scraper -s test https://www.gutenberg.org/files/9198/9198-h/9198-h.htm")
			#https://www.gutenberg.org/files/9198/9198-h/9198-h.htm
            break
		#original format: /ebooks/34672
        print ("Each contains ebooks = " + each)
        ebook = each
		eList.append(ebook)
        each = each.replace("/ebooks/","") #leaves just book number e.g. 34762, now replace in format: /files/35351/35351-h/35351-h.htm
        each = "/files/" + each + "/" + each + "-h/" + each + "-h.htm"
		
        #Create Directory for Image Files
        path = "/ImageFiles"
        createDir(cwd + path)
		
		#URL for Webpage and HTTP Request
        print("...............................................................................")
        print("Processing Using BeautifulSoup")
        bsUrl = CONST_GUTEN_URL_PRE_HTTPS + each #Full URL constructed from Category Page
        print ("URL = " + bsUrl)
		
		#Download Ebooks with WGET
		#https://www.gutenberg.org/ebooks/34672.epub.images?session_id=4dc0f43e99f266fadd5155f53ed7e7a1835c3cb0

        try:
            fileUrl = 'https://www.gutenberg.org' + ebook + '.epub.images?session_id=4dc0f43e99f266fadd5155f53ed7e7a1835c3cb0'
            file_name = wget.download(fileUrl)
        except:
             print("Error Downloading file with WGET: " + fileUrl)
        
		#URL for Webpage and HTTP Request
        spage = requests.get(bsUrl)
        strPage = spage.text
        soup = BeautifulSoup(strPage, 'html.parser')
        
        try:
            #print(soup.prettify())
            #get Title
            #soup.title
            #print(soup.title.string)
            print ("Content or Book Title: " + soup.title.string)
        except:
            print ("Error in BeautifulSoup Encountered")
		
        #GET IMAGES via ImageScraper
		#HTTP Call
		#sURL = "image-scraper -s ImageFiles " + CONST_GUTEN_URL_PRE_HTTP + each
        #print('sURL = ' + sURL)
        #os.system (sURL) #note:  Getting some error 404 returns		
		
		
        #HTTPS Call Attempt, then HTTP if Err 
        try:
             sURL = "image-scraper -s ImageFiles " + CONST_GUTEN_URL_PRE_HTTPS + each
             print('ImageScraper sURL = ' + sURL)
             os.system (sURL) #note:  Getting some error 404 returns 
        except:
             print ("Error in ImageScraper Encountered")
             print ("...Trying HTTP call")
             try:
                 sURL = "image-scraper -s ImageFiles " + CONST_GUTEN_URL_PRE_HTTP + each
                 print('ImageScraper sURL = ' + sURL)
                 os.system (sURL) 
             except:
                print ("Error in ImageScraper Encountered")
             
        

		
#----------------------------------------------------------------------

parser = HTMLParser_Tags()
#parser.feed(your_html_string)
#print(parser.feed(url))



	