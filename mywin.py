import os
import json
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *

from PIL import Image, ImageTk

import Suibi
import Judou

class MainWindow(Tk):

    def __init__(self):
        super().__init__()
        self.title("书阁二楼")
        self.geometry("615x510+370+100")
        self.resizable(0,0)
        #全局变量
        self.Bookname = {}
        #自动加载文件
        self.inspect_file()
        self.load_files()
        #现有分类及分类对应的索引
        self.class_item = list(self.Bookname.keys())
        self.class_index ={}
        #加载主界面
        self.setup_GUI()

    #检查存档是否被改动
    def inspect_file(self):
        if not os.path.exists("D:\\BookAttic\\Bookname.json"):
            showinfo("⚠提示","书籍信息被改动或删除！")

    #加载信息至self.Bookname
    def load_files(self):
        try:
            with open ("D:\\BookAttic\\Bookname.json",mode="r",encoding='UTF-8') as fd:
                self.Bookname=json.load(fd)
        except:
            showinfo("系统消息","文件读取出现异常")


    #构建主界面GUI
    def setup_GUI(self):
        
        #在菜单中建立保存按键
        self.Menu = Menu(background="Black",foreground="Gold")
        self.Menu.add_command(label="保存",command=self.save)
        self.config(menu=self.Menu)
        # 建立插入栏
        self.namelab = Label(text="书名：")
        self.namelab.grid(row=0, column=0, padx=5, pady=3, sticky=E)
        self.nameEntry = Entry()
        self.nameEntry.grid(row=0, column=1, sticky=W + E, padx=5, pady=3)
        self.tiplab = Label(text="批注：")
        self.tiplab.grid(row=0, column=2, sticky=E)
        self.tipEntry = Entry()
        self.tipEntry.grid(row=0, column=3, sticky=W + E, padx=5, pady=3)
        # 建立insert按钮
        self.inbtn = Button(text="添加", command=self.insertItem)
        self.inbtn.grid(row=0, column=4, padx=5, pady=3)

        # 建立Treeview,可以有多项选择
        self.tree = Treeview(columns="tips", selectmode=BROWSE)
        self.tree.heading("#0", text="书籍")
        self.tree.heading("tips", text="批注")
        self.tree.column("tips", anchor=CENTER)
        self.tipGUI_Door = 0
        
        #self.class_item = list(self.Bookname.keys())
        self.tree.tag_configure("groundcolor",background="lemonchiffon")
        for x in range(len(self.Bookname)):
            i=x
            self.allkeys = self.Bookname.get(self.class_item[x])
            x = self.tree.insert("",index=END,text=self.class_item[x],tags=("groundcolor"))
            self.class_index[self.class_item[i]] = x 
            for k in self.allkeys:
                self.tree.insert(x,index=END,text=list(k.keys()),values=list(k.values()))

        self.tree.bind("<<TreeviewSelect>>",self.getdata)
        self.tree.grid(row=1, column=0, columnspan=5, padx=15, sticky=W + E + N + S)
            
        self.rmbtn = Button(text="删除", command=self.removeItem, width=16)
        self.rmbtn.grid(row=2, column=2, padx=5, pady=3)


        self.yscrollbar = Scrollbar(orient=VERTICAL, command=self.on_scroll)
        self.yscrollbar.grid(row=1, column=5, sticky=S + W + E + N)
        self.yscrollbar.config(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscrollbar.set)

        # 插入分隔图片
        self.image = Image.open("D:\Python\PYTHON\My Programe\image.jpg")
        self.flowerpic = ImageTk.PhotoImage(self.image)
        self.labelf = Label(image=self.flowerpic)
        self.labelf.grid(row=3, column=0, columnspan=6)
        # 下部分增加按钮
        self.btnadd = Button(text="增  加\n分  类",command=self.add_class_GUI,)
        self.btnadd.grid(row=4, column=1,padx=5,pady=30,)
        self.btnMclass = Button(text="转  移\n分  类",command=self.moveToclass_GUI)
        self.btnMclass.grid(row=4,column=2,pady=30,)
        self.btnset = Button(text="句\n读")
        self.btnset.grid(row=4, column=3, pady=30,)
        self.btnpen = Button(text="记  录\n随  笔")
        self.btnpen.grid(row=4, column=4, pady=30,)

    #实现数据的保存
    def save(self):
        try:
            with open("D:\\BookAttic\\Bookname.json",'w',encoding='UTF-8') as f:
                json.dump(self.Bookname, f, ensure_ascii=False)
            showinfo("⊙ω⊙","保存成功！")
        except:
            showinfo("呜呜呜","储存信息时出错！")

    #实现删除功能
    def removeItem(self): 
        self.ids = self.tree.selection()
        for id in self.ids:
            del_class = self.tree.item(id,"text")
            self.tree.delete(id)
            #删除相关的数据
            del self.Bookname[del_class]
            self.class_item.remove(del_class)
            del self.class_index[del_class]

    #构建修改备注GUI
    def addtip_GUI(self):
        self.attributes("-disabled",1)
        self.tl = Toplevel()
        self.tl.protocol("WM_DELETE_WINDOW",self.this)
        self.tl.resizable(0,0)
        self.tl.title("修改备注")
        self.tl.geometry("518x140+500+300")
        self.thistip = StringVar()
        self.tipE = Entry(self.tl,textvariable=self.thistip)
        self.tipE.pack(anchor=CENTER,fill=X,padx=15,pady=40)
        #显示已有的备注
        self.tipE.insert(0,self.final_tip)
        self.Cabtn = Button(self.tl,text="取消",command=self.exit_tl)
        self.Cabtn.pack(anchor=S,side=RIGHT,padx=5,pady=5)
        self.OKbtn = Button(self.tl,text="确定",command=self.addtips)
        self.OKbtn.pack(anchor=S,side=RIGHT,pady=5)

    #获取表格数据/指向备注GUI
    def getdata(self,event):
        for item in self.tree.selection():
            self.item_key = self.tree.item(item,"text")
            self.this_tip = self.tree.item(item,"values")
            self.final_tip = str(self.this_tip)[2:-3]
        if self.item_key in self.Bookname:
            pass
        elif self.tipGUI_Door == 0 :
            self.addtip_GUI()
            self.nowclass = self.findkey()
        else:
            self.nowclass = self.findkey()

    #退出功能窗口的处理
    def exit_tl(self):
        self.attributes("-disabled",0)
        self.tl.destroy()
    def exit_ad(self):
        self.attributes("-disabled",0)
        self.ad.destroy()

    #寻找字典上一级(数据处理)
    def findkey(self):
        for key,val in self.Bookname.items():
            if isinstance(self.Bookname[key],list):
                can = self.Bookname[key]
                for book in can:
                    if self.item_key in book:
                        return key

    #实现修改备注功能
    def addtips(self):
        item_text = self.tipE.get()
        book_list= self.Bookname[self.nowclass]
        for i in book_list:
            if list(i.keys())[0] == self.item_key:
                i[self.item_key] = item_text
                #更新界面
                self.tree.item(self.tree.selection(),values=item_text) 
        #保存self.Bookname文件
        
        self.exit_tl()

    #使备注窗口的X失效
    def this(self):
        pass

    #打开/关闭功能开关
    def changeDoor(self):
        self.tipGUI_Door = 0
        self.mt.destroy()
        
    #实现添加功能(不对应分类)
    def insertItem(self):
        self.name = self.nameEntry.get()
        self.tip = self.tipEntry.get()
        if self.name == '':
            showinfo("╯▽╰","请输入书名!")
            return
        self.tree.insert("", END, text=self.name, values=self.tip)
        if "" in self.Bookname.keys():
            self.Bookname[""].append({self.name:self.tip})
        else:
            self.Bookname[""] = [{self.name:self.tip}]
            self.class_item.append("")
        self.nameEntry.delete(0, END) 
        self.tipEntry.delete(0, END) 

    # 建立滑动条
    def on_scroll(self,*args):  # 防止滚动条弹回顶部
        self.pos = Scrollbar.get()
        print(self.pos)
        self.page = 0.1
        if args[0] == 'scroll':
            if args[2] == 'units':
                first = self.pos[0] + int(args[1]) * 0.01
            elif args[2] == 'pages':
                first = self.pos[0] + int(args[1]) * 0.1
            else:
                first = 0
        elif args[0] == 'moveto':
            first = float(args[1])
        else:
            first = 0
        Scrollbar.set(first, first + 0.1)
        self.label.config(text=str(args))

    #构建增加分类GUI
    def add_class_GUI(self):
        if self.tipGUI_Door == 1:
            pass
        else:
            self.attributes("-disabled",1)
            self.ad = Toplevel()
            self.ad.protocol("WM_DELETE_WINDOW",self.this)
            self.ad.resizable(0,0)
            self.ad.title("请输入新的分类")
            self.ad.geometry("318x140+500+300")
            self.thisclass = StringVar()
            self.tipE = Entry(self.ad,textvariable=self.thisclass)
            self.tipE.pack(anchor=CENTER,fill=X,padx=15,pady=40)
            self.Cabtn = Button(self.ad,text="取消",command=self.exit_ad)
            self.Cabtn.pack(anchor=S,side=RIGHT,padx=5,pady=5)
            self.OKbtn = Button(self.ad,text="确定",command=self.add_class)
            self.OKbtn.pack(anchor=S,side=RIGHT,pady=5)

    #实现增加分类功能
    def add_class(self):
        getword = self.thisclass.get()
        newindex = self.tree.insert("",index=END,text=getword) #获取新分类的索引
        self.Bookname[getword] = []
        self.class_item.append(getword)
        self.class_index[getword] = newindex
        self.exit_ad()

    #构建移动分类GUI
    def moveToclass_GUI(self):
        self.tipGUI_Door = 1
        self.mt = Toplevel()
        self.mt.resizable(0,0)
        self.mt.title("移动书籍")
        self.mt.geometry("290x360")
        self.bar = Scrollbar(self.mt)
        self.bar.pack(side=RIGHT,fill=Y)
        self.mt_book = "__________"
        self.mtL1 = Label(self.mt,text="    请选择需要移动的书籍",background="lightyellow",font=10)
        self.mtL1.pack(fill=X)
        self.mtL2 = Label(self.mt,text="将 "+self.mt_book+" 移动至：",font="Hevetic 10 bold")
        self.mtL2.pack(anchor=NW,padx=10,pady=5)
        self.lb = Listbox(self.mt,height=13,width=25,relief="ridge",yscrollcommand=self.bar.set)
        self.bar.config(command=self.lb.yview)

        self.mt.protocol("WM_DELETE_WINDOW",self.changeDoor)

        for cl in self.class_item:
            self.lb.insert(END,cl)
        self.lb.pack(pady=10)
        
        self.mtbtn = Button(self.mt,text="确定",width=30,command=self.moveToclass)
        self.mtbtn.pack()
        
    #实现移动分类功能
    def moveToclass(self):
        self.index = self.lb.curselection()
        self.mv_class=self.lb.get(self.index)
        
        if self.item_key in self.Bookname:
            showinfo("ಥ_ಥ","尚不支持二级及以上分类")
        else:
            
            self.Bookname[self.mv_class].append({self.item_key:self.final_tip})
            self.tree.delete(self.tree.selection())
            self.Bookname[self.nowclass].remove({self.item_key:self.final_tip})
            self.tree.insert(self.class_index[self.mv_class],index=END,text=self.item_key,values=self.final_tip)

if __name__ == "__main__":
    A = MainWindow()
    A.mainloop()