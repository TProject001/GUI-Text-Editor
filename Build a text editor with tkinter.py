from tkinter import *
from tkinter import filedialog as fd

root=Tk()
root.title("My Text-Editor")
root.geometry("1100x660")

#set variable for open file name
global open_file_name
open_file_name = False

#set variable for selected text( use in different block like function of cut_text,copy_text and paste_text)
global selected
selected= False

#Create Main Frame
my_frame=Frame(root)
my_frame.pack(pady=5)

#create our Scrollbar for the Text Box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT,fill=Y)

#Create Text Box
my_text = Text(my_frame,width=97,height=25,font=("helvetica",16 ), selectbackground="yellow" , selectforeground="black",undo=True,yscrollcommand=text_scroll.set)
#selectbackground = to highligth selected text
my_text.pack()

#configure our Scrollbar
text_scroll.config(command=my_text.yview)

#create  Menu
My_menu=Menu(root)
root.config(menu=My_menu)

def new_file():    
    #Delete previous text
    my_text.delete("1.0",END) #start point(it is always 0.1) to last(END)
    #update title and status bar
    root.title("New File - TextPad!")
    status_bar.config(text="New File     ")

    global open_file_name
    open_file_name = False
    
def open_file():
    my_text.delete("1.0",END)
    #Grab Filename
    text_file=fd.askopenfilename(initialdir="C:/",title="My file opener",filetypes=(("Text Files","*.txt"),("HTML File","*.html"),("Python Files","*.py"),("All Files","*.*")))
  
    #check to see if there is a file open(for file name)
    if text_file:
        #make fiename global so we can access throughout the program
        #here is global declare ,so to update the value
        
        global open_file_name
        open_file_name = text_file
        status_bar.config(text=f'Save mode     ')
        
    #update title and Status bars
    name=text_file
    root.title(f'{name}  - TextPad')    # f is format()
    ch = name.rfind('/')
    name= name.replace(name,name[ch+1:])
    status_bar.config(text=f'Saved as: {name}     ')

    #Open the file
    text_file = open(text_file,'r')
    stuff = text_file.read()
    #Add file to text
    my_text.insert(END,stuff)
    #Closed the opened file
    text_file.close()

#create Save as file  
def save_as_file():
    text_file=fd.asksaveasfilename(defaultextension=".*", initialdir="C:/",title="save File", filetypes=(("Text File","*.txt"),("Python File","*.py"),("HTML File","*.html"),("All Files","*.*")))
    if text_file:
        #update status bars
        name = text_file
        
        root.title(f'{name}  - TextPad')    # f is format()
        ch = name.rfind('/')
        name= name.replace(name,name[ch+1:])
        status_bar.config(text=f'Saved as: {name}     ')

        
        #Save the file
        text_file = open(text_file,"w")
        text_file.write(my_text.get(1.0,END))
        #close the file
        text_file.close()

# Save File
def save_file():
    global open_file_name
    if open_file_name:
        text_file = open(open_file_name,"w") 
        text_file.write(my_text.get(1.0,  END))

        #close the file
        text_file.close()
        
        name = open_file_name
        ch = name.rfind('/')
        name= name.replace(name,name[ch+1:])
        status_bar.config(text=f'Saved: {name}     ')
        
    else:
        save_as_file()

# Cut Text
def cut_text(e):
    global selected
    #check to see if we used keyboard shortcut or not
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            #Grab selected text from text box
            selected = my_text.selection_get()
            #delete selected text from text box
            my_text.delete("sel.first","sel.last")
            #clear anything in clipboard
            root.clipboard_clear()
            #append selected text in clipboard
            root.clipboard_append(selected)

# Copy Text
def copy_text(e):
    global selected
    #check to see if we used keyboard shortcut or not
    if e:
        selected = root.cllipboard_get()
    if my_text.selection_get():
        #Grab selected text from text box
        selected = my_text.selection_get()
        #clear anything in clipboard
        root.cllipboard_clear()
        #append selected text in clipboard
        root.cllipboard_append(selected)

# Paste Text
def paste_text(e):
    global selected
    #check to see if we used keyboard shortcut or not
    if e:
        selected = root.clipboard_get()  
    if selected:
        #Get current position of cursor
        position= my_text.index(INSERT)
        my_text.insert(position, selected)

#Add file menu
file_menu = Menu(My_menu,tearoff=0)
My_menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New",command=new_file)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Save",command=save_file)  #,command=save_file
file_menu.add_command(label="Save As",command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=root.quit)

#Add edit menu
edit_menu = Menu(My_menu,tearoff=0)
My_menu.add_cascade(label="Edit",menu=edit_menu)
edit_menu.add_command(label="Cut", command= lambda: cut_text(False))
edit_menu.add_command(label="Copy", command= lambda: copy_text(False))
edit_menu.add_command(label="Paste", command= lambda: paste_text(False))
edit_menu.add_separator()
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

#Edit Binding to Keyboard
root.bind("<Control-Key-x>", cut_text)
root.bind("<Control-Key-c>", copy_text)
root.bind("<Control-Key-v>", paste_text)

#Add status to bottom
status_bar = Label( root , text="Welcome!         " , anchor=E)
status_bar.pack(fill=X , side = BOTTOM , ipady=5)

root.mainloop()
