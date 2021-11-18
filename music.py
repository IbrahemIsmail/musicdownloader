from __future__ import unicode_literals
import youtube_dl
from selenium import webdriver
from bs4 import BeautifulSoup
from os import system
import sys
import os
import time 

pathToSave = "C:/Users/Ibrahem/Music/Music/"

def titleCase(s):
    '''
    A function to convert the given song name to title case.
    The default function in Python convert the words 'the', 'and', 'of', etc.
    And I find that annoying
    '''

    l = s.split()
    str = l[0][0].upper() + l[0][1:]
    
    for word in l[1:]:
        if word not in ['in', 'the', 'for', 'of', 'a', 'at', 'an', 'is', 'and']:
            str += '+' + word[0].upper() + word[1:]
        else:
            str += '+' + word
    print(str)
    return str

def getVidID(title):
    '''
    This function gets the ID of the Video you have to download.
    '''
    URL = 'https://www.youtube.com/results?search_query='
    search = title + '+audio'
    searchQuery = '+'.join(search.split())
    searchURL = URL + searchQuery
    print(searchURL)
    driver = webdriver.Chrome()
    driver.get(searchURL)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "lxml")
    vidID = soup.find_all(id="video-title")[0]['href']
    vidTitle = soup.find_all(id="video-title")[0].text.strip()
    return ["https://www.youtube.com"+vidID, vidTitle, vidID]

def getLink(link):
    print(link)
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(2)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "lxml")
    vidID = link[32:]
    vidTitle = soup.find_all("yt-formatted-string", {'class':['style-scope', 'ytd-video-primary-info-renderer']})[3].text.strip()
    return [link, vidTitle, vidID]

def download(song):
    print("Downloading " + song.title())
    i=0
    vidLink, vidTitle, vidID = getVidID(song)

    new_file = pathToSave+ song.title() + '.mp3'
    # old_file = 'C:/Users/ibrax/Desktop/Uni/Random/musicDownloader/'+vidTitle+'-'+vidID[9:]
    old_file = os.getcwd()+'\\'+vidTitle+'-'+vidID[9:]
    extentions = ['.webm', '.m4a']
    ydl_opts = {
        'format': 'bestaudio/best'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([vidLink])
    print((old_file+extentions[i]).replace('?', '').replace('//', '_'))
    while not os.path.exists((old_file+extentions[i]).replace('?', '').replace('//', '-')):
        i=i+1
    print((old_file+extentions[i]).replace('?', '').replace('//', '_'))
    old_file=(old_file+extentions[i]).replace('?', '').replace('//', '_')
    os.rename(old_file, new_file)
    print("Downloaded " + song.title() + "\n") 

def downloadLink(link):
    print("Downloading " + link)
    i=0
    vidLink, vidTitle, vidID = getLink(link)
    print('THISS THE VID TITLE ======>', vidTitle)
    print('THISS THE VID ID ======>', vidID)
    new_file = pathToSave+ vidTitle.title() + '.mp3'
    # old_file = 'C:/Users/ibrax/Desktop/Uni/Random/musicDownloader/'+vidTitle+'-'+vidID
    old_file = os.getcwd()+'\\'+vidTitle+'-'+vidID[9:]
    extentions = ['.webm', '.m4a']
    ydl_opts = {
        'format': 'bestaudio/best'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([vidLink])
    while not os.path.exists((old_file+extentions[i]).replace('?', '')):
        i=i+1
    os.rename(old_file, new_file)

    print("Downloaded " + link + "\n") 

def main():
    print('-------------------------------------------------------------')
    if (len(sys.argv) == 3 and (sys.argv[1] == '-f' or sys.argv[1] == '-F')):
        for song in open(sys.argv[2]).readlines():
            download(song.rstrip())
    
    elif (len(sys.argv) == 3 and (sys.argv[1] == '-lf' or sys.argv[1] == '-LF')):
        for link in open(sys.argv[2]).readlines():
            downloadLink(link)
    
    elif (len(sys.argv) == 3 and (sys.argv[1] == '-l' or sys.argv[1] == '-L')):
        for link in sys.argv[2:]:
            downloadLink(link)

    else:
        for song in sys.argv[1:]:
            download(song)

if __name__ == '__main__':
    main();