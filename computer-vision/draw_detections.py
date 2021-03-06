from PIL import Image, ImageDraw, ImageFont
import os

def draw_objects(image_path, objects):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font="assets/Hack-Bold.ttf", size=15)
    for object in objects:
        draw.rectangle((
            object.rectangle.x,
            object.rectangle.y,
            object.rectangle.x + object.rectangle.w,
            object.rectangle.y + object.rectangle.h
        ), fill=None, outline="red", width=2)
        draw.text((object.rectangle.x + 1, object.rectangle.y + 1), object.object_property, font=font, fill="red")
    image.show()

    filename, ext = os.path.splitext(os.path.basename(image_path))
    n = 0
    if not os.path.isdir("output"):
        os.mkdir("output")
    while os.path.exists("output/" + filename + "_" + str(n) + ext):
        n += 1
    image.save("output/" + filename + "_" + str(n) + ext)