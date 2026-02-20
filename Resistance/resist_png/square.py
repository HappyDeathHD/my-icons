import os
from PIL import Image

def process_image(input_path, output_path):
    """
    Обрабатывает одно изображение:
    - К самой длинной грани +100 пикселей (по 50 с каждой стороны)
    - Затем дополняет до квадрата по второй оси (равномерно с двух сторон)
    """
    with Image.open(input_path) as img:
        # Конвертируем в RGBA для прозрачности
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        width, height = img.size
        
        # Определяем самую длинную грань
        if width >= height:
            # Широкая: +50 слева/справа (new_width = width + 100)
            new_width = width + 100
            side_size = new_width  # Квадрат по ширине
            new_height = side_size
            pad_left = 50
            pad_right = 50
            pad_top = (new_height - height) // 2
            pad_bottom = new_height - height - pad_top
        else:
            # Высокая: +50 сверху/снизу (new_height = height + 100)
            new_height = height + 100
            side_size = new_height  # Квадрат по высоте
            new_width = side_size
            pad_top = 50
            pad_bottom = 50
            pad_left = (new_width - width) // 2
            pad_right = new_width - width - pad_left
        
        # Новый прозрачный холст
        new_img = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
        
        # Вставляем оригинал
        new_img.paste(img, (pad_left, pad_top))
        
        # Сохраняем с оптимизацией
        new_img.save(output_path, 'PNG', optimize=True)

def main():
    current_dir = os.getcwd()
    padded_dir = os.path.join(current_dir, "padded")
    
    # Создаем папку padded если её нет
    os.makedirs(padded_dir, exist_ok=True)
    
    png_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.png')]
    
    if not png_files:
        print("PNG-файлы в текущей директории не найдены.")
        return
    
    processed = 0
    for filename in png_files:
        input_path = os.path.join(current_dir, filename)
        output_path = os.path.join(padded_dir, filename)
        
        try:
            process_image(input_path, output_path)
            print(f"Обработан: {filename} → padded/{filename}")
            processed += 1
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")
    
    print(f"\nГотово! Обработано файлов: {processed}")

if __name__ == "__main__":
    main()
