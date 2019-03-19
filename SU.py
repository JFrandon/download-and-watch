from html.parser import HTMLParser
from html.entities import name2codepoint
import requests
import re
import os 
import csv
import shlex, subprocess
import time

global minS
global minE
global proc
proc = None

if not(os.path.isfile('episode.csv')):
    minS = int(input("Current Season: "))
    minE = int(input("Current Episode: "))
else:
    with open('episode.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            minS=int(row[0])
            minE=int(row[1])

def downloadAndQueue(link):
    fileName =  re.search(r's\d+e\d+.*', link).group(0)
    season = int(re.search(r's\d+', link).group(0)[1:])
    episode = int(re.search(r'e\d+', link).group(0)[1:])
    global proc
    print(link+'='+fileName+'_'+str(season)+'_'+str(episode))
    if ((season > minS) or (season==minS and episode>minE)):
        if not(os.path.isfile(fileName)):
            print(link)
            r = requests.get(link, allow_redirects=True)
            print("ok1")
            open(fileName, 'wb').write(r.content)
            print("ok2")
        if not(proc is None) :
            while proc.poll()==None:
                time.sleep(1)
        proc = subprocess.Popen(shlex.split('"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe" --fullscreen '+ fileName+' vlc://quit'))
        with open('episode.csv', mode='w') as episode_file:
            episode_file.write(str(season)+","+str(episode))



class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "source":
            for attr in attrs:
                if attr[0]=='src':
                    downloadAndQueue(attr[1])


parser = MyHTMLParser()
parser.feed(requests.get('https://stevenuniver.se').text)

