from PIL import Image, ImageDraw, ImageFont
import os

def save_image(image, filename, ext):
    n = 0
    if not os.path.isdir("output"):
        os.mkdir("output")
    while os.path.exists("output/" + filename + "_" + str(n) + ext):
        n += 1
    image.save("output/" + filename + "_" + str(n) + ext)

def draw_objects(image_path, objects, label=False):
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
        if label: draw.text((object.rectangle.x + 1, object.rectangle.y + 1), object.object_property, font=font, fill="red")
    image.show()

    filename, ext = os.path.splitext(os.path.basename(image_path))
    save_image(image, filename, ext)

def draw_faces(image_path, faces):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font="assets/Hack-Bold.ttf", size=15)
    for face in faces:
        draw.rectangle((
            face.face_rectangle.left,
            face.face_rectangle.top,
            face.face_rectangle.left + face.face_rectangle.width,
            face.face_rectangle.top + face.face_rectangle.height
        ), fill=None, outline="red", width=2)
        # draw.text((face.face_rectangle.left + 1, face.face_rectangle.top + 1), "face", font=font, fill="red")
    image.show()

    filename, ext = os.path.splitext(os.path.basename(image_path))
    save_image(image, filename, ext)