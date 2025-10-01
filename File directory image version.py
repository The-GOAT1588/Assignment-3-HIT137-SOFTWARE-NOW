from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk




class App(Tk):
    def __init__(self):
        super().__init__()
            # this is the name of the program and visual detail, delete self.iconbitmap to get it working on another device
        self.title("File Directory")
        self.iconbitmap('C:/Users/Nicholas/Desktop/Assignment3code/clown.ico')
        self.geometry('700x500')
            
        self.image_label = Label(self)
        self.image_label.pack(pady=20)

        #button function
        self.my_button = Button(self, text="Open Image", command=self.open_image)
        self.my_button.pack(pady=20)


        # prevents garbage
        self.img = None

    
    
    def open_image(self):
        #this is the important code that allows use to find files and keeps track of file directory
        file_path = filedialog.askopenfilename(
            initialdir="",
            title="Select an Image File",
            filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*"))
        )
               #opens the image
        if file_path:
            image = Image.open(file_path)
            
            # Resize image to fit window if it's too big
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.img)

# runs the app
app = App()
app.mainloop()