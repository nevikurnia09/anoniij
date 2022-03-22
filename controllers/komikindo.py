import json
import urllib
import tools
from bs4 import BeautifulSoup
baseURL = "https://komikindo.id/"

def index(request):
    response = tools.get(baseURL)
    
    resolve = {
        'status': 'success',
        'message': 'Welcome to Komikindo API',
        'statusCode': response.status_code,
    }
    
    return resolve

def home(request):
    response = tools.get(baseURL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    obj["menu"] = []
    mangas_menu = soup.find(id="menu-second-menu").find_all("li")
    for manga in mangas_menu:
        name = manga.find("a").text
        link = {
            'url': manga.find("a").get("href"),
            'endpoint': manga.find("a").get("href").replace(baseURL, "")
        }
        
        obj["menu"].append({ 'name': name, 'link': link })
        
    obj["body"] = {}
    mangas_menu = soup.find_all("section", {"class": "whites"})
    for manga in mangas_menu:
        if (manga.find(id="informasi")):
            continue
        
        popular = manga.find_all("div", {"class": "mangapopuler"})
        if (len(popular) > 0):
            obj["body"]["popular"] = []
            mangas = manga.find("div", {"class": "mangapopuler"}).find_all("div", {"class": "animepost"})
            for m in mangas:
                name = m.find("a", itemprop="url").get("title")
                thumb = m.find("img").get("src").split("?")[0]
                link = {
                    'url': m.find("a", itemprop="url").get("href"),
                    'endpoint': m.find("a", itemprop="url").get("href").replace(baseURL, "")
                }
                last_upload = m.find("span", {"class": "datech"}).text
                last_chapter = {
                    'name': m.find("div", {"class": "lsch"}).find("a").text,
                    'url': m.find("div", {"class": "lsch"}).find("a").get("href"),
                    'endpoint': m.find("div", {"class": "lsch"}).find("a").get("href").replace(baseURL, "")
                }
                obj["body"]["popular"].append({ 'name': name, 'thumb': thumb, 'link': link, 'last_upload': last_upload, 'last_chapter': last_chapter })
            continue
            
        latest = manga.find_all("div", {"class": "latestupdate-v2"})
        if (len(latest) > 0):
            obj["body"]["latest"] = []
            mangas = manga.find_all("div", {"class": "animepost"})
            for m in mangas:
                name = m.find("a", itemprop="url").get("title")
                thumb = m.find("img").get("src").split("?")[0]
                link = {
                    'url': m.find("a", itemprop="url").get("href"),
                    'endpoint': m.find("a", itemprop="url").get("href").replace(baseURL, "")
                }
                obj["body"]["latest"].append({ 'name': name, 'thumb': thumb, 'link': link })
            continue

    return obj

def daftar_komik(request, page):
    response = tools.get(baseURL + 'daftar-komik/page/' + str(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    mangas = soup.find_all("div", {"class": "animepost"})
    
    obj["mangas"] = []
    for manga in mangas:
        
        name = manga.find("a", itemprop="url").get("title")
        thumb = manga.find("img").get("src").split("?")[0]
        link = {
            'url': manga.find("a", itemprop="url").get("href"),
            'endpoint': manga.find("a", itemprop="url").get("href").replace(baseURL, "")
        }
        
        obj["mangas"].append({ 'name': name, 'thumb': thumb, 'link': link })
    
    obj["pagination"] = []    
    pagination = soup.find_all(class_="page-numbers")
    for page in pagination:
        name = page.text
        url = page.get("href")
        endpoint = None
        if (url):
            endpoint = url.replace(baseURL, "")
            
        obj["pagination"].append({'name': name, 'url': url, 'endpoint': endpoint })

    return obj

def komik_terbaru(request, page):
    response = tools.get(baseURL + 'komik-terbaru/page/' + str(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    mangas = soup.find_all("div", {"class": "animepost"})
    
    obj["mangas"] = []
    for manga in mangas:
        
        name = manga.find("a", itemprop="url").get("title")
        thumb = manga.find("img").get("src").split("?")[0]
        link = {
            'url': manga.find("a", itemprop="url").get("href"),
            'endpoint': manga.find("a", itemprop="url").get("href").replace(baseURL, "")
        }
        
        obj["mangas"].append({ 'name': name, 'thumb': thumb, 'link': link })
    
    obj["pagination"] = []    
    pagination = soup.find_all(class_="page-numbers")
    for page in pagination:
        name = page.text
        url = page.get("href")
        endpoint = None
        if (url):
            endpoint = url.replace(baseURL, "")
            
        obj["pagination"].append({'name': name, 'url': url, 'endpoint': endpoint })

    return obj

def komik(request, type, page):
    response = None
    if (type == "manga"):
        response = tools.get(baseURL + 'manga/page/' + str(page))
    elif (type == "manhua"):
        response = tools.get(baseURL + 'manhua/page/' + str(page))
    elif (type == "manhwa"):
        response = tools.get(baseURL + 'manhwa/page/' + str(page))
    elif (type == "smut"):
        response = tools.get(baseURL + 'konten/smut/page/' + str(page))
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    mangas = soup.find_all("div", {"class": "animepost"})
    
    obj["mangas"] = []
    for manga in mangas:
        name = manga.find("a").get("title")
        thumb = manga.find("img").get("src").split("?")[0]
        link = {
            'url': manga.find("a").get("href"),
            'endpoint': manga.find("a").get("href").replace(baseURL, "")
        }
        
        obj["mangas"].append({ 'name': name, 'thumb': thumb, 'link': link })
    
    obj["pagination"] = []    
    pagination = soup.find_all(class_="page-numbers")
    for page in pagination:
        name = page.text
        url = page.get("href")
        endpoint = None
        if (url):
            endpoint = url.replace(baseURL, "").replace("konten/", "komikk/")
            
        obj["pagination"].append({'name': name, 'url': url, 'endpoint': endpoint })

    return obj
    
def komik_detail(request, endpoint):
    prox = "https://komikindo-id.translate.goog/"
    proxq = "?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=id"
    response = tools.get(baseURL + endpoint)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    manga = soup.find(class_="postbody")
    obj["title"] = manga.find(class_="entry-title").text.replace("Komik ","")
    obj["thumb"] = manga.find(class_="thumb").find("img").get("src").split("?")[0]
    obj["alter"] = manga.find(class_="spe").find_all("span")[0].text.split(": ")[1].split(", ")
    obj["status"] = manga.find(class_="spe").find_all("span")[1].text.split(": ")[1]
    obj["author"] = manga.find(class_="spe").find_all("span")[2].text.split(": ")[1]
    obj["illustator"] = manga.find(class_="spe").find_all("span")[3].text.split(": ")[1]
    obj["grafis"] = manga.find(class_="spe").find_all("span")[4].text.split(": ")[1]
    obj["score"] = manga.find(itemprop="ratingValue").text
    
    obj["genres"] = []
    genres = manga.find(class_="genre-info").find_all("a")
    for genre in genres:
        name = genre.get("title")
        link = {
            'url': genre.get("href"),
            'endpoint': genre.get("href").replace(baseURL, "")
        }
        obj["genres"].append({ 'name': name, 'link': link })  
    
    obj["synopsis"] = manga.find(itemprop="description").text.split("\n")[1]
    
    obj["chapters"] = []
    chapters = manga.find(id="chapter_list").find_all(class_="lchx")
    for chapter in chapters:
        name = chapter.find("a").text
        url = chapter.find("a").get("href")
        endpoint = None
        if ("komikindo-id" in url):
            endpoint = url.replace(prox, "").replace(proxq, "")
        else:
            endpoint = url.replace(baseURL, "")
        link = { 'url': url, 'endpoint': endpoint }
        obj["chapters"].append({ 'name': name, 'link': link })
        
    
    return obj

def search(request, query):
    page = request.GET.get('page')
    if (page == None):
        page = 1
    response = tools.get(baseURL + 'page/' + str(page) + '/?' + urllib.parse.urlencode({'s': query}))
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    mangas = soup.find_all("div", {"class": "animepost"})
    
    obj["mangas"] = []
    for manga in mangas:
        name = manga.find("a").get("title")
        thumb = manga.find("img").get("src").split("?")[0]
        link = {
            'url': manga.find("a").get("href"),
            'endpoint': manga.find("a").get("href").replace(baseURL, "")
        }
        
        obj["mangas"].append({ 'name': name, 'thumb': thumb, 'link': link })
    
    obj["pagination"] = []    
    pagination = soup.find_all(class_="page-numbers")
    for page in pagination:
        name = page.text
        url = page.get("href")
        endpoint = None
        if (url):
            uri = url.split('/')
            if (len(uri) >= 5):
                 endpoint = f"search/{query}/?page={url.split('/')[4]}" 
            else:
                endpoint = f"search/{query}/?page=1" 
            
        obj["pagination"].append({'name': name, 'url': url, 'endpoint': endpoint })
    
    return obj

def chapter(request, endpoint):
    response = tools.get(baseURL + endpoint)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    obj = {}
    manga = soup.find("head")
    chapter_link = manga.find("link", {"type": "application/json"}).get("href")
    
    reschap = tools.get(chapter_link)
    res = json.loads(reschap.text)
    obj["title"] = res["title"]["rendered"]
    
    soupp = BeautifulSoup(res["content"]["rendered"], 'html.parser')
    obj["images"] = []
    imgs = soupp.find_all("img")
    for img in imgs:
        obj["images"].append(img.get("src"))
    
    nav = soup.find("div", {"class": "navig"}).find(class_="nextprev")
    obj["chapter"] = {}
    
    prev = nav.find(rel="prev")
    if (prev == None):
        obj["chapter"]["prev"] = None
    else:
        obj["chapter"]["prev"] = prev.get("href").replace(baseURL, "")
    
    nextq = nav.find(rel="next")
    if (nextq == None):
        obj["chapter"]["next"] = None
    else:
        obj["chapter"]["next"] = nextq.get("href").replace(baseURL, "")
    
    return obj