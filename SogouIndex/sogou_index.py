import requests
import re
import json
import multiprocessing
import sys
import os
from prettyPrint import (INFO, ERROR)
import time



def E(text): ERROR('\033[0;31m{}\033[0m'.format(text))
def I(text): INFO('\033[0;32m{}\033[0m'.format(text))
def G(text, end='\n'): print('\033[0;32m{}\033[0m'.format(text), end=end)
def Y(text, end='\n'): print('\033[0;33m{}\033[0m'.format(text), end=end)
def R(text, end='\n'): print('\033[0;31m{}\033[0m'.format(text), end=end)


try:
    dataType = sys.argv[2]
except IndexError as e:
    dataType = 'all'
try:
    kwdNamesStr = sys.argv[1]
except IndexError as e:
    R('＊请输入正确的关键字')
    Y('''Search for heat index from Sogou.
    
    Usage:
        index <Names> <Data> <TimePeriod>
        

    ''') # 无视这个(:。。。。
    sys.exit()
try:
    timePeriodType = sys.argv[3]
except IndexError as e:
    timePeriodType = 'MONTH'


class sogouIndex:
    
    def __init__(self):

        self.url = 'http://index.sogou.com/getRenderData'
        all = 'SEARCH_ALL'
        pc = 'SEARCH_PC'
        wap = 'SEARCH_WAP'
        self.params = {
                'kwdNamesStr': kwdNamesStr,
                'timePeriodType': timePeriodType.upper(),
                'dataType': all,
                'queryType': 'INPUT',
                }
        self.settings()
        
        self.pv = []
        self.date = []
        self.ratioWapChain = None # 移动环比
        self.ratioWapMonth = None # 移动同比
        self.avgWapPv = None # 移动搜索指数
        self.ratioChain = None # 整体环比
        self.ratioMonth = None # 整体同比 
        self.kwdName = None # 关键字名
        self.avgPv = None # 整体搜索指数/平均值
        
        
    def settings(self):
        '''初始化必要参数 initialization parameters.'''
        #I('＊Start Settings...')
        G('＊开始配置参数...', end=' ')
        
        all = 'SEARCH_ALL'
        pc = 'SEARCH_PC'
        wap = 'SEARCH_WAP'
        
        if dataType == 'pc' or dataType == 'PC': self.params['dataType'] = pc
        elif dataType == 'all' or dataType == 'ALL': self.params['dataType'] = all
        elif dataType == 'wap' or dataType == 'WAP': self.params['dataType'] = wap
 
        G('OK')   
            
            
    def crawler(self, _=''):
        '''开始抓取,返回JSON格式 start crawler, return JSON type results.'''
        
        #self.settings()
        try:
            #I('＊Start Requesting...')
            #I('＊开始请求...')
            G('＊开始请求...', end=' ')
            result = requests.get(self.url, params=self.params)
            if result.status_code != 200:
                R('ERROR 状态码:{}'.format(result.status_code))
                sys.exit()
            G('OK')
            return result.json()
        except ValueError as e:
            R('转换JSON格式出错，请稍后再试!')
            sys.exit()
            
            
        
    def parser(self):
        '''解析结果 parser results.'''
        #I('＊Start Parsing...')
        pool = multiprocessing.Pool(1)
        result = pool.map(self.crawler, ('_',))[0]
        # result = self.crawler()
        G('＊开始解析...', end=' ')
        if result:
            pvList = result['data']['pvList'][0]
            infoList = result['data']['infoList'][0]
            
            for pv in pvList:
                self.pv.append(pv['pv'])
                self.date.append(pv['date'])
                
            self.ratioWapChain = infoList['ratioWapChain']
            self.ratioWapMonth = infoList['ratioWapMonth']
            self.avgWapPv = infoList['avgWapPv']
            self.ratioChain = infoList['ratioChain']
            self.ratioMonth = infoList['ratioMonth']
            self.kwdName = infoList['kwdName']
            self.avgPv = infoList['avgPv']
            
            G('OK')
            

    def prettyPrint(self):
        '''漂亮输出 Beautiful Print.'''
        
        if not self.date: self.parser()
        
        date_start = str(self.date[0]) # 获取日期开头
        start = date_start[:4] + '-' + date_start[4:-2] + '-' + date_start[-2:] # 格式化
        
        date_end = str(self.date[-1]) # 获取日期结尾
        end = date_end[:4] + '-' + date_end[4:-2] + '-' + date_end[-2:]
        
        
        print ('''\n\033[0;36m关键字\033[0m：\033[0;33m{kwd}\033[0m\n\033[0;36m时间\033[0m：\033[0;33m{date}\033[0m\n\033[0;36m整体搜索指数/平均值\033[0m：\033[0;32m{avgPv}\033[0m\n\033[0;36m整体同比\033[0m：\033[0;{rm_color}m{ratioMonth}\033[0m\n\033[0;36m整体环比\033[0m：\033[0;{rc_color}m{ratioChain}\033[0m\n\033[0;36m移动搜索指数\033[0m：\033[0;{awp_color}m{avgWapPv}\033[0m\n\033[0;36m移动同比\033[0m：\033[0;{rwm_color}m{ratioWapMonth}\033[0m\n\033[0;36m移动环比\033[0m：\033[0;{rwc_color}m{ratioWapChain}\033[0m\n'''
               .format(
                   kwd = self.kwdName,
                   date = start + '~' + end,
                   avgPv = self.avgPv,
                   rm_color = 32 if float(self.ratioMonth.split('%')[0]) >= 0 else 31, # 判断数据是否大于等于０来决定输出的颜色是红色还是绿色
                   ratioMonth = self.ratioMonth,
                   rc_color = 32 if float(self.ratioChain.split('%')[0]) >= 0 else 31,
                   ratioChain = self.ratioChain,
                   awp_color = 32 if self.avgWapPv >= 0 else 31,
                   avgWapPv = self.avgWapPv,
                   rwm_color = 32 if float(self.ratioWapMonth.split('%')[0]) >= 0 else 31,
                   ratioWapMonth = self.ratioWapMonth,
                   rwc_color = 32 if float(self.ratioWapChain.split('%')[0]) >= 0 else 31,
                   ratioWapChain = self.ratioWapChain
                   ))
        
        # 以下是保存文件代码 The following is to save the file code. 
        if os.path.exists('sogouPv.txt'): os.remove('sogouPv.txt')
        
        with open('sogouPv.txt','a') as f:
            f.write('日期\t\t\t指数\n')
            for pv, date in zip(self.pv, self.date):
                d = str(date)[:4] + '-' + str(date)[4:-2] + '-' + str(date)[-2:]
                f.write(d + "\t\t" + str(pv) + '\n')
            f.close()
            
        if os.path.exists('sogouPv.txt'):
            if open('sogouPv.txt','r').read():
                print('\033[0;37m详细信息已写入当前目录文件sogouPv.txt(:\n\033[0m')
            else:
                R('信息写入失败，请稍后再试):\n')
        else:
            R('文件保存失败，请稍后再试):\n')
    
if __name__ == '__main__':
    
    sogou = sogouIndex()
    sogou.parser()
    sogou.prettyPrint()
    
    
    
    
    
