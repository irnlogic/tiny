
import short_url
from tinyurl.models import Url 


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
        url = Url.objects.get(id=id)
        return url.originalurl


#import redis
#r = redis.Redis(host='redis', port=6379, db=0)
#r.set('foo', 'bar')
#r.get('foo')
'