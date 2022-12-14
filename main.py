from redis import Redis
from tasks import crawl

connection = Redis(db=1)
starting_url = 'https://scrapeme.live/shop/page/1/'

maximum_items = 5
connection.rpush('crawling:to_visit', starting_url)

while True:
    visited = connection.scard('crawling:visited') # count URLs in visited
    queued = connection.scrard('crawling:queued')
    if queued + visited > maximum_items:
        print('Exiting! Over maximum')
        break
    
    # timeout after 1 minute
    item = connection.blpop('crawling:to_visit', 60)
    if item is None:
        print('Timeout! No more items to process')
        break

    url = item[1].decode('utf-8')
    print('Pop URL', url)
    crawl.delay(url)