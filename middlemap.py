from pyautogui import *
from tkinter import *
import customtkinter as ct
import time
import os

class ButtonCom:
    def __init__(self):
        ct.set_appearance_mode('dark')
        ct.set_default_color_theme('blue')
        #replace XYZ with a directory path that holds other python programs for day to day use
        self.apps = os.listdir('XYZ')
        for n in self.apps:
            if n[0] == '.':
                self.apps.remove(n)
        self.apps.remove('middlemap.py')
        self.lst = []
        self.shcuts = {'screenshot':['ctrl','win','s']}
        self.root = ct.CTk()
        self.root.attributes('-topmost', True)
        self.root.resizable(0,0)
        self.root.title('ShortHub')
        self.cmd = 'off'
        self.all = ['ctrl', 'alt', 'shift', 'win', 'tab'] + [chr(i) for i in range(97,123)]
        self.draw()
        self.active = 'keys'
        self.root.mainloop()

    def draw(self):
        self.hbf = ct.CTkFrame(self.root)
        self.hbf.pack()
        self.cmdbuttons = ct.CTkFrame(self.root)

        self.shcb = ct.CTkButton(master=self.hbf, text='Shortcuts', command=self.scscreenswap)
        self.shcb.grid(row=0, column=0)
        self.sw_var = ct.StringVar(value='off')
        self.swt = ct.CTkSwitch(master=self.hbf, text='CMD off', command=self.switchev, variable=self.sw_var, onvalue='on', offvalue='off')
        self.swt.grid(row=0,column=1)
        self.appsw = ct.CTkButton(master=self.hbf, text='Apps', command=self.appscreenswap)
        self.appsw.grid(row=0,column=2)

        self.eb = ct.CTkButton(master=self.cmdbuttons, text='Go', command=self.cmdexec)
        self.eb.grid(row=0,column=0)
        self.cb = ct.CTkButton(master=self.cmdbuttons, text='Clear', command=self.clear)
        self.cb.grid(row=0,column=1)
        self.cmdl = ct.CTkLabel(master=self.root, text='')
        self.cmdl.pack()
        self.cmdbuttons.pack()

        self.bframe = ct.CTkScrollableFrame(master=self.root, width=420)
        r = 0
        c = 0
        for n in self.all:
            bu = ct.CTkButton(master=self.bframe, text=n, command=lambda n=n: self.chain([n]))
            bu.grid(row=r, column=c)
            c+=1
            if c ==3:
                c=0
                r+=1
        self.bframe.pack()

        self.aframe = ct.CTkScrollableFrame(master=self.root, width=420)
        r = 0
        c = 0
        for n in self.apps:
            bu = ct.CTkButton(master=self.aframe, text=n.split('.')[0], command=lambda n=n: self.appopen(n))
            bu.grid(row=r, column=c)
            c += 1
            if c == 3:
                c = 0
                r += 1

        self.sframe = ct.CTkScrollableFrame(master=self.root, width=420)
        r = 0
        c = 0
        for n in self.shcuts.keys():
            bu = ct.CTkButton(master=self.sframe, text=n, command=lambda n=n: self.shcexec(n))
            bu.grid(row=r, column=c)
            c += 1
            if c == 3:
                c = 0
                r += 1

        self.switchev()

    def appscreenswap(self):
        if self.active == 'apps':
            self.active = 'keys'
            self.shcb.configure(text='Shortcuts')
            self.appsw.configure(text='Apps')
            self.aframe.pack_forget()
            self.bframe.pack()
        else:
            if self.active == 'keys':
                self.bframe.pack_forget()
            else:
                self.sframe.pack_forget()
            self.aframe.pack()
            self.shcb.configure(text='Shortcuts')
            self.appsw.configure(text='Keys')
            self.active = 'apps'

    def scscreenswap(self):
        if self.active == 'shc':
            self.active = 'keys'
            self.sframe.pack_forget()
            self.bframe.pack()
            self.shcb.configure(text='Shortcuts')
            self.appsw.configure(text='Apps')
        else:
            if self.active == 'keys':
                self.bframe.pack_forget()
            else:
                self.aframe.pack_forget()
            self.sframe.pack()
            self.active = 'shc'
            self.shcb.configure(text='Keys')
            self.appsw.configure(text='Apps')

    def shcexec(self, name):
        self.lst = self.shcuts[name]
        self.exec()
        self.clear()

    def appopen(self, n):
        ty = n.split('.')[-1]
        self.root.destroy()
        if ty == 'py':
            os.system('python3 .customapps/' + n)
        quit()

    def clear(self):
        self.lst = []
        self.cmdl.configure(text='')

    def switchev(self):
        self.cmd = self.sw_var.get()
        self.swt.configure(text='CMD ' + self.cmd)
        if self.cmd == 'on':
            self.cmdbuttons.pack()
            self.cmdl.pack()
            if self.active == 'keys':
                self.bframe.pack_forget()
                self.bframe.pack()
            else:
                self.sframe.pack_forget()
                self.aframe.pack()
        else:
            self.cmdbuttons.pack_forget()
            self.cmdl.pack_forget()

    def chain(self, b):
        if self.cmd == 'off':
            with hold('alt'):
                press('tab')
            time.sleep(0.05)
            self.lst += b
            self.exec()
        else:
            if b[0] not in self.lst:
                self.lst += b
                self.cmdl.configure(text='+'.join(self.lst))

    def cmdexec(self):
        with hold('alt'):
            press('tab')
        time.sleep(0.05)
        self.exec()
        self.clear()

    def exec(self):
        if not len(self.lst):
            return
        if len(self.lst) == 1:
            press(self.lst[0])
            self.lst = []
            return
        with hold(self.lst[0]):
            self.lst = self.lst[1:]
            self.exec()

ButtonCom()
