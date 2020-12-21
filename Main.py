#Main Page
import sys
from tkinter import *

b=sys.path.append(r"Python_Poc_V0.10")
import Login_Page

if __name__ == '__main__':
    root = Tk()
    root.title('RMT Login Page')
    root.configure(background = "#191970")
    root.withdraw()
    Login_Page.window()
