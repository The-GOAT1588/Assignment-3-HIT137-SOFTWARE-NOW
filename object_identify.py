
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline



model = pipeline("object-detection", model="facebook/detr-resnet-50")
def run_detection(image_path: str):

    image = Image.open(image_path).convert("RGB")
    results = model(image)
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
            outline="red", width=8
        )

        # Label text
        text = f"{label} ({score:.2f})"
        

        # Get text size
        try:
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except AttributeError:
            text_width, text_height = font.getsize(text)

        text_ymin = max(0, box['ymin'] - text_height - 4)

        # Draw background and label
        draw.rectangle(
            [box['xmin'], text_ymin, box['xmin'] + text_width + 4, text_ymin + text_height + 4],
            fill="black"
        )
        draw.text((box['xmin'] + 2, text_ymin + 2), text, fill="white", font=font)
    
    return image, results 