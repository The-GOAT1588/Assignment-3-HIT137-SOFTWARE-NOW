import tkinter as tk
from tkinter import filedialog, scrolledtext
from transformers import pipeline

# Load Hugging Face image classification model
image_model = pipeline("image-classification", model="google/vit-base-patch16-224")

class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Classification Demo")
        self.geometry("700x500")

        # Browse button
        tk.Button(self, text="Browse Image", command=self.browse_file).pack(pady=10)

        # Run button
        tk.Button(self, text="Run Model", command=self.run_model).pack(pady=5)

        # Output area
        self.output_area = scrolledtext.ScrolledText(self, height=12, width=80)
        self.output_area.pack(pady=10)

        self.selected_file = None

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.webp")]
        )
        if file_path:
            self.selected_file = file_path
            self.output_area.insert(tk.END, f"Selected file: {file_path}\n")

    def run_model(self):
        self.output_area.delete(1.0, tk.END)
        if not self.selected_file:
            self.output_area.insert(tk.END, "⚠ Please select an image first.\n")
            return
        result = image_model(self.selected_file)[0]  # Top prediction
        label = result['label']
        score = round(result['score'] * 100, 2)
        self.output_area.insert(tk.END, f"Prediction: {label} ({score}% confidence)\n")

if __name__ == "__main__":
    app = ImageApp()
    app.mainloop()
