
from PIL import Image, ImageDraw

# Создаём изображение 256x256
size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Рисуем компьютер (монитор + системный блок)
# Монитор
draw.rectangle([50, 50, 206, 180], outline=(0, 120, 215), width=4, fill=(240, 248, 255))
draw.rectangle([70, 70, 186, 150], fill=(30, 144, 255))

# Системный блок
draw.rectangle([210, 120, 250, 200], outline=(0, 120, 215), width=4, fill=(240, 248, 255))

# Клавиатура
draw.rectangle([60, 190, 200, 210], fill=(100, 100, 100))

# Стрелка обмена (две стрелки по кругу)
# Стрелка от компьютера к весам
draw.arc([100, 140, 200, 240], start=180, end=360, width=6, fill=(0, 200, 0))
# Стрелка от весов к компьютеру
draw.arc([80, 120, 180, 220], start=0, end=180, width=6, fill=(255, 100, 0))

# Сохраняем как ICO
img.save('exchange_icon.ico', format='ICO', sizes=[(256, 256)])
