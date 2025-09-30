import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

# Use GPU if available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Ask user to input image path
image_path = input("Enter the full path to the image file: ").strip()

# Load image
try:
    image = Image.open(image_path).convert("RGB")
except Exception as e:
    print(f"Error loading image: {e}")
    exit()

# Load model and processor
print("[1] Loading processor...")
processor = AutoProcessor.from_pretrained("ibm-granite/granite-docling-258M")

print("[2] Loading model...")
model = AutoModelForImageTextToText.from_pretrained("ibm-granite/granite-docling-258M").to(DEVICE)

print("[3] Preparing input...")
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "Extract all visible text from this image."}
        ]
    }
]
inputs_text = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(text=inputs_text, images=[image], return_tensors="pt").to(DEVICE)

print("[4] Running inference... (this may take 10–30 seconds on CPU)")
generated_ids = model.generate(**inputs, max_new_tokens=2048)

print("[5] Decoding output...")
output = processor.decode(generated_ids[0], skip_special_tokens=True)
print("\n📝 Extracted Text:\n")
print(output)
