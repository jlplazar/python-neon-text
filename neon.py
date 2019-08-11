#!/usr/bin/env python3

import argparse
import cairo
from PIL import ImageFilter, Image
from tools import transform_color

MIN_FONT_SIZE = 20
MAX_FONT_SIZE = 300
MAX_PADDING = 120
MIN_SHADOW = 20
FONT = "Zapfino"

BG_COLOR = '000000'
SHADOW_COLOR = 'ec0e77' #(0.929, 0.055, 0.467)
FG_COLOR_1 = 'ff31f4' #(1, 0.196, 0.957)
FG_COLOR_2 = 'ffd796' #(1, 0.847, 0.592)
FILL_COLOR = 'FFFFFF'

def _initialize(cr, width, height, text):
    cr.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    font_size = MAX_FONT_SIZE
    cr.set_font_size(font_size)
    x_bearing, y_bearing, t_width, t_height, _, _ = cr.text_extents(text)
    while (t_width > width - min(MAX_PADDING, font_size) or
           t_height > height - min(MAX_PADDING, font_size)) \
            and font_size > MIN_FONT_SIZE:
        font_size -= 2
        cr.set_font_size(font_size)
        x_bearing, y_bearing, t_width, t_height, _, _ = cr.text_extents(text)

    x = width / 2 - (t_width / 2 + x_bearing)
    y = height / 2 - (t_height / 2 + y_bearing)

    cr.move_to(x, y)
    cr.text_path(text)
    return font_size

def _draw_border(cr, rgb, line_width):
    cr.set_source_rgb(*rgb)
    cr.set_line_width(line_width)
    cr.stroke_preserve()

def _draw_base(cr, width, height, text, bg_color, shadow_color, fill_color):
    cr.set_source_rgb(*bg_color)
    cr.paint()

    font_size = _initialize(cr, width, height, text)

    _draw_border(cr, shadow_color, max(font_size / 3, MIN_SHADOW))
    _fill(cr, fill_color)

def _draw_text(cr, width, height, text, fg_color_1, fg_color_2, fill_color):
    font_size = _initialize(cr, width, height, text)

    _draw_border(cr, fg_color_1, 10 if font_size > 100 else 5)
    _draw_border(cr, fg_color_2, 5 if font_size > 100 else 2)
    _fill(cr, fill_color)

def _fill(cr, rgb):
    cr.set_source_rgb(*rgb)
    cr.fill()

def main():
    width, height = ARGS.width, ARGS.height
    text, filename = ARGS.text, ARGS.filename
    bg_color = transform_color(ARGS.background)
    shadow_color = transform_color(ARGS.shadow)
    fill_color = transform_color(ARGS.fill)
    fg1_color = transform_color(ARGS.fg1)
    fg2_color = transform_color(ARGS.fg2)

    # Draw a background with a blurry light
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(surface)
    _draw_base(cr, width, height, text, bg_color, shadow_color, fill_color)
    surface.write_to_png(filename)

    original_image = Image.open(filename)
    blurred_image = original_image.filter(ImageFilter.GaussianBlur(35))
    blurred_image.save(filename)

    # Draw the text
    surface = cairo.ImageSurface.create_from_png(filename)
    cr = cairo.Context(surface)
    _draw_text(cr, width, height, text, fg1_color, fg2_color, fill_color)
    surface.write_to_png(filename)

def _parse_arguments():
    parser = argparse.ArgumentParser(
        description='Creates a neon glow effect image with the given text')

    parser.add_argument('-t', '--text',
                        help='Text to render',
                        required=True)
    parser.add_argument('-f', '--filename',
                        help='Image filename (png)',
                        required=True)

    parser.add_argument('--width',
                        help='Image width in pixels',
                        type=int,
                        default=1920)
    parser.add_argument('--height',
                        help='Image height in pixels',
                        type=int,
                        default=1080)
    parser.add_argument('--background',
                        help='Image background color in hex (e.g. FF2200)',
                        default=BG_COLOR)
    parser.add_argument('--shadow',
                        help='Text shadow color in hex (e.g. FF2200)',
                        default=SHADOW_COLOR)
    parser.add_argument('--fill',
                        help='Text fill color in hex (e.g. FF2200)',
                        default=FILL_COLOR)
    parser.add_argument('--fg1',
                        help='Text border color 1 in hex (e.g. FF2200)',
                        default=FG_COLOR_1)
    parser.add_argument('--fg2',
                        help='Text border color 2 in hex (e.g. FF2200)',
                        default=FG_COLOR_2)

    return parser.parse_args()

if __name__ == '__main__':
    ARGS = _parse_arguments()
    main()
