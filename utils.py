from PIL import Image

import base64
import pytesseract
import io

imgstring = ''

with open("img1.jpg",'rb') as img_file:
    imgstring = base64.b64encode(img_file.read())
#print(imgstring)
#imgstring = imgstring.split('base64,')[-1].strip()
# pic = io.StringIO(imgstring)
def image_to_text(img_string):
    image_string = io.BytesIO(base64.b64decode(imgstring))
    image = Image.open(image_string)

    # # Overlay on white background, see http://stackoverflow.com/a/7911663/1703216
    # bg = Image.new("RGB", image.size, (255,255,255))
    # x, y = image.size
    # bg.paste(image,(0,0,x,y),image)

    return((pytesseract.image_to_string(image,lang="vie")))
