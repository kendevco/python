from PIL import Image
import os

def convert_webp_to_png(source_folder):
    # List all files in the directory
    for filename in os.listdir(source_folder):
        # Check if the file is a WebP image
        if filename.endswith('.webp'):
            # Construct full file path
            file_path = os.path.join(source_folder, filename)
            # Define the output filename (change extension to .png)
            output_filename = os.path.splitext(file_path)[0] + '.png'
            # Check if the output file already exists
            if os.path.exists(output_filename):
                print(f'PNG file for {filename} already exists, skipping...')
                continue
            # Open the WebP image file
            with Image.open(file_path) as image:
                # Save the image as PNG
                image.save(output_filename, 'PNG')
                print(f'Converted {filename} to PNG format.')

if __name__ == '__main__':
    # Correctly specify the directory containing the WebP files
    source_folder = r'C:\Users\kenne\OneDrive\Pictures\AI Generated'
    convert_webp_to_png(source_folder)