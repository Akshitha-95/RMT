from tkinter import *
import sqlite3
from tkinter import messagebox
import tkinter.font as tkFont
import sys
import os
b=sys.path.append(r"Python_Poc_V0.10")
import Employee_search
import tkcalendar
from tkcalendar import DateEntry

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
         root.destroy()
         os.remove("unamefile.txt")
         os.system('TASKKILL /F /IM python.exe')

def cleardata():
    e1.delete(first=0,last=100)
    e2.delete(first=0,last=100)
    tkvar.set('Select Location')
    desig.set('Select Designation')
    e5.delete(first=0,last=100)

def savedata():
    #Database Connection
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     empdata=cursor.execute("select * from Employee")
     employeedetails=empdata.fetchall()
     conn.close

    #Variable Declaration
     emid=e1.get()
     emname=e2.get()
     emname=emname.capitalize()
     location=tkvar.get()
     designation=desig.get()
     maneger=e5.get()
     doj=e6.get()
     
     #Prechecks
     for i in range (len(employeedetails)):
          if emid=="" or emname=="" or location=='Select Location' or designation=='Select Designation' or maneger=="" or doj=="":
               messagebox.showinfo('Add Resource','Please fill all the fields')
               break          
          elif emid in employeedetails[i][0] and emid != "" and len(emid)== len(employeedetails[i][0]):
                  messagebox.showinfo('Add Resource','Employee ID already exist')
                  break

          elif emname in employeedetails[i][1] and emid != "":
                messagebox.showinfo('Add Resource','Employee Name already exist')
                break

          elif any(char.isalpha() for char in emid):
                     messagebox.showinfo('Add Resource',"Please Enter correct Employee ID")
                     break

          elif any(char.isdigit() for char in emname):
                     messagebox.showinfo('Add Resource',"Please Enter correct Employee Name")
                     break

          elif any(char.isdigit() for char in designation):
                     messagebox.showinfo('Add Resource',"Please Enter correct Designation")
                     break

          elif any(char.isdigit() for char in maneger):
                     messagebox.showinfo('Add Resource',"Please Enter correct Manager Name")
                     break

          #Insert Data into Database   
          elif i == (len(employeedetails)-1):
            cursor.execute("Insert into Employee Values(?,?,?,?,?,?)",(emid,emname,location,designation,maneger,doj))
            conn.commit()
            conn.close
            messagebox.showinfo('Add Resource','Employee details are added')
            cleardata()
            
def creategui():
     global e1,e2,tkvar,desig,e5,e6,root
     root = Toplevel()

     #GUIConfiguration
     window_height = 400
     window_width = 470
     screen_width = root.winfo_screenwidth()
     screen_height = root.winfo_screenheight()
     x_cordinate = int((screen_width/2) - (window_width/2))
     y_cordinate = int((screen_height/2) - (window_height/2))
     root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))   
     root.resizable(0,0)
     root.title('Add Resource Page')
     root.configure(background = "#191970")
     
     #Font Declaration
     fontStyle = tkFont.Font(family="Courier", size=13,weight="normal", slant="roman")
     fontStyle1 = tkFont.Font(family="Courier", size=10,weight="normal", slant="roman")
     fontStyle2 = tkFont.Font(family="Courier", size=17,weight="bold", slant="roman")
     
     #Background Image
     bgimage = PhotoImage(file = r"Backimagefor_POC.PNG")
     img=Label(root,image=bgimage)
     img.place(x=0,y=0)

     #Label
     Label(root, text="ADD RESOURCE PAGE",bg='#5190ED',fg='white',font=fontStyle2).place(x=100 ,y=20)
     Label(root, text="Employee Id *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=65)
     Label(root, text="Employee Name *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=105)
     Label(root, text="Location *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=145)
     Label(root, text="Designation *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=185)
     Label(root, text="Project Manager *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=225)
     Label(root, text="DOJ *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=265)

     #Employee Id
     e1 = Entry(root)
     e1.place(x=270 ,y=67)
     e1.config(width=28)
     e1.focus_set()
     
     #Employee Name
     e2 = Entry(root)
     e2.config(width=28)
     e2.place(x=270 ,y=107)

     #Location
     tkvar = StringVar(root)
     choices = {'Bangalore','Chennai','Coimbatore','Noida'}
     tkvar.set('Select Location')
     popupMenu = OptionMenu(root, tkvar, *choices)
     popupMenu.place(x=270 ,y=143)
     popupMenu.config(width=21)

     #Designation
     desig = StringVar(root)
     choices = {'Jr.Consultant','Consultant','Adv.Consultant','Sr.Consultant','Team Leader','Specialist','System Architect'}
     desig.set('Select Designation')
     popupMenu = OptionMenu(root, desig, *choices)
     popupMenu.place(x=270 ,y=188)
     popupMenu.config(width=21)

     #Project Manger
     with open("unamefile.txt",'r',encoding = 'utf-8') as f:
         userid=f.read()
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()    
     manager=cursor.execute("select Empname from New_User where Username=?",(userid,))
     managern=manager.fetchall()
     conn.close()
     if managern != []:
          managern = (managern[0])
          managern=(managern[0])

     v=StringVar()
     e5 = Entry(root,textvariable=v)
     v.set(managern)
     e5.place(x=270 ,y=228)
     e5.config(state='disabled')
     e5.config(width=28)

     #Doj
     e6 = DateEntry(root, locale='en_US', date_pattern='MM/dd/yyyy')
     e6.place(x=270 ,y=269)
     e6.config(width=26)

     #Save Button
     Savebutton=Button(root,text="SAVE",bg='#7EC0EE',fg='black',font=fontStyle1,command=savedata,width = 10)
     Savebutton.place(x=65 ,y=330)

     #Cancle Button
     Cancel = Button(root,text="CLEAR",bg='#7EC0EE',fg='black',font=fontStyle1,command=cleardata,width = 10)
     Cancel.place(x=198 ,y=330)

     #Back
     Back = Button(root,text="BACK",bg='#7EC0EE',fg='black',font=fontStyle1,command=lambda:[root.withdraw(),Employee_search.creategui()],width = 10)
     Back.place(x=330 ,y=330)
     root.protocol("WM_DELETE_WINDOW", on_closing)        
     mainloop()