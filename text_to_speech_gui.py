
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog
from pathlib import Path

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    import winsound
except Exception:
    winsound = None


OUTPUT = Path("output.wav")


def speak_to_file(text: str, path: Path) -> None:
    """Synthesize text to the given WAV file using pyttsx3."""
    if pyttsx3 is None:
        raise RuntimeError("pyttsx3 is not installed")
    engine = pyttsx3.init()
    engine.save_to_file(text, str(path))
    engine.runAndWait()


class SimpleTTS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple TTS")
        self.geometry("600x360")

        tk.Label(self, text="Enter text:").pack(pady=(10, 0))
        self.text = scrolledtext.ScrolledText(self, height=10)
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        frame = tk.Frame(self)
        frame.pack(pady=6)

        self.btn = tk.Button(frame, text="Convert & Save", command=self.on_convert)
        self.btn.pack(side=tk.LEFT, padx=6)

        self.play_btn = tk.Button(frame, text="Play", command=self.on_play, state=tk.DISABLED)
        self.play_btn.pack(side=tk.LEFT)

        self.status = tk.Label(self, text=f"Output: {OUTPUT}")
        self.status.pack(pady=(6, 12))

    def on_convert(self):
        txt = self.text.get("1.0", tk.END).strip()
        if not txt:
            self.status.config(text="Please type some text first")
            return
        self.btn.config(state=tk.DISABLED)
        self.status.config(text="Generating...")

        def worker():
            try:
                speak_to_file(txt, OUTPUT)
                self.after(0, lambda: self.status.config(text=f"Saved: {OUTPUT}"))
                self.after(0, lambda: self.play_btn.config(state=tk.NORMAL))
            except Exception as e:
                self.after(0, lambda: self.status.config(text=f"Error: {e}"))
            finally:
                self.after(0, lambda: self.btn.config(state=tk.NORMAL))

        threading.Thread(target=worker, daemon=True).start()

    def on_play(self):
        if winsound:
            winsound.PlaySound(str(OUTPUT), winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            self.status.config(text=f"Play not available; open {OUTPUT} manually")


if __name__ == "__main__":
    app = SimpleTTS()
    app.mainloop()
