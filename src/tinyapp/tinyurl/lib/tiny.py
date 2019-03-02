
import short_url
from tinyurl.models import Url 

try:
    import redis
except ModuleNotFoundError:
    print ('Warning: You are running tinyapp without caching/redis')

try:
    g_redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
except NameError:
    g_redis = None 


class UrlHandler():

    @staticmethod
    def get_tinyurl(originalurl):
        """given a url, return tinyurl"""
        db_obj = UrlHandler._get_or_create_in_db(originalurl)
    
        return short_url.encode_url(db_obj.id) 

    @staticmethod
    def _get_or_create_in_db(originalurl):
        obj, created = Url.objects.update_or_create(originalurl=originalurl, defaults={'originalurl':originalurl})
        return obj 

    @staticmethod
    def get_originalurl(tinurl):
        
        id = short_url.decode_url(tinurl)
   
        # attempt to get from Redis cache
        originalurl = UrlHandler.redis_get(str(id))
        print ("Url id is {}. Redis returned {}".format(id, originalurl))

        if originalurl:
            return originalurl

        # not in Redis, fetch from database
        url = None
        try:
            url = Url.objects.get(id=id)
            print ("Url id is {}. Postgres returned {}".format(id, url.originalurl))
            # cache the response
            UrlHandler.redis_set(str(id), url.originalurl)        
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


#import redis
#r = redis.Redis(host='redis', port=6379, db=0)
#r.set('foo', 'bar')
#r.get('foo')
