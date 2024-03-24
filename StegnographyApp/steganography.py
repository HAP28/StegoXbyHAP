from PIL import Image
import io

def bin_to_message(binary_str):
    """Convert binary to message."""
    message = ''
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        message += chr(int(byte, 2))
    return message

def reveal_data_from_image(image_path):
    """Retrieve a hidden message from an image."""
    img = Image.open(image_path)
    pixels = img.load()
    binary_str = ''
    
    for x in range(img.width):
        for y in range(img.height):
            pixel = pixels[x, y]
            
            for n in range(0, 3):
                binary_str += str(pixel[n] & 1)
                
                if binary_str[-16:] == '1111111111111110':  # Check for delimiter
                    return bin_to_message(binary_str[:-16])
    return "No message found or the message is incomplete."


def message_to_bin(message):
    """Convert a message to binary."""
    return ''.join(format(ord(char), '08b') for char in message)

def hide_data_in_image(image_path, message):
    """Hide a message in an image."""
    img = Image.open(image_path)
    binary_message = message_to_bin(message) + '1111111111111110'  # Delimiter to indicate end of message.
    
    pixels = img.load()
    print(pixels)
    data_index = 0
    
    for x in range(img.width):
        for y in range(img.height):
            pixel = list(pixels[x, y])
            
            for n in range(0, 3):
                if data_index < len(binary_message):
                    pixel[n] = pixel[n] & ~1 | int(binary_message[data_index])
                    data_index += 1
                else:
                    pixels[x, y] = tuple(pixel)
                    # img.save('hidden_message.png')
                    # return "Message hidden in image."
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_content = img_buffer.getvalue()

                    return img_content

                    
            pixels[x, y] = tuple(pixel)
    # img.save('hidden_message.png')
    
    return "Message hidden in image, but it was too long for the image."