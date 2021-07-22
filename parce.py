from os import write
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from pytube import YouTube, Channel
import requests, time, os


URL = "https://www.youtube.com/results?search_query="
HEADERS = {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "accept" : "*/*"}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

#def get_video(url):
#    driver = webdriver.Chrome()
#    driver.get(url)  # Можно ждать до загрузки страницы, но проще подождать 10 секунд, их хватит с запасом
#    html = driver.page_source
#    soup = BS(html, "html.parser")
#    link = "https://www.youtube.com" + soup.find("a", class_="yt-simple-endpoint inline-block style-scope ytd-thumbnail").get("href")
#
#
#    yt.streams.get_by_itag(22).download("video", filename=yt.title)
#
#    return yt.title


def get_content(html):
    data = []
    soup = BS(html, "html.parser")
    print("soup for searh name")
    name = soup.find("yt-formatted-string",{"class":"style-scope ytd-channel-name"}).text
    print("name of channel: " + name)
    get_link = soup.find("a",{"class":"channel-link yt-simple-endpoint style-scope ytd-channel-renderer"}).get("href")
    print("парсинг ссылки со страницы: " + get_link)
    if get_link == None:
        link = "Ссылку найти не удалось"
    else:
        link = "https://www.youtube.com" + get_link
        print("link channel: " + link)
    c = Channel(link)
    print("Connect to channel, find 1st video: ", c.video_urls[0])
    yt = YouTube(c.video_urls[0])
    print("download video...")
    yt.streams.get_by_itag(18).download("video", filename=name)
    print("video is downloaded: " + "video/"+name+".mp4")
    b = os.path.getsize("video/"+name+".mp4")
    b = (b/1024)/1024
    print("video size:" + str(b))
    if b > 50:
        error = f"Размер видеоролика {yt.title} более 50 мбайт.\nТелеграм бот не может отправлять файлы более 50 мбайт"
        return error

    video_name = yt.title
    print("name video: " + video_name)

    print("search logo img..")
    pick_link = "https:" + soup.find("div", {"id":"avatar"}).find("img", {"id":"img"}).get("src")
    img = requests.get(pick_link)
    img_file = open("img/" + name + ".jpg", "wb")
    img_file.write(img.content)
    img_file.close()
    print("img is done")

    last_video = "video/" + name + ".mp4"
    print("make answer for user...")
    data.append({
        "channel_name": name,
        "link": link,
        "pick": "img/" + name + ".jpg",
        "video_name": video_name,
        "last_video": last_video
    })
    print("answer")
    print(data)
    return data

def parse(name):
    print("Init chrome")
    driver = webdriver.Chrome()
    driver.get(URL + name)
    html = driver.page_source
    print("check page")
    data = get_content(html)
    return data

#parse("Droider")

#<img id="img" class="style-scope yt-img-shadow" alt="" height="136" width="136" src="//yt3.ggpht.com/ytc/AKedOLRCpXDeP7nK8rFX-tHHRVkpRtQHk0fpwKx5SRCaLA=s176-c-k-c0x00ffffff-no-rj-mo">