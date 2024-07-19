#!/usr/bin/python3
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import menu
import os
import os.path

class WindowPrev:
    def __init__(self,canvas,border,backgr,text,indicator,child_border,name):
        self.canvas=canvas
        self.border=border
        self.backgr=backgr
        self.text=text
        self.indicator=indicator
        self.child_border=child_border
        self.name=name
        return
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
                print('didnt open anything')
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
        o=[]
        for i in c:
            t=i.strip()
            t=t.split(" ")
            if t[0]!=f'client.{self.name}':
                o.append(i)
            else:
                o.append(towrite)
        o="\n".join(o)
        f.close()
        f=open(fpath,"w")
        f.write(o)
        return
root=tk.Tk()
root.geometry("640x480")
root.attributes('-type', 'dialog')

bar=Menu(root)
root.config(menu=bar)

pres=tk.Canvas(root, bg='white',width=280,height=230)
pres.place(x=10,y=25)
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
file='ahdkjfhakfhd'
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
    tk.Checkbutton(root,text=windows[i].name,var=value[i],command=lambda:genDrawStack(value)).place(x=10+xshift,y=270+yshift)
    xshift+=130
    if xshift>=260:
        xshift=0
        yshift+=20

tk.Label(root,text="Editing: ").place(x=300,y=25)

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
tk.OptionMenu(root,option,*options,command=lambda x:changeFrameContent(frame,x,windows)).place(x=360,y=20)

frame=tk.Frame(root,height=202,width=330)
frame.place(x=300,y=55)
frame['borderwidth']=1
frame['relief']='solid'

tk.Label(frame,text="hewwo uwu").place(x=0,y=0)

root.mainloop()


