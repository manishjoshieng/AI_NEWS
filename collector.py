import requests,re,time
import os, threading
from datetime import datetime, timedelta
from schema import Post
from bs4 import BeautifulSoup
from cache import *
from helper import *

END_POINT = "https://newsdata.io/api/1/news"
MAX_CHARS = 140
MAX_POST  = 30


collecting_data = False
cache = Cache()
cache_lock = threading.Lock()

@print_function_name
def mark_collecting_data(val= True):
    global collecting_data
    with cache_lock:
        collecting_data = val

@print_function_name
def remove_html_tags(input_string):
    soup = BeautifulSoup(input_string, "html.parser")
    text_content = soup.get_text()
    return text_content
@print_function_name
def process(post:Post)->Post:
    # if post.content is not None:
    #     post.content = remove_html_tags(post.content)
    if post.description is not None:
        post.description = remove_html_tags(post.description)
    if post.description is not None and len(post.description) > MAX_CHARS:
        post.description = post.description[:MAX_CHARS] +"..."
    return post
@print_function_name
def isContain(post:Post, q:str):
    # print(f"checking post with query {q}",post.title,post.description)
    q = remove_html_tags(q)
    words = q.split()
    for q in words:
        pattern = re.compile(r'\b' + re.escape(q) + r'\b', re.IGNORECASE)
        if post.title and bool(re.search(pattern, post.title)):
            return True
        if post.description and bool(re.search(pattern, post.description)):
            return True
        if post.content and bool(re.search(pattern, post.content)):
            return True
    return False


@print_function_name
def updateCache(category="BUSINESS", country= "in", timeframe=24):
    global cache
    
    param = {}
    param["timeframe"]  =   timeframe
    param["category"]   =   category
    param["country"]    =   country
    param["language"]   =   "en"

    new_data = []
    max_allowed_request = MAX_POST/10
    try:
        param["apikey"]  = os.environ.get("NEWSDATAIO")
        print("Fatching articles from newsdata.io")
        response = requests.get(url=END_POINT,params=param)
        response.raise_for_status()
        max_allowed_request-=1
    except Exception as e:
        print(f"Exception Message: {str(e)}")
    else:
        filtered_data = [{k: v for k, v in post.items() if k in Post.__annotations__} for post in response.json()["results"]]
        new_data = [process(Post(**post)) for post in filtered_data]
        next_page = response.json().get("nextPage")
        total_posts = response.json().get("totalResults")
        print(f"Total posts: {total_posts}")
        print(f"next page {next_page}")
        
        for post in new_data:
            cache.addArticle(post)
        
            
        while next_page is not None and max_allowed_request > 0:
            print(f"processing page: {next_page}")
            param["page"] = next_page
            try:
                print("Fatching articles from newsdata.io")
                response = requests.get(url=END_POINT,params=param)
                response.raise_for_status()
                max_allowed_request-=1
            except Exception as e:
                print(f"Exception Message: {str(e)}")
            else:
                filtered_data = [{k: v for k, v in post.items() if k in Post.__annotations__} for post in response.json()["results"]]
                new_data = [process(Post(**post)) for post in filtered_data]
                next_page = response.json().get("nextPage")
                
                for post in new_data:
                    cache.addArticle(post)
                        
    cache.updateCache()
    cache.lastUpdate = datetime.now()



@print_function_name
def getPosts(query=None, category="BUSINESS", country= "in", timeframe=24)->dict:
    global cache
    valid_till = cache.lastUpdate + timedelta(hours=1)
    valid_time = dateToStr(valid_till)
    current_time = dateToStr(datetime.now())
    
    if cache.isNotEmpty() and valid_till > datetime.now():
        print(f"Returning cached data, cache valid till{valid_time}. current time{current_time}")
        return cache.getPosts()
    
   
        
    param = {}
    param["timeframe"]  =   timeframe
    param["category"]   =   category
    param["country"]    =   country
    param["language"]   =   "en"

    if query is not None:
        param["q"] = query
   
    if cache.isNotEmpty() and valid_till > datetime.now():
        print(f"Returning cached data, cache valid till{valid_time}. current time{current_time}")
        return cache.getPosts()

    new_data = []
    max_allowed_request = MAX_POST/10
    try:
        param["apikey"]  = os.environ.get("NEWSDATAIO")
        print("Fatching articles from newsdata.io")
        response = requests.get(url=END_POINT,params=param)
        response.raise_for_status()
        max_allowed_request-=1
    except Exception as e:
        print(f"Exception Message: {str(e)}")
    else:
        filtered_data = [{k: v for k, v in post.items() if k in Post.__annotations__} for post in response.json()["results"]]
        new_data = [process(Post(**post)) for post in filtered_data]
        next_page = response.json().get("nextPage")
        total_posts = response.json().get("totalResults")
        print(f"Total posts: {total_posts}")
        print(f"next page {next_page}")
        
        for post in new_data:
            cache.addArticle(post)
        
            
        while next_page is not None and max_allowed_request > 0:
            print(f"processing page: {next_page}")
            param["page"] = next_page
            try:
                print("Fatching articles from newsdata.io")
                response = requests.get(url=END_POINT,params=param)
                response.raise_for_status()
                max_allowed_request-=1
            except Exception as e:
                print(f"Exception Message: {str(e)}")
            else:
                filtered_data = [{k: v for k, v in post.items() if k in Post.__annotations__} for post in response.json()["results"]]
                new_data = [process(Post(**post)) for post in filtered_data]
                next_page = response.json().get("nextPage")
                
                for post in new_data:
                    cache.addArticle(post)
                        
    cache.updateCache()
    cache.lastUpdate = datetime.now()
    return cache.getPosts()    