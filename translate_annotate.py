"""
Translate Annotate 文件注释翻译

email: zckuna@gmail.com

"""


from YouDao import Translate
import sys


def main():
    
    try :
        fn = sys.argv[1]
    except IndexError as e:
        print ('请正确的输入文件名):')
        return
            

        _file = fn.split ('.')[1]

    try:
        f = open (str(fn), 'r')
    except FileNotFoundError as e:
        print ('没有找到该文件，请重试):')
        return 
        
    result = []
    mid1 = ' // '
    mid2 = ' # '
    tmp_lines = lines = f.readlines()
    
    
    import re
    num = int()
    
    if _file == 'java' or _file == 'c' or _file == 'cpp' or _file == 'js' :
        
        for i in lines:
            
            s = re.findall ('//', i, re.S)
            if s == []: pass
            else :
                
                head = i.split ('//')[0]
                tail = i.split ('//')[-1]
                tail = Translate.crawler (tail)
                content = head + mid1 + tail
                result.append (content + '\n')
                tmp_lines[num] = content
            
            num += 1
    
    elif _file == 'py' :
        
        for i in lines :
    
            s = re.findall ('#', i, re.S)
            if s == [] : pass
            else :
                
                # num = tmp_num
                head = i.split ('#')[0]
                tail = i.split ('#')[-1]
                print (tail)
                tail = Translate.crawler (tail)
                content = head + mid2 + tail
                result.append (content + '\n')
                tmp_lines[num] = content + '\n'
                
            num += 1
            
    elif _file == '' :
        pass
            
            
    f.close()
    if result == []:
        print ('翻译出错，请重试！')
        return 1
    else :
        print ('注释翻译完成，正在替换内容...')

    f2 = open (str(fn), 'w')
    for i in tmp_lines:
    
        f2.write (i)
    
    f2.close()
    
    print ('替换完成，已保存至文件{}'.format (fn))
    
    
if __name__ == '__main__':
    
    main()
