from tkinter import *
import sqlite3
from tkinter import messagebox
import sys
import tkinter.font as tkFont
b=sys.path.append(r"Python_Poc_V0.10")
from  itertools import chain
import Login_Page
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
    tkvar.set('Select Question')
    e3.delete(first=0,last=100)
    e4.delete(first=0,last=100)
    e5.delete(first=0,last=100)

def updatedata():
    #Variable Declaration
    connections()
    username=e1.get()
    empid=e2.get()
    secretquestion=tkvar.get()
    secretanswer=e3.get()
    password=e4.get()
    confirmpassword=e5.get()
    SpecialSym =['$', '@', '#', '%'] 
    res=username in chain(*data1)
    res1=empid in chain(*data1)
    res2=secretquestion in chain(*data1)
    res3=secretanswer in chain(*data1)
  
    #Precheck conditions
    for i in range (len(data1)):
                        
                if username == "" or empid == "" or secretquestion == 'Select Question' or secretanswer == "" or password == "" or confirmpassword == "" :
                    messagebox.showinfo("User_Update","Mandatory feilds should not be empty")
                    break
                elif  res!= True and username != "" :
                   messagebox.showinfo('User_Update',"Invalid Username")
                   break

                elif res1!= True and empid != "" :
                    messagebox.showinfo('User_Update',"Invalid Employee Id")
                    break
               
                elif res2!= True and secretquestion != "" :
                     messagebox.showinfo('User_Update',"Invalid Secret Question")
                     break

                elif res3!= True and secretanswer != "" :
                     messagebox.showinfo('User_Update',"Invalid Secret Answer")
                     break

               
                elif len(password) < 6: 
                    messagebox.showinfo("New_User","length should be \n at least 6") 
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
               
                elif username in data1[i][2] and empid not in data1[i][1]:
                     messagebox.showinfo('Login','Invalid Employee Id')
                     break

                elif username in data1[i][2] and secretquestion not in data1[i][5]:
                     messagebox.showinfo('Login','Invalid Secret Question')
                     break

                elif username in data1[i][2] and secretanswer not in data1[i][6]:
                     messagebox.showinfo('Login','Invalid Secret Answer')
                     break
                    
                elif username in data1[i][2] and password in data1[i][3]:
                     messagebox.showinfo('Login','New Password Cannot Be The Same As \n The Last Three Passwords')
                     break 
                #Update Database
                elif i == (len(data1)-1):
                     cursor.execute("Update New_User Set Password=? Where Username=?",(password,username)) 
                     conn.commit()
                     conn.close
                     messagebox.showinfo("User_Update","Password Updated Successfully")
                     cleardata()
                     break
                            


def creategui():
         global e1,e2,e3,e4,e5,tkvar,root
         root = Toplevel()  
         root.title('Forgot Password Page')
         root['bg']='#191970'

         #Background Image
         bgimage = PhotoImage(file = r"Backimagefor_POC.PNG")
         img=Label(root,image=bgimage)
         img.place(x=0,y=0)

         #GUI Configuration
         window_height = 400
         window_width = 560
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
         
         #Label
         Label(root, text="FORGOT PASSWORD",bg='#5190ED',fg='white',font=fontStyle2).place(x=125 ,y=20)
         Label(root, text="Username *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=65)
         Label(root, text="Employee ID *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=105)
         Label(root, text="Secret Question *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=145)
         Label(root, text="Secret Answer *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=185)
         Label(root, text="Password *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=225)
         Label(root, text="Confirm Password *",bg='#5190ED',fg='black',font=fontStyle).place(x=60 ,y=265)

         #Username
         e1 = Entry(root)
         e1.place(x=270 ,y=67)
         e1.focus_set()

         #EmpID
         e2 = Entry(root)
         e2.place(x=270 ,y=107)

         #Secret Question
         tkvar = StringVar(root)
         choices = {'Year of joining the current company?',
                    'What is your pet name?',
                    'What is your higher secondary school name?',
                    'What is your mother’s maiden name?',
                    'What was your favorite food as child?'}
         tkvar.set('Select Question')
         popupMenu = OptionMenu(root, tkvar, *choices)
         popupMenu.place(x=270 ,y=143)
         popupMenu.config(width=40)

         #Secret Answer
         e3 = Entry(root)
         e3.place(x=270 ,y=188)
         e3.config(width=40)

         #Password
         e4 = Entry(root,show="*")
         e4.place(x=270 ,y=228)

         #Confirm Password
         e5 = Entry(root,show="*")
         e5.place(x=270 ,y=269)

         #Save Button
         Savebutton=Button(root,text="SAVE",bg='#7EC0EE',fg='black',font=fontStyle1,command=updatedata,width = 10)
         Savebutton.place(x=65 ,y=330)

         # cancle Button
         Canclebutton=Button(root,text='CLEAR',bg='#7EC0EE',fg='black',font=fontStyle1,command=cleardata,width = 10)
         Canclebutton.place(x=198 ,y=330)

         #Back Button
         Back = Button(root,text="BACK",bg='#7EC0EE',fg='black',font=fontStyle1,command=lambda:[root.withdraw(),Login_Page.window()],width = 10)
         Back.place(x=330 ,y=330)

         root.protocol("WM_DELETE_WINDOW", on_closing)
         
         mainloop()

