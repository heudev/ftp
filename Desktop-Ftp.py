#-*-coding:utf-8-*-
from tkinter import filedialog
from tkinter import *
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import socket
from socket import gethostbyname
import tkinter.scrolledtext as scrolledtext
import threading
import sys
import string
import random
import os

def localip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip
    except:
        ip=gethostbyname(socket.gethostname())
        return ip
    finally:
        try:
            s.close()
        except:
            pass

permlist=["elr","awMT","d","f","m"]
def ftp():
    try:
        authorizer = DummyAuthorizer()
        if usernameentry.get()!="" or passwordentry.get()!="":
            authorizer.add_user(usernameentry.get(), passwordentry.get(), directoryentry.get(), perm="".join(permlist))
        else:
            authorizer = DummyAuthorizer()
            authorizer.add_anonymous(directoryentry.get(), perm="".join(permlist))
        print("\n---------------------------------")
        print("\nPermissions:","".join(permlist),)
        print("\nFTP connect adress:\nftp://{}:21\n".format(localip()))
        handler = FTPHandler
        handler.authorizer = authorizer
        global server
        server = FTPServer((localip(), 21), handler)
        server.max_cons=int(maxconnectionsentry.get())+1
        print("Username:",usernameentry.get())
        print("Password:",passwordentry.get())
        print("Max Connections:",maxconnectionsentry.get())
        print("Ftp is running")
        server.serve_forever()
    except:
        directoryentry.delete(0,"end")
        buton["bg"]="#3E54D3"
        buton["text"]="Start"
        print("No such directory!")

def resource_path(relative_path):
    base_path = getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

app=Tk()
app.geometry("300x410")
app.resizable(False,False)

def on_closing():
    try:
        server.close_all()
    except:
        pass
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.wm_attributes("-alpha",0.95)
app.title("FTP")
photo = PhotoImage(file = resource_path("logo.png"))
app.iconphoto(False, photo)
title=Label(text="✦DISTANGER FTP✦",font=('Arial', 15,'bold',"italic"),bg="#2A3A51",fg="white")
title.pack(fill=BOTH)

def selectdirectory():
    directory = filedialog.askdirectory()
    directoryentry.delete(0,"end")
    directoryentry.insert(0,directory)
 
directorybuton=Button(app,text="Select Directory",font=("Arial",15),bg="#FE9677",fg="#2A3A51",bd=2,command=selectdirectory)
directorybuton.pack(fill=BOTH,ipady=1,ipadx=1)

directoryentry=Entry(app,bg="black",fg="white",bd=2,justify='center')
directoryentry.pack(fill=BOTH)

usernameandpassword=Frame(borderwidth=2, relief="groove")
usernameandpassword.pack(pady=5)

usernameframe=Frame(usernameandpassword)
usernameframe.pack()

usernamelabel=Label(usernameframe,text="Username:",font=("Arial",10,"italic","underline","bold"),width=8)
usernamelabel.pack(side=LEFT,padx=1.47)

usernameentry=Entry(usernameframe,font=("Arial",10,"bold"),bg="#0AB68B",bd=0,width=21)
usernameentry.pack(side=RIGHT,padx=1.47,pady=2,ipady=3)

passwordframe=Frame(usernameandpassword)
passwordframe.pack()

passwordlabel=Label(passwordframe,text="Password:",font=("Arial",10,"italic","underline","bold"),width=8)
passwordlabel.pack(side=LEFT,padx=1.47)

passwordentry=Entry(passwordframe,font=("Arial",10,"bold"),bg="#0AB68B",show="*",bd=0,width=21)
passwordentry.pack(side=RIGHT,padx=1.47,pady=2,ipady=3)

maxconnections=Frame(borderwidth=2, relief="groove")
maxconnections.pack()
maxconnectionslabel=Label(maxconnections,text="Max Connections:",font=("Arial",10,"italic","underline","bold"))
maxconnectionslabel.pack(side=LEFT)

maxconnectionsentry=Entry(maxconnections,width=3,bd=0,bg="#0AB68B",justify='center',font=("Arial",10,"bold"))
maxconnectionsentry.insert(0,256)
maxconnectionsentry.pack(side=RIGHT,padx=2,pady=2,ipady=3)

def permissionsadd(perm):
    permlist.append(perm)
def permissionsremove(perm):
    permlist.remove(perm)

readcheckvar=IntVar()
readcheckvar.set(0)
def readcheckfunc():
    if readcheckvar.get()==0:
        permissionsremove("elr")
        print("Read Denied")
    else:
        permissionsadd("elr")
        print("Read Allowed")
        
uploadcheckvar=IntVar()
uploadcheckvar.set(0)
def uploadcheckfunc():
    if uploadcheckvar.get()==0:
        permissionsremove("awMT")
        print("Upload Denied")
    else:
        
        permissionsadd("awMT")
        print("Upload Allowed")

deletecheckvar=IntVar()
deletecheckvar.set(0)
def deletecheckfunc():
    if deletecheckvar.get()==0:
        permissionsremove("d")
        print("Delete Denied")
    else:
        permissionsadd("d")
        print("Delete Allowed")
        
renamecheckvar=IntVar()
renamecheckvar.set(0)
def renamecheckfunc():
    if renamecheckvar.get()==0:
        permissionsremove("f")
        print("Rename Denied")
    else:
        permissionsadd("f")
        print("Rename Allowed")
        
createcheckvar=IntVar()
createcheckvar.set(0)
def createcheckfunc():
    if createcheckvar.get()==0:
        permissionsremove("m")
        print("Create Directory Denied")
    else:
        permissionsadd("m")
        print("Create Directory Allowed")
        
check=Frame()
check.pack()

readcheck=Checkbutton(check,text="Allow Read",variable=readcheckvar,command=readcheckfunc)
readcheck.select()
readcheck.pack(side=LEFT)

uploadcheck=Checkbutton(check,text="Allow Upload",variable=uploadcheckvar,command=uploadcheckfunc)
uploadcheck.select()
uploadcheck.pack(side=LEFT)

deletecheck=Checkbutton(check,text="Allow Delete",variable=deletecheckvar,command=deletecheckfunc)
deletecheck.select()
deletecheck.pack(side=LEFT)

check2=Frame()
check2.pack()

renamecheck=Checkbutton(check2,text="Allow Rename",variable=renamecheckvar,command=renamecheckfunc)
renamecheck.select()
renamecheck.pack(side=LEFT)

createcheck=Checkbutton(check2,text="Allow Create Directory",variable=createcheckvar,command=createcheckfunc)
createcheck.select()
createcheck.pack(side=LEFT)

group=Frame()
group.pack(side=BOTTOM)

charlist=[]
def ftpthreding():
    char = "".join(random.choice(string.ascii_letters) for x in range(10))
    charlist.append(char)
    if char not in charlist:
        ftpthreding()
    thread=threading.Thread(target=ftp,name=char)
    return thread

def startstop():
    if directoryentry.get()=="":
        print("Please select directory!")
    else:
        if len(threading.enumerate())==1:
            ftpthreding().start()
            buton["text"]="Stop"
            buton["bg"]="#BE375F"
        else:
            server.close_all()
            buton["bg"]="#3E54D3"
            buton["text"]="Start"
            print("Ftp stopped")
  
buton=Button(group,text="Start",font=("Arial",15),bg="#3E54D3",fg="white",bd=2,command=startstop)
buton.pack(fill=BOTH)

text = scrolledtext.ScrolledText(group,height=7,bd=5,bg="black",fg="white")
text.pack(fill=Y,side=BOTTOM)

class Redirect():
    def __init__(self, widget):
        self.widget = widget
        
    def write(self, text):
        self.widget.insert('end', text)
        self.widget.yview_pickplace("end")
        
old_stdout = sys.stdout   
sys.stdout = Redirect(text)

print("Devoloper: Enes Uysal")
app.mainloop()
sys.stdout = old_stdout

