from PIL import Image, ImageDraw, ImageFont
from barcode import EAN13
from barcode.writer import ImageWriter


# Generate barcode image

def generate_barcode(code):
    barcode = EAN13(code, writer=ImageWriter())
    barcode_image = barcode.render()
    return barcode_image


def add_text_to_image(image_path, output_path, fields=[]):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Define the font size and font type
    font_size = 30
    font = ImageFont.truetype("arial", font_size)  # Replace "path_to_font.ttf" with the actual path to your font file

    # Define the position where the text will be drawn
    text1_position = (220, 370 - 10)
    text2_position = (220, 412 - 10)
    text3_position = (220, 453 - 10)
    text4_position = (220, 498 - 10)
    text5_position = (220, 540 - 10)

    # Define the color of the text (optional)
    text_color = (0, 0, 0)  # Black color

    # Add the text to the image
    draw.text(text1_position, fields[0], font=font, fill=text_color)
    draw.text(text2_position, fields[1], font=font, fill=text_color)
    draw.text(text3_position, fields[2], font=font, fill=text_color)
    draw.text(text4_position, fields[3], font=font, fill=text_color)
    draw.text(text5_position, fields[4], font=font, fill=text_color)

    # Generate the barcode image
    barcode_image = generate_barcode(fields[5])

    # Resize the barcode image to fit the original image
    barcode_image = barcode_image.resize((200, 100))

    # Calculate the position to place the barcode on the original image
    # x = 609
    # y = 358

    # Paste the barcode image onto the original image
    image.paste(barcode_image, (660, 340))

    # Save the modified image
    image.save(output_path)


# Example usage
image_path = "D:\Python Projects\Student Management System Clg Project\SMS\Images\Card Design.png"  # Replace "path_to_image.jpg" with the actual path to your image file
text = "Hello, World!"
output_path = "D:\Python Projects\Student Management System Clg Project\SMS\Images\generated.png"  # Replace "output_image.jpg" with the desired output image path

# 220, 370  name
# 220, 412  rollno
# 220, 453  class
# 220, 498  shift
# 220, 540  technology
# 220, 540  technology
add_text_to_image(image_path, output_path, ['name', 'rollno', 'class', 'shift', 'technology', '382982938293'])
