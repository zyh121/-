import os
import json
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *
from tkinter.font import Font

class WriteWindow(Tk):

    def __init__(self):
        super().__init__()
        self.title("记录随笔")
        self.geometry("1200x730")
        self.resizable(0,0)
        self.iconbitmap('D:\\Npy\\Booktest\\favicon.ico')
        #全局变量
        self.book_name = None
        self.tree_index = dict()
        self.book_chaText = list()
        self.book_chapter = list()

        #初始化信息
        self.load_files()
        self.creat_file()
        #创建界面
        self.Suibi_GUI()

    #加载需要用到的信息
    def load_files(self):
        try:
            with open ("D:\\BookAttic\\Bookname.json",mode="r",encoding='UTF-8') as fd:
                self.treedata = json.load(fd)
            self.first_tree = list(self.treedata.keys())
        except:
            showinfo("系统消息","文件读取出现异常!")
        finally:
            fd.close()

        for cls in self.first_tree:
            self.tree_index[cls] = []
            for item in self.treedata[cls]:
                self.tree_index[cls].append(list(item.keys())[0])


    #创建储存用到的文件
    def creat_file(self):
        for key in self.tree_index.keys():
            if not os.path.exists("D:\\BookAttic\\"+key):
                os.mkdir("D:\\BookAttic\\"+key)
            for val in self.tree_index[key]:
                if not os.path.exists("D:\\BookAttic\\"+key+"\\"+val+".json"):
                    with open ("D:\\BookAttic\\"+key+"\\"+val+".json","w",encoding='UTF-8') as f:
                        f.write("")

    #分割出三个功能区域
    def Suibi_GUI(self):
        self.pw = PanedWindow(orient=HORIZONTAL,height=700,width=1190)
        self.ClassF = LabelFrame(self.pw,text="选择书籍",width=240,height=690)
        self.pw.add(self.ClassF,weight=1)
        self.ChapterF = LabelFrame(self.pw,text="选择章节",width=230)
        self.pw.add(self.ChapterF,weight=1)
        self.NoteF = LabelFrame(self.pw,text="随笔")
        self.pw.add(self.NoteF,weight=1)
        self.pw.grid(padx=2,pady=2,sticky=N+S+W+E)
        self.Tree_GUI()
        self.Chapter_GUI()
        self.Text_GUI()

    #创建左侧的Treeview分类GUI
    def Tree_GUI(self):
        self.tree = Treeview(self.ClassF,selectmode=BROWSE,height=31)
        self.tree.heading("#0",text="书架")
        self.tree.tag_configure("groundcolor",background="lemonchiffon")
        for key in self.tree_index:
            x = self.tree.insert("",index=END,text=key)
            for val in self.tree_index[key]:
                self.tree.insert(x,index=END,text=val)
        self.tree.grid(row=0,column=0,sticky=W + E + N + S)
        self.yscrollbar = Scrollbar(self.ClassF,orient=VERTICAL,command=self.on_scroll)
        self.yscrollbar.grid(row=0,column=1,sticky=W + E + N + S)
        self.yscrollbar.config(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscrollbar.set)
        self.tree.bind("<<TreeviewSelect>>",self.Tree_data)

    #取得所选项的数据
    def Tree_data(self,even):
        for item in self.tree.selection():
            self.book_name = self.tree.item(item,"text")
        if self.book_name in self.treedata:
            return

        self.class_name = self.find_classname()
        self.default_Cha()
        self.Show_CertainBook_Cha()

    #为新书添加一个默认的Chapter
    def default_Cha(self):
        #确定这本书之前是否进行过初始化
        if not os.path.exists("D:\\BookAttic\\"+self.class_name+"\\"+self.book_name+".json"):
            try:
                with open("D:\\BookAttic\\"+self.class_name+"\\"+self.book_name+".json",mode="w",encoding='UTF-8') as fd:
                    defCha = [{"默认":"\n"}]
                    json.dump(defCha,fd,ensure_ascii=False)
            except:
                showinfo("系统消息","初始化默认书摘出错！")

    #寻找上一级
    def find_classname(self):
        for key,val in self.tree_index.items():
            if isinstance(self.tree_index[key],list):
                can = self.tree_index[key]
                for book in can:
                    if self.book_name == book:
                        return key

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

    #创建左侧的Listbox书签GUI
    def Chapter_GUI(self):
        self.scollbarC = Scrollbar(self.ChapterF)
        self.scollbarC.grid(row=0,column=1,sticky=N+S+E+W)
        self.lb = Listbox(self.ChapterF,width=29,height=36,yscrollcommand=self.scollbarC.set)
        self.scollbarC.config(command=self.lb.yview)
        self.lb.grid(row=0,column=0,sticky=N+S+W+E)
        self.lb.bind("<Double-Button-1>",self.Chapter_Data)

    def Chapter_Data(self,event):
        #获取选择的项目
        self.cha_index = self.lb.curselection()
        self.sel_cha = self.lb.get(self.cha_index)
        if self.cha_index != None:  #如果发生了选择
            #考虑Text中已有文本
            if self.novel.get("1.0",END) != '\n':
                self.attributes("-disabled",1)
                answer = askokcancel("提示","所写内容尚未保存，确定切换吗？")
                if answer == True:
                    self.attributes("-disabled",0)
                    self.Show_CertainCha_Novel()
                else:
                    self.attributes("-disabled",0)
            else:
                self.Show_CertainCha_Novel()

    #将所选书摘显示在右侧
    def Show_CertainCha_Novel(self):
        try:
            with open("D:\\BookAttic\\"+self.class_name+"\\"+self.book_name+".json",mode="r",encoding='UTF-8') as fd:
                thisbook=json.load(fd)
        except:
            showinfo("系统消息","文件读取出现异常！")
        finally:
            fd.close()
        for item in thisbook:
            if self.sel_cha in item.keys():
                try:
                    self.ChapterE.delete(0,END)
                except:
                    pass
                self.ChapterE.insert(0,self.sel_cha)
                self.novel.insert(END,str(item.values())[14:-5])

    #加载指定某一本书的所有章节并显示在Listbox
    def Show_CertainBook_Cha(self):
        try:
            with open("D:\\BookAttic\\"+self.class_name+"\\"+self.book_name+".json",mode="r",encoding='UTF-8') as fd:
                thisbook = json.load(fd)
        except json.decoder.JSONDecodeError:
            return
        finally:
            fd.close()
        self.lb.delete(0,END)
        for item in thisbook:
            self.book_chapter.append(str(item.keys())[12:-3])
        for cha in self.book_chapter:
            self.lb.insert(END,cha)

    #创建右侧的Text书摘GUI
    def Text_GUI(self):
        self.ChapterE = Entry(self.NoteF,width=100)
        #self.ChapterE.insert(0,"在此输入标题")
        self.ChapterE.grid(row=0,column=0,columnspan=10,padx=8,pady=2,sticky=W+E)
        #创建工具栏
        self.toolbar = Frame(self.NoteF,relief=RAISED,border=1,width=180)
        self.toolbar.grid(row=1,column=0,columnspan=10,sticky=W+E,padx=8,pady=1)
        #创建字体菜单
        self.familyVar = StringVar()
        self.familyFamily = ("字体","Arial","楷体")
        self.familyVar.set(self.familyFamily[1])
        self.famliy = OptionMenu(self.toolbar,self.familyVar,*self.familyFamily,command=self.famliyChanged)
        self.famliy.grid(row=1,column=0,pady=2)
        #创建字形菜单
        self.weightVar = StringVar()
        self.weightFamily = ("字形","normal","bold")
        self.weightVar.set(self.weightFamily[1])
        self.weight = OptionMenu(self.toolbar,self.weightVar,*self.weightFamily,command=self.weightChanged)
        self.weight.grid(row=1,column=1,pady=3)
        #创建字号菜单
        self.sizeVar = StringVar()
        self.size = Combobox(self.toolbar,textvariable=self.sizeVar)
        self.sizeFamily = [x for x in range(8,30)]
        self.size["value"] = self.sizeFamily
        self.size.current(4)
        self.size.bind("<<ComboboxSelected>>",self.sizeSelected)
        self.size.grid(row=1,column=2)
        #建立复原与重做Button
        self.undoBtn = Button(self.toolbar,text="复原",command=self.undojob)
        self.undoBtn.grid(row=1,column=3,pady=2)
        self.redoBtn = Button(self.toolbar,text="重做",command=self.redojob)
        self.redoBtn.grid(row=1,column=4,pady=2)
        #建立高亮菜单(结合标签)
        self.colorVar = StringVar()
        self.colorFamily = ("")
        #创建查找文字栏
        self.findbar = Frame(self.NoteF,relief=RIDGE,border=1,width=180)
        self.findbar.grid(row=2,column=0,columnspan=10,sticky=W+E,padx=8,pady=1)
        self.findE = Entry(self.findbar,width=87)
        self.findE.grid(row=2,column=0,columnspan=5,sticky=W+E,padx=2,pady=1)
        self.findbtn = Button(self.findbar,text="查找",command=self.searchText)
        self.findbtn.grid(row=2,column=6,pady=1,padx=2)

        #建立插入书签按钮:插入书签可行，但无法将光标移动到指定位置，无法实现。
        #建立高亮菜单:因无法保存和加载所定义的各种标签而无法实现

        #创建文字编辑区域
        self.scollbarN = Scrollbar(self.NoteF)
        self.scollbarN.grid(row=3,column=1,sticky=N+S+E+W,rowspan=3)
        self.novel=Text(self.NoteF,undo=True,width=77,height=30,yscrollcommand=self.scollbarN.set,font=("Arial"))
        self.novel.tag_configure("found",background = "yellow")
        self.novel.grid(row=3,column=0,sticky=W+N+S+E,padx=8,pady=3)
        self.novel.focus_set()
        self.scollbarN.config(command=self.novel.yview)

        self.OKbtn = Button(self.NoteF,text="保 存",command=self.Save)
        self.OKbtn.grid(row=6,column=0,sticky=E,pady=3)
        self.newbtn = Button(self.toolbar,text="新建章节",command=self.create_text)
        self.newbtn.grid(row=1,column=6,pady=2,columnspan=2,padx=12)
    """
    以下六个均为实现书摘功能的函数
    """
    def searchText(self):
        self.novel.tag_remove("found","1.0",END)
        self.start = "1.0"
        self.key = self.findE.get()
        if (len(self.key.strip()) == 0):
            return
        while True:
            self.pos = self.novel.search(self.key,self.start,END)
            if (self.pos == ""):
                break
            self.novel.tag_add("found",self.pos,"%s+%dc" % (self.pos,len(self.key)))
            self.start = "%s+%dc" % (self.pos,len(self.key))

    def famliyChanged(self,event):
        f = Font(family=self.familyVar.get())
        self.novel.configure(font=f)

    def weightChanged(self,event):
        f = Font(weight=self.weightVar.get())
        self.novel.configure(font=f)

    def sizeSelected(self,event):
        f = Font(size=self.sizeVar.get())
        self.novel.configure(font=f)

    def undojob(self):
        try:
            self.novel.edit_undo()
        except:
            showinfo("◐﹏◑","先前没有动作")
    def redojob(self):
        try:
            self.novel.edit_redo()
        except:
            showinfo("◑﹏◐","先前没有动作")

    def create_text(self):
        """
        所谓的“新建”只是清空了Text，其实质上由保存函数实现：新建则保存。
        """
        #考虑Text中已有文本
        if self.novel.get("1.0",END) != '\n':
            self.attributes("-disabled",1)
            answer = askokcancel("提示","所写内容尚未保存，确定新建吗？")
            if answer == True:
                self.attributes("-disabled",0)
                self.ChapterE.delete(0,END)
                self.novel.delete("1.0",END)
            else:
                self.attributes("-disabled",0)

    #保存文本内容并刷新Listbox中的内容
    def Save(self):
        self.Cha_name = self.ChapterE.get()
        self.novel_text = self.novel.get("1.0",END)
        if self.Cha_name == '':
            showinfo("╯▽╰","请输入标题!")
            return
        if self.book_name == None:
            showinfo("╯▽╰","请在书架中选择书籍！")
            return
        for name in self.book_chapter:
            #保存已有的chapter的修改
            if self.Cha_name == name:
                try:
                    with open("D:\\BookAttic\\"+self.class_name+"\\"+self.book_name+".json",mode="r",encoding='UTF-8') as fd:
                        goalbook = json.load(fd)
                    with open ("D:\\BookAttic\\"+self.class_name+"\\"+self.book_name+".json",mode="w",encoding='UTF-8') as fd:
                        for item in goalbook:
                            if self.Cha_name == str(item.keys())[12:-3]:
                                item[self.Cha_name] = self.novel_text
                                json.dump(goalbook,fd,ensure_ascii=False)
                                self.Refresh()
                except:
                    showinfo("系统消息","修改内容时出现异常!")
            #保存新的chapter
            else:
                try:
                    with open ("D:\\BookAttic\\"+self.class_name+"\\"+self.book_name+".json",mode="w",encoding='UTF-8') as fd:
                        self.book_chaText.append({self.Cha_name:self.novel_text})
                        json.dump(self.book_chaText,fd,ensure_ascii=False)
                        self.Refresh()
                except:
                    showinfo("系统消息","保存文本时出现异常!")
    #刷新界面
    def Refresh(self):
        self.ChapterE.delete(0,END)
        self.novel.delete("1.0",END)
        self.Show_CertainBook_Cha()



if __name__ == "__main__":
    B = WriteWindow()
    B.mainloop()