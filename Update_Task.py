from tkinter import *
import sqlite3
from tkinter import messagebox
import tkinter.font as tkFont
import sys
import Employee_search
import tkcalendar
from tkcalendar import DateEntry
from datetime import date,timedelta,datetime
import numpy as np
import os
from  itertools import chain

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
         root.destroy()
         os.remove("unamefile.txt")
         os.system('TASKKILL /F /IM python.exe')

b=sys.path.append(r"Python_Poc_V0.10")

def cleardata():
    e1.delete(first=0,last=100)
    e4.delete(first=0,last=100)
    name.set('Select Task Id')
    svar.set('Select Status')
    
def deletetask():
     #global taskid
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     empdata=cursor.execute("select * from Task")
     employeedetails=empdata.fetchall()

     taskid=name.get()
     if taskid != "Select Task Id" :
         
         taskid=eval(taskid)
         taskid=(taskid[0])
     for i in range (len(employeedetails)):
         
         if  taskid == 'Select Task Id':
             messagebox.showinfo('Delete Task','Please select task id')
             break
         else:
                 if messagebox.askokcancel("Delete", "Are you sure you want to Delete the Task?"):
                     cursor.execute("Delete from Task where taskid=? ", (taskid,))
                     conn.commit()
                     conn.close
                     messagebox.showinfo('Delete',"Employee Task Deleted Successfully")
                     cleardata()
        
                     break
     cursor.execute("SELECT taskid FROM Task WHERE empid=? ", (employeeid or ename,))
     empname=cursor.fetchall()
     if empname != []:
         root.withdraw()
         Employee_search.updatetask()
     else:
         messagebox.showinfo('Delete',"All Task Deleted!")
         root.withdraw()
         Employee_search.creategui()
        
         
         
def updatedata():
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     empdata=cursor.execute("select * from Task")
     employeedetails=empdata.fetchall()
     conn.close

     #Variable Declaration
     tid=name.get()
     if tid != "Select Task Id":
         
         tid=eval(tid)
         tid=(tid[0])
     taskname=e1.get()
     startdate=e2.get()
     nstartdate =startdate
     enddate=e3.get()
     nenddate=enddate
     hours=e4.get()
     status=svar.get()

     if nenddate < nstartdate:
         messagebox.showinfo('Add Resource','End date should be greater than start date')
         return

     #Utilization Calculation
     startdate=datetime.strptime(startdate, '%m/%d/%Y').date()
     enddate=datetime.strptime(enddate, '%m/%d/%Y').date()
     days = np.busday_count(startdate, enddate)
     days=days+1
     
     if hours != "" and  any(char.isdigit() for char in hours):
         
         Days= int(days)
         Hours=int(hours)
         
         if(Hours > Days*8):
              messagebox.showinfo('Error', 'Hours cannot be more than 40Hrs per week')
              cleardata()
              return
            
     if hours != "" and not any(char.isalpha() for char in hours):
                  
         utilization=((int(hours)/int(days*8))*100)
         utilization=('%.2f'%utilization)
         utilization=str(utilization)+'%'
     else:
         utilization="0%"
            
    #Precheck Conditions
     for i in range (len(employeedetails)):
         
         if  tid == 'Select Task Id' or taskname == "" or startdate == "" or enddate == "" or hours =="" or status == 'Select Status':
             messagebox.showinfo('Add Resource','Please fill all the fields')
             break
            
         elif any(char.isalpha() for char in hours):
                     messagebox.showinfo('New_User',"Please Enter Correct Hours")
                     break

         elif nenddate < nstartdate:
             messagebox.showinfo('Add Resource','End date should be greater than start date')
             break

         #Update Query
         elif i == (len(employeedetails)-1):
             cursor.execute("Update Task Set taskname=?,startdate=?,enddate=?,hours=?,utilization=?, status=? Where taskid=?",(taskname,nstartdate,nenddate,hours,utilization,status,tid,)) 
             conn.commit()
             conn.close
             messagebox.showinfo("User_Update","Task Updated Successfully")
             cleardata()
             break
            
def display(event):
    #variable Declaration
     tn=name.get()
     tn=eval(tn)
     tn=(tn[0])
     #v.set(tn)

     #Database Connection
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     eupdate=cursor.execute("select taskname,startdate,enddate,hours,status from Task where taskid=? and empid=?",(tn,employeeid or ename,))
     empupdate=eupdate.fetchall()
     conn.close

     #Variable Defination
     tn=empupdate[0][0]
     sd=empupdate[0][1]
     ed=empupdate[0][2]
     hr=empupdate[0][3]
     st=empupdate[0][4]
     
     v.set(tn)
     p.set(sd)
     q.set(ed)
     s.set(hr)
     svar.set(st)
     
     return
    
def creategui():
     global e1,e2,e3,e4,name,root,v,s,p,q,svar
     root = Toplevel() 
     global employeeid,employeename,ename
     #Background Image
     bgimage = PhotoImage(file = r"Backimagefor_POC.PNG")
     img=Label(root,image=bgimage)
     img.place(x=0,y=0)

     #GUI Configuration
     window_height = 400
     window_width = 470
     screen_width = root.winfo_screenwidth()
     screen_height = root.winfo_screenheight()
     x_cordinate = int((screen_width/2) - (window_width/2))
     y_cordinate = int((screen_height/2) - (window_height/2))
     root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
     root.resizable(0,0)    
     root.title('Update Task Page')
     root.configure(background = "#191970")

     #Font Declaration
     fontStyle = tkFont.Font(family="Courier", size=13,weight="normal", slant="roman")
     fontStyle1 = tkFont.Font(family="Courier", size=10,weight="normal", slant="roman")
     fontStyle2 = tkFont.Font(family="Courier", size=17,weight="bold", slant="roman")

     #Label
     Label(root, text="UPDATE TASK PAGE",bg='#5190ED',fg='white',font=fontStyle2).place(x=155 ,y=20)
     Label(root, text="SELECT TASK ID *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=65)
     Label(root, text="TASK NAME *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=105)
     Label(root, text="START DATE *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=145)
     Label(root, text="END DATE *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=185)
     Label(root, text="NO OF HOURS *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=225)
     Label(root, text="STATUS *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=265)

     #Query to fetch the data for Updation from database
     employeeid=Employee_search.empid
     employeename=Employee_search.empname
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     ename=cursor.execute("select Empid from Employee where Empname=?",(employeename,))
     ename= cursor.fetchall()
     if ename != []:
         ename = (ename[0])
         ename=(ename[0])

     cursor.execute("SELECT taskid FROM Task WHERE empid=? ", (employeeid or ename,))
     empname=cursor.fetchall()
     empname.sort()

     with open("unamefile.txt",'r',encoding = 'utf-8') as f:
         userid=f.read()

     manager=cursor.execute("select Empname from New_User where Username=?",(userid,))
     managern=manager.fetchall()

     if managern != []:
         managern = (managern[0])
         managern=(managern[0])

         allempid=cursor.execute("select Empid from Employee where Manager=?",(managern,))
         empnameall=allempid.fetchall()
     conn.close
     
     #Task Option Menu Name
     if employeeid in chain(*empnameall) or ename in chain(*empnameall) :
         
         name = StringVar(root)
         choices = {*empname}
         name.set('Select Task Id')
         popupMenu = OptionMenu(root, name, *sorted(choices),command=display)
         popupMenu.place(x=270 ,y=65)
         popupMenu.config(width=17)
     else:
         name = StringVar(root)
         choices = {'No Record...'}
         name.set('Select Task Id')
         popupMenu = OptionMenu(root, name, *choices)
     popupMenu.place(x=270 ,y=65)
     popupMenu.config(width=17)

     #Task name     
     v=StringVar()
     e1 = Entry(root,textvariable=v)
     e1.place(x=270 ,y=108)
     e1.config(width=24)   
     #Start date
     p=StringVar()
     e2=DateEntry(root, locale='en_US', date_pattern='MM/dd/yyyy',textvariable=p)
     e2.place(x=270 ,y=144)
     e2.config(width=20)
       
     #End date
     q=StringVar()
     e3 = DateEntry(root, locale='en_US', date_pattern='MM/dd/yyyy',textvariable=q)
     e3.place(x=270 ,y=188)
     e3.config(width=20)

     #No of hours
     s=StringVar()
     e4 = Entry(root,textvariable=s)
     e4.place(x=270 ,y=229)
     e4.config(width=24)

     #status
     svar = StringVar(root)
     choice = {'In Progess','Yet to start','Completed'}
     svar.set('Select Status')
     popMenu = OptionMenu(root, svar, *choice)
     popMenu.place(x=270 ,y=269)
     popMenu.config(width=17)
     
     #Assign Button
     Updatebutton=Button(root,text="Update Task",bg='#7EC0EE',fg='black',font=fontStyle1,command=updatedata,width = 12)
     Updatebutton.place(x=25 ,y=320)

     #Cancle Button
     Cancel = Button(root,text="Clear",bg='#7EC0EE',fg='black',font=fontStyle1,command=cleardata,width = 12)
     Cancel.place(x=135 ,y=320)

     #Delete Button
     Delete = Button(root,text="Delete Task",bg='#7EC0EE',fg='black',font=fontStyle1,command=deletetask,width = 12)
     Delete.place(x=245 ,y=320)
     
     #Back
     Back = Button(root,text="Back",bg='#7EC0EE',fg='black',font=fontStyle1,command=lambda:[root.withdraw(),Employee_search.creategui()],width = 12)
     Back.place(x=355 ,y=320)

     root.protocol("WM_DELETE_WINDOW", on_closing)
     mainloop()

