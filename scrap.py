import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import time

def trade_spider():
    url = 'https://www.tutorialspoint.com/tutorialslibrary.htm'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'html.parser')
    # print(soup)
    for link in soup.findAll('ul',{'class':'menu'}):
    	title_list = []
    	link_list = []
    	title = BeautifulSoup(str(link),'lxml')
    	attr = title.find('ul').attrs
    	id_name = attr['id']
    	path = 'data/' + str(id_name)
    	# if(os.path.exists(path)):
    	# 	continue
    	os.makedirs(path, exist_ok= True)
    	for li in title.findAll('li'):
    		a = li.find('a')
    		link = a['href'].strip()
    		title = a.get_text().strip()
    		print(title)
    		if(title == 'Who is Who'):
    			continue
    		title_list.append(title)
    		link_list.append(link)
    		title = re.sub(r'[/\:"?<>*|]', ' ', title)
    		title = re.sub(r'\\', ' ', title)
    		title = re.sub(r'\r', ' ', title)
    		title = re.sub(r'\n', ' ', title)
    		new_path = path + '/' + str(title)
    		if(os.path.exists(new_path)):
    			continue
    		os.makedirs(new_path, exist_ok= True)
    		getTopic(new_path,title,link)
    	csv_path = path + '/' + str(id_name) + '.csv'
    	createCSV(csv_path,title_list,link_list)
    	


def createCSV(path,title,link):
	with open(path, 'w', encoding="utf-8", newline='') as f:
    		writer = csv.writer(f)
    		writer.writerow(('title','links'))
    		for row in zip(title,link):
    			writer.writerow(row)


def getTopic(path,topic_name,link):
	chp_title = []
	chp_link = []
	if(link[0]!='/'):
		link = '/' + link
	links = 'https://www.tutorialspoint.com' + link
	print(links)
	source_code_1 = requests.get(links)
	# time.sleep(2)
	plain_text_1 = source_code_1.text
	topic_text = BeautifulSoup(plain_text_1,'html.parser')
	for link in topic_text.findAll('ul', {'class':'nav nav-list primary left-menu'}):
		title = BeautifulSoup(str(link),'lxml')
		for li in title.findAll('li'):
			a = li.find('a')
			if a != None and a.has_attr('href'):
				topic_link = a['href'].strip()
				topic_title = a.get_text().strip()
				getText(path,topic_title,topic_link)
				chp_title.append(topic_title)
				chp_link.append(topic_link)
		createCSV(path + '/' + topic_name + '.csv',chp_title,chp_link)


def getText(path,topic,link):
	topic = re.sub(r'[/\:"?<>*|]', ' ', topic)
	topic = re.sub(r'\\', ' ', topic)
	topic = re.sub(r'\r', ' ', topic)
	topic = re.sub(r'\n', ' ', topic)
	topic.strip()
	links = 'https://www.tutorialspoint.com' + link
	source_code = requests.get(links)
	# time.sleep(2)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text,'html.parser')
	for link in soup.findAll('div', {'class':'col-md-7 middle-col'}):
		class_list = ['cover', 'pre-btn', 'nxt-btn', 'topgooglead', 'clearer', 'center-aligned tutorial-menu', 'print-btn', 'bottomgooglead','pre-btn', 'nxt-btn']
		for i in class_list:
			if(link.find('div',{'class': str(i)})!= None):
				link.find('div',{'class': str(i)}).decompose()
		check_ad = link.find('div',{'style':'padding-bottom:5px;padding-left:10px;text-align: center;'})
		if(check_ad != None):
			link.find('div',{'style':'padding-bottom:5px;padding-left:10px;text-align: center;'}).decompose()

		text = link.get_text()
		with open(path+ '/' + topic + '.txt','w', encoding='utf-8') as f:
			f.write(str(text))




trade_spider()