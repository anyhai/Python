#hisory
#20180609        HuangHai        First Version
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox as messagebox
from  tkinter import ttk  
import os
import re
import pylab

i=1
root = Tk()
re_fun = re.compile(r'([0-9]*x(\*\*[0-9]+)?)([\+\-][0-9]*x(\*\*[0-9]+)?)*([\+\-][0-9]+)?')  #匹配多项式
re_subfun = re.compile(r'([0-9]*)(x)(\*\*[0-9]+)?')   #解析子式
re_plusminus = re.compile(r'[\+\-]')      #分割多项式
re_multi= re.compile(r'(.*)[0-9]x(.*)')   #乘法识别
re_mi= re.compile(r'(.*)[/^](.*)')
s_s=None
pylab.grid()

class App(Frame):
    def __init__(self, master=None):
        self.subDir=IntVar()                        #类变量放前面
        Frame.__init__(self, master)
        self.master.title('文件查找工具')
        self.master.geometry('800x320') 
        self.pack()
        self.createWidgets()    
        
    def createWidgets(self):
        self.fileLabel = Label(self,text="文件名包含:", font=20)
        self.fileLabel.grid(row=1, column=1, padx=20, pady=20)
        
        self.fileNameInput = Entry(self, text="输入文件名", font=20)
        self.fileNameInput.grid(row=1, column=2, padx=20, pady=20)
        
        self.DLabel = Label(self,text="目录:", font=20)
        self.DLabel.grid(row=2, column=1, padx=20, pady=20)
        
        self.DNameInput = Entry(self, text="输入目录", font=20)
        self.DNameInput.grid(row=2, column=2, padx=20, pady=20)
        
        self.subDirCheckButton = Checkbutton(self, text='包含子目录', variable=self.subDir, font=16)
        self.subDirCheckButton.grid(row=2, column=3, padx=20, pady=20)
        self.subDirCheckButton.select() 
        
        self.browseDirButton = Button(self, text='选择目录', command=self.browseDir, font=20)
        self.browseDirButton.grid(row=2, column=4, padx=20, pady=20)
        
        #self.alertButton = Button(self, text='Find File', command=self.file_find(os.path.abspath('.')))
        self.alertButton = Button(self, text='开始查找', command=self.file_find, font=20, bg='green')       #这里的command函数不能加括号， 如果加括号就直接调用了
        self.alertButton.grid(row=3, column=2, padx=20, pady=20)
        
        self.quitButton = Button(self, text='退出', command=self.quit, font=20)
        self.quitButton.grid(row=3, column=3, padx=20, pady=20)
        
        self.fileLabel = Label(self,text="输入函数:", font=20)
        self.fileLabel.grid(row=4, column=1, padx=20, pady=20)
        
        #self.funInput = Entry(self, text='input the function', font=20)
        #self.funInput.grid(row=4, column=2, padx=20, pady=20, columnspan=2, ipadx=100)
        #self.funInput.insert(10, 'f(x)=x^3-50x^2+3x+6')
        
        self.funButton = Button(self, text='画图', command = self.drawFun, font=20)
        self.funButton.grid(row=4, column=4, padx=20, pady=20)
        
        self.funHistoryCombo = ttk.Combobox(self, text='hisory', font=20)
        self.funHistoryCombo['values']=('f(x)=x^3-50x^2+3x+6')
        self.funHistoryCombo.current(0)
        self.funHistoryCombo.bind("<<ComboboxSelected>>",self.getHistory)  #绑定事件
        self.funHistoryCombo.grid(row=4, column=2, padx=20, pady=20, columnspan=2, ipadx=100)
        
    def browseDir(self):                      #可以通过窗口指定目录
        initialdir = os.path.abspath('.')
        self.dir = askdirectory(initialdir=initialdir, title="Select Dir to search")
        if self.dir:
            self.DNameInput.delete(0, END)
            self.DNameInput.insert(0, self.dir)  

    def getHistory(self, *argv):
        pass
        
    def insertHistory(self, s):                #记录历史输入
        l=list(self.funHistoryCombo['values'])
        if s not in l:
            l.insert(0,s)
            self.funHistoryCombo['values'] = l        
            
    def drawFun(self):                        #画图主函数
        global re_fun
        global s_s
        s=self.funHistoryCombo.get() or 'f(x)=x^3-50x^2+3x+6'
        self.insertHistory(s)
        s_y=s.split('=')[0]
        s_x=s.split('=')[1]
        s_s=str(s_x)
        s_m=self.replace_mi(s_s)
        s_s=self.insert_multiply(s_m)
        s_x_sub = re_plusminus.split(s_x)      #使用正则表达式以+-作分割符取到多项式的每个单项
        with open("C:\haihu\Python\MyCode\GUI_paint.txt", "w",encoding='utf-8') as f:         #打开文件写入结果
            f.write('原始函数：'+str(s)+'\n')
            f.write('多项式  ：'+str(s_x)+'\n')
            f.write('幂识别  ：'+str(s_m)+'\n')
            f.write('乘法识别：'+str(s_s)+'\n')
            for i in s_x_sub:
                f.write(str(i)+'\n')
        pylab.plot(range(0,100),list(map(self.myeval, range(0,100))))
        pylab.xmin=-10000
        pylab.show()
        
    def insert_multiply(self, s):           #插入乘法符号
        global re_multi
        result=re_multi.search(s)
        if(result==None):
            return s
        else:
            sub=result.groups()
            for i in sub:
                s0 = self.insert_multiply(s[0:len(str(sub[0]))+1])
                return s0 + '*' + s[len(str(sub[0]))+1:]

    def replace_mi(self, s):                 #替换幂指数符号
        return s.replace('^', '**') 
         
    def myeval(self, x):                     #使用eval函数实现字符串到表达式的转换
        global s_s
        return eval(str(s_s))
        
    def file_find_1(self, s, path, f):       #实现查找功能
        #i=1
        total = 0
        global i
        for x in os.listdir(path):
            if os.path.isfile(os.path.join(path,x)) and (os.path.splitext(x)[0].find(s)>=0):  #这里isfile必须使用全路径判断
                #print('Dir: %s, file %d: %s' %(path, i, x))
                f.write('Dir: '+path+', file '+str(i)+': '+x+'\n')
                i = i+1
                total += 1
            elif os.path.isdir(os.path.join(path,x)):
                if self.subDir.get():                #checkbutton要使用get函数获得值
                    total+=self.file_find_1(s, os.path.join(path,x),f)
        return total

    def file_find(self):                 #查找入口函数
        global i
        '''
        try:
            f = open("F:\Python\Code\MyCode\GUI.txt", "w+",encoding='utf-8')
        except FileNotFoundError as e:
            f = open("F:\Python\Code\MyCode\GUI.txt", "w",encoding='utf-8')
        finally:
            f = open("F:\Python\Code\MyCode\GUI.txt", "w+",encoding='utf-8')
        '''
        s = self.fileNameInput.get()
        d = self.DNameInput.get() or os.path.abspath('.')
        with open("C:\haihu\Python\MyCode\GUI.txt", "w",encoding='utf-8') as f:         #打开文件写入结果
            f.write('Searching file name include \"'+s+'\"\n')
            total = self.file_find_1(s, d, f)
            f.write('Find '+str(total)+ ' files in '+ d)
        #f.close()
        i=1
        messagebox.showinfo('Message', 'Find %s files in %s, subDir=%s' % (total,d, self.subDir.get()))

app=App()
#app.master.title('My App')
#app.master.geometry('1000x500') 
app.mainloop()