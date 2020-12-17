from tkinter import *
import sqlite3
from tkinter import messagebox
import sys
import os
import tkinter.font as tkFont
import time
b=sys.path.append(r"Python_Poc_V0.10")
import Forgot_password
import New_user
import pathlib
from  itertools import chain

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
         root.destroy()
         path=pathlib.Path("unamefile.txt")
         if path.exists():
             os.remove("unamefile.txt")
             os.system('TASKKILL /F /IM python.exe')
         else:
             os.system('TASKKILL /F /IM python.exe')

def connections():
     global data1,conn,cursor,data
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     data=cursor.execute("select * from New_user")
     data1=data.fetchall()
     conn.close
     
def insertdata():
    import Employee_search
    global uname,empid
    connections()
    #Variable Declaration
    uname=e1.get()
    uname=uname.lower()
    passw=e2.get()
    res=uname in chain(*data1)
    res1=passw in chain(*data1)

    #Precheck Conditions
    for i in range (len(data1)):
     
           if   uname == "":
              messagebox.showinfo('Login',"Enter Username")
              break
          
           elif passw == "":
             messagebox.showinfo('Login',"Enter Password")
             break
          
           elif res != True and uname != "":
               messagebox.showinfo('Login','Invalid Username')
               break
          
           elif  res1!= True  and passw != "":
               messagebox.showinfo('Login','Invalid Password')
               break
          
           elif uname in data1[i][2] and passw not in data1[i][3]:
                messagebox.showinfo('Login','Invalid Password')
                break
                                 

           elif uname in data1[i][2] and passw in data1[i][3]:
               with open("unamefile.txt",'w',encoding = 'utf-8') as f:
                   f.write(uname)

               empid = data1[i][1]  
               root.withdraw()
               if data1[i][4]== "Manager":
                    Employee_search.creategui()
               else:
                    displaydata()
             
def displaydata():
     global empname,empid,uname
     fontStyle=12
    
     root = Toplevel()  
     root.title('Employee Search Page')
     root.configure(background = "#191970")

     #GUI Configuration
     window_height = 470
     window_width = 1000
     screen_width = root.winfo_screenwidth()
     screen_height = root.winfo_screenheight()
     x_cordinate = int((screen_width/2) - (window_width/2))
     y_cordinate = int((screen_height/2) - (window_height/2))
     root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
     root.resizable(0,1)
     
     #Database Connection
     db = sqlite3.connect("sqlite_database")
     cur=db.cursor()
     cur1=db.cursor()
     uname=uname.lower()
     empnamedata=cur.execute("select Empname from New_User where Username=?",(uname,))
     empname=empnamedata.fetchall()
     
     if uname != "":
         empname=empname[0]
         empname=empname[0]
         #empname=empname.capitalize()
         
     cur.execute("SELECT * FROM Employee WHERE Empname=?", (empname,))
     cur1.execute("SELECT * FROM Task WHERE Empid=?", (empid,))

     #Label To display Employee Record
     Label(root, text="EMP_ID",bg='#191970',fg='white',font=fontStyle).place(x=20 ,y=32)
     Label(root, text="EMP_Name",bg='#191970',fg='white',font=fontStyle).place(x=160 ,y=32)
     Label(root, text="Location",bg='#191970',fg='white',font=fontStyle).place(x=300 ,y=32)
     Label(root, text="Designation",bg='#191970',fg='white',font=fontStyle).place(x=440 ,y=32)
     Label(root, text="Manager",bg='#191970',fg='white',font=fontStyle).place(x=580 ,y=32)
     Label(root, text="DOJ",bg='#191970',fg='white',font=fontStyle).place(x=720 ,y=32)
     Label(root, text="-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
           bg='#191970',fg='white',font=fontStyle).place(x=20 ,y=53)
     index=0
     #Fetch Employee data From The Database
     ch=50
     for row in cur:
          index=index+80
          rh=20
          ch=ch+32
          for i in range(len(row)):
               Libcontect_label = Label(root, text=row[i],bg='#191970',fg='white',font=fontStyle).place(x=rh ,y=ch)
               rh=rh+140

     #Label To display Task Record
     Label(root, text="EMP_ID",bg='#191970',fg='white',font=fontStyle).place(x=20 ,y=132)
     Label(root, text="Task_Name",bg='#191970',fg='white',font=fontStyle).place(x=160 ,y=132)
     Label(root, text="Startdate",bg='#191970',fg='white',font=fontStyle).place(x=300 ,y=132)
     Label(root, text="Enddate",bg='#191970',fg='white',font=fontStyle).place(x=440 ,y=132)
     Label(root, text="Hours",bg='#191970',fg='white',font=fontStyle).place(x=580 ,y=132)
     Label(root, text="Utilization",bg='#191970',fg='white',font=fontStyle).place(x=720 ,y=132)
     Label(root, text="Status",bg='#191970',fg='white',font=fontStyle).place(x=860 ,y=132)
     Label(root, text="-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
           bg='#191970',fg='white',font=fontStyle).place(x=20 ,y=150)
     scrollbar = Scrollbar(root)
     scrollbar.pack( side = RIGHT, fill = Y ) 
     ch = 100

     #Fetch Task data From The Database
     for row in cur1:
          index=index+80
          rh=20
          ch=ch+100
          for i in range(len(row)):
               Libcontect_label = Label(root, text=row[i], bg='#191970',fg='white',font=fontStyle).place(x=rh ,y=ch)
               rh=rh+140
          ch=ch-50    

     fontStyle1 = tkFont.Font(family="Courier", size=10,weight="normal", slant="roman")     
     Logout = Button(root,text="LOGOUT",bg='#7EC0EE',fg='black',font=fontStyle1,command= lambda:[root.withdraw(),window()],width = 10) 
     Logout.place(x=880 ,y=10)
     root.protocol("WM_DELETE_WINDOW", on_closing)
     mainloop()                 
   
def window():
     global e1,e2,root

     #window
     root = Toplevel()
     root.title('RMT Login Page')
     root.configure(background = "#191970")

     #GUI Configuration
     window_height = 300
     window_width = 470
     screen_width = root.winfo_screenwidth()
     screen_height = root.winfo_screenheight()
     x_cordinate = int((screen_width/2) - (window_width/2))
     y_cordinate = int((screen_height/2) - (window_height/2))
     root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
     root.resizable(0,0)

     #Font Declaration
     fontStyle = tkFont.Font(family="Courier", size=13,weight="normal", slant="roman")
     fontStyle1 = tkFont.Font(family="Courier", size=10,weight="normal", slant="roman")
     fontStyle2 = tkFont.Font(family="Courier", size=17,weight="bold", slant="roman")

     #Background Image
     bgimage = PhotoImage(file = r"Backimagefor_POC.PNG")
     img=Label(root,image=bgimage)
     img.place(x=0,y=0)

     #Label
     Label(root, text="RESOURCE MANAGEMENT TOOL - LOGIN ",bg='#5190ED',fg='white',font=fontStyle2 ).place(x=5 ,y=12)
     Label(root, text="USERNAME",bg='#5190ED',fg='black',font=fontStyle).place(x=120 ,y=60)
     Label(root, text="PASSWORD",bg='#5190ED',fg='black',font=fontStyle).place(x=120 ,y=100)

     #Username
     e1 = Entry(root)
     e1.place(x=240 ,y=62)
     e1.focus_set()

     #Paassowrd
     e2 = Entry(root,show="*")
     e2.place(x=240 ,y=102)

     #Login Button
     Loginbutton=Button(root,text="LOGIN", bg='#7EC0EE',fg='black',font=fontStyle1,command=insertdata,width = 17)
     Loginbutton.place(x=90 ,y=155)

     #Cancel Button
     Cancelbutton=Button(root,text="CLOSE",bg='#7EC0EE',fg='black',font=fontStyle1,command=on_closing,width = 17)
     Cancelbutton.place(x=250 ,y=155)

     #Forgot Password
     Forgotbutton=Button(root,text="FORGOT PASSWORD?",bg='#7EC0EE',fg='black',font=fontStyle1,command= lambda:[root.withdraw(),
          Forgot_password.creategui()],width = 17)
     Forgotbutton.place(x=90 ,y=205)

     #New User
     Newbutton=Button(root,text="NEW USER",bg='#7EC0EE',fg='black',font=fontStyle1,command=lambda:[root.withdraw(),
          New_user.creategui()],width = 17)
     Newbutton.place(x=250 ,y=205)

     root.protocol("WM_DELETE_WINDOW", on_closing)
     
     mainloop()
