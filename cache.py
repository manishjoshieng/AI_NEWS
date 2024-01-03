from datetime import datetime, timedelta
from schema import *
from collections import OrderedDict
import threading, json

from JsonHandler import *
from helper import *


cacheFileName = "/home/manish/Desktop/GITHUB/Python_bootcamp/Backend/AI_NEWS/Data/newsdataio.json"

class Cache:
    def __init__(self) -> None:
        self.article_id_map     =   {}
        self.article_date_map   =   {}
        self.lastUpdate         =   datetime.now()
        self.lock               =   threading.Lock()
        self.fileName           =   cacheFileName
        self.fileHandler        =   JsonHandler(cacheFileName)

        
        old_data = self.fileHandler.getFile()
        valid_time = datetime.now() - timedelta(days=1)
        recent_article = valid_time
        if old_data:
            if old_data.get("lastUpdate") is not None:
                self.lastUpdate = strToDate(old_data.get("lastUpdate"))
            posts = old_data.get("articles")
            for post in posts:
                post_time = strToDate(post["pubDate"])
                if valid_time < post_time:
                    if post_time > recent_article:
                        recent_article = post_time
                    self.addArticle(deserialize_post(post))
        self.updateCache()
        print("cache construction completed")

    @print_function_name
    def addArticle(self, post:Post)-> bool:
        with self.lock:
            print(f"Adding new article to cache: {post.article_id}")
            if post.article_id in self.article_id_map:
                print(f"Article already present")
                return False
            
            self.article_id_map[post.article_id] = post
            if post.pubDate not in self.article_date_map:
                self.article_date_map[post.pubDate] = {}
            
            self.article_date_map[post.pubDate][post.article_id] = post
            return True
        
    @print_function_name
    def isExpired(self, post:Post)->bool:
        with self.lock:
            valid_time = datetime.now() - timedelta(hours=24)
            post_time = strToDate(post.pubDate)
            if valid_time > post_time:
                return True
            return False
    
    @print_function_name
    def updateCache(self):
        print("Updating cache...")
        with self.lock:
            older_posts = []
            valid_time = datetime.now() - timedelta(hours=24)
            print(f"collecting post older than {dateToStr(valid_time)}")
            for publish_date, posts in self.article_date_map.items():
                publish_date_date = strToDate(publish_date)
                if publish_date_date < valid_time:
                    older_posts.extend(posts.values())
                
            print(f"collected older post {len(older_posts)}")

            for post in older_posts:
                print(f"Post removed from cache: {post.article_id}")
                self.article_id_map.pop(post.article_id)
                del self.article_date_map[post.pubDate][post.article_id]
                if len(self.article_date_map[post.pubDate]) == 0:
                    del self.article_date_map[post.pubDate]
            self.saveCacheData()
    
    @print_function_name
    def saveCacheData(self):
        print("saving file on disk")
        cache_data ={}
        cache_data["lastUpdate"] = dateToStr(self.lastUpdate)
        articles = [serialize_post(post) for post in self.article_id_map.values()]
        cache_data["articles"]   =  articles
        self.fileHandler.removeFile()
        self.fileHandler.updateFile(cache_data)
        print("saving file on disk completed")
    
    @print_function_name
    def getPosts(self)->dict:
        return self.article_id_map
    
    @print_function_name
    def getPost(self,id)->Post:
        return self.article_id_map.get(id)
    
    @print_function_name
    def isNotEmpty(self):
        if len(self.article_id_map) > 0:
            return True
        return False
