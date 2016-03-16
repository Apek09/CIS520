from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from lxml import html
import csv


baseurl = "http://losangeles.craigslist.org"

mydriver = webdriver.Firefox()
mydriver.get(baseurl)


#Navigate to the resale category
link = mydriver.find_element_by_link_text('cell phones')
link.click()

#Parse the new page inside the category
item_listings = mydriver.current_url
print(item_listings)

#Scrape the page for details of the items listed in the selected category
r = requests.get(item_listings)
tree = html.fromstring(r.content)

#Getting the url of each item on the listing page
listings = tree.xpath('//p[@class="row"]/a[@class="i"]/@href')
print(len(listings))
 
#Get inside each item and fetch the details
i=0
with open('craiglist.csv', 'w') as csvfile:
		a = csv.writer(csvfile, dialect='excel')
for item in listings[:10]:
			item_url = baseurl + listings[i]
			print(item_url)
			i+=1
			r = requests.get(item_url)
			tree = html.fromstring(r.content)
			#print(tree)
			item_name = tree.xpath('//span[@class="postingtitletext"]/span[@id="titletextonly"]/text()')
			#print(item_name)
			item_price = tree.xpath('//span[@class="postingtitletext"]/span[@class="price"]/text()')
			#print(item_price)
			item_area = tree.xpath('//span[@class="postingtitletext"]/small/text()')
			#print(item_area)
			item_address = tree.xpath('//div[@class = "mapAndAttrs"]/div[@class="mapbox"]/div[@class="mapaddress"]/text()')
			#print(item_address)			
			item_details = tree.xpath('//div[@class = "mapAndAttrs"]/p[@class = "attrgroup"]/span/b/text()')
			#print(item_details[0])
			#item_make = tree.xpath('//div[@class = "mapAndAttrs"]/p[@class = "attrgroup"]/span[text()="make / manufacturer:"]/b/text()')
			#print(item_make)
			#item_os = tree.xpath('//div[@class = "mapAndAttrs"]/p[@class = "attrgroup"]/span[text()="mobile OS:"]/b/text()')
			#print(item_os)
			#item_model = tree.xpath('//div[@class = "mapAndAttrs"]/p[@class = "attrgroup"]/span[text()="model name / number:"]/b/text()')
			#print(item_model)
			item_post_id = tree.xpath('//div[@class = "postinginfos"]/p[@class = "postinginfo"][1]/text()')
			#print(item_post_id)
			item_posted_date = tree.xpath('//time/text()')
			#print(item_posted_date[0])
			#item_updated_date = tree.xpath('//div[@class = "postinginfos"]/time/text()')
			#print(item_updated_date)
			data = (item_name,  item_price, item_area, item_address, item_details, item_details, item_post_id, item_posted_date)
			print(data)
			#a.writerow(data)



mydriver.close()
