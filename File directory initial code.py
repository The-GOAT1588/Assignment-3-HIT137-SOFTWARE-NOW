from tkinter import *
from tkinter import filedialog

class App(Tk):
    def __init__(self):
        super().__init__()
            # this is the name of the program and visual detail, delete self.iconbitmap to get it working on another device
        self.title("File Directory")
        self.iconbitmap('C:/Users/Nicholas/Desktop/Assignment3code/clown.ico')
        self.geometry('700x450')
            #this determines size
        self.my_text = Text(self, width=80, height=20)
        self.my_text.pack(pady=20)

        #this decides the 
        self.my_button = Button(self, text="Open File", command=self.file)
        self.my_button.pack(pady=20)

    
    
    def file(self):
        #this is the important code that allows use to find files and keeps track of file directory
        self.my_file = filedialog.askopenfilename(
            initialdir="",
            title="Select a File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
                #this reads text doccuments, not particurly useful for this assignment but proves the code works. 
        if self.my_file:
            with open(self.my_file, "r") as f:  # USE context manager
                content = f.read()
                self.my_text.delete(1.0, END)  # Clear existing text
                self.my_text.insert(END, content)

# runs the app
app = App()
app.mainloop()