import requests
from bs4 import BeautifulSoup
import logging
import time
from multiprocessing import Process




class playList:
    
    
    def __init__ (self):
        self.urls = []
        self.song_name = []
        self.song_id = []
        self.config()
        
        
        
    def config(self):
        '''
        云音乐飙升榜:19723756
        云音乐新歌榜:3779629
        网易原创歌曲榜:2884035
        云音乐热歌榜:3778678
        云音乐韩语榜:745956260
        云音乐ACG音乐榜:71385702
        云音乐古典音乐榜:71384707
        云音乐电音榜:10520166
        UK排行榜周榜:180106
        美国Billboard周榜:60198
        Beatport全球电子舞曲榜:3812895
        法国 NRJ Vos Hits 周榜:27135204
        KTV唛榜:21845217
        iTunes榜:11641012
        日本Oricon周榜:60131
        Hit FM Top榜:120001
        台湾Hito排行榜:112463
        中国TOP排行榜（港台榜）:112504
        中国TOP排行榜（内地榜）:64016
        香港电台中文歌曲龙虎榜:10169002
        '''
        listId = ['19723756', '3779629', '2884035', '3778678', '745956260', '71385702', '71384707', '10520166', '180106',
                       '60198', '3812895', '27135204', '21845217', '11641012', '60131', '120001', '112463', '112504', '64016',
                       '10169002']
        url = 'http://music.163.com/discover/toplist?id='
        for id in listId:
            self.urls.append( url+id )         
        
        
    def crawler (self, _=0):
        
        # resp = requests.get('http://music.163.com/discover/toplist?id=60198')
        for url in self.urls:
            yield requests.get(url)
            
        
    def parser (self, _=0):
        
        # INFO ('＊开始抓取并解析...')
        for resp in self.crawler():
            playlistSoup = BeautifulSoup(resp.text, 'html.parser')
                
            ulTag = playlistSoup.find_all('ul', attrs={'class': "f-hide"})[0]
            aTags = ulTag.find_all('a')
                
            for a in aTags:
                    
                self.song_id.append(a['href'].split('=')[1])
                self.song_name.append(a.get_text())
        
    
    # @property
    def result(self):
        return self.song_name, self.song_id
            
    
    def print_(self):
        
        for name, id in zip(self.song_name, self.song_id):
            with open('text.txt','a') as f: f.write(name + '\t' + id + '\n')
            print ('%s\t%s'% (name, id))
        f.close()
        
        
if __name__ == '__main__':
    
    list = playList()
   # p = Process(target=list.parser, args=('hello',))
   # p.start()
    #p.join()
    list.parser(12)
    list.print_()
        
        
        
        
        
        
        
        