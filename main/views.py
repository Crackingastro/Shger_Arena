import pyrebase
from django.shortcuts import render
from . import creds
from collections import OrderedDict

firebaseConfig = creds.f

# Intilizing the firebase Configration
firebase = pyrebase.initialize_app(firebaseConfig)

# The way the data is stored in the database
# Data = {"ID": Normal_ID, "title":Title_news, "full":Full_news, "image":url_image, "type":news_type}

# Intilizing an empty Dictonaries to store values passed to the HTML
Trending = {}
Hot = {}
Latest = {}

# Intilizing an empty array for the main news 
main_news = []

hash = {}
# type_of_news_list = ["trending","hot","normal","latest"]

db = firebase.database()

all_users = db.child("news_info").get()

counter = 0
length = 0
for user in all_users.each():
    length += 1


for user in all_users.each():
    value = user.val()

    # Data sent to the front
    temp = value.get("type")

    if temp == "trending":
        Trending[user.key()] = [value.get("title"),value.get("image")] 
    

    if temp == "hot":
        Hot[user.key()] = [value.get("title"),value.get("image")]
    if temp == "latest" or temp == "normal":
        Latest[user.key()] = [value.get("title"),value.get("image")] 

    # Data stored for the next page
    hash[user.key()] = value

    if counter == length-1:
        main_news.append(value.get("title"))
        main_news.append(value.get("image"))
        main_news.append(user.key())


    counter += 1

Trending = OrderedDict(reversed(list(Trending.items())))
Hot = OrderedDict(reversed(list(Hot.items())))
Latest = OrderedDict(reversed(list(Latest.items())))

def index(response):
    return render(response, "main/index.html", {"Trending":Trending, "Hot":Hot,"Latest":Latest,"main":main_news})
    
def pages(response,id):
    value = hash[id]

    info_sent = []
    info_sent.append(value.get("full"))
    info_sent.append(value.get("title"))
    info_sent.append(value.get("image"))

    
    return render(response, "main/page.html", {"info":info_sent,"Trending":Trending})

def handler404(request, exception):
    return render(request, 'main/404.html')

def handler500(request):
    return render(request, 'main/404.html')     