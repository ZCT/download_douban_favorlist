# -*- coding: utf-8 -*-

import os
import eyed3
import glob
import sys
import requests



def GetLocalMusic(target_dir):
    mp3_txt =file("mp3_name.txt",'w')
    data=[]
    only_txt = glob.glob(target_dir+r'\*'+'.mp3')
    for i in only_txt:
        try:
            mp3_tag = eyed3.load(i)
            key = mp3_tag.tag.track_num     ## sid is string?
            artist=mp3_tag.tag.artist
            title=mp3_tag.tag.title
            data.append(str(key[0]))
            if title:
                title_split =title.split(u'（')
                data.append('\t'+ title_split[0].encode('utf-8'))
            if artist:
                data.append('\t'+artist.encode('utf-8'))
        except Exception:
            continue
    mp3_txt.writelines(data)
    mp3_txt.close()

def main():
    GetLocalMusic()


if __name__ == '__main__':
    main()
