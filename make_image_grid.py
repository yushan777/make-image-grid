import argparse
from PIL import Image
import os
import math

"""
What it does:
Creates a single image containing a grid layout of multiple images from a directory
All images in the grid are arranged side by side with no margins
Assumes all source images have the same dimensions

Output:
Creates a file named "grid.jpg" (or "prefix_grid.jpg" if prefix is provided)
The output is saved in the same directory as the input images
Will overwrite existing files with the same name without warning

# Basic usage
python script.py -i /path/to/images

# With prefix
python script.py -i /path/to/images -p myprefix

# With custom columns
python script.py -i /path/to/images -c 3 -p myprefix
"""

def create_image_grid(image_dir, cols=4):

    # Get list of image files, excluding those with 'grid' in the filename
    image_files = [
        f for f in os.listdir(image_dir)
        if (f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and
            'grid' not in f.lower())
    ]

    if not image_files:
        raise ValueError("No valid image files found in directory")

    # Open first image to get dimensions
    first_image = Image.open(os.path.join(image_dir, image_files[0]))
    img_width, img_height = first_image.size

    # Calculate grid dimensions
    num_images = len(image_files)
    rows = math.ceil(num_images / cols)

    # Create blank canvas
    grid_width = img_width * cols
    grid_height = img_height * rows
    grid_image = Image.new('RGB', (grid_width, grid_height))

    # Place images in grid
    for idx, img_file in enumerate(image_files):
        img = Image.open(os.path.join(image_dir, img_file))

        # Calculate position
        row = idx // cols
        col = idx % cols
        x = col * img_width
        y = row * img_height

        # Paste image
        grid_image.paste(img, (x, y))

    return grid_image


def main():
    parser = argparse.ArgumentParser(description='Create a grid from images in a directory')

    parser.add_argument('-i', '--input-dir', required=True, help='Directory containing images')
    parser.add_argument('-c', '--cols', type=int, default=4, help='Number of columns in grid (default: 4)')
    parser.add_argument('-p', '--prefix', help='Prefix for the output filename (default: none)')

    args = parser.parse_args()

    try:
        # Construct output filename with optional prefix
        output_filename = 'grid.jpg'
        if args.prefix:
            output_filename = f"{args.prefix}_{output_filename}"

        # Create the output path in the same directory as input
        output_path = os.path.join(args.input_dir, output_filename)

        grid = create_image_grid(args.input_dir, args.cols)
        grid.save(output_path)
        print(f"Grid image saved as {output_path}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()