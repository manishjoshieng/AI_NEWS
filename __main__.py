from flask import Flask, render_template, request
from collector import *
import os, threading, copy
from helper import *
from apscheduler.schedulers.background import BackgroundScheduler

IPADD  = os.environ.get("LOCAL_IP")
PORT   = os.environ.get("LOCAL_PORT")

app = Flask(__name__)

# Create a scheduler
scheduler = BackgroundScheduler()

# Schedule the update_cache function to run every hour
scheduler.add_job(updateCache, 'interval', hours=1)

# Start the scheduler when the Flask app starts
scheduler.start()


@app.route('/news',methods=['GET'])
def home():
    user_ip = request.remote_addr
    query_param = request.args.get('q')

    print(f"Request received from: {user_ip} with q:{query_param}")
    
    posts = getPosts()
    
    if posts is None or len(posts)==0:
        print("No news found")
    else:
        filtered_posts = posts.values()
        if query_param is not None:
            filtered_posts = [post for post in posts.values() if isContain(post , query_param)]
            if len(filtered_posts)==0:
                print("There is no post with given query")
                posts = getPosts(query=query_param)
                filtered_posts = posts.values()
    data = copy.deepcopy(sorted(filtered_posts, key=lambda post: strToDate(post.pubDate), reverse=True))

    for post in data:
        post.pubDate = dateToStr(strToDate(post.pubDate),FINAL_DATE_FORMATE)

    return render_template("index.html", posts=data)

@app.route("/news/about",methods=['GET'])
def about():
    return render_template("about.html")

@app.route("/news/contact",methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        sendmail(data)
        return render_template("feedback.html", name=data["username"].title())
    else:
        return render_template("contact.html")

@app.route("/news/<id>")
def show_post(id):
    post = copy.deepcopy(cache.getPost(id))
    post.pubDate = dateToStr(strToDate(post.pubDate),FINAL_DATE_FORMATE)
    return render_template("post.html", post=post)

@print_function_name
def start_server():
    thread = threading.Thread(target=updateCache)
    thread.start()
    app.run(host=IPADD, port=PORT, debug=True)

if __name__ == "__main__":
    start_server()
    

    
    


