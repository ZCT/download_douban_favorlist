# coding: utf-8
 
import urllib, urllib2, cookielib, re, json, eyed3, os
import Cookie

##import download
##import download_album

##RE_ALBUM = re.compile(r'/subject/\d+/')

def html_decode(html):
    #return html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    import HTMLParser
    return HTMLParser.HTMLParser().unescape(html)
 
def get(myurl, cookie,mp3_file):
##    urllib2.install_opener(opener)
    req = urllib2.Request(myurl)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    req.add_header('Cookie', cookie)
    req.add_header('Referer', 'http://douban.fm/mine')
    content = urllib2.urlopen(req, timeout=20).read()
    data=[]
    for s in json.loads(content)['songs']:
        sid = s['id']
##        album = RE_ALBUM.search(s['path']).group(0)
##        try:
    ##            print "song:" + html_decode(s['title']) + "\nsinger:" + html_decode(s['artist']) + "\nalbum:" + s['path']
        data.append(html_decode(s['id']).encode('utf-8')+'\t')
        data.append(html_decode(s['title']).encode('utf-8')+'\t')
        data.append(html_decode(s['artist']).encode('utf-8')+'\n')
##        except:
##            print 'song...'
##        try:
##            ssid = download_album.get_ssid(album, sid)
##            if download.handle(sid, ssid):
##                print 'succeed!\n\n'
##            else:
##                print 'fail!\n\n'
##        except:
##            print 'fail!\n\n'
    mp3_file.writelines(data)
 
def InputFavor():
    cookie = raw_input('cookie:')
    user_id_sign = raw_input('window.user_id_sign:')
    c = Cookie.SimpleCookie()
    c.load(cookie)
    ck = c.get('ck').value
    bid = c.get('bid').value
    spbid = urllib.quote(user_id_sign+bid)
    url = 'http://douban.fm/j/play_record?ck=' + ck + '&type=liked&start=%d&spbid='
    print 'you should enter the pages you want to download'
    page0 = int(raw_input('page from:'))
    page1 = int(raw_input('page to:'))
    mp3_file=file('douban_favor.txt','w')
    for i in range(page1-page0+1):
        get(url%((i+page0-1)*15)+spbid, cookie,mp3_file)
        

if __name__ == '__main__':
    InputFavor()

