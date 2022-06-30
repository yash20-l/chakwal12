import redis
r = redis.Redis(host='redis-11935.c252.ap-southeast-1-1.ec2.cloud.redislabs.com', port=11935, 
                password='nNtEF7G1kdfQNrV8vD2cvYNdRWvYg2iC')
r.set('hello', 'world')
print(r.get('hello'))
