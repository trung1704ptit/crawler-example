https://www.zenrows.com/blog/distributed-web-crawling#intro-to-celery-and-redis

# Install Redis
## Volume
docker volume create redis-data
## Running
docker run -d \
  -h redis \
  -e REDIS_PASSWORD=redis \
  -v redis-data:/data \
  -p 6379:6379 \
  --name redis \
  --restart always \
  redis:5.0.5-alpine3.9 /bin/sh -c 'redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}'
## Remove
docker rm -f redis
docker volume rm redis-data

## Usage
broker_url='redis://default:redis@127.0.0.1:6379/1'