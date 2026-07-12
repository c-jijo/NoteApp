import customtkinter
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

def save_file(textdata): #Writes the textbox data to a text file
        print(textdata)
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        with open(file, "w") as f:
            f.write(textdata)

def open_file(textbox):
     file = filedialog.askopenfilename()        
     with open(file) as f:
          textbox.insert("0.0", f.read())

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self, corner_radius=20, undo=True)
        self.textbox.grid(padx=30, pady=30, row=0, column=0, sticky="nsew")
        savebutton = customtkinter.CTkButton(self, text="Save As", command=lambda: save_file(self.textbox.get("0.0", "end"))) #Save As button
        savebutton.grid(padx=0, pady=0)
        openbutton = customtkinter.CTkButton(self, text="Open", command=lambda:open_file(self.textbox)) #Open button
        openbutton.grid(padx=0, pady=0)

    
         
        

app = App()
app.mainloop()
