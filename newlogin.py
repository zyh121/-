import json
import os
from tkinter import *
from tkinter.messagebox import *  # showinfo
from tkinter.ttk import *

import mywin


class LoginWindow(Tk):
    """
    创建登录窗体的GUI界面以及登录的方法
    """
    def __init__(self):
        super().__init__() # 执行tk这个类的初始化
        self.title("书阁")
        self.geometry("300x310+500+300")
        self.resizable(0,0)

        # 加载窗体
        self.setup_GUI()

        # 定义变量
        self.Boss_dir = "D:\\BookAttic"
        self.user_path = "D:\\BookAttic\\User.txt" # 文件路径
        self.user_list = [] # 储存所有的用户信息
        self.password_error_times = 0 # 记录密码输入错误次数
        self.user = "" # 当前用户
        self.password = "" # 当前用户的密码
        self.current_user_list = []

        #创建文件储存信息：
        if os.path.isdir("D:\\BookAttic"):
            pass
        else:
            self.creat_File()

        # 自动执行文件账号中的加载
        self.load_file_info() 

    def creat_File(self):
        """
        创建总文件夹
        """
        os.mkdir("D:\\BookAttic")
        #创建需要的各种文件
        tip = {'说明': [{'若直接删除分类': '会将类内所有书都删掉'}]}
        try:
            with open(self.user_path,mode="w") as fd:
                fd.write("")
            with open("D:\\BookAttic\\Bookname.json", 'w',encoding='UTF-8') as f:
                json.dump(tip, f, ensure_ascii=False)
            
        except:
            showinfo("系统消息","创建储存用文件出错！")

    def setup_GUI(self):
        """
        创建登录界面
        """
        # 账号的布置（用空格代替排版了，感觉这样方便一些）
        self.accountL = Label(self, text="            账号")
        self.accountL.grid(row=3, sticky=E,pady=2)
        self.var_account = StringVar()
        self.accountE = Entry(self,textvariable = self.var_account)
        self.accountE.grid(row=3, column=1,pady=2)
        #密码的布置
        self.pwdL = Label(self, text="             密码")
        self.pwdL.grid(row=4, sticky=W)
        self.var_pwd = StringVar()
        self.pwdE = Entry(self, show="●",textvariable = self.var_pwd)
        # show="*"隐藏密码显示
        self.pwdE.grid(row=4, column=1)
        # 创建登录按钮
        self.exitbtn = Button(self, text="进入", command=self.Judge, width=20)
        self.exitbtn.grid(row=5, column=1, pady=5)
        # 创建注册按钮
        self.newbtn = Button(self,text="注册",command=self.AddUser_GUI,width=20)
        self.newbtn.grid(row=6,column=1)
        # 建立标题
        self.label_title1 = Label(self, justify="center", text="                     书  阁 ", font="Helvetica 15 bold ")
        self.label_title1.grid(row=0, column=0, columnspan=3, sticky=W + E)
        # 插入标题与图片的分割线
        self.sep = Separator(self, orient=HORIZONTAL)
        self.sep.grid(row=1, column=1, columnspan=3, sticky=W + E, pady=5)
        # 插入图片(提示：把图片和.py文件放在 同一个文件夹中才能显示)
        self.bkgif = PhotoImage(file="D:\Python\PYTHON\My Programe\pic.gif")
        self.label = Label(self, image=self.bkgif)
        self.label.grid(row=2, column=1, columnspan=2, pady=5)

    def AddUser_GUI(self):
        """
        建立注册用户界面
        """
        self.attributes("-disabled",1)
        self.au = Toplevel()
        self.au.title("创建用户")
        self.au.geometry("220x220+510+310")
        self.au.resizable(0,0)
        self.newaccountL = Label(self.au, text="新账号:",font="楷体 15 bold")
        self.newaccountL.grid(row=0,column=0,sticky=W,padx=5,pady=5)
        self.var_newaccount = StringVar()
        self.newaccountE = Entry(self.au,textvariable = self.var_newaccount,width=25)
        self.newaccountE.grid(row=1,column=0,sticky=W,padx=5)
        self.newpwdL = Label(self.au, text="新密码:",font="楷体 15 bold")
        self.newpwdL.grid(row=2,column=0,sticky=W,padx=5,pady=5)
        self.var_newpwd = StringVar()
        self.newpwdE = Entry(self.au,textvariable = self.var_newpwd,width=25)
        self.newpwdE.grid(row=3,column=0,sticky=W,padx=5)
        #确认密码
        self.againpwdL = Label(self.au,text="请再次输入密码:",font="楷体 15 bold")
        self.againpwdL.grid(row=4,column=0,sticky=W,padx=5,pady=5)
        self.var_againpwd = StringVar()
        self.againpwdE = Entry(self.au,textvariable=self.var_againpwd,width=25)
        self.againpwdE.grid(row=5,column=0,sticky=W,padx=5)
        #确定
        self.okbtn = Button(self.au,text="确 定",command=self.AddUser)
        self.okbtn.grid(row=6,column=0,sticky=W+E,padx=5,pady=5)

    def AddUser(self):
        """
        注册用户的数据处理
        """
        account = self.newaccountE.get()
        pwd = self.newpwdE.get()
        again = self.againpwdE.get()

        if account == '' or pwd == '' or again =='':
            showinfo("系统消息","密码或账号不能为空！")
        else:
            for name in self.user_list:
                if name[0] == account:
                    showinfo("系统消息","用户名已存在!")
                    self.newaccountE.delete(0,END)
                    
            #储存新用户信息
            if pwd == again :
                done  = account + ',' + pwd + ',1\n'
                with open(self.user_path,mode="a") as fd:
                    fd.write(done)
                fd.close()
                self.load_file_info()
                self.au.destroy()
                self.attributes("-disabled",0)
            else:
                showinfo("系统消息","两次密码输入不一致!")

    def load_file_info(self):
        """
        加载文件中的用户信息（用户名、密码、状态）
        """
        if not os.path.exists(self.user_path):
            showinfo("系统消息","提供的文件名不存在！") #import messagebox 以消息的方式提醒
        else:
            try:
                with open(file=self.user_path, mode="r") as fd:
                    # 读取第一行
                    current_line = fd.readline()
                    while current_line:
                        temp_list = current_line.split(",")
                        self.user_list.append(temp_list)
                        # 读取下一行
                        current_line = fd.readline()
            except:
                showinfo("系统消息","文件读取出现异常！")

    def Judge(self):
        '''
        判断账号密码是否输入正确
        '''
        # 获取输入的账号和密码
        self.user = self.var_account.get()
        self.password = self.var_pwd.get()
        
        if self.user == '' or self.password == '':
            showinfo("系统消息","登录信息不全！")
        # 进行判断
        else:
            for index in range(len(self.user_list)):
                # 先判断用户名是否存在
                if self.user.strip() == str(self.user_list[index][0]).strip():
                # 判断账号是否禁用
                    if "0" in str(self.user_list[index][2]):
                        showinfo("系统消息","错误次数已达上限！账号已禁用！")
                        break
                    # 判断密码是否正确
                    if self.password != str(self.user_list[index][1]):
                        self.password_error_times += 1

                        #判断是否到三次
                        if self.password_error_times >= 3:
                            showinfo("系统消息","密码错误已达三次！")
                            # 改变状态
                            self.user_list[index][2] = "0\n" #注意！这里不是数字0，需要\n，否则后面会出错
                    
                            # 写入文件
                            self.write_file_info()
                        else:
                            showinfo("系统消息", "密码错误！")
                        break
                    else:
                        #验证正确后就将错误次数归为0
                        self.password_error_times = 0
                        self.current_user_list = self.user_list[index]
                        #加载主界面
                        self.load_main()
                        break
            # 如果校验到最后都没有想用的用户名，则用户名不存在！
                if index == len(self.user_list) - 1:
                    showinfo("系统消息","输入的用户名不存在")
                    

    def write_file_info(self):
        """
        先清空文件，再重新写入
        """
        try:
            with open(file=self.user_path,mode="w") as fd:
                fd.write("")
            with open(file=self.user_path,mode="a") as fd:
                for item in self.user_list:
                    fd.write(",".join(item))
        except:
            showinfo("系统消息","写入文件出现异常!")

    def load_main(self):
        # 关闭当前的窗体
        self.destroy() 
        # 加载新的窗体
        self.main_window = mywin.MainWindow()
    
if __name__ == "__main__":
    win = LoginWindow()
    win.mainloop()
