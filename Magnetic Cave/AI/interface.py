from tkinter import *
import os

root = Tk()
root.minsize(height=400, width=700)
root.configure(bg='#D3D3D3')

def open_main_file():
    os.system('python main.py')

def open_trying_file():
    os.system('python trying.py')

def open_part3_file():
    os.system('python part3.py')

label1 = Label(root, text='WELCOME IN MAGNATEC CAVE GAME', font=('Times_New_Roman', 30))
label1.grid(row=1, column=4, padx=25, pady=80)

button1 = Button(root, text='First Mode', font=('Times_New_Roman', 15), command=open_main_file)
button1.grid(row=3, column=4, padx=25, pady=40)

button2 = Button(root, text='Second Mode', font=('Times_New_Roman', 15), command=open_trying_file)
button2.grid(row=5, column=4, padx=25, pady=40)

button3 = Button(root, text='Third Mode', font=('Times_New_Roman', 15), command=open_part3_file)
button3.grid(row=7, column=4, padx=25, pady=40)

root.mainloop()