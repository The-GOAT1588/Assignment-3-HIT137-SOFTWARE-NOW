from transformers import VitsTokenizer, VitsModel, set_seed
import torch
import sounddevice as sd

tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-eng")
model = VitsModel.from_pretrained("facebook/mms-tts-eng")


inputs = tokenizer(text="Hello - my dog is cute", return_tensors="pt")

set_seed(555)  # make deterministic

with torch.no_grad():
    outputs = model(inputs["input_ids"])
outputs.waveform.shape

waveform_np = outputs.waveform.squeeze().cpu().numpy()

sd.play(waveform_np, samplerate=16000)
sd.wait()