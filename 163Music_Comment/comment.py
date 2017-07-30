from playList import playList
from bs4 import BeautifulSoup
import requests
from prettyPrint import (INFO, DEBUG, ERROR)
import json
import time
import multiprocessing
from multiprocessing import Process
import xlsxwriter



class Comment:
    
    def __init__(self):
        
        self.urls = []
        self.list = playList()
        self.song_ids = None
        self.song_names = None
        self.urls = []
        self.data = {}
        
        self.contents = []
        self.nicknames = []
        self.times = []
        self.likedCounts = []
        self.userIds = []
        
        self.config()
    
        
    def config(self):
        
        parser = multiprocessing.Process (target=self.list.parser(), args=('1',))
        parser.start()
        parser.join()
        
        self.song_ids = self.list.song_id
        self.song_names = self.list.song_name
        
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}'
        self.urls = [url.format(id) for id in self.song_ids]
        
        self.data.update({
            'params': 'W+TI/laknMAGViFvmayiK5OPLiugaSMvzqOGH2kSOnQE7EYGALsbDjhS8dCsRlfbqZMQkJU8ubKhOfltwYVr3EAypYPjtSHf8NMm7H0sMIg1nf9YClge+TU8yJJRN+H439yA8B1crtgTvAp6XQwUVA7awo/rxSacMFC4nTTjkYI/k/2vnez9O/TQrRZMg1cPre3G9Q52fBDLt1ddIKtneVRDc4/aVd1Rz4eWiACov6s=',
            'encSecKey': '8b0e0477d1301115cee862bf4389fa42ae316a8f66af2c10c3be54bc0d68aecd4c532a01f78930586440b219b4996e85f7940bf91732558c9829ee10e3bdd12062bcd9d1d0b0c70f4b6793ca6dd8de5c14c1d74353796afdd882a55ffe538116ac476619066a3a9cfaeb92f92096ad446f2ed73c3fd6d076228960416e6ff34e',
            })
        
        
    def crawler(self):
        
        response = []
        number = 1
        
        for name, url in zip(self.song_names, self.urls):
            
            if number == 5: return response
            
            INFO ('＊开始请求第{}首歌-{}...'.format(number, name))
            resp = requests.post(url, data=self.data)
            
            if resp.status_code == 200:
                try:
                    response.append(resp.json()['hotComments'])
                    number += 1
                except ValueError as e:
                    ERROR(e)
                    continue
                
            else: continue
        
        return response
    
            
    def parser(self, x='hello'):
        #num = 0
        _ = self.crawler()
        
        if _:
            for results in _:
                """
                content = []
                nickname = []
                userId = []
                likedCount = []
                time = []
                if num == 5: return None
                num += 1
                """
                for result in results:
                    
                    # print (result)
                    self.contents.append (result['content'])
                    self.nicknames.append (result['user']['nickname'])
                    self.userIds.append (result['user']['userId'])
                    self.likedCounts.append (result['likedCount'])
                    self.times.append (int(str(result['time'])[:-3]))
                    
                    
                    print ('用户: {}\n用户ID: {}\n评论时间: {}\n内容: {}\n赞: {}'.format (
                        result['user']['nickname'],
                        result['user']['userId'],
                        time.strftime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(str(result['time'])[:-3])))),
                        result['content'],
                        result['likedCount'],
                        ))
                    print()
                    
                print ('--'*50)

            # self.contents.append(content)
            # self.nickname.append(nickname)
            # self.userIds.append(userId)
            # self.likedCounts.append(likedCount)
            # self.times.append(time)
        
    
    def save_xls(self, fn='163Music_Comment.xls'):
        
        _all = [
            self.contents,
            self.nicknames,
            self.times,
            self.likedCounts,
            self.userIds
        ]
        
        book = xlsxwriter.Workbook(fn)
        sheet = book.add_worksheet('Comment')
        
        
        for x, _ in enumerate(_all):
            
            length = len(_)
            for content, y in zip(_, range(0, length)):
                sheet.write(y+1, x, content)
                
        book.close()
    
    
    def print_(self):
        
        for name, id, time, content, liked in zip(
                                                self.nickname,
                                                self.userIds,
                                                self.times,
                                                self.contents,
                                                self.likedCount
                                                    ):
            print('用户名:', name, '\n')
            print('用户id:', id, '\n')
            print('时间:', time, '\n')
            print('内容:', content, '\n')
            print('赞:', liked, '\n')
            
    
    
    
        
if __name__ == '__main__':
    
    c = Comment()
    
    parse = Process (target=c.parser, args=('hello',))
    # save = Process (target=c.save_xls, args=('163Music_Comment.xls',))
    
    parse.start()
    # save.start()
    
    parse.join()
    # save.join()
    
    # c.print_()
    c.save_xls()   

