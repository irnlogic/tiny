import urllib.request
import sys, time, argparse
import re 
from multiprocessing import Pool 



host = '35.230.2.53:8001'
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


def create_tinyurls(urls):
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
   

def test_fetch(urls):
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

def run_tests(count, num_processes, repeat_fetch, create_urls):
    print ("Number of processes1 {}".format(num_processes))
    urls = [ [{'url':'www.test.com/{}'.format(str(v*dataset))} for v in range(count) ] for dataset in range (1,1+num_processes)]
    total_urls = sum( (len (u) for u in urls ) ) 

    # test make tiny url
    urls_updated=[]
    start = time.time()

    print("\nTest url creation")
    if num_processes == 1:
        print('In process execution: creating urls')
        urls_updated = [create_tinyurls(u) for u in urls]
    else:
        print('Multi-process execution: creating urls')
        with Pool(num_processes) as p:
            urls_updated = p.map( create_tinyurls, urls)
    end = time.time()
    create_duration=end-start
    print("Creating tinyurls: elapsed time {}\n".format(create_duration))

    ## test url fetch
    ## warm up cache
    print ("\nWarming up cache")
    with Pool(num_processes) as p:
        d = p.map( test_fetch, urls_updated)

    print("\nTesting fetch")
    start = time.time()
    for _ in range(repeat_fetch):
        if num_processes == 1:
            print ('single threaded fetch')
            d = [test_fetch(u) for u in urls_updated]
        else:
            with Pool(num_processes) as p:
                d = p.map( test_fetch, urls_updated)
    end = time.time()
    print(d)

    get_duration=end-start

    print("\n----------- Test summary ---------------------------------")
    print("Creating tinyurls: elapsed time {}".format(get_duration))
    print ("Total urls {}".format( total_urls )) 
    print ("Creating tinyurls throughput {}".format (total_urls/create_duration) )
    print ("Fetch tinyurls throughput {} . ({} repeats)".format ((total_urls*repeat_fetch)/get_duration, repeat_fetch) )
    print("----------------------------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Run tiny performance tests")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--create", action="store_true")
    group.add_argument("-f", "--fetch", action="store_true")
    parser.add_argument("n", type=int, help="the number of creates or fetches")
    parser.add_argument("p", type=int, help="number of processes", default=1)
    parser.add_argument("repeat_fetch", type=int, help="number of repeat fetches", default=1)

    args = parser.parse_args()

    if args.create:
           print ("Perf test: create {} urls ".format(args.n))
    elif args.fetch:
           print ("Perf test: fetche {} urls".format(args.n))
    else:
        print ("Not a valid request")
        exit()

    num_processes = args.p

    run_tests(args.n, num_processes, args.repeat_fetch, True)

if __name__ == "__main__":
    main()