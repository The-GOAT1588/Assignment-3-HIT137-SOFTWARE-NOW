from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
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
    
    def run_detection(self):
        
        

        image = Image.open(self.selected_image_path).convert("RGB")
        results = self.model(image)
        draw = ImageDraw.Draw(image)

        # Font with fallback
        try:
            font = ImageFont.truetype("arial.ttf", size=200)
        except IOError:
            print("Arial font not found, using default.")
            font = ImageFont.load_default()

        for obj in results:
            box = obj['box']
            label = obj['label']
            score = obj['score']

            # Draw rectangle
            draw.rectangle(
                [(box['xmin'], box['ymin']), (box['xmax'], box['ymax'])],
                outline="red", width=7
            )

            # Label text
            text = f"{label} ({score:.2f})"

            # Get text size safely
            try:
                # Preferred method (Pillow ≥ 8.0)
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
            except AttributeError:
                # Fallback for older Pillow versions
                text_width, text_height = font.getsize(text)

            # Prevent text from going above the image
            text_ymin = max(0, box['ymin'] - text_height - 4)

            # Draw text background
            draw.rectangle(
                [box['xmin'], text_ymin, box['xmin'] + text_width + 4, text_ymin + text_height + 4],
                fill="black"
            )

            # Draw text
            draw.text((box['xmin'] + 2, text_ymin + 2), text, fill="white", font=font)

        # Resize for display
        image = image.resize((600, 400), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.img)   




# Run the app
if __name__ == "__main__":
    app = App()
    app.mainloop()