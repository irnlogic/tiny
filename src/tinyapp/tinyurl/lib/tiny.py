
import short_url
from tinyurl.models import Url 
import redis

g_redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
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
        global g_redis

        id = short_url.decode_url(tinurl)
        
        originalurl = g_redis.get(str(id))
        print ("Url id is {}. Redis returned {}".format(id, originalurl))
        if originalurl:
            return originalurl

        url = Url.objects.get(id=id)
        print ("Url id is {}. Postgres returned {}".format(id, url.originalurl))
        g_redis.set(str(id), url.originalurl)
        return url.originalurl


#import redis
#r = redis.Redis(host='redis', port=6379, db=0)
#r.set('foo', 'bar')
#r.get('foo')
