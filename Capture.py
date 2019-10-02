######################################################################################
#                                 C A P T U R E . P Y                                #
#                              -CR WILLIAM W COLLINS 2018                            #
#                                                                                    #
#                                                                                    #
######################################################################################

#Retrieves ebooks and images from wikipedia, google searches for images
#Tested for Date Retrieved from Gutenberg Library - both ebooks and images
#Tested for Date Retrieved from Google Image searches - images
#Tested for Date Retrieved from Instagram Image searches - images
#TODO - for Date Retrieved from Pinterest Image searches - images
#TODO - Calibre Study and Integration - in progress - Ebook Reader and Organizer
#TODO - Gutenberg Mirror Site - On RPi NAS or other? Accessable from Calibre

#Import Packages
import sys
import pathlib
from pathlib import Path
import requests #pip install requests
from bs4 import BeautifulSoup #pip install bs4
import image_scraper #https://pypi.org/project/ImageScraper/ pip install ImageScraper
from lxml import html
import os #e.g. os.system("arp -a")
import wget # pip install wget
#fileUrl = 'http://speedtest.ftp.otenet.gr/files/test10Mb.db'; import wget; file_name = wget.download(fileUrl)

import time
import datetime as date

import argparse
import json
import itertools
import logging
import re
import uuid
from urllib.request import urlopen, Request

#CONSTANTS
#CONSTANTS - GUTENBERG
CONST_GUTEN_CATEGORY_URL = "https://www.gutenberg.org/browse/loccs/sh" #Browse By Library of Congress Class: Agriculture: Aquaculture, Fisheries, Angling
CONST_GUTEN_CATEGORY_URL_NAME = "Class: Agriculture: Aquaculture, Fisheries, Angling"
CONST_GUTEN_URL_PRE_HTTP = "http://www.gutenberg.org"
CONST_GUTEN_URL_PRE_HTTPS = "https://www.gutenberg.org"
CONST_WGET_EBOOK_DOWNLOAD_PATH= "/EBOOKS"
CONST_LOG_PATH= "/LOGS"

CONST_INSTAG_ACCNT_USER = "williamwcollinsjr"
CONST_INSTAG_ACCNT_USER_PW = "!@Tyler555"

CONSTANT_GOOGLE_SEARCH_DEFAULT = "Atlantic Salmon Fly"

REQUEST_HEADER = {
		'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('[%(asctime)s %(levelname)s %(module)s]: %(message)s'))
    logger.addHandler(handler)
    return logger

logger = configure_logging()
logger.info("Starting...")
localtime = time.localtime(time.time())
#print ("Local current time :", localtime)
logger.info (time.asctime(localtime))

    
class CommonLib:

	#Get Current Working Directory
	def getCWDir():
		cwd = os.getcwd()
		print ("Current working Directory = " + cwd)
		return cwd
		
	#change current working directory e.g. os.chdir('C:\\Users\\username\\Desktop\\headfirstpython')
	def changeCWDir(path):
		try:
			os.chdir(path)
			logger.info("Current working directory changed to: " + path)
		except:
			logger.info("Error changing current working directory")
	
			
	def pathExists(path):
		if os.path.isdir(path):
			print ("Path Exists >>> " + path)
			return True
		else:
			print ("Path Does not Exists - Creating >>> " + path)
			return False
			
	def pathExistsFile(path):
		if os.path.isfile(path):
			print ("Path Exists >>> " + path)
			return True
		else:
			print ("Path Does not Exists - Creating >>> " + path)
			return False
			
	def createDir(path):
		# check if Dir Exists, Create if Not
		if cl.pathExists(path) != True:
			try:  
			   os.mkdir(path)
			except OSError:  
				print ("Creation of the directory %s failed" % path + "(May Exist)")
			else:  
				print ("Successfully created the directory %s " % path)	
				return "Successfully created the directory %s " % path
			 
		else:
			print ("Path Exists %s " % path)	
			return "Path Exists %s " % path
			 
	def write2File(fileDir, fileName, text):
		cc = CommonLib
		if cc.pathExists(fileDir) != True:
			cc.createDir(fileDir)
		print ("Attempting to Write to dir " + fileDir + " and filename " + fileName)
		
		#check to see if ':' is in path and assume fullpath defined if true
		path = fileDir
		filePath = ""
		if path.find(":") < 0: #assume full path not defined, build out a relative path
			filePath = cc.getCWDir() + "\\" + fileDir + "\\" + fileName
		else:
			filePath = fileDir + "\\" + fileName
			
		filePath = filePath.replace("\\\\", "\\")
			
		try:
			#check if file already exists, append 
			if cc.pathExistsFile(filePath) == True:
				file = open(filePath, "a")
				print ("Now Appending to filePath >>> " + filePath)
			else:
				print ("Now Writing to new filePath >>> " + filePath)
				file = open(filePath, "w")

			#file.write("\n" + "This is a test") 
			#file.write("\n" + "To add more lines.”")
			file.write("\n" + text)
			file.close()
			print ("Write Successful to File: " + filePath)
			return "File Write Successful!"
		except:
			print ("Print Error Opening and or Reading to File: " + filePath)
			return "File Write Unsuccessful!"

class GeneralData:

	def httpGet (url):
			if (url == ""):
				url = 'https://api.github.com/events' #test url
			try:
				r = requests.get(url)
				return (r.text)
				logger.info ("Successfully returned data from: ", url)
			except:
				logger.info ("Error in httpGet:")
			
class GutenData:
		
	def id():
		print("GutenData")
		
	def Get_Gutenberg_Category_Data(categUrl):
		gd = GutenData
		if categUrl == "":
			categUrl = CONST_GUTEN_CATEGORY_URL
		page = requests.get(categUrl)
		webpage = html.fromstring(page.content)
		#print (webpage.xpath('//a/@href'))
		strP = webpage.xpath('//a/@href') #save xpath result as string
		print ("List Elements found in Collection ...........................")
		#print (strP) 
		#print (type(strP))
		intPlen = len(strP)
		print ("Number of Elements Found in Collection: " + categUrl, intPlen)
		#return strP #Collection based upon Category
		filter = "/ebooks/"
		ret = gd.Clean_Categ_List(strP, filter) #filter category results to return only eBook IDs as list
		print("Number of Books found in " + categUrl, len(ret))
		return ret
		
	def Clean_Categ_List(cList, filter): #Extract only ebook reference IDs, return as list
		#print(cList)
		eList = []
		for elem in cList:
			#print (elem)
			if (elem.find("ebooks") > 0): 
				elem = elem.replace(filter,"")
				eList.append(elem) #leaves just book number e.g. 34762
		return eList
		
	def Get_Gutenberg_Images(ebookList):
		logger.info ("Get_Gutenberg_Images")
		gd = GutenData
		urlList = gd.Create_Guten_HTML_URLs(ebookList) #format as list of HTML URLs for book pages
		# Extract Images from each book URLs
		#HTTPS Call Attempt, then HTTP if Err
		for each in urlList:
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
					 

	def Get_Gutenberg_Ebooks(ebookList):
		#TBD - Code needs to be debugged and tested
		logger.info ("Get_Gutenberg_Ebooks")
		#Download Ebooks with WGET
		#https://www.gutenberg.org/ebooks/34672.epub.images?session_id=4dc0f43e99f266fadd5155f53ed7e7a1835c3cb0
		
		for ebook in ebookList:
			print (" .... Attempting to Download Ebook: " + ebook)
			try:
				fileUrl = 'https://www.gutenberg.org/' + ebook + '.epub.images?session_id=4dc0f43e99f266fadd5155f53ed7e7a1835c3cb0'
				file_name = wget.download(fileUrl)
			except:
				 print("Error Downloading file with WGET: " + fileUrl)
		
	
	def Create_Guten_HTML_URLs (ebookList):
		urlList = []
		for each in ebookList:
			each = "/files/" + each + "/" + each + "-h/" + each + "-h.htm"
			urlList.append(each)
		logger.info("Generated Gutenberg HTML", urlList)
		return urlList
		
	
class GoogleData:
	
	def id():
		print("GoogleData")
		
	def get_soup(url, header):
		response = urlopen(Request(url, headers=header))
		return BeautifulSoup(response, 'html.parser')

	def get_query_url(query):
		return "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % query

	def extract_images_from_soup(soup):
		image_elements = soup.find_all("div", {"class": "rg_meta"})
		metadata_dicts = (json.loads(e.text) for e in image_elements)
		link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
		return link_type_records

	def extract_images(query, num_images):
		url = goog.get_query_url(query)
		logger.info("Souping")
		soup = goog.get_soup(url, REQUEST_HEADER)
		logger.info("Extracting image urls")
		link_type_records = goog.extract_images_from_soup(soup)
		return itertools.islice(link_type_records, num_images)

	def get_raw_image(url):
		req = Request(url, headers=REQUEST_HEADER)
		resp = urlopen(req)
		return resp.read()

	def save_image(raw_image, image_type, save_directory):
		extension = image_type if image_type else 'jpg'
		file_name = uuid.uuid4().hex + "." + extension
		save_path = os.path.join(save_directory, file_name)
		with open(save_path, 'wb') as image_file:
			image_file.write(raw_image)

	def download_images_to_dir(images, save_directory, num_images):
		for i, (url, image_type) in enumerate(images):
			try:
				logger.info("Making request (%d/%d): %s", i, num_images, url)
				raw_image = goog.get_raw_image(url)
				goog.save_image(raw_image, image_type, save_directory)
			except Exception as e:
				logger.exception(e)

	def run(query, save_directory, num_images=100):
		query = '+'.join(query.split())
		logger.info("Extracting image links")
		images = goog.extract_images(query, num_images)
		logger.info("Downloading images")
		goog.download_images_to_dir(images, save_directory, num_images)
		logger.info("Finished")
		

	def main(search,numimages=5,dir='google_data'):
		cl = CommonLib
		cur = cl.getCWDir()
		cl.createDir(cur + "\\" + dir)
		path = cur + "\\" + dir
		
		parser = argparse.ArgumentParser(description='Scrape Google images')
		parser.add_argument('-s', '--search', default=search, type=str, help='search term')
		parser.add_argument('-n', '--num_images', default=numimages, type=int, help='num images to save')
		parser.add_argument('-d', '--directory', default=path, type=str, help='save directory')
		args = parser.parse_args()
		goog.run(args.search, args.directory, args.num_images)
		
	#if __name__ == '__main__':
	#	main()
	

class Scrapy:

	def id():
		print ("Scrapy")
		print ("Install information and Reference:  pip install Scrapy.  https://doc.scrapy.org/en/latest/faq.html.  Note: Scrapy crashes with: ImportError: No module named win32api.  You need to install pywin32 because of this Twisted bug. Dependencies:  lxml, an efficient XML and HTML parser parsel, an HTML/XML data extraction library written on top of lxml, w3lib, a multi-purpose helper for dealing with URLs and web page encodings twisted, an asynchronous networking framework cryptography and pyOpenSSL, to deal with various network-level security needs")
	
	def Fetch(url):
		#format:  Scrapy fetch <url>
		os.system (url)
		

class InstagramData:

    #Properties
	def __init__(self,user):
		self.user = user
	@property
	def user(self):
		return self.__user
	@user.setter
	def user(self, user):
		self.__user = user
		
	def Instagram_API():
		from InstagramAPI import InstagramAPI #pip install InstagramAPI
		username = CONST_INSTAG_ACCNT_USER
		pw = CONST_INSTAG_ACCNT_USER_PW
		InstagramAPI = InstagramAPI(username, pw)
		InstagramAPI.login()
		InstagramAPI.logout()
		
		#TBD - Continue build-out of this Class
	
	def id():
		print("InstagramData")
		#pip install instagram-python
		#eval - failure to install.  Perhaps Windows compat issue

		#pip install instagram-scraper - https://github.com/rarcega/instagram-scraper
		#usage:  
		#	user media:  $ instagram-scraper <username> -u <your username> -p <your password>    (must be approved follower)
		#	instagram-scraper williamwcollinsjr -u williamwcollinsjr -p !@Tyler555  <<< Download your own posts
		#	hash tag: $ instagram-scraper <hashtag without #> --tag  (It may be useful to specify the --maximum <#>)
		#	To specify multiple users, pass a delimited list of users:  $ instagram-scraper username1,username2,username3           
		#	You can also supply a file containing a list of usernames:  $ instagram-scraper -f ig_users.txt (CRLF between usernames)
		# 	Other usage information: https://github.com/rarcega/instagram-scraper
		
		#	instagram-scraper williamwcollinsjr -u williamwcollinsjr -p !@Tyler555 -d instagram  <<< Download your own posts
		#	instagram-scraper jeromemolloy -u williamwcollinsjr -p !@Tyler555 -d instagram  <<< images from user
		#	instagram-scraper jeromemolloy -u williamwcollinsjr -p !@Tyler555 -d instagram -m 5 -n --comments <<< images from user, user, pw, path, max,
		#	instagram-scraper --tag atlanticsalmonfly -u williamwcollinsjr -p !@Tyler555 -d instagram -m 10 -n  <<< images from hashtag	
 
		
	def Get_Instag_Images (tag, path, imgmax="10", type="hash", media="image"): #target user, base path, number of images, type (user name or hashtag)
			
		preURL = "instagram-scraper "
		postURL = " -u " + CONST_INSTAG_ACCNT_USER +  " -p " + CONST_INSTAG_ACCNT_USER_PW +  " -d " + path +  " -m " + imgmax + " --latest " + " -t " + media
		
		#2 search types, by user or hash, formatted URL slightly different
		if (type == "user"):
			targURL = preURL + tag + postURL
		else: #type=hash
			targURL = preURL + "--tag " + tag + postURL

		try:
			print('Instagram Scraper Target URL = ' + targURL)
			os.system (targURL) #note:  Getting some error 404 returns 
		except:
			print ("Error in Instagram ImageScraper Encountered")
			print ("...Trying HTTP call")


class PinterestData:
	#https://pypi.org/project/pinterest-python-sdk/ (poor documentation)
	# or pip install pinterest-client
	#Pinterest API: App: ImageExplorer  AppID: 4965748616997125067  AppSecret: aeed3198d42b28ca0ca7e86cea12b9dfef33851a47e26a83a4b15bfd3276033f
	def ID():
		print ("Pinterest Data")
	
	


#-------------------------------------  T E S T I N G  ---------------------------------------
	
#Testing/Examples
class Test():

	def testGoogleScrape():
		print ("Testing testGoogleScrape")
		search = "Atlantic Salmon Fly"
		search = "Redfish Fly"
		search = "michael koors shoes black white"
		search = "wikipedia fly fishing"
		search = "Clark Gable"
		search = "Carey Grant"
		search = "Audrey Hepburn"
		search = "earnest hemmingway"
		search = "Charles Dickens characters"
		search = "obsidian arrowheads"
		search = "koors shoes"
		search = "dry flies"
		search = "atlantic salmon flies"
		

		numimages = 99	
		goog.main(search,numimages,search)
		
	def testGoogleScrapeMulti(searchTerms): #input list of search terms
		print ("Testing testGoogleScrape: Search Term = " + searchTerm)
		search = "Atlantic Salmon Fly"
		search = "Redfish Fly"
		numimages = 20
		goog.main(searchTerm,numimages,search)
		
	def testInstagScrape():
		instagram.user = "williamwcollinsjr"
		print ("Instagram User = " + instagram.user)

		print ("Testing InstagramAPI")
		#instagram.Instagram_API()

		tag = "atlanticsalmonfly" # hash tag
		#tag = "atlanticsalmonfly,salmonfly" # hash tag
		#tag = "jeromemolloy" #user
		#tag = "jeromemolloy,williamwcollinsjr" #user
		path = "asf"
		imgmax = "5"
		type = "hash" #user or hash, default is hash
		media = "image"
		#Get_Instag_Images (tag, path, imgmax, type)
		instagram.Get_Instag_Images (tag, path, imgmax, type, media)  # <<< Get Images from Instagram

		#test hash tag for #atlanticsalmonfly at https://www.instagram.com/explore/tags/atlanticsalmonfly
		# Instagram Hashtags for test:  #flytying #flyfishing #destin #30a #emeraldcoast #redfish #redfishonfly #redfishfly #redfishflies #crabfly #crabflies #sandbar_flies #saltwaterflyfishing #saltwaterflies #flyfishing #flytyer #flytying #saltwater #saltwaterflyfishing #saltwaterfly #redfish #redfishfly #floodtide #inshore #inshorefishing #saltmarsh #saltlife #lowtide #hightide #flatsfishing #flatsflyfishing #puppydrum #blackdrum #likesforlikes #likeforlike #likes4likes #like #saltwaterflyfishing #saltwaterfly #flyfishing #fly #saltwaterfishing #redfish #snook #snookfishing #snookfly #redfishfly #speckledtroutflies #speckfly #speckledtrout #inshore #inshorefishing #inshorefly #flyrods #orvisflyfishing #orvis #helios3 #docklightfishing #likesforlikes #like4like #like #likes #crabfly #redfishfly #redfishflyfishing #saltwaterflyfishing #saltwaterflytying #flyfishing #flytying #texasflyfishing #texasflytying #redfishslider #texascoastalbend #redfishmunchies #spookingredfish @allenflyfishing #flytying #flyfishing #redfish #redfishonfly #redfishfly #flyfishlouisiana #baitfishfly #mullet #mulletfly #saltwaterflies #saltwaterflyfishing #orvis #orvisflyfishing #orvisflytying #flytying #quiettime #needabiggerflybox #redfishfly #flyfishing #girlswhoflyfish #salmonfly #chasingsilver #balticsalmon #atlanticsalmon #salmonflyfishing #flytying #tubefly #perhokalastus #lohtaperholla #perhonsidonta #putkiperho #vesanputki

	def testGutenberg():
		print(gutenD.id)
		#http://www.gutenberg.org/browse/loccs/pr <<<  Test Category URL
		#create list of categories, better:  find method to 
		categ = "http://www.gutenberg.org/browse/loccs/pr"
		coll = gutenD.Get_Gutenberg_Category_Data(categ)
		print (type(coll))
		print(*coll)
		gutenD.Get_Gutenberg_Images(coll) #<<< return images for a collection
		gutenD.Get_Gutenberg_Ebooks(coll) #<<< return ebooks of type epub for a collection

	def testHTTPreq():
		#Test Generic HTML Request
		url = ""
		print ("Test getURL........")
		print (genD.httpGet(url)) #should return text from HTTP Get call

	def testCreateDirFile():
		#Test Simple Logic for Dir Create and File Write 
		fileName = "TestWrite.txt"
		fileDir = "TestWrite"
		print (fileDir)
		print (fileName)
		cl.write2File(fileDir, fileName, "Write to File: " + fileName)

	def testChangeCWD():
		print ("Testing Change CWD")
		path = "C:\\"
		cl.changeCWDir(path)
		print (cl.getCWDir())
		
class DoEmail:	#New Feature - TBD
	def id():
		print ("Do Email")
		
	# Send an HTML email with an embedded image and a plain text message for
	# email clients that don't want to display the HTML.



	



#CREATE CLASS INSTANCES
cl = CommonLib
genD = GeneralData
gutenD = GutenData
instagram = InstagramData
goog = GoogleData
tst = Test

Test.testGoogleScrape()



