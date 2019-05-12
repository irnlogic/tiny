
import hashlib

from tinyurl.models import Url 

try:
    import redis
except ModuleNotFoundError:
    print ('Warning: You are attempting to run tinyapp without caching/redis module')

try:
    g_redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
except NameError:
    g_redis = None 


class UrlHandler():

    @staticmethod
    def get_tinyurl(originalurl):
        """given a url, return tinyurl"""
        db_obj = UrlHandler._get_or_create_in_db(originalurl)
    
        return db_obj.shorturl

    @staticmethod
    def _get_or_create_in_db(originalurl):
        #print ("Original url is {} type {}".format(originalurl, type(originalurl)))
        #shorturl = short_url.encode_url(44) # originalurl
        shorturl = hashlib.md5(originalurl.encode('utf-8')).hexdigest()[-6:]
        obj, created = Url.objects.update_or_create(shorturl=shorturl, originalurl=originalurl, defaults={'originalurl':originalurl})
        return obj 

    @staticmethod
    def get_originalurl(tinurl):
        
        # attempt to get from Redis cache
        originalurl = UrlHandler.redis_get(tinurl)
        print ("Short url is {}. Redis returned {}".format(tinurl, originalurl))

        if originalurl:
            return originalurl

        # not in Redis, fetch from database
        url = None
        try:
            url = Url.objects.get(shorturl=tinurl)
            print ("Short url is {}. Postgres returned {}".format(tinurl, url.originalurl))
            # cache the response
            UrlHandler.redis_set(tinurl, url.originalurl)        
        except Url.DoesNotExist:
            print ("Invalid url code")
            return None

        return url.originalurl

    @staticmethod
    def redis_get(key):
        global g_redis
        if g_redis:
            return g_redis.get(key)
        else:
            return None

    @staticmethod
    def redis_set(key, value):
        global g_redis
        if g_redis:
            g_redis.set(key, value)
