import os
from PIL import Image, ExifTags
Image.MAX_IMAGE_PIXELS = None

MAX_DIMENSION = 65500  # Maximum supported image dimension
MAX_FILE_SIZE = 5 * 1024 * 1024  # Maximum file size in bytes (5 MB)
MAX_PIXELS = 178956970  # Maximum number of pixels allowed

def resize_and_compress_image(image_path, output_path, quality=85):
    image = Image.open(image_path)

    # Correct orientation if necessary
    if hasattr(image, '_getexif'):
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            exif_orientation = exif.get(orientation, 1)
            if exif_orientation == 3:
                image = image.transpose(Image.ROTATE_180)
            elif exif_orientation == 6:
                image = image.transpose(Image.ROTATE_270)
            elif exif_orientation == 8:
                image = image.transpose(Image.ROTATE_90)

    image = resize_image(image)
    image.save(output_path, optimize=True, quality=quality)

def resize_image(image):
    width, height = image.size
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        if width > height:
            new_width = MAX_DIMENSION
            new_height = int(MAX_DIMENSION * height / width)
        else:
            new_width = int(MAX_DIMENSION * width / height)
            new_height = MAX_DIMENSION
        return image.resize((new_width, new_height), Image.ANTIALIAS)
    return image

def merge_images_vertically(image_folder, output_path, file_extension=".jpg"):
    image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(file_extension)]

    # Resize and compress each image
    for i, image_path in enumerate(image_paths):
        output_image_path = f"temp_image_{i}.{file_extension}"
        resize_and_compress_image(image_path, output_image_path)
        image_paths[i] = output_image_path

    # Merge the resized and compressed images
    merge_images(image_paths, output_path)

def merge_images(image_paths, output_path):
    images = [Image.open(path) for path in image_paths]

    widths, heights = zip(*(i.size for i in images))

    total_height = sum(heights)
    max_width = max(widths)

    # Split the merged image into smaller sections if the dimensions exceed the maximum supported dimension
    if total_height > MAX_DIMENSION:
        merged_images = []
        y_offset = 0
        while y_offset < total_height:
            section_height = min(MAX_DIMENSION, total_height - y_offset)

            # Calculate new section height to avoid exceeding the maximum number of pixels
            section_width = max_width * section_height // total_height

            section_images = [image.crop((0, y_offset, section_width, y_offset + section_height)) for image in images]
            section_merged = Image.new('RGB', (section_width, section_height))
            for section_image in section_images:
                section_merged.paste(section_image, (0, y_offset))
            merged_images.append(section_merged)
            y_offset += section_height

        # Save each section as a separate image
        for i, section_image in enumerate(merged_images):
            section_image.save(f"{output_path}_{i}.jpg")
    else:
        # Otherwise, merge images vertically as before
        merged_image = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for image in images:
            merged_image.paste(image, (0, y_offset))
            y_offset += image.size[1]
        merged_image.save(output_path)

if __name__ == "__main__":
    image_folder = "input folder"  # Replace with the path to your image folder
    output_path = "output folder"  # Replace with your desired output path
    merge_images_vertically(image_folder, output_path)