from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

from Texttospeechfile import speak_text  
from object_identify import run_detection


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("File Directory with Object Detection and text to speech")
        self.geometry('900x550') 

        
        self.content_frame = Frame(self)
        self.content_frame.pack(pady=20)

        # Image display label
        self.image_label = Label(self.content_frame)
        self.image_label.grid(row=0, column=0, padx=10)

        # Text box beside the image
        self.text_box = Text(self.content_frame, width=30, height=25, wrap=WORD)
        self.text_box.grid(row=0, column=1, padx=10)

        # "Speak" button under the text box
        self.speak_button = Button(
            self.content_frame,
            text="Speak",
            command=self.speak_text_from_box
        )
        self.speak_button.grid(row=1, column=1, pady=10)

    
        self.my_button = Button(self, text="Open Image", command=self.open_image)
        self.my_button.pack(pady=10)

        self.detect_button = Button(self, text="Run object detection", command=self.run_detection, state=DISABLED)
        self.detect_button.pack(pady=5)

        
        self.img = None
        self.selected_image_path = None

        

    def speak_text_from_box(self):
        text = self.text_box.get("1.0", END).strip()
        if text:
            speak_text(text)
        else:
            print("Textbox is empty. Nothing to speak.")

    def open_image(self):
        file_path = filedialog.askopenfilename(
            initialdir="",
            title="Select an Image File",
            filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*"))
        )

        if file_path:
            self.selected_image_path = file_path
            image = Image.open(file_path).convert("RGB")
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.img)

            self.detect_button.config(state=NORMAL)

    def run_detection(self):
        if not self.selected_image_path:
            return

        annotated_image, results = run_detection(self.selected_image_path)

        
        self.text_box.delete("1.0", END)
        for obj in results:
            label = obj["label"]
            score = obj["score"]
            self.text_box.insert(END, f"{label}: {score:.2f}\n")

       
        annotated_image = annotated_image.resize((600, 400), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(annotated_image)
        self.image_label.config(image=self.img)
            

        


# Run the app
if __name__ == "__main__":
    app = App()
    app.mainloop()