from urllib.parse import urlparse
from parsers import defaults

parsers = {
    'scrapme.live': defaults,
    'quotes.toscrape.com': defaults,
}

def get_perser(url):
    hostname = urlparse(url).hostname
    if  hostname in parsers:
        return parsers[hostname]
    return defaults