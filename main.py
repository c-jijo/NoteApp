import customtkinter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from pathlib import Path

customtkinter.set_appearance_mode("dark")

tagdict = {'': []}
currentTag = ""
selectedFileIndex = None


def new_tag(tagmenu): #Creates a new tag
     global currentTag
     tagname = customtkinter.CTkInputDialog(text="Enter name of new tag", title="New Tag")
     newtagname = tagname.get_input()
     tagdict[newtagname] = []
     currentTag = newtagname
     tagmenu.configure(values=list(tagdict.keys()))
     
    
def delete_tag(rtag, tagmenu): #Deletes tags
     global currentTag
     tagdict.pop(rtag)
     tagmenu.configure(values=list(tagdict.keys()))
    
def show_tagContextMenu(event, tagContextMenu, notelist): #Creates a context menu when right clicking in the tag frame
    global selectedFileIndex
    selectedFileIndex = notelist.nearest(event.y)
    notelist.selection_set(selectedFileIndex)
    tagContextMenu.tk_popup(event.x_root, event.y_root)
    notelist.selection_clear(0, tk.END)
     

def add_notes(notelist): #Add notes to a tag
    global currentTag
    file = filedialog.askopenfilename()
    tagdict.setdefault(currentTag, []).append(file)
    fileList = [Path(path).stem for path in tagdict[currentTag]]
    notelist.delete(0, tk.END)
    for x in fileList:
        notelist.insert(tk.END, x) 

def delete_notes(notelist): #Delete notes from a tag
    global currentTag
    global selectedFileIndex
    selectedFile = notelist.get(selectedFileIndex)
    notelist.delete(selectedFileIndex)
    fileToDelete = next((f for f in tagdict[currentTag] if Path(f).stem == selectedFile), None)
    tagdict[currentTag].remove(fileToDelete)

    fileList = [Path(path).stem for path in tagdict[currentTag]]
    notelist.delete(0, tk.END)
    for x in fileList:
        notelist.insert(tk.END, x) 
     

def selecttag(selectedtag, notelist):  #Sets selected tag to currentTag
    global currentTag
    currentTag = selectedtag
    fileList = [Path(path).stem for path in tagdict[currentTag]]
    notelist.delete(0, tk.END)
    for x in fileList:
        notelist.insert(tk.END, x) 
     
     
def select_tagged_note(textbox, notelist): #Opens selected note in a tag
    taggedFileIndex = notelist.curselection()
    taggedFile = notelist.get(taggedFileIndex)
    file = next((f for f in tagdict[currentTag] if Path(f).stem == taggedFile), None)
    open_file(textbox, file)
     
     
def save_file(textdata): #Writes the textbox data to a text file
        print(textdata)
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        with open(file, "w") as f:
            f.write(textdata)

def open_file(textbox, readyfile): #Inserts data from opened files into the textbox
    if readyfile == None:
        file = filedialog.askopenfilename()
    else:
        file = readyfile
   
    textbox.delete("0.0", "end")
    with open(file) as f:
          textbox.insert("0.0", f.read())

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        global currentTag
        self.geometry("800x500")
        taglist = list(tagdict.keys())
        noteframe = customtkinter.CTkFrame(master=self, border_width=5)
        tagframe = customtkinter.CTkFrame(master=self, border_width=5)
        dateframe = customtkinter.CTkFrame(master=self, border_width=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #Frane that contains the textbox
        noteframe.grid(column=1, row=0, sticky="nsew", rowspan=2)
        noteframe.grid_rowconfigure(0, weight=1)
        noteframe.grid_columnconfigure(0, weight=1)

        tagframe.grid(column=0, row=0, sticky="nsew") #Frame that contains the tags and notes associated with them
        dateframe.grid(column=0, row=1, sticky="nsew" ) #Frame that contains the calendar

        self.notelist = tk.Listbox(tagframe, selectmode=tk.SINGLE)
        self.notelist.grid()
        self.notelist.bind("<Double-Button-1>", lambda e:select_tagged_note(self.textbox, self.notelist))

        #Top left corner menubar
        self.menubar = tk.Menu(self)
        self.configure(menu=self.menubar)

        self.file = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "File", menu = self.file)
        self.file.add_command(label = "Open Note", command = lambda:open_file(self.textbox, None))
        self.file.add_command(label = "Save Note As", command=lambda: save_file(self.textbox.get("0.0", "end")))

        self.tag = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "Tag", menu = self.tag)
        self.tag.add_command(label = "New Tag", command=lambda:new_tag(tagmenu))
        self.tag.add_command(label = "Delete Tag", command=lambda:delete_tag(currentTag, tagmenu))

        #Context menu that appears when you right click in the tagframe
        self.tagContextMenu = tk.Menu(self, tearoff=0)
        self.tagContextMenu.add_command(label = "Add note to tag", command=lambda:add_notes(self.notelist))
        self.tagContextMenu.add_command(label = "Delete note from tag", command=lambda:delete_notes(self.notelist))
        self.notelist.bind("<Button-3>", lambda event: show_tagContextMenu(event, self.tagContextMenu, self.notelist))

        #Textbox in which notes are taken
        self.textbox = customtkinter.CTkTextbox(master=noteframe, corner_radius=20, undo=True, border_width=5, font=(None, 24))
        self.textbox.grid(padx=30, pady=30, sticky="nsew")

        #Menu that contains a list of all tags and allows you to select one
        tagmenu = customtkinter.CTkOptionMenu(tagframe, values=taglist, command=lambda selectedtag: selecttag(selectedtag, self.notelist))
        tagmenu.grid()

        self.protocol("WM_DESTROY_WINDOW", self.destroy)

app = App()
app.mainloop()
