import os
import cv2

def save_image(image, filename, ext):
    n = 0
    if not os.path.isdir("output"):
        os.mkdir("output")
    while os.path.exists("output/" + filename + "_" + str(n) + ext):
        n += 1
    image.save("output/" + filename + "_" + str(n) + ext)

# using basic cv2 to draw lol. Can use pillow later tho
def draw_objects(image, objects, wait=False):
    # file path, read it. Else, it's a cv2 image
    if isinstance(image, str):
        img = cv2.imread(image)
    else:
        img = image
    w = img.shape[1]
    h = img.shape[0]

    for object in objects:
        start = (int(object.bounding_box.left*w), int(object.bounding_box.top*h))
        end = (int(object.bounding_box.left*w + object.bounding_box.width*w), int(object.bounding_box.top*h + object.bounding_box.height*h))
        color = (0, 0, 255)
        thickness = 2
        img = cv2.rectangle(img, start, end, color, thickness)
    cv2.imshow("viewing", img)
    if wait:
        print ("Press any key to continue...")
        cv2.waitKey(0) 
        cv2.destroyAllWindows()

    # filename, ext = os.path.splitext(os.path.basename(image_path))
    # save_image(img, filename, ext)
