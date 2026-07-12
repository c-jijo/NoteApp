import customtkinter
import tkinter

class Textbox(customtkinter.CTkTextbox):
    def __init__(self, master):
        super().__init__(master)
        self.textbox = customtkinter.CTkTextbox(master=self, height=500, width=300, corner_radius=20, undo=True)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        

    
        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        self.textbox = Textbox(master=self)
        self.textbox.grid(padx=30, pady=30, sticky="nsew")


app = App()
app.mainloop()
