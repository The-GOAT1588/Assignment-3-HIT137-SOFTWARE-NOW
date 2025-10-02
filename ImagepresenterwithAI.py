from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from transformers import pipeline


class App(Tk):
    def __init__(self):
        super().__init__()

        # visual aspects of the program, removed the .ico file
        self.title("File Directory with Object Detection")
       
        self.geometry('700x500')

        self.image_label = Label(self)
        self.image_label.pack(pady=20)
        #button to open image
        self.my_button = Button(self, text="Open Image", command=self.open_image)
        self.my_button.pack(pady=20)
        #button to run object detection
        self.detect_button = Button(self, text="Run object detection", command=self.run_detection, state=DISABLED)
        self.detect_button.pack(pady=10)

        #cleans rubbish
        self.img = None
        self.selected_image_path = None

        # Load Hugging Face DETR pipeline
        self.model = pipeline("object-detection", model="facebook/detr-resnet-50")

    def open_image(self):
        #this is the important code that allows use to find files and keeps track of file directory
        file_path = filedialog.askopenfilename(
            initialdir="",
            title="Select an Image File",
            filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*"))
        )
        #opens the image and converts it to rgb 

        if file_path:
            self.selected_image_path = file_path
            image = Image.open(file_path).convert("RGB")
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.img)

            self.detect_button.config(state=NORMAL) 
    #ai part
    def run_detection(self):
        if not self.selected_image_path:
            print("No image selected.")
            return

        image = Image.open(self.selected_image_path).convert("RGB")
        results = self.model(image)
        #proof of concept, prints the identified features in the terminal 
        print("\n🔍 Detection Results:")
        if not results:
            print("No objects detected.")
        for obj in results:
            label = obj['label']
            score = obj['score']
            box = obj['box']
            print(f"- {label} ({score:.2f}) at {box}")


# Run the app
if __name__ == "__main__":
    app = App()
    app.mainloop()