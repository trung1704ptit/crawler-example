from redis import Redis

connection = Redis(db=1)

to_visit_key = 'crawling:to_visit'
visited_key = 'crawling:visited'
queued_key = 'crawling:queued'
content_key = 'crawling:content'

def pop_to_visit_blocking(timeout=0):
    return connection.blpop(to_visit_key, timeout)

def count_visited():
    return connection.scard(visited_key)

def is_queued(value):
    return connection.sismember(queued_key, value)

def set_content(key, value):
    connection.hset(content_key, key=key, value=value)