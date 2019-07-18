import urllib.request
import time
import re 
from multiprocessing import Pool 



urls = [ [{'url':'www.test.com/{}'.format(str(v*dataset))} for v in range(100) ] for dataset in range (1,2)]

host = '45.230.2.53:8001'
#host = 'localhost:3000'

def make_tiny(url, host):
    endpoint_url = 'http://{}/maketiny/{}'.format(host,url)
    response = urllib.request.urlopen(endpoint_url)
    txt = response.read()
    g  = re.search( '==> http:\/\/{}\/(.{})'.format(host, '{6}'),  str(txt))
    return g.group(1)

def get_url(tiny, host):
    url = 'http://{}/{}'.format(host,tiny)
    response = urllib.request.urlopen(url)
    txt = response.read()
    g  = re.search( ': (\S+)',  str(txt))
    return g.group(1)


def test_create(urls):

    start = time.time()
    for url in urls:
        start1 = time.time()
        t = make_tiny(url['url'], host)
        url['tinyurl'] = t
        url['create_time'] = time.time()-start1
        print (url['url'])

    end = time.time()
    duration_create = end-start
    print ('duration {}'.format(end-start))

    return urls
   

def test_get(urls):
    print ('verifying')
    start = time.time()
    for url in urls:
        start1 = time.time()
        t = get_url(url['tinyurl'], host)
        url['fetch_time'] = time.time()-start1
        print(t)
        if not (url['url']==t):
            print ('error actual {}  returned {}'.format(url['url'], t))
    end = time.time()
    duration_get = end-start
    return urls



#duration_create = get_create_tester(host)(urls[0])
#duration_get = get_fetch_tester(host)(urls[0])

#print ('create throughput {}'.format(duration_create/len(urls[0])))
#print ('get throughput {}'.format(duration_get/len(urls[0])))

total_urls = sum( (len (u) for u in urls ) ) 

# test make tiny url
urls_updated=[]
start = time.time()
with Pool(5) as p:
    urls_updated = p.map( test_create, urls)
end = time.time()
print(urls_updated)

create_duration=end-start
print("Creating tinyurls: elapsed time {}".format(create_duration))

## test url fetch
## warm up cache
with Pool(5) as p:
    d = p.map( test_get, urls_updated)

start = time.time()
with Pool(5) as p:
    d = p.map( test_get, urls_updated)
end = time.time()
print(d)

get_duration=end-start


print("Creating tinyurls: elapsed time {}".format(get_duration))


print ("Total urls {}".format( total_urls )) 
print ("Creating tinyurls throughput {}".format (total_urls/create_duration) )


print ("Fetch tinyurls throughput {}".format (total_urls/get_duration) )