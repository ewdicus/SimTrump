from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import textwrap

# Resources and Output
BASE_IMAGE_PATH = "./assets/base_image.jpg"
FONT_PATH = "./assets/pixChicago.ttf"
RESULT_IMAGE_PATH = "./output/{}.jpg"

# Parameters for drawing text
TEXT_START_LOCATION = (370, 90)
COLOR = (0,0,0)
LINE_SPACING = 10
MAX_WIDTH = 560
MAX_HEIGHT = 270

# Defaults for wrapping text
MAX_FONT = 35
MIN_FONT = 20
MAX_WRAP = 35
MIN_WRAP = 30
STEP = 1

def make_image(text, filename='result'):
    path = RESULT_IMAGE_PATH.format(filename)
    with Image.open(BASE_IMAGE_PATH) as img:
        # Get a drawing context
        draw = ImageDraw.Draw(img)

        text, font_size = find_text_parameters(draw, text)
        if not text:
            return

        # Uncomment to check bounding box for text
        # draw.rectangle(
        #     (TEXT_START_LOCATION,
        #     (TEXT_START_LOCATION[0] + MAX_WIDTH, TEXT_START_LOCATION[1] + MAX_HEIGHT)
        # ), fill=(255,0,0), outline=None)

        font = ImageFont.truetype(FONT_PATH, font_size)
        draw.multiline_text(TEXT_START_LOCATION,
                            text,
                            COLOR,
                            font=font,
                            spacing=LINE_SPACING,
                            align='left')
        img.save(path)
    return path

def find_text_parameters(draw, text):
    font_size = MAX_FONT
    wrap = MAX_WRAP

    doesFit = False
    while not doesFit:
        wrapped = textwrap.fill(text, wrap)
        doesFit, tooWide, tooTall = check_fit(draw, wrapped, font_size)

        # if we bottom out on a lower limit of font or wrap, log that we can't do it
        # along with the text
        if font_size <= MIN_FONT and wrap <= MAX_WRAP:
            print("Error: Text doesn't fit! Text: {}".format(text))
            return None, None

        # if it's too tall, reduce font size and check again
        if tooTall:
            font_size -= STEP

        # if it's too wide, reduce wrap and check again
        elif tooWide:
            wrap -= STEP

    return wrapped, font_size

def check_fit(draw, text, font_size):
    font = ImageFont.truetype(FONT_PATH, font_size)
    w,h = draw.multiline_textsize(text, font=font, spacing=LINE_SPACING)
    tooWide = w > MAX_WIDTH
    tooTall = h > MAX_HEIGHT
    doesFit = not tooWide and not tooTall
    return doesFit, tooWide, tooTall


