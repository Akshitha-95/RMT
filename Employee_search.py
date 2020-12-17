from tkinter import *
import sqlite3
from tkinter import messagebox
import sys
import os
import tkinter.font as tkFont
b=sys.path.append(r"Python_Poc_V0.10")
from  itertools import chain
import Add_Resource
import Add_Task
import Update_Task
global empid,empname

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
         root.destroy()
         os.remove("unamefile.txt")
         os.system('TASKKILL /F /IM python.exe')    
    
def cleardata():
    e1.delete(first=0,last=100)
    e2.delete(first=0,last=100)

def fetch():
     global empid,empname,result,result1,taskename

     #Database Connection
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     empdata=cursor.execute("select * from Employee")
     empdetails=empdata.fetchall()

     #Variable Declaration
     empid=e1.get()
     empname=e2.get()
     empname=empname.capitalize()
     nempname=empname
     result=empid in chain(*empdetails)
     result1=empname in chain(*empdetails)

     #Prechecks
     for i in range (len(empdetails)):
          if  result!= True and empid != "":
              messagebox.showinfo('Fetchdata','Invalid Employee Id Or Employee Id Not Exists')
              cleardata()
              break
          
          elif  result1!= True  and empname != "":
              messagebox.showinfo('Fetch Data','Invalid Employee Name Or Employee Name Not Exists')
              cleardata()
              break
          
          elif empid == "" and empname =="":
              messagebox.showinfo('Fetch Data',"Enter Employee Id/Employee Name")
              break

          elif empid != "" and empname != "":
              messagebox.showinfo('Fetch Data',"Modify The Search Criteria")
              cleardata()
              break

          
          elif result == True or result1 == True:
              
              if empname!= "" and not any(char.isalpha() for char in empname):
                  messagebox.showinfo('Fetch Data',"Please Enter correct Employee Name")
                  cleardata()
                  break
              else:
                  with open("unamefile.txt",'r',encoding = 'utf-8') as f:
                      userid=f.read()
                  manager=cursor.execute("select Empname from New_User where Username=?",(userid,))
                  managern=manager.fetchall()
                  conn.close
                  if managern != []:
                          managern = (managern[0])
                          managern=(managern[0])

                  #Data Report
                  root.withdraw()
                  displaydata()

def deleteemp():
     global empid,empname,result,result1

     #Database Connection
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     cursor1=conn.cursor()
     empdata=cursor.execute("select * from Employee")
     empdetails=empdata.fetchall()
        
     #Variable Declaration
     empid=e1.get()
     empname=e2.get()
     empname=empname.capitalize()
     result=empid in chain(*empdetails)
     result1=empname in chain(*empdetails)

     with open("unamefile.txt",'r',encoding = 'utf-8') as f:
         userid=f.read()
     manager=cursor.execute("select Empname from New_User where Username=?",(userid,))
     managern=manager.fetchall()
     if managern != []:
          managern = (managern[0])
          managern=(managern[0])
          allempid=cursor.execute("select Empid from Employee where Manager=?",(managern,))
          empnameall=allempid.fetchall()

     #Precheck Conditions
     for i in range(len(empdetails)):
          if  result!= True and empid != "":
              messagebox.showinfo('Delete','Employee does not exists')
              cleardata()
              break
          
          elif  result1!= True  and empname != "":
              messagebox.showinfo('Delete','Employee does not exists')
              cleardata()
              break
          
          elif empid == "" and empname =="":
              messagebox.showinfo('Delete',"Enter Employee Id/Employee Name")
              break

          elif empid != "" and empname != "":
              messagebox.showinfo('Delete',"Modify The Search Criteria")
              cleardata()
              break

          #Delete Employee
          elif result == True or result1== True:
              if empname!= "" and not any(char.isalpha() for char in empname):
                  messagebox.showinfo('Delete',"Please Enter correct Employee Name")
                  cleardata()
                  break
              else:
                                        
                  taskename=cursor.execute("select Empid from Employee where Empname=?",(empname,))
                  taskename= cursor.fetchall()
                  if taskename != []:
                      taskename = (taskename[0])
                      taskename=(taskename[0])
                  if empid in chain(*empnameall) or taskename in chain(*empnameall):
                      if messagebox.askokcancel("Delete", "Are you sure you want to Delete the Record?"):
                                                   
                          cursor1.execute("Delete from Task where empid=? ", (str(empid) or str(taskename),))
                          cursor.execute("Delete from Employee where Empid=? OR Empname=?",(empid,empname,))
                          cursor.execute("Delete from New_User where Empid=? OR Empname=?",(empid,empname,))
                          conn.commit()
                          conn.close
                          messagebox.showinfo('Delete',"Employee Record Deleted...")
                          cleardata()
                          break
                      else:
                          
                          break
                  else:
                      messagebox.showinfo("Delete", "You are not granted to delete this employee")
                      break
               

def displaydata():
     fontStyle=12
     global empid,empname
     import Employee_search
     root = Tk()

     #GUI Configuration
     window_height = 470
     window_width = 1000
     screen_width = root.winfo_screenwidth()
     screen_height = root.winfo_screenheight()
     x_cordinate = int((screen_width/2) - (window_width/2))
     y_cordinate = int((screen_height/2) - (window_height/2))
     root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
     root.resizable(0,1)
     root.title('Employee Search Page')
     root.configure(background = "#191970")
     taskename=""

     #Database Connection
     db = sqlite3.connect("sqlite_database")
     cur=db.cursor()
     cur1=db.cursor()    
     taskename=cur.execute("select Empid from Employee where Empname=?",(empname,))
     taskename= cur.fetchall()
     
     if taskename != []:
         taskename = (taskename[0])
         taskename=(taskename[0])

     #Querty to fetch Employee and Task Details    
     cur.execute("SELECT * FROM Employee WHERE Empname=? OR Empid=?", (empname,empid,))
     cur1.execute("SELECT * FROM Task WHERE empid=? ", (empid or taskename,))

     #Display Employee Record Label
     Label(root, text="EMP_ID",bg='#191970',fg='white',font=fontStyle).place(x=20 ,y=32)
     Label(root, text="EMP_Name",bg='#191970',fg='white',font=fontStyle).place(x=160 ,y=32)
     Label(root, text="Location",bg='#191970',fg='white',font=fontStyle).place(x=300 ,y=32)
     Label(root, text="Designation",bg='#191970',fg='white',font=fontStyle).place(x=440 ,y=32)
     Label(root, text="Manager",bg='#191970',fg='white',font=fontStyle).place(x=580 ,y=32)
     Label(root, text="DOJ",bg='#191970',fg='white',font=fontStyle).place(x=720,y=32)
     Label(root, text="-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
           bg='#191970',fg='white',font=fontStyle).place(x=20 ,y=53)

       
     sb = Scrollbar(root)  
     sb.pack(side = RIGHT, fill = Y)

     #Fetch data from Database
     index=0
     ch=50
     for row in cur:
          index=index+80
          rh=20
          ch=ch+32
          for i in range(len(row)):
              Libcontect_label = Label(root, text=row[i], bg='#191970',fg='white',font=fontStyle).place(x=rh ,y=ch)
              rh=rh+140
     
     #Display Task Record Label
     Label(root, text="EMP_ID",bg='#191970',fg='white',font=fontStyle).place(x=20 ,y=132)
     Label(root, text="Task_Name",bg='#191970',fg='white',font=fontStyle).place(x=160 ,y=132)
     Label(root, text="Startdate",bg='#191970',fg='white',font=fontStyle).place(x=300 ,y=132)
     Label(root, text="Enddate",bg='#191970',fg='white',font=fontStyle).place(x=440 ,y=132)
     Label(root, text="Hours",bg='#191970',fg='white',font=fontStyle).place(x=580,y=132)
     Label(root, text="Utilization",bg='#191970',fg='white',font=fontStyle).place(x=720 ,y=132)
     Label(root, text="Status",bg='#191970',fg='white',font=fontStyle).place(x=860 ,y=132)
     Label(root, text="-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
           bg='#191970',fg='white',font=fontStyle).place(x=20 ,y=150)
     ch = 100

     #Fetch Data from database
     for row in cur1:
          index=index+80
          rh=20
          ch=ch+100
          for i in range(len(row)):
              Libcontect_label = Label(root, text=row[i], bg='#191970',fg='white',font=fontStyle).place(x=rh ,y=ch)
              rh=rh+140
          ch=ch-50    

     Back = Button(root,text="BACK",bg='#7EC0EE',fg='black',command=lambda:[root.withdraw(),Employee_search.creategui()],width = 10)
     Back.place(x=900 ,y=8)  
     root.protocol("WM_DELETE_WINDOW", on_closing)         
     root.mainloop()

def updatetask():
     global empid,empname,result,result1

     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()

     with open("unamefile.txt",'r',encoding = 'utf-8') as f:
         userid=f.read()
     manager=cursor.execute("select Empname from New_User where Username=?",(userid,))
     managern=manager.fetchall()
     
     if managern != []:
         managern = (managern[0])
         managern=(managern[0])
     allempid=cursor.execute("select Empid from Employee where Manager=?",(managern,))
     empnameall=allempid.fetchall()
     
     #Database Connection
     empdata=cursor.execute("select * from Employee")
     empdetails=empdata.fetchall()

     #Variable Declaration
     empid=e1.get()
     empname=e2.get()
     empname=empname.capitalize()
     result=empid in chain(*empdetails)
     result1=empname in chain(*empdetails)
     
     #Task Fetch
     if empname!= "" and not any(char.isalpha() for char in empname):
                  messagebox.showinfo('Update',"Please Enter correct Employee Name")
                  cleardata()
                  return
     else:
         if(empid !="" and result == True) or (empname !="" and result1 == True):
             
             emptn=cursor.execute("select Empid from Employee where Empname=?",(empname,))
             name=emptn.fetchall()
             if name != []:
                 name = (name[0])
                 name=(name[0])
             if empid in chain(*empnameall) or name in chain(*empnameall):    
                 emptk=cursor.execute("select empid from Task where empid=?",(empid or name,))
                 emp=emptk.fetchall()
                 conn.close
             else:
                 messagebox.showinfo("Update", "You are not granted to update this employee Record")
                 return
     
     #Precheck Condition
     for i in range (len(empdetails)):
          if  result!= True and empid != "":
              messagebox.showinfo('Update','Employee does not exists')
              break
          
          elif  result1!= True  and empname != "":
              messagebox.showinfo('Update','Employee does not exists')
              break
          
          elif empid == "" and empname =="":
              messagebox.showinfo('Update',"Enter Employee Id/Employee Name")
              break
            
          elif emp == []:
              messagebox.showinfo('Update',"Employee doesn't have any task to update")
              cleardata()
              break

          elif empid != "" and empname != "":
              messagebox.showinfo('Update',"Modify The Search Criteria")
              cleardata()
              break
          
                     
          elif result == True or result1== True:
              if empname!= "" and not any(char.isalpha() for char in empname):
                  messagebox.showinfo('Update',"Please Enter correct Employee Name")
                  cleardata()
                  break
              else:
                  root.withdraw()
                  Update_Task.creategui()
              
def creategui():
     import Login_Page
     global e1,e2,e3,e4,root
     root = Toplevel()
     
     #GUI Background
     bgimage = PhotoImage(file = r"Backimagefor_POC.PNG")
     img=Label(root,image=bgimage)
     img.place(x=0,y=0)

     #GUI Configuration
     window_height = 370
     window_width = 470
     screen_width = root.winfo_screenwidth()
     screen_height = root.winfo_screenheight()
     x_cordinate = int((screen_width/2) - (window_width/2))
     y_cordinate = int((screen_height/2) - (window_height/2))
     root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
     root.resizable(0,0)
     root.title('Employee Search Page')

     #Font Declararion
     fontStyle = tkFont.Font(family="Courier", size=13,weight="normal", slant="roman")
     fontStyle1 = tkFont.Font(family="Courier", size=10,weight="normal", slant="roman")
     fontStyle2 = tkFont.Font(family="Courier", size=17,weight="bold", slant="roman")
     fontStyle3 = tkFont.Font(family="Courier", size=15,weight="bold", slant="roman")
     
     #Label
     Label(root, text="EMPLOYEE SEARCH PAGE",bg='#5190ED',fg='white',font=fontStyle2).place(x=90 ,y=22)
     Label(root, text="Employee Id",bg='#5190ED',fg='black',font=fontStyle).place(x=110 ,y=78)
     Label(root, text="Or",bg='#5190ED',fg='black',font=fontStyle).place(x=155 ,y=108)
     Label(root, text="Employee Name",bg='#5190ED',fg='black',font=fontStyle).place(x=110 ,y=138)
     Label(root, text="--------------------------------------------------------------------------",bg='#5190ED',fg='#5190ED',font=fontStyle).place(x=2 ,y=255)
     Label(root, text="EMPLOYEE MANAGEMENT OPERATION",bg='#5190ED',fg='white',font=fontStyle3).place(x=60 ,y=255)
     
     #Employee ID
     e1 = Entry(root)
     e1.place(x=260 ,y=78)
     e1.focus_set()

     #Employee Name
     e2 = Entry(root)
     e2.place(x=260 ,y=138)

     #Fetch Button
     Fetchdata=Button(root,text="Fetch",bg='#7EC0EE',fg='black',font=fontStyle1,command=fetch,width = 10)
     Fetchdata.place(x=50 ,y=180)

     #Clear Button
     Clear=Button(root,text="Clear",bg='#7EC0EE',fg='black',font=fontStyle1,command=cleardata,width = 10)
     Clear.place(x=180 ,y=180)

     #Cancel Button
     Cancelbutton=Button(root,text="Log Off",bg='#7EC0EE',fg='black',font=fontStyle1,command=lambda:[root.withdraw(),Login_Page.window()],width = 10)
     Cancelbutton.place(x=310 ,y=180)
     
     #Add Resource Button
     Addresource=Button(root,text="Add Resource",bg='#7EC0EE',fg='black',font=fontStyle1,command=lambda:[root.withdraw(),Add_Resource.creategui()],width = 16)
     Addresource.place(x=75 ,y=300)

     #Assign Task Button
     Assigntask=Button(root,text="Add Task",bg='#7EC0EE',fg='black',font=fontStyle1,command=lambda:[root.withdraw(),Add_Task.creategui()],width = 16)
     Assigntask.place(x=235 ,y=300)

     #Delete Button
     Deleteemp=Button(root,text="Delete Employee",bg='#7EC0EE',fg='black',font=fontStyle1,command=deleteemp,width = 16)
     Deleteemp.place(x=235 ,y=220)

     #Update Button
     Updatebutton=Button(root,text="Update Task",bg='#7EC0EE',fg='black',font=fontStyle1,command=updatetask,width = 16)
     Updatebutton.place(x=75 ,y=220)
     root.protocol("WM_DELETE_WINDOW", on_closing)
     mainloop()
