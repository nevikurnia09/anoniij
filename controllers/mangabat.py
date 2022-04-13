from urllib.parse import urlparse
import tools
from bs4 import BeautifulSoup
baseURL = "https://m.mangabat.com/"

def index(request):
    response = tools.get(baseURL)
    
    return { 'success': True, 'statusCode': response.status_code }

def home(request):
    response = tools.get(f"{baseURL}m")
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    main = soup.find(class_="body-site")
    
    obj = {}
    obj["title"] = "Home"
    
    obj["popular"] = []
    popular = main.find(id="owl-slider").find_all(class_="item")
    for manga in popular:
        name = manga.find("a").text
        thumb = manga.find("img").get("src")
        url = manga.find("a").get("href")
        endpoint = url.replace(baseURL, "")
        
        chapter_name = manga.find_all("a")[1].text
        chapter_url = manga.find_all("a")[1].get("href")
        chapter_endpoint = chapter_url.replace(baseURL, "")
        
        obj["popular"].append({
            'name': name,
            'thumb': thumb,
            'url': url,
            'endpoint': endpoint,
            'chapter': {
               'name': chapter_name,
               'url': chapter_url,
               'endpoint': chapter_endpoint
            }
        })
        
    obj["latest"] = []
    latest = main.find_all(class_="content-homepage-item")
    for manga in latest:
        name = manga.find(class_="item-img").get("title")
        thumb = manga.find("img").get("src")
        score = manga.find(class_="item-rate").text
        url = manga.find(class_="item-img").get("href")
        endpoint = url.replace(baseURL, "")
        
        arr_chapter = []
        chapters = manga.find_all(class_="item-chapter")
        for chapter in chapters:
            chapter_name = chapter.find("a").text
            chapter_url = chapter.find("a").get("href")
            chapter_endpoint = chapter_url.replace(baseURL, "")

            arr_chapter.append({ 'name': chapter_name, 'url': chapter_url, 'endpoint': chapter_endpoint })
        
        obj["latest"].append({
            'name': name,
            'thumb': thumb,
            'url': url,
            'endpoint': endpoint,
            'score': '⭐' + score,
            'chapters': arr_chapter
        })
            
    return obj

def comic(request, endpoint):
    response = tools.get(f"{baseURL}{endpoint}")
    soup = BeautifulSoup(response.text, "html.parser")
    
    is404 = soup.find(style="font: 700 22px sans-serif;")
    if is404 is not None and "404" in is404.text:
        response = tools.get(f"https://read.mangabat.com/{endpoint}")
        soup = BeautifulSoup(response.text.replace("https://read.mangabat.com/", baseURL), "html.parser")
        is404 = soup.find(style="font: 700 22px sans-serif;")
        
        if is404 is not None and "404" in is404.text:
            return { 'success': False, 'statusCode': 404 }
        
    obj = {}
    main = soup.find(class_="body-site")
    
    obj['name'] = main.find(class_="story-info-right").find("h1").text
    obj['thumb'] = main.find(class_="info-image").find("img").get("src")
    obj['alter'] = main.find(class_="variations-tableInfo").find_all("tr")[0].find(class_="table-value").text
    
    obj["authors"] = []
    authors = main.find(class_="variations-tableInfo").find_all("tr")[1].find(class_="table-value").find_all("a")
    for author in authors:
        author_name = author.text
        author_url = author.get("href")
        author_endpoint = author_url.replace(baseURL, "")
        
        obj["authors"].append({ 'name': author_name, 'url': author_url, 'endpoint': author_endpoint })
    obj["status"] = main.find(class_="variations-tableInfo").find_all("tr")[2].find(class_="table-value").text
    
    obj["genres"] = []
    genres = main.find(class_="variations-tableInfo").find_all("tr")[3].find(class_="table-value").find_all("a")
    for genre in genres:
        genre_name = genre.text
        genre_url = genre.get("href")
        genre_endpoint = genre_url.replace(baseURL, "")
        
        obj["genres"].append({ 'name': genre_name, 'url': genre_url, 'endpoint': genre_endpoint })
    
    info_extends = main.find(class_="story-info-right-extent").find_all("p")
    for info in info_extends:
        key = info.find(class_="stre-label").text.split(":")[0].lower().strip().replace(" ", "_")
        value = info.find(class_="stre-value").text
        
        obj[key] = value
    
    main.find(class_="panel-story-info-description").find("h3").decompose()
    obj["synopsis"] = main.find(class_="panel-story-info-description").text.strip()
    
    obj["chapters"] = []
    chapters = main.find(class_="row-content-chapter").find_all("li")
    for chapter in chapters:
        name = chapter.find("a").text
        date = chapter.find(class_="chapter-time text-nowrap").text
        url = chapter.find("a").get("href")
        endpoint = url.replace(baseURL, "")
        
        obj["chapters"].append({ 'name': name, 'date': date, 'url': url, 'endpoint': endpoint })
        
    return obj

def chapter(request, endpoint):
    response = tools.get(f"{baseURL}{endpoint}")
    soup = BeautifulSoup(response.text, "html.parser")
    
    is404 = soup.find(style="font: 700 22px sans-serif;")
    if is404 is not None and "404" in is404.text:
        response = tools.get(f"https://read.mangabat.com/{endpoint}")
        soup = BeautifulSoup(response.text, "html.parser")
        is404 = soup.find(style="font: 700 22px sans-serif;")
        
        if is404 is not None and "404" in is404.text:
            return { 'success': False, 'statusCode': 404 }
    
    obj = {}
    
    obj["title"] = soup.find(class_="panel-chapter-info-top").find("h1").text.capitalize()
    
    obj["chapters"] = []
    chapters = soup.find(class_="container-chapter-reader").find_all("img")
    for chapter in chapters:
        image = chapter.get("src").replace("https://", "")
        uri = f"https://cdn-mangabat.katowproject.workers.dev/{image}"
        
        obj["chapters"].append(uri)
        
    return obj
    
    
    
    