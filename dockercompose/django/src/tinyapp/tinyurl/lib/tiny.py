
import hashlib
import logging 
import time
import random

from tinyurl.models import Url 

#enable logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

try:
    import redis
except ModuleNotFoundError:
    logging.error ("Redis module missing")

try:
    g_redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
except NameError:
    g_redis = None 


class UrlHandler():

    @staticmethod
    def get_tinyurl(originalurl):
        """Given a url, return tinyurl, create if necessary.
        Args:
            originalurl: url to shorten.

        Returns:
            Returns short url
        """        
     
        logging.debug("Creating short url for {}".format(originalurl))
        start = time.time()
        db_obj = UrlHandler._get_or_create_in_db(originalurl)
        end = time.time()
        logging.info("Tinurl created {} in {} in seconds".format(db_obj.shorturl, end-start))
        return db_obj.shorturl

    @staticmethod
    def _get_or_create_in_db(originalurl):
        """
        Helper function to get or create tiny url
        Generates 32 bit md5 hash and returns right most 6 characters as tiny url code
        In case of collision, it shifts left through the md5 hash until an available 6 character window is found
        Args:
            originalurl: Tthe url to shorten.

        Returns:
            Returns short url
        """            

        md5hash = hashlib.md5(originalurl.encode('utf-8')).hexdigest()
        shorturl = md5hash[-6:]
        obj, created = Url.objects.update_or_create(shorturl=shorturl, originalurl=originalurl, defaults={'originalurl':originalurl})
        
        # handle collisions, make 10 attempts
        # shift left through the md5 if the 6 character code chosen so far is taken by a different url
        max_tries = 16
        while obj.originalurl != originalurl and max_tries<=10:
            shorturl = md5hash[-6-max_tries:-max_tries]
            obj, created = Url.objects.update_or_create(shorturl=shorturl, originalurl=originalurl, defaults={'originalurl':originalurl})
            logging.info('Collision occured, {} resolution attempts so far'.format(max_tries))
            max_tries += 1

        return obj 

    @staticmethod
    def get_originalurl(tinurl):
        """
        Fetch original url
        Looks up the tinyurl code in Redis cache before going to Postgres database
        Args:
            tinurl: tiny url code.

        Returns:
            Returns the orginal url
        """    
        logging.debug ("Original url requested for {}".format(tinurl))
        
        # attempt to lookup  Redis cache
        start = time.time()
        originalurl = UrlHandler.redis_get(tinurl)
        if originalurl:
            logging.info ("Cache hit. Redis returned url {} in {} seconds".format(originalurl, time.time()-start))
            return originalurl

        logging.info ("Cache miss for {}".format(tinurl))
        # not in Redis, fetch from database
        url = None
        try:
            url = Url.objects.get(shorturl=tinurl)
            # cache the response
            UrlHandler.redis_set(tinurl, url.originalurl)        
        except Url.DoesNotExist:
            logging.error ("Invalid url code")
            return None

        logging.info ("Postgres returned url {} in {} seconds".format(url.originalurl, time.time()-start) )
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
