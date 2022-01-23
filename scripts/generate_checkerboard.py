import math
from PIL import Image, ImageDraw

def generate_checkerboard(output, size):
    width = size
    height = size // 2
    image = Image.new("L", (width, height))
    print("Setting pixels")
    for x in range(0, width, 2):
        for y in range(x%2, height, 2):
            image.putpixel((x, y), 255)

    print("Saving")
    image.save(output)

if __name__ == "__main__":
    size = 2048
    generate_checkerboard(
        "public/checkerboard_%dx%d.jpeg" % (size, size//2),
        size
    )