from PIL import Image

def remove_background(image, background_color):
    # Convert image to RGBA (if it's not already in this mode)
    image = image.convert('RGBA')
    
    # Get data of the image
    data = image.getdata()
    
    # Create a new data list for the image without the background
    new_data = []
    
    for item in data:
        # Change all pixels that are the background color to be transparent
        if item[:3] == background_color[:3]:
            new_data.append((255, 255, 255, 0))  # Fully transparent
        else:
            new_data.append(item)
    
    # Update image data with new data
    image.putdata(new_data)
    return image

def overlay_gif_frames(gif_path, output_path, background_color=(255, 255, 255)):
    # Open the GIF file
    gif = Image.open(gif_path)

    # Initialize an empty image for the result
    result = Image.new('RGBA', gif.size, (255, 255, 255, 0))

    try:
        while True:
            # Remove the background from the current frame
            frame = remove_background(gif.convert('RGBA'), background_color)

            # Composite the current frame with the result
            result = Image.alpha_composite(result, frame)

            # Move to the next frame
            gif.seek(gif.tell() + 1)
    except EOFError:
        # End of the GIF frames
        pass

    # Convert result to 'RGB' to remove alpha channel if desired
    result = result.convert('RGB')

    # Save the resulting image
    result.save(output_path)

# Usage
gif_path = 'flag_2.gif'         # Replace with the path to your GIF
output_path = '2.jpg'  # Replace with the desired output path
background_color = (255, 255, 255)        # Replace with the background color to remove
overlay_gif_frames(gif_path, output_path, background_color)