import os
import sys
import torch
from PIL import Image
from transformers import AutoProcessor
from huggingface_hub import snapshot_download

model_id = "vikhyatk/moondream1"
local_dir = snapshot_download(model_id)

sys.path.append(local_dir)

from moondream import MoondreamForConditionalGeneration

processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
model = MoondreamForConditionalGeneration.from_pretrained(model_id, trust_remote_code=True)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

image_path = r"C:\Users\John\Documents\Python\Assignment3\sign.JPG"
image = Image.open(image_path).convert("RGB")

image_embeds = model.encode_image(image)

question = "What is happening in this image?"
answer = model.answer_question(image_embeds=image_embeds, question=question, tokenizer=processor)

print("Answer:", answer)
