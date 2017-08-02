from tkinter import *
from tkinter import messagebox


'''
Python GUI Calculator
Email:<zckuna@gmail.com>
'''

__author__ == 'ZCkun'


class Calculator:
    
    def __init__(self):
        
        self.app = Tk()
        self.app.title('Calculator') # 窗口标题
        self.app.geometry("275x250+500+270") # 窗口大小和打开在桌面的位置
        self.ui()
        
    
    def ui(self):
        
        # 编辑框
        self.out = StringVar()
        self.in_out_put = Entry(self.app, textvariable=self.out)
        self.in_out_put.config(font=100)
        self.in_out_put.place(x=0, y=10, width=275, height=30)
        
        '''
        # 清空
        self.clean = Button(self.app, text='CLEAN', command=lambda: self.cle())
        self.clean.place(x=210, y=10, width=60, height=30)
        '''
        
        # 加减乘除按钮 Addition, subtraction, multiplication, division
        # + /addition
        self.addition = Button(self.app, text='+', command=lambda: self.input('+'))
        self.addition.config(font=50)
        self.addition.place(x=0, y=50, width=60, height=40)
        # - /subtraction
        self.subtraction = Button(self.app, text='-', command=lambda: self.input('-'))
        self.subtraction.config(font=50)
        self.subtraction.place(x=70, y=50, width=60, height=40)
        # x /multiplication
        self.multiplication = Button(self.app, text='*', command=lambda: self.input('*'))
        self.multiplication.config(font=50)
        self.multiplication.place(x=140, y=50, width=60, height=40)
        # / /division
        self.division = Button(self.app, text='/', command=lambda: self.input('/'))
        self.division.config(font=50)
        self.division.place(x=210, y=50, width=60, height=40)
        
        
        # 数字按钮 [1,2,3,4,5,6,7,8,9,0]
        self.nine = Button(self.app, text='9', command=lambda: self.input(9))
        self.nine.config(font=60)
        self.nine.place(x=0, y=100, width=60, height=40)

        self.eigt = Button(self.app, text='8', command=lambda: self.input(8))
        self.eigt.config(font=60)
        self.eigt.place(x=70, y=100, width=60, height=40)
        
        self.seven = Button(self.app, text='7', command=lambda: self.input(7))
        self.seven.config(font=60)
        self.seven.place(x=140, y=100, width=60, height=40)
        
        # 6 /six
        self.six = Button(self.app, text='6', command=lambda: self.input(6))
        self.six.config(font=60)
        self.six.place(x=0, y=140, width=60, height=40)  
        
        # 5 /five
        self.five = Button(self.app, text='5', command=lambda: self.input(5))
        self.five.config(font=60)
        self.five.place(x=70, y=140, width=60, height=40)
        
        # 4 /four
        self.four = Button(self.app, text='4', command=lambda: self.input(4))
        self.four.config(font=60)
        self.four.place(x=140, y=140, width=60, height=40)
        
        # 3 /three
        self.three = Button(self.app, text='3', command=lambda: self.input(3))
        self.three.config(font=60)
        self.three.place(x=0, y=180, width=60, height=40)
        
        # 2 /two
        self.two = Button(self.app, text='2', command=lambda: self.input(2))
        self.two.config(font=60)
        self.two.place(x=70, y=180, width=60, height=40)
        
        # 1 /one
        self.one = Button(self.app, text='1', command=lambda: self.input(1))
        self.one.config(font=60)
        self.one.place(x=140, y=180, width=60, height=40)
            
        # . /point
        self.point = Button(self.app, text='.', command=lambda: self.input('.'))
        self.point.config(font=60)
        self.point.place(x=210, y=100, width=60, height=40)
        
        # 0 /zero
        self.zero = Button(self.app, text='0', command=lambda: self.input(0))
        self.zero.config(font=60)
        self.zero.place(x=210, y=140, width=60, height=40)
        
        # = /equal
        self.equal = Button(self.app, text='=', command=lambda: self.cal())
        self.equal.config(font=60)
        self.equal.place(x=210, y=180, width=60, height=40)
        
        self.a = ''
      
    def input(self,_):
        
        
        self.a += str(_)
        self.result = None
          
        self.out.set(_)
          
    # 清空
    def cle(self):
        
        self.a = ''
          
    # 计算
    def cal(self):
        
        if '+' in self.a:
            self.result = int((self.a.split('+')[0])) + int((self.a.split('+')[1]))
        elif '-' in self.a:
            self.result = int((self.a.split('-')[0])) - int((self.a.split('-')[1]))
        elif '*' in self.a:
            self.result = int((self.a.split('*')[0])) * int((self.a.split('*')[1]))
        elif '/' in self.a:
            self.result = int((self.a.split('/')[0])) / int((self.a.split('/')[1]))
            
        messagebox.showinfo('OUTPUT', self.result)
        self.cle()
        
        
    def run(self):
        
        self.app.mainloop()
        
        
        
if __name__ == '__main__':
    
    cal = Calculator()
    cal.run()