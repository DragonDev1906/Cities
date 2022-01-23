import csv
# import json
import glob
# import os
import math
from PIL import Image, ImageDraw

def IsFloat(s):
    try:
        float(s)
    except:
        return False
    else:
        return True

def FloatOrZero(s):
    try:
        return float(s)
    except:
        return 0.0

def IntOrZero(s):
    try:
        return int(s)
    except:
        return 0

def generate_globe_data(files, output, size):
    width = size
    height = size // 2
    data = []
    # Read all cities into data
    for filename in files:
        print("Processing %s" % filename)
        with open(filename, "r") as fp:
            reader = csv.reader(fp, delimiter=";")
            next(reader) # Skip header
            data += [
                (x[0], FloatOrZero(x[3]), FloatOrZero(x[4]), IntOrZero(x[5])) 
                for x in reader
                if len(x) == 9
            ]

    image = Image.new("L", (width, height))
    # draw = ImageDraw.Draw(image)
    print("Setting pixels")
    brightnessMul = size / 1024 / 8       # Found by experimenting at size=2048
    for _, lat, lon, pop in data:
        x = int((width / 2) + lon * width / 360)
        y = int((height / 2) - lat * height / 180)
        # brightness = int(brightnessMul * min(math.log2(max(pop, 1)), 2**12) + 0.5)
        brightness = size // 2048
        image.putpixel((x, y), min(image.getpixel((x, y)) + brightness, 255))
        # draw.rectangle((x-10, y-10, x+10, y+10), fill=64, outline=0)

    print("Saving")
    image.save(output)

if __name__ == "__main__":
    size = 2048
    generate_globe_data(
        # 2,3,4,5,6,7
        # 
        # glob.glob("raw-data/villages.94.csv"), 
        # glob.glob("raw-data/*.csv"),
        ["raw-data/cities.csv", "raw-data/towns.csv", "raw-data/villages.csv"],
        "public/cities-%dx%d.jpeg" % (size, size//2),
        size
    )