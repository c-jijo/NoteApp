import customtkinter
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

customtkinter.set_appearance_mode("dark")

def save_file(textdata): #Writes the textbox data to a text file
        print(textdata)
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        with open(file, "w") as f:
            f.write(textdata)

def open_file(textbox): #Inserts data from opened files into the textbox
     file = filedialog.askopenfilename()        
     textbox.delete("0.0", "end")
     with open(file) as f:
          textbox.insert("0.0", f.read())

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")

        noteframe = customtkinter.CTkFrame(master=self, border_width=5)
        tabframe = customtkinter.CTkFrame(master=self, border_width=5)
        dateframe = customtkinter.CTkFrame(master=self, border_width=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)


        noteframe.grid(column=1, row=0, sticky="nsew", rowspan=2)
        noteframe.grid_rowconfigure(0, weight=1)
        noteframe.grid_columnconfigure(0, weight=1)

        tabframe.grid(column=0, row=0, sticky="nsew")
        dateframe.grid(column=0, row=1, sticky="nsew" )

        self.textbox = customtkinter.CTkTextbox(master=noteframe, corner_radius=20, undo=True, border_width=5, font=(None, 24))
        self.textbox.grid(padx=30, pady=30, sticky="nsew")
        savebutton = customtkinter.CTkButton(noteframe, text="Save As", command=lambda: save_file(self.textbox.get("0.0", "end")), fg_color="grey") #Save As button
        savebutton.grid(padx=0, pady=0)
        openbutton = customtkinter.CTkButton(noteframe, text="Open", command=lambda:open_file(self.textbox), fg_color="grey") #Open button
        openbutton.grid(padx=0, pady=0)

app = App()
app.mainloop()
