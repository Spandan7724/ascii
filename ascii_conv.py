from PIL import Image
import numpy as np
import argparse

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / float(width) / 1.65
    new_height = int(aspect_ratio * new_width)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def map_pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_chars = len(ASCII_CHARS)
    ascii_str = "".join([ASCII_CHARS[int(pixel * ascii_chars / 256)] for pixel in pixels])
    return ascii_str

def convert_image_to_ascii(image, new_width=100):
    image = resize_image(image, new_width)
    ascii_str = map_pixels_to_ascii(image.convert("L"))
    img_width = image.width
    ascii_img = "\n".join([ascii_str[index:index+img_width] for index in range(0, len(ascii_str), img_width)])
    return ascii_img

def colorize_ascii(image, ascii_str, new_width=100):
    width = new_width
    height = len(ascii_str.split("\n"))
    image = image.resize((width, height))
    image = image.convert("RGB")
    colored_ascii = []
    for i, line in enumerate(ascii_str.split("\n")):
        for j, char in enumerate(line):
            r, g, b = image.getpixel((j, i))
            colored_ascii.append(f"\033[38;2;{r};{g};{b}m{char}")
        colored_ascii.append("\033[0m\n")
    
    return "".join(colored_ascii)

def main(image_path, new_width=100):
    image = Image.open(image_path)
    ascii_str = convert_image_to_ascii(image, new_width)
    colored_ascii = colorize_ascii(image, ascii_str, new_width)
    print(colored_ascii)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images to colored ASCII art.")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("--width", type=int, default=100, help="Width of the ASCII art")
    
    args = parser.parse_args()
    
    main(args.image_path, args.width)
