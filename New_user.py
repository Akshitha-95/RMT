from tkinter import *
import sqlite3
from tkinter import messagebox
import sys
import tkinter.font as tkFont
b=sys.path.append(r"Python_Poc_V0.10")
from  itertools import chain
import Login_Page
from tkcalendar import DateEntry
from datetime import date,timedelta,datetime
import os
import pathlib


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
     global data1,conn,cursor
     conn=sqlite3.connect(r"sqlite_database")
     cursor=conn.cursor()
     data=cursor.execute("select * from New_user")
     data1=data.fetchall()
     conn.close

def cleardata():
    e1.delete(first=0,last=100)
    e2.delete(first=0,last=100)
    e3.delete(first=0,last=100)
    tkvar1.set('Select privilage')
    tkvar2.set('Select Question')
    e4.delete(first=0,last=100)
    e5.delete(first=0,last=100)
    e6.delete(first=0,last=100)
    
def userdata():
        connections()
        #Variable  Declaration
        empname=e1.get()
        empid=e2.get()
        username=e3.get()
        username=username.lower()
        privilege=tkvar1.get()
        secretquestion=tkvar2.get()  
        secretanswer=e4.get()
        password=e5.get()
        confirmpassword=e6.get()
        SpecialSym =['$', '@', '#', '%'] 
        res=username in chain(*data1)
        res1=empid in chain(*data1)
        yearlen = (len(str(secretanswer)))
        #Precheck Condition
        for i in range (len(data1)):
         
                if empname == "" or username == "" or empid == "" or privilege == 'Select privilage' or secretquestion == 'Select Question' or secretanswer == "" or password == "" or confirmpassword == "" :
                     messagebox.showinfo("User_Update"," * Mandatory feilds should not be empty")
                     break
                        
                    
                elif res == True and username != "":
                     messagebox.showinfo('Login','Username already exist')
                     
                     break
          
                elif  res1 == True  and empid != "":
                      messagebox.showinfo('Login','Employee Id already exist')
                      break

                elif any(char.isdigit() for char in empname):
                     messagebox.showinfo('New_User',"Please Enter Correct Employee Name")
                     break
                    
                elif any(char.isdigit() for char in username):
                     messagebox.showinfo('New_User',"Please Enter Correct Employee Username \n (Accept only Characters)")
                     break 
                    
                elif any(char.isalpha() for char in empid):
                     messagebox.showinfo('New_User',"Please Enter Correct Employee ID")
                     break 


                elif secretquestion == 'Year of joining the current company?'and any(char.isalpha() for char in secretanswer):
                     messagebox.showinfo('New_User',"Enter the Correct Answer \n in 'YYYY' format")
                     break

                elif secretquestion != 'Year of joining the current company?'and any(char.isdigit() for char in secretanswer):
                     messagebox.showinfo('New_User',"Enter the Correct Answer in string format")
                     break    

                elif secretquestion == 'Year of joining the current company?'and len(str(secretanswer)) != 4 :
                     messagebox.showinfo('New_User',"Enter the Correct secret Answer \n in 'YYYY' format")
                     break      

                elif len (empid) >=8:
                     messagebox.showinfo('New_User',"EmpID is restricted \n to 8 charcters")
                     break  
                     
                elif len(password) < 8: 
                    messagebox.showinfo("New_User","length should be \n at least 8")
                    break
              
                elif len(password) > 20: 
                    messagebox.showinfo("New_User","length should be not \n be greater than 20") 
                    break
              
                elif not any(char.isdigit() for char in password): 
                    messagebox.showinfo("New_User","Password should have at \n least one numeral") 
                    break
              
                elif not any(char.isupper() for char in password): 
                    messagebox.showinfo("New_User","Password should have at least \n one uppercase letter") 
                    break
              
                elif not any(char.islower() for char in password): 
                    messagebox.showinfo("New_User","Password should have at least \n one lowercase letter") 
                    break
              
                elif not any(char in SpecialSym for char in password): 
                    messagebox.showinfo("New_User","Password should have at \n least one of the symbols \n $ @ # %") 
                    break
                
                elif  password !=  confirmpassword:
                   messagebox.showinfo("New_User","Password and Confirm Password \n did not match")
                   break
            
                elif i == (len(data1)-1):
                    #Insert Into Database
                    cursor.execute("Insert into New_User Values(?,?,?,?,?,?,?)",(empname,empid,username,password,privilege,secretquestion,secretanswer))
                    conn.commit()
                    conn.close
                    messagebox.showinfo("New_User","Added Successfully")
                    cleardata()
                    break
                
def creategui():
        global e1,e2,e3,e4,e5,e6,root,tkvar1,tkvar2
        root = Toplevel()
        root.title('New User Page')
        root['bg']='#191970'

        #Background Image
        bgimage = PhotoImage(file = r"Backimagefor_POC.PNG")
        img=Label(root,image=bgimage)
        img.place(x=0,y=0)

        #GUI Configuration
        window_height = 450
        window_width = 570
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        #root.resizable(0,0)
        #root.overrideredirect(1)

        #Font Declaration     
        fontStyle = tkFont.Font(family="Courier", size=13,weight="normal", slant="roman")
        fontStyle1 = tkFont.Font(family="Courier", size=10,weight="normal", slant="roman")
        fontStyle2 = tkFont.Font(family="Courier", size=17,weight="bold", slant="roman")
        
        #Label
        Label(root, text="NEW USER",bg='#5190ED',fg='white',font=fontStyle2).place(x=170 ,y=23)
        Label(root, text="Emp Name *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=65)
        Label(root, text="Emp ID *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=105)
        Label(root, text="Username *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=145)
        Label(root, text="Privilage *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=186)
        Label(root, text="Secret Question *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=227)
        Label(root, text="Secret Answer *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=266)
        Label(root, text="Password *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=306)
        Label(root, text="Confirm Password *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=346)

        #Empname
        e1 = Entry(root)
        e1.place(x=250 ,y=67)
        e1.focus_set()

        #Username
        e2 = Entry(root)
        #textvariable=IntVar()
        e2.place(x=250 ,y=107)
        
        #Username
        e3 = Entry(root)
        e3.place(x=250 ,y=147)

        #Privilege
        tkvar1 = StringVar(root)
        choices = { 'Manager','Employee'}
        tkvar1.set('Select privilage')
        popupMenu = OptionMenu(root, tkvar1, *choices)
        popupMenu.place(x=250 ,y=183)
        popupMenu.config(width=40)

        #Secret Question
        tkvar2 = StringVar(root)
        choices = { 'Year of joining the current company?',
                    'What is your pet name?',
                    'What is your higher secondary school name?',
                    'What is your mother’s maiden name?',
                    'What was your favorite food as child?'}
        tkvar2.set('Select Question')
        popupMenu = OptionMenu(root, tkvar2, *choices)
        popupMenu.place(x=250 ,y=230)
        popupMenu.config(width=40)

        e4 = Entry(root)
        e4.place(x=250 ,y=270)
        e4.config(width=40)

        #Password
        e5 = Entry(root,show="*")
        e5.place(x=250 ,y=310)

        #Confirm Password
        e6 = Entry(root,show="*")
        e6.place(x=250 ,y=350)

        #Add Button
        Addbutton=Button(root,text="Add",bg='#7EC0EE',fg='black',font=fontStyle1,command=userdata,width = 12)
        Addbutton.place(x=65 ,y=390)

        #Cancle Button
        Cancelbutton=Button(root,text='CLEAR',bg='#7EC0EE',fg='black',font=fontStyle1,command=cleardata,width = 12)
        Cancelbutton.place(x=222 ,y=390)
        
        #Back
        Back = Button(root,text="BACK",bg='#7EC0EE',fg='black',font=fontStyle1,command=lambda:[root.withdraw(),Login_Page.window()],width = 12)
        Back.place(x=380 ,y=390)

        root.protocol("WM_DELETE_WINDOW", on_closing)
        mainloop()
