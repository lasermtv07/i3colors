#!/usr/bin/python3

# i3colors
# NOT AFFILIATED WITH OFFICIAL i3 PROJECT!
# a GUI app to configure colors of the i3 window manager
# this program is free software, released under the UNLICENSE license
# (c) lasermtv07, 2024

import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import Menu
from tkinter.messagebox import showinfo,showwarning
from tkinter import filedialog
import os
import os.path
import shutil
import sys

class WindowPrev:
    def __init__(self,canvas,border,backgr,text,indicator,child_border,name):
        self.canvas=canvas
        self.border=border
        self.backgr=backgr
        self.text=text
        self.indicator=indicator
        self.child_border=child_border

        self.defCanvas=canvas
        self.defBorder=border
        self.defBackgr=backgr
        self.defText=text
        self.defIndicator=indicator
        self.defChild_border=child_border

        self.name=name
        return
    def restoreDefaults(self):
        self.canvas=self.defCanvas
        self.border=self.defBorder
        self.backgr=self.defBackgr
        self.text=self.defText
        self.indicator=self.defIndicator
        self.child_border=self.defChild_border
        global value
        genDrawStack(value)

    def draw(self,x,y):
        self.canvas.create_rectangle((x,y+10,x+125,y+70),outline=self.child_border, fill='#f0efde',width=2)
        self.canvas.create_rectangle((x,y,x+125,y+10),fill=self.backgr, outline=self.border)
        self.canvas.create_text((x+15,y+5),text="test",fill=self.text, font='tkDefaultFont 7')
        return
    def askColor(self,par):
        match par:
            case "self.border":self.border=askcolor(color=eval(par))[1]
            case "self.backgr":self.backgr=askcolor(color=eval(par))[1]
            case "self.text":self.text=askcolor(color=eval(par))[1]
            case "self.indicator":self.indicator=askcolor(color=eval(par))[1]
            case "self.child_border":self.child_border=askcolor(color=eval(par))[1]
        global value
        genDrawStack(value)
        return
    def parseFile(self,fname):
        exists=True
        try:
            f=open(fname,'r')
        except:
            exists=False
        if not exists:
            try:
                f=open(f'/home/{os.getlogin()}/.config/i3/config','r')
            except:
                showwarning(title="Couldnt load anything",message="No file specified and default config doesnt exist")
                return
        s=(f.read()).split("\n")
        for i in s:
            t=(i.strip()).split(" ")
            if t[0]==("client."+self.name):
                #removes all used-to-be spaces
                j=0
                while j<len(t):
                    if t[j]=='':
                        del t[j]
                        j-=1
                    j+=1
                print(t)
                self.border=t[1]
                self.backgr=t[2]
                self.text=t[3]
                self.indicator=t[4]
                self.child_border=t[5]
                return
    def writeFile(self,file):
        towrite=f'client.{self.name} {self.border} {self.backgr} {self.text} {self.indicator} {self.child_border}'
        fpath=file
        if not os.path.exists(file) and os.path.exists(f'/home/{os.getlogin()}/.config/i3/config'):
            print("default")
            fpath=f'/home/{os.getlogin()}/.config/i3/config'
        try:
            f=open(fpath,"r")
        except:
            #when the file simply doesnt exists..
            w=fopen(fpath,"w")
            w.write(towrite)
        c=(f.read()).split("\n")
        f.close()
        o=[]
        for i in c:
            t=i.strip()
            t=t.split(" ")
            if t[0]!=f'client.{self.name}':
                o.append(i)
        o="\n".join(o)
        o+="\n"+towrite
        f=open(fpath,"w")
        f.write(o)
        return

def backup(fname):
    if os.path.exists(fname):
        f=fname
    elif os.path.exists(f'/home/{os.getlogin()}/.config/i3/config'):
        f=f'/home/{os.getlogin()}/.config/i3/config'
    else:
        showwarning(title="Couldnt backup file",message="Couldn't backup nonexistent file. Please back up first.")
        return
    fn=f.split("/")
    fn=fn[len(fn)-1]
    fp=f.split("/")
    fp.pop()
    fp=("/".join(fp))+"/"
    while os.path.exists(fp+fn):
        fn="."+fn
    shutil.copyfile(f,fp+fn)

if len(sys.argv)>=2:
    file=sys.argv[1]
else:
    #handled later
    file='adfakdfseopw'
root=tk.Tk()
root.geometry("640x330")
root.attributes('-type', 'dialog')
root.title("i3color")

bar=Menu(root)
root.config(menu=bar)
fmenu=Menu(bar)
imenu=Menu(bar)

info=lambda:showinfo(title='Info',message='A program to configure window colors of the i3 window manager.\n\nProgram is not affiliated with i3wm project.\n\n(c) lasermtv07,2024. Under UNLICENSE.')
imenu.add_command(label='Info',command=info)

def copen():
    fpath=file
    ft=filedialog.askopenfilename()
    if ft!=() and ft!="": fpath=ft
    else: return
    #DONT. LOOK. HERE.
    root.destroy()
    os.system(f"{__file__} {fpath}")
    exit(0)
def cwrite():
    for i in windows:
        i.writeFile(file)

fmenu.add_command(label='Open',command=copen)
fmenu.add_command(label='Write',command=cwrite)
fmenu.add_command(label='Backup',command=lambda:backup(file))
fmenu.add_command(label='Quit',command=lambda:exit(0))

bar.add_cascade(label="File",menu=fmenu)
bar.add_cascade(label="Info",menu=imenu)

pres=tk.Canvas(root, bg='white',width=280,height=230)
pres.place(x=10,y=10)
x=20
y=20
windows=[
    WindowPrev(pres,'#0000ff','#6666aa','#ffffff','#0000ff','#0000ff',"focused"),
    WindowPrev(pres,'#00ff00','#11ee11','#ffffff','#00ff00','#00ff00',"focused_inactive"),
    WindowPrev(pres,'#ff0000','#ff00ff','#ffffff','#0000ff','#ff0000',"focused_tab_title"),
    WindowPrev(pres,'#000000','#555555','#ffffff','#0000ff','#000000',"unfocused"),
    WindowPrev(pres,'#dddddd','#ffffff','#000000','#0000ff','#dddddd',"urgent"),
    WindowPrev(pres,'orange','yellow','#000000','#0000ff','orange',"placeholder"),
]
windows[0].writeFile(file)
for i in windows:
    i.parseFile(file)

# handles drawing preview
def draw(stack):
    pres.delete("all")
    global windows
    for i in range(len(stack)):
        windows[stack[i]].draw(x+20*i,y+20*i)
drawStack=[]
def genDrawStack(val):
    global drawStack
    drawStack=[]
    for i in range(len(val)):
        if(val[i].get()==1):
            drawStack.append(i)
    draw(drawStack)
    #print(drawStack)
    return

value=[None]*len(windows)
for i in range(len(windows)):
    value[i]=tk.IntVar()
xshift=0
yshift=0
for i in range(len(value)):
    j=value[i]
    tk.Checkbutton(root,text=windows[i].name,var=value[i],command=lambda:genDrawStack(value)).place(x=10+xshift,y=255+yshift)
    xshift+=130
    if xshift>=260:
        xshift=0
        yshift+=20

tk.Label(root,text="Editing: ").place(x=300,y=10)

def changeFrameContent(f,x,win):
    #erase content of frame
    for i in f.winfo_children():
        i.destroy()
    for i in win:
        if i.name==x:
            s=i
            tk.Label(f,text="border:").place(x=5,y=10)
            tk.Button(f,text="change",command=lambda:s.askColor('self.border')).place(x=90,y=5)
            tk.Label(f,text="background:").place(x=5,y=40)
            tk.Button(f,text="change",command=lambda:s.askColor('self.backgr')).place(x=90,y=35)
            tk.Label(f,text="text:").place(x=5,y=70)
            tk.Button(f,text="change",command=lambda:s.askColor('self.text')).place(x=90,y=65)
            tk.Label(f,text="indicator:").place(x=5,y=100)
            tk.Button(f,text="change",command=lambda:s.askColor('self.indicator')).place(x=90,y=95)
            tk.Label(f,text="child border:").place(x=5,y=130)
            tk.Button(f,text="change",command=lambda:s.askColor('self.child_border')).place(x=90,y=125)
    return
options=[]
for i in windows:
    options.append(i.name)
option=tk.StringVar()
option.set(options[0])
tk.OptionMenu(root,option,*options,command=lambda x:changeFrameContent(frame,x,windows)).place(x=360,y=5)

frame=tk.Frame(root,height=202,width=330)
frame.place(x=300,y=40)
frame['borderwidth']=1
frame['relief']='solid'

tk.Label(root,text=f"Editing: {file}").place(x=300,y=250)
changeFrameContent(frame,'focused',windows)

def undoChanges():
    for i in windows:
        i.restoreDefaults()
tk.Button(root,text="Undo", command=undoChanges).place(x=455,y=6)

def loadBackup():
        f=None
        f=filedialog.askopenfilename()
        if f==() or f=="": return
        for i in windows:
            i.parseFile(f)
        global value
        genDrawStack(value)
tk.Button(root,text="Load backup ", command=loadBackup).place(x=520,y=6)
root.mainloop()
