import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Window settings
        self.title("File Directory")
        self.geometry("720x520")

        # Optional icon: keep commented if unavailable on your machine
        # try:
        #     self.iconbitmap(r"C:\path\to\icon.ico")
        # except Exception:
        #     pass

        # UI widgets
        self.image_label = tk.Label(self, text="No image selected", bd=2, relief=tk.SUNKEN, width=72, height=20)
        self.image_label.pack(padx=10, pady=(20, 8))

        self.filename_var = tk.StringVar(value="(no file)")
        tk.Label(self, textvariable=self.filename_var).pack()

        self.open_btn = tk.Button(self, text="Open Image", command=self.open_image)
        self.open_btn.pack(pady=12)

        # Keep a reference to the PhotoImage to prevent it being garbage-collected
        self._photo_image = None

    def open_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=(("Image files", ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif")), ("All files", "*.*"))
        )

        if not file_path:
            return

        try:
            img = Image.open(file_path).convert("RGB")

            # Compute fit size while preserving aspect ratio
            max_w, max_h = 680, 400
            w, h = img.size
            scale = min(max_w / w, max_h / h, 1.0)
            new_size = (int(w * scale), int(h * scale))
            if new_size != img.size:
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            self._photo_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self._photo_image, text="")  # remove text once image shown
            self.filename_var.set(file_path)
        except Exception as e:
            # Basic error reporting
            self.filename_var.set(f"Failed to open image: {e}")
            self.image_label.config(image="", text="No image selected")
            self._photo_image = None

if __name__ == "__main__":
    app = App()
    app.mainloop()