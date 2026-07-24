import customtkinter
import tkinter as tk
import tkcalendar
from tkcalendar import Calendar
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from pathlib import Path
from datetime import datetime

customtkinter.set_appearance_mode("dark")

tagdict = {'': []}
datedict = {'': []}
currentTag = ""
currentDate = datetime.now()
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

def show_dateContextMenu(event, dateContextMenu, dateNoteList): #Creates a context menu when right clicking in the day frame
    global selectedFileIndex
    selectedFileIndex = dateNoteList.nearest(event.y)
    dateNoteList.selection_set(selectedFileIndex)
    dateContextMenu.tk_popup(event.x_root, event.y_root)
    dateNoteList.selection_clear(0, tk.END)
     

def add_notes(notelist): #Add notes to a tag
    global currentTag
    file = filedialog.askopenfilename()
    tagdict.setdefault(currentTag, []).append(file)
    populate_notelist(notelist)

def delete_notes(notelist): #Delete notes from a tag
    global currentTag
    global selectedFileIndex
    selectedFile = notelist.get(selectedFileIndex)
    notelist.delete(selectedFileIndex)
    fileToDelete = next((f for f in tagdict[currentTag] if Path(f).stem == selectedFile), None)
    tagdict[currentTag].remove(fileToDelete)

    populate_notelist(notelist)

     
def selecttag(selectedtag, notelist):  #Sets selected tag to currentTag
    global currentTag
    currentTag = selectedtag
    populate_notelist(notelist)

def add_notes_date(dateNoteList): #Add notes to a date
    global currentDate
    file = filedialog.askopenfilename()
    if currentDate in datedict:
        datedict.setdefault(currentDate, []).append(file)
    else:
        datedict[currentDate] = []
        datedict.setdefault(currentDate, []).append(file)
    print(datedict)
    populate_dateNotelist(dateNoteList)

def delete_notes_date(dateNoteList): #Delete notes from a date
    global currentDate
    global selectedFileIndex
    selectedFile = dateNoteList.get(selectedFileIndex)
    dateNoteList.delete(selectedFileIndex)
    fileToDelete = next((f for f in datedict[currentDate] if Path(f).stem == selectedFile), None)
    datedict[currentDate].remove(fileToDelete)

    populate_notelist(dateNoteList)


def populate_notelist(notelist):
    fileList = [Path(path).stem for path in tagdict[currentTag]]
    notelist.delete(0, tk.END)
    for x in fileList:
        notelist.insert(tk.END, x) 

def populate_dateNotelist(dateNoteList):
    fileList = [Path(path).stem for path in datedict[currentDate]]
    dateNoteList.delete(0, tk.END)
    for x in fileList:
        dateNoteList.insert(tk.END, x) 
    
     
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

def date_select(calendar, title, dateNoteList):
    global currentDate
    date = calendar.selection_get()
    currentDate = date
    formattedDate = date.strftime("%B %d, %Y")
    title.configure(text = formattedDate)
    if currentDate in datedict:
        populate_dateNotelist(dateNoteList)
    else:
        dateNoteList.delete(0, tk.END)

    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        global currentTag
        global currentDate
        self.geometry("800x500")
        taglist = list(tagdict.keys())
        noteframe = customtkinter.CTkFrame(master=self, border_width=5)
        tagframe = customtkinter.CTkFrame(master=self, border_width=5)
        dateframe = customtkinter.CTkFrame(master=self, border_width=5)
        monthframe = customtkinter.CTkFrame(master=dateframe, border_width=5)
        dayframe = customtkinter.CTkFrame(master=dateframe, border_width=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #Frame that contains the textbox
        noteframe.grid(column=1, row=0, sticky="nsew", rowspan=2)
        noteframe.grid_rowconfigure(0, weight=1)
        noteframe.grid_columnconfigure(0, weight=1)

        tagframe.grid(column=0, row=0, sticky="nsew") #Frame that contains the tags and notes associated with them

        dateframe.grid(column=0, row=1, sticky="nsew" ) #Frame that contains the calendar
        dateframe.grid_rowconfigure(0, weight=1)
        dateframe.grid_columnconfigure(0, weight=1)

        for frame in (monthframe, dayframe):
            frame.grid(row = 0, column = 0, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)


        self.notelist = tk.Listbox(tagframe, selectmode=tk.SINGLE)
        self.notelist.grid(sticky="nsew")
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

        self.dateTitle = customtkinter.CTkLabel(dayframe, text=currentDate.strftime("%B %d, %Y"))
        self.dateTitle.grid()

        self.backButton = customtkinter.CTkButton(dayframe, text="Calendar", command=lambda: monthframe.tkraise())
        self.backButton.grid(sticky="nw")

        self.dateNoteList = tk.Listbox(dayframe, selectmode=tk.SINGLE)
        self.dateNoteList.grid(sticky="nsew")

        #Context menu that appears when you right click in the day
        self.dateContextMenu = tk.Menu(self, tearoff=0)
        self.dateContextMenu.add_command(label = "Add note", command=lambda:add_notes_date(self.dateNoteList))
        self.dateContextMenu.add_command(label = "Delete note", command=lambda:delete_notes_date(self.dateNoteList))
        self.dateNoteList.bind("<Button-3>", lambda event: show_dateContextMenu(event, self.dateContextMenu, self.dateNoteList))

        #Calendar
        self.calendar = Calendar(monthframe, selectmode="day")
        self.calendar.grid(sticky="nsew")
        for dayRow in self.calendar._calendar:
            for date in dayRow:
                date.bind("<Double-Button-1>", lambda e: [date_select(self.calendar, self.dateTitle, self.dateNoteList), dayframe.tkraise()])

        self.protocol("WM_DESTROY_WINDOW", self.destroy)

app = App()
app.mainloop()
