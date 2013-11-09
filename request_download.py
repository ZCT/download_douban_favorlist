# coding=utf-8
import time
from threads import DistrubeThread, DownThread
import douban_favor
import get_locallist
import os


def TxtToDict(txt_file, my_dict):
    for line in txt_file:
        try:
            key, title, artist = line.split('\t')
            my_dict[int(key)] = (title, artist)
        except Exception:
            print "this line in the favorlist didn't match the format"+ line
            continue

def GetDownloadList(download_dict, target_dir):
##    douban_favor.InputFavor()          ## when test can cancel this line
    favor_txt = file("douban_favor.txt", 'r')
    favor_dict = dict()
    TxtToDict(favor_txt, favor_dict)

##    download_dict = favor_dict       ## this for test
##    return download_dict
    get_locallist.GetLocalMusic(target_dir)
    local_txt = file("mp3_name.txt",'r')
    local_dict = dict()
    TxtToDict(local_txt, local_dict)
    favor_keys = favor_dict.keys()
    local_key_set = set(local_dict.keys())
    for key in favor_keys:
        if key in local_key_set:
            pass
        else:
            download_dict[int(key)] = favor_dict[int(key)]
        
        
        
            
    
    

def main():
    target_dir = os.getcwd()
##    target_dir = current_dir+r'\song'
##    if os.path.exists(target_dir):
##        pass
##    else:
##        os.mkdir(target_dir)
        
    download_dict = dict()
    GetDownloadList(download_dict, target_dir)

    t1= DistrubeThread(download_dict)
    t1.start()
    time.sleep(2)
    t2 = DownThread(download_dict, target_dir)
    t2.start()
    

    
def test():
    mp3_txt = file("mp3_name.txt", 'r')
    download_dict = dict()
    count=0
    for line in mp3_txt:
        count += 1
        if count > 63:
            break
        key, title, artist = line.split('\t')
    download_dict[int(key)] = (title, artist)
    t1= DistrubeThread(download_list)
    t1.start()
    time.sleep(10)
    t2 = DownThread(download_list)
    t2.start    




if __name__=='__main__':
    main()
