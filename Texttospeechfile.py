class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("File Directory with Object Detection")
        self.geometry('900x550')  # Wider window for side-by-side layout

        # === Frame to hold image and text side-by-side ===
        self.content_frame = Frame(self)
        self.content_frame.pack(pady=20)

        # Image display label
        self.image_label = Label(self.content_frame)
        self.image_label.grid(row=0, column=0, padx=10)

        # Text box beside the image
        self.text_box = Text(self.content_frame, width=30, height=25, wrap=WORD)
        self.text_box.grid(row=0, column=1, padx=10)

        # "Speak" button under the text box
        self.speak_button = Button(self.content_frame, text="Speak", command=self.speak_text)
        self.speak_button.grid(row=1, column=1, pady=10)

        # Buttons below
        self.my_button = Button(self, text="Open Image", command=self.open_image)
        self.my_button.pack(pady=10)

        self.detect_button = Button(self, text="Run object detection", command=self.run_detection, state=DISABLED)
        self.detect_button.pack(pady=5)

        # Keep track of state
        self.img = None
        self.selected_image_path = None

        # Load Hugging Face DETR pipeline
        self.model = pipeline("object-detection", model="facebook/detr-resnet-50")