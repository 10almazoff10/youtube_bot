from os import write
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from pytube import YouTube, Channel
import requests, os


URL = "https://www.youtube.com/results?search_query="

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
