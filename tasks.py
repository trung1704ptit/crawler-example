from celery import Celery 
import requests 
from bs4 import BeautifulSoup 
from urllib.parse import urljoin
from redis import Redis

connection = Redis(db=1)
 
app = Celery('tasks', broker_url='redis://default:redis@127.0.0.1:6379/1') 
 
@app.task 
def crawl(url):
	connection.sadd('crawling:queued', url) # Add url to set
	html = get_html(url) 
	soup = BeautifulSoup(html, 'html.parser') 
	links = extract_links(url, soup) 
	for link in links:
		if allow_url_filter(link) and not seen(link):
			print('Add URL to visit queue', link)
			add_to_visit(link)
	
	# automically move a URL from queued to visited
	connection.smove('crawling:queued', 'crawling:visited', url)

def allow_url_filter(url):
	return '/shop/page/' in url and '#' not in url

def seen(url):
	return connection.sismember('crawling:visited', url) or connection.sismember('crawling:queued', url)


def add_to_visit(url):
	# if LPOS is not available in Redis library
	if connection.execute_command('LPOS', 'crawling:to_visit', url) is None:
		connection.rpush('crawling:to_visit', url) ## add URL to the end of this list

def get_html(url): 
	try: 
		response = requests.get(url) 
		return response.content 
	except Exception as e: 
		print(e) 
 
	return '' 
 
def extract_links(url, soup): 
	return list({ 
		urljoin(url, a.get('href')) 
		for a in soup.find_all('a') 
		if a.get('href') and not(a.get('rel') and 'nofollow' in a.get('rel')) 
	}) 
