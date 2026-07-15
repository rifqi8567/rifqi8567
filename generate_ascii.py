"""
Convert face.jpg to high-resolution ASCII art for SVG header.
Uses more characters for finer detail gradation.
"""
from PIL import Image
import sys

# Extended ASCII chars from darkest to lightest (more gradation = more detail)
ASCII_CHARS_EXTENDED = "@%#W$9876543210?!abc;:+=-,._ "

def image_to_ascii(image_path, width=96, height=66):
    """Convert image to ASCII art with specified dimensions."""
    img = Image.open(image_path)
    
    # Crop to focus more on the face/upper body area
    w, h = img.size
    # Focus on the upper 75% where the face is
    crop_top = int(h * 0.0)
    crop_bottom = int(h * 0.82)
    crop_left = int(w * 0.08)
    crop_right = int(w * 0.92)
    img = img.crop((crop_left, crop_top, crop_right, crop_bottom))
    
    # Resize with aspect ratio correction (characters are taller than wide)
    img = img.resize((width, height), Image.LANCZOS)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Enhance contrast
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)
    
    pixels = list(img.getdata())
    
    ascii_lines = []
    for i in range(0, len(pixels), width):
        row = pixels[i:i+width]
        line = ""
        for pixel in row:
            # Map pixel value (0-255) to ASCII character
            idx = int(pixel / 255 * (len(ASCII_CHARS_EXTENDED) - 1))
            line += ASCII_CHARS_EXTENDED[idx]
        ascii_lines.append(line)
    
    return ascii_lines

if __name__ == "__main__":
    ascii_lines = image_to_ascii("face.jpg", width=96, height=66)
    
    # Output the ASCII art
    for line in ascii_lines:
        print(line)
    
    # Also save to file for SVG integration
    with open("ascii_output.txt", "w") as f:
        for line in ascii_lines:
            f.write(line + "\n")
    
    print(f"\n--- Generated {len(ascii_lines)} lines of {len(ascii_lines[0])} chars ---", file=sys.stderr)
