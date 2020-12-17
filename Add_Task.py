from tkinter import *
import sqlite3
from tkinter import messagebox
import tkinter.font as tkFont
import sys
import os
import Employee_search
import tkcalendar
from tkcalendar import DateEntry
from datetime import date,timedelta,datetime
import numpy as np
from  itertools import chain

b=sys.path.append(r"Python_Poc_V0.10")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
         root.destroy()
         os.remove("unamefile.txt")
         os.system('TASKKILL /F /IM python.exe')
         
def cleardata():
    e4.delete(first=0,last=100)
    name.set('Select Emp ID')
    tname.set('Select Task Name')

def savedata():
     #Database Connection
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     empdata=cursor.execute("select * from Task")
     employeedetails=empdata.fetchall()
     #conn.close
     
     #Variable Declaration
     ename=name.get()
     if ename != 'Select Emp ID':
         ename=eval(ename)
         ename=(ename[0])  
     taskname=tname.get()
     startdate=e2.get()
     nstartdate =startdate
     enddate=e3.get()
     nenddate=enddate
     hours=e4.get()
     status="Yet To Start"

     if nenddate < nstartdate:
         messagebox.showinfo('Add Task','End date should be greater than start date')
         return

     #Utilization Calculation
     startdate=datetime.strptime(startdate, '%m/%d/%Y').date()
     enddate=datetime.strptime(enddate, '%m/%d/%Y').date()
     days = np.busday_count(startdate, enddate)
     days=days+1
     if hours != "" and any(char.isdigit() for char in hours):
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

     #Utilization Date Check
     startdateu= ""
     enddateu=""
     if ename != 'Select Emp ID':
         newquery = cursor.execute("select startdate, enddate from Task where empid={} order by enddate desc limit 1".format(ename))
         filteredElement = newquery.fetchall()
         if filteredElement != []:
             startdate1=filteredElement[0]
             startdateu=startdate1[0]
             enddateu=startdate1[1]

     #Upadte TaskId
     edata=cursor.execute("select count(empid) from Task where empid=?",(ename,))
     empdetails=edata.fetchall()
     empdetails=empdetails[0]
     empdetails=empdetails[0]
     print(empdetails)
     id="Task_Id_"
     tid='Task_Id_1'
     a=1
     if empdetails ==0:
         count=1
         taskid=id + str(count)
     else:
         count=empdetails + 1
         taskid=id + str(count)

     #Fetching Taskid
     if ename != 'Select Emp ID' and empdetails != 0:
         etid=cursor.execute("select taskid from Task where empid=?",(ename,))
         etask=etid.fetchall()
     
         #convert tuple to list
         res = [list(ele) for ele in etask]
         res1 = [ item for elem in etask for item in elem]
         
         #Fetching Numbers
         res2 = list(map(lambda sub:int(''.join([ele for ele in sub if ele.isnumeric()])), res1)) 
         res2.sort()

         #Checking Number Sequence
         result=sorted(set(range(res2[0], res2[-1])) - set(res2))
         for i in range(len(res1)):
             if result !=[]:
                 for i in range(len(res1)):
                     
                     if str(result[0]) not in res1[i]:
                         taskid='Task_Id_' + str(result[0])
                     elif taskid in res1[i]:
                         taskid='Task_Id_' + str(result[0])
                         
             elif result ==[] and str(a) not in str(res2[0]):
                       taskid=tid
             else:
                taskid=taskid
             
         taskid=taskid
     dt=date.today()
     dt=str(dt)
     datetimeobject = datetime.strptime(dt,'%Y-%m-%d')
     todaydate = datetimeobject.strftime('%m/%d/%Y')      
     #PreChecks
     for i in range (len(employeedetails)):
         if startdateu != "" and (startdateu < nstartdate < enddateu) or nstartdate == startdateu :
             messagebox.showinfo('Add Task', 'Already Occupied,Please check previous task assignments')
             break

         elif ename == 'Select Emp ID' or taskname == 'Select Task Name' or startdate == "" or enddate == "" or hours =="" :
             messagebox.showinfo('Add Task','Please fill all the fields')
             break
            
         elif any(char.isalpha() for char in hours):
                     messagebox.showinfo('Add Task',"Please Enter Correct Hours")
                     break

                    
         elif nenddate < nstartdate:
             messagebox.showinfo('Add Task','End date should be greater than start date')
             break

         elif nenddate < todaydate or nstartdate < todaydate:
             messagebox.showinfo('Add Task','Can not assign the task on previous date')
             break     
            
         elif i == (len(employeedetails)-1):
            cursor.execute("insert into Task Values(?,?, ?, ?, ?, ?,?,?)",(ename,taskname,nstartdate,nenddate,hours,utilization,status,taskid))
            conn.commit()
            conn.close
            messagebox.showinfo('Add Task','Task is assigned')
            cleardata()
     
def creategui():
     global e1,e2,e3,e4,name,root,tname
     root = Toplevel() 
    
     #Backgroung Image
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
     root.title('Add Task Page')
     root.configure(background = "#191970")
     
     #Font Defination
     fontStyle = tkFont.Font(family="Courier", size=13,weight="normal", slant="roman")
     fontStyle1 = tkFont.Font(family="Courier", size=10,weight="normal", slant="roman")
     fontStyle2 = tkFont.Font(family="Courier", size=17,weight="bold", slant="roman")

     #Label
     Label(root, text="ADD TASK PAGE",bg='#5190ED',fg='white',font=fontStyle2).place(x=155 ,y=20)
     Label(root, text="EMPLOYEE ID *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=65)
     Label(root, text="TASK NAME *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=105)
     Label(root, text="START DATE *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=145)
     Label(root, text="END DATE *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=185)
     Label(root, text="NO OF HOURS *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=225)
     
     #Database Connection
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     with open("unamefile.txt",'r',encoding = 'utf-8') as f:
         userid=f.read()
     manager=cursor.execute("select Empname from New_User where Username=?",(userid,))
     managern=manager.fetchall()

     if managern != []:
         managern = (managern[0])
         managern=(managern[0])
         ename=cursor.execute("select Empid from Employee where Manager=?",(managern,))
         empname=ename.fetchall()
         conn.close
     
     #Employee Name
     if managern == None or empname==[] :
             #messagebox.showinfo('Add Task','No user exists under you')        
             name = StringVar(root)
             choices = {'No Records...'}
             name.set('Select Emp ID')
             popupMenu = OptionMenu(root, name, *choices)
     else:
                  
         name = StringVar(root)
         choices = {*empname}
         name.set('Select Emp ID')
         popupMenu = OptionMenu(root, name, *choices)
         
     popupMenu.place(x=270 ,y=65)
     popupMenu.config(width=17)
     
     #Task name
     tname = StringVar(root)
     choices = {'L&D Trainings' ,'White Paper' ,'L& D Assignment' , 'POC project'}
     tname.set('Select Task Name')
     popupMenu = OptionMenu(root, tname, *choices)
     popupMenu.place(x=270 ,y=108)
     popupMenu.config(width=17)

     #Start date
     e2=DateEntry(root, locale='en_US', date_pattern='MM/dd/yyyy')
     e2.place(x=270 ,y=148)
     e2.config(width=20)
        
     #End date
     e3 = DateEntry(root, locale='en_US', date_pattern='MM/dd/yyyy')
     e3.place(x=270 ,y=188)
     e3.config(width=20)

     #No of hours
     e4 = Entry(root)
     e4.place(x=270 ,y=229)
     e4.config(width=23)

     #Assign Button
     Assignbutton=Button(root,text="ASSIGN",bg='#7EC0EE',fg='black',font=fontStyle1,command=savedata,width = 10)
     Assignbutton.place(x=65 ,y=290)

     #Cancle Button
     Cancel = Button(root,text="CLEAR",bg='#7EC0EE',fg='black',font=fontStyle1,command=cleardata,width = 10)
     Cancel.place(x=198 ,y=290)

     #Back
     Back = Button(root,text="BACK",bg='#7EC0EE',fg='black',font=fontStyle1,command=lambda:[root.withdraw(),Employee_search.creategui()],width = 10)
     Back.place(x=330 ,y=290)

     root.protocol("WM_DELETE_WINDOW", on_closing)
     
     mainloop()

#creategui()