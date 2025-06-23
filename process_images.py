import os
from PIL import Image, ImageOps
import glob

def process_image(image_path, output_size=(400, 400)):
    """
    Process an image to:
    1. Remove transparent background
    2. Make background white
    3. Scale to consistent size
    4. Center the image content
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create a white background
        white_bg = Image.new('RGBA', img.size, (255, 255, 255, 255))
        
        # Composite the image onto white background
        # This removes transparency and makes background white
        result = Image.alpha_composite(white_bg, img)
        
        # Convert to RGB (remove alpha channel)
        result = result.convert('RGB')
        
        # Get the bounding box of non-white content
        bbox = result.getbbox()
        if bbox:
            # Crop to content
            cropped = result.crop(bbox)
            
            # Calculate scaling to fit in output size while maintaining aspect ratio
            width, height = cropped.size
            scale = min(output_size[0] / width, output_size[1] / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # Resize the image
            resized = cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create final image with white background
            final = Image.new('RGB', output_size, (255, 255, 255))
            
            # Calculate position to center the image
            x = (output_size[0] - new_width) // 2
            y = (output_size[1] - new_height) // 2
            
            # Paste the resized image onto the white background
            final.paste(resized, (x, y))
        else:
            # If no content found, create white image
            final = Image.new('RGB', output_size, (255, 255, 255))
        
        return final
    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def main():
    # Define the assets directory
    assets_dir = "assets"
    
    # Define output size for all images
    output_size = (400, 400)
    
    # Get all image files
    image_extensions = ['*.png', '*.jpg', '*.jpeg']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(assets_dir, ext)))
        image_files.extend(glob.glob(os.path.join(assets_dir, ext.upper())))
    
    print(f"Found {len(image_files)} images to process:")
    for img in image_files:
        print(f"  - {img}")
    
    # Process each image
    for image_path in image_files:
        print(f"\nProcessing: {image_path}")
        
        # Process the image
        processed = process_image(image_path, output_size)
        
        if processed:
            # Save the processed image (overwrite original)
            processed.save(image_path, quality=95, optimize=True)
            print(f"  ✓ Processed and saved: {image_path}")
        else:
            print(f"  ✗ Failed to process: {image_path}")
    
    print(f"\nCompleted processing {len(image_files)} images!")
    print("All images now have:")
    print("- White backgrounds (no transparency)")
    print("- Consistent 400x400 size")
    print("- Centered content")

if __name__ == "__main__":
    main()