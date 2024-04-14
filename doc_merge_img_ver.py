from PIL import Image

def merge_images_vertically(image_paths, output_path):
    """
    Объединяет изображения вертикально.

    :param image_paths: Список путей к изображениям для объединения.
    :param output_path: Путь для сохранения объединенного изображения.
    """
    images = [Image.open(path) for path in image_paths]

    # Определяем ширину и высоту для нового изображения
    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)

    # Создаем новое изображение
    merged_image = Image.new('RGB', (max_width, total_height))

    # Склеиваем изображения
    y_offset = 0
    for img in images:
        merged_image.paste(img, (0, y_offset))
        y_offset += img.height

    # Сохраняем объединенное изображение
    merged_image.save(output_path)

    # Закрываем изображения
    for img in images:
        img.close()

# Пример использования:
image_paths = ['input file','input file2']
output_path = 'output folder'
merge_images_vertically(image_paths, output_path)