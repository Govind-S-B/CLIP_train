from PIL import Image, ImageOps
import os
import cairosvg

def regularize_images(source_directory, output_size=(256, 256), background_color='white'):
    # Create output directory if it doesn't exist
    output_directory = "regularized_data"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over each file in the source directory
    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)
        name, ext = os.path.splitext(filename)

        # Handle SVG conversion
        if ext.lower() == '.svg':
            try:
                # Convert SVG to PNG using CairoSVG then process with Pillow
                png_path = os.path.join(output_directory, f"{name}.png")
                cairosvg.svg2png(url=file_path, write_to=png_path)
                processed_img = Image.open(png_path)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        else:
            # Open image if it's a supported type
            try:
                processed_img = Image.open(file_path)
            except Exception as e:
                print(f"Error opening {filename}: {e}")
                continue

        # Convert image to RGBA if it has an alpha channel, otherwise RGB
        if processed_img.mode in ('RGBA', 'LA') or (processed_img.mode == 'P' and 'transparency' in processed_img.info):
            # Create a background image
            background = Image.new("RGB", processed_img.size, background_color)
            processed_img = Image.alpha_composite(background.convert('RGBA'), processed_img.convert('RGBA'))
        else:
            processed_img = processed_img.convert("RGB")

        # Resizing while maintaining aspect ratio
        processed_img.thumbnail(output_size, Image.LANCZOS)
        
        # Create a new image with the desired size and background color
        new_img = Image.new("RGB", output_size, background_color)
        offset = ((output_size[0] - processed_img.size[0]) // 2, 
                  (output_size[1] - processed_img.size[1]) // 2)
        new_img.paste(processed_img, offset)

        # Save it to the output directory as JPG
        output_file_name = os.path.join(output_directory, f"{name}.jpg")
        new_img.save(output_file_name, "JPEG")

def main():
    # Set the source directory
    source_directory = "renamed_data"
    
    # Regularize the images
    regularize_images(source_directory)
    print("Images have been regularized successfully.")

if __name__ == "__main__":
    main()
