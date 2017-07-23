"""
YouDao Translate 有道翻译

email: zckuna@gmail.com

"""


import requests
import time
import random
import hashlib
import json


# content = input('PLEASE ENTER THE SENTENCE YOU NEED TO TRANSLATE: ')
url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom=null'

def __all__():
    
    print (['init', 'crawler'])
    
    
def init(text):
    
    content = text
    data = {}
    
    u = 'fanyideskweb'
    d = content
    f = str (int (time.time()*1000) + random.randint (1, 10))
    c = "rY0D^0'nM0}g5Mm1z%1G4"
    sign = hashlib.md5 ( ( u+d+f+c ).encode ('utf-8') ).hexdigest()
    
    data['i'] = content
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = u
    data['salt'] = f
    data['sign'] = sign
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CL1CKBUTTON'
    data['typoResult'] = 'true'
    
    return data


def crawler(text):
    
    data = init(text)
    
    ydResp = requests.post (url, data=data)
    
    result = json.loads(ydResp.text)
    try:
        translateResult = result['translateResult'][0][0]['tgt']
    except IndexError as e:
        pass
    
    return translateResult
    
  
"""
    
if __name__ == '__main__':
    
    text = input('PLEASE ENTER THE SENTENCE YOU NEED TO TRANSLATE: ')
    crawler(text)
"""
