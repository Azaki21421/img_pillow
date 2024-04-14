from PIL import Image

def compress_image(input_image_path, output_image_path, quality=85):
    """
    Сжимает изображение с помощью Pillow.

    :param input_image_path: Путь к исходному изображению.
    :param output_image_path: Путь для сохранения сжатого изображения.
    :param quality: Качество сжатия (0-100). Чем меньше значение, тем сильнее сжатие.
    """
    with Image.open(input_image_path) as img:
        img.save(output_image_path, optimize=True, quality=quality)

# Пример использования:
input_path = 'input_image.jpg'
output_path = 'compressed_image.jpg'
compress_image(input_path, output_path, quality=50)