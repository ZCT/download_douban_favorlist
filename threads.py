# coding = utf-8
import Queue

import threading
import requests
import re
from bs4 import BeautifulSoup
import json
import Queue
import time
import eyed3
import glob
import sys
import os

g_task_lock = threading.Lock()
g_task_queue = Queue.Queue()
g_put_complete = False
g_thread_num = 1


class DistrubeThread(threading.Thread):
    def __init__(self, download_dict): ## download list is a dict
        threading.Thread.__init__(self)
        self.download_dict_ = download_dict
        self.search_url_ = 'http://music.baidu.com/search?key='
        self.link_url_ = 'http://ting.baidu.com/data/music/links?songids='
        self.baud_url_ = '&rate=320'
        


    def run(self):
        exception_key =[]
        global g_task_queue  
        global g_task_lock
        global g_put_complete
        g_put_complete = False
        for key in self.download_dict_.keys():
            try:
##                time.sleep(1)   ## prevent the yanzhenma
                search_html = requests.get(self.search_url_ + self.download_dict_[key][0])
                soup = BeautifulSoup(search_html.text)
                container = soup.find('div', {'class':'search-result-container'})
                result = container.find('li',{'id': 'first_song_li'})

                song_list = json.loads(result['data-songitem'])
                song_item = song_list['songItem']
                song_sid = song_item['sid']

                link_html = requests.get(self.link_url_ + str(song_sid) + self.baud_url_)
                link_list = json.loads(link_html.text)
                link_url = link_list['data']['songList'][0]['showLink']
            except Exception:
                if key:
                    print str(key)+"UnicodeEncodeError"
                else:
                    print " bingo by baidu music , should change the ip!!!!!!!!"
                continue
            g_task_lock.acquire()
            g_task_queue.put((key, link_url))
            g_task_lock.release()
        g_put_complete = True
        
##            except Exception:
##                print int(key)
##                print self.download_list_[key][0]
##                exception_key.append(key)
##                continue
     
class DownThread(threading.Thread):
    def __init__(self, download_dict, target_dir):
        global g_thread_num
        threading.Thread.__init__(self)
        self.download_dict_ = download_dict
        self.thread_tasks_ = 5
        self.target_dir_ = target_dir
##        g_thread_num +=1             ## assert it is atomic operation
    def run(self):
        "get a job and process it. if the link contains the pan.baidu.com ???"
        global g_task_queue  
        global g_task_lock 
        global g_put_complete
        global g_thread_num
        time.sleep(1)
        while True:
            
            g_task_lock.acquire()
            if(g_task_queue.empty()):
                if g_put_complete:
                    print "exit download thread--------->:):):)"
                    g_task_lock.release()
                    break
                else:
                    print ".........wait the distrubethread"
                    g_task_lock.release()
                    time.sleep(2)
                    continue
##            if(g_task_queue.qsize() > (self.thread_tasks_*g_thread_num)):    ## there has a problem!!
##                g_thread_num +=1
##                g_task_lock.release()
##                print "--!--!--!--!--!create a new thread to download music --!--!--!--!--!--!--!--!--!!"
##                download_t = DownThread( self.download_dict_, self.target_dir_)
##                download_t.start()
##                g_task_lock.acquire()
            song_info = g_task_queue.get() ## song info is yuanzu , 0 is key, 1 is url
            g_task_lock.release()
            song = requests.get(song_info[1])
            try:
                with open(self.target_dir_+'\\'+self.download_dict_[int(song_info[0])][0].decode('utf-8')+".mp3",'wb') as mp3:
                    mp3.write(song.content)
                    mp3_tag = eyed3.load(mp3.name)
                    mp3_tag.tag.track_num = int(song_info[0])
                    mp3_tag.tag.title = self.download_dict_[int(song_info[0])][0].decode('utf-8')
                    mp3_tag.tag.artist = self.download_dict_[int(song_info[0])][1].decode('utf-8')
                    mp3_tag.tag.save()
                    mp3.close()
                    print self.download_dict_[int(song_info[0])][0].decode('utf-8')+ " =======>was downloaded ^_^_^_^"
            except Exception:                       ## exception is because the rul is pan.baidu.com
                    print self.download_dict_[int(song_info[0])][0].decode('utf-8')+"has link such as pan.baidu.com"
                    mp3.close()
                    os.remove(mp3.name)
                    continue
            
        g_thread_num -= 1
                
                
        
        
                
        

