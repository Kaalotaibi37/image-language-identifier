import os
import shutil

try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from langdetect import detect

# Set up the folders
folder = os.getcwd()
os.makedirs(os.path.join(folder, 
                "foreign_lang"), exist_ok=True)
os.makedirs(os.path.join(folder, "read_fail"), exist_ok=True)

print(pytesseract.get_languages(config=''))

for f in os.listdir(folder):

    if "png" in f:

        # OCR, convert image to text
        pic_txt = pytesseract.image_to_string(Image.open(os.path.join(
                                                    folder, f)))
        
        # Words that would exist in an English nutrition data table
        wordList = ["Energy", "Calories", "Fat", "Cholesterol", 
                    "Carbohydrate", "Protein"]

        # If tesseract completely failed to read the entire image
        if pic_txt.strip() == "" or len(pic_txt.strip()) == 1:
            shutil.move(os.path.join(folder, f),
                        os.path.join(folder, "read_fail", f))

        else:

            # Assume every image should be moved, unless
            # either one of the English words is recognized in pic_txt
            # or if language detection concludes the text in English
            toMove = True

            for word in wordList:
                if word in pic_txt:
                    toMove = False
          
            try:
                if detect(pic_txt) == "en":
                    toMove = False
            except:
                shutil.move(os.path.join(folder, f),
                        os.path.join(folder, "read_fail", f))
                continue

            if toMove:
                shutil.move(os.path.join(folder, f),
                            os.path.join(folder, "foreign_lang", f))


