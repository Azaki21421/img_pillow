from PIL import Image

def merge_images_horizontally(image_paths, output_path):
    """
    Объединяет изображения горизонтально.

    :param image_paths: Список путей к изображениям для объединения.
    :param output_path: Путь для сохранения объединенного изображения.
    """
    images = [Image.open(path) for path in image_paths]

    # Определяем ширину и высоту для нового изображения
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)

    # Создаем новое изображение
    merged_image = Image.new('RGB', (total_width, max_height))

    # Склеиваем изображения
    x_offset = 0
    for img in images:
        merged_image.paste(img, (x_offset, 0))
        x_offset += img.width

    # Сохраняем объединенное изображение
    merged_image.save(output_path)

    # Закрываем изображения
    for img in images:
        img.close()

# Пример использования:
image_paths = ['input file1', 'input file2']
output_path = 'output file'
merge_images_horizontally(image_paths, output_path)