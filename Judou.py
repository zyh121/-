import os
import json
import random  # 用于产生随机数
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *

class JudouWindow(Toplevel):

    def __init__(self):
        super().__init__()
        self.title("句读")
        self.resizable(0,0)
        self.geometry("710x400+370+100")
        self.iconbitmap('D:\\Npy\\Booktest\\favicon.ico')
        #全局变量
        self.judou = list()
        #创建句读界面
        self.Judou_GUI()

    def load_files(self):
        if not os.path.exists("D:\\BookAttic\\Judou.json"):
            showinfo("系统消息","提供的文件名不存在！")
        else:
            try:
                with open("D:\\BookAttic\\Judou.json","r",encoding='UTF-8') as f:
                    self.judou = json.load(f)
            except:
                showinfo("系统消息","读取文件时出错！")

    def Judou_GUI(self):
        #左部分
        self.ju = Label(self,text="句:",font="楷体 20 bold")
        self.ju.grid(row=0,column=0,sticky=W,pady=2,padx=5)
        self.ju_text = Text(self,height=10,)
        self.ju_text.grid(row=1,sticky=N+S+W+E,padx=5)
        self.dou = Label(self,text="读:",font="楷体 20 bold")
        self.dou.grid(row=2,sticky=W,pady=2,padx=5)
        self.dou_text = Text(self,height=10,)
        self.dou_text.grid(row=3,sticky=N+S+W+E,padx=5)
        
        #右部分
        self.redpic = PhotoImage(file="D:/Npy/Booktest/REDbtn.gif")
        self.redbutton = Button(self,image=self.redpic,command=self.Random_show)
        self.redbutton.grid(row=1,column=1,padx=10)
        self.bluepic = PhotoImage(file="D:/Npy/Booktest/BLUEbtn.gif")
        self.bluebutton = Button(self,image=self.bluepic,command=self.saveAndclear)
        self.bluebutton.grid(row=3,column=1,padx=10)

    #随机抽取一个已有的句读
    def Random_show(self):
        self.count = len(self.judou)
        if len==0:
            pass
        else:
            num = random.randint(1,self.count)
            self.ju_text.delete("1.0",END)
            self.dou_text.delete("1.0",END)
            key = str(self.judou.index(num).keys())[2:-3]
            val = str(self.judou.index(num).values())[2:-3]
            self.ju_text.insert(END,key)
            self.dou_text.insert(END,val)

    def saveAndclear(self):
        ju = self.ju_text.get("1.0",END)
        dou = self.dou_text.get("1.0",END)
        if ju == '\n':
            showinfo("提示","请输入[句]")
            return
        else:
            self.judou.append({ju:dou})
            try:
                with open("D:\\BookAttic\\Judou.json","w",encoding='UTF-8') as f:
                    json.dump(self.judou,f,ensure_ascii=False)
                self.ju_text.delete("1.0",END)
                self.dou_text.delete("1.0",END)
            except:
                showinfo("系统消息","保存失败！")

if __name__ == "__main__":
    C = JudouWindow()
    C.mainloop()
    
