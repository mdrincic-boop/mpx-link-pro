from PIL import Image, ImageDraw

size = 256
img = Image.new('RGB', (size, size), color='#1e293b')
draw = ImageDraw.Draw(img)

center = size // 2
outer_radius = 100
inner_radius = 70

draw.ellipse(
    [center - outer_radius, center - outer_radius,
     center + outer_radius, center + outer_radius],
    fill='#3b82f6'
)

draw.ellipse(
    [center - inner_radius, center - inner_radius,
     center + inner_radius, center + inner_radius],
    fill='#06b6d4'
)

wave_y = center
amplitude = 20
for i in range(0, size, 3):
    x1 = i
    x2 = i + 3
    y_offset = int(amplitude * (i / size - 0.5))
    draw.line([(x1, wave_y + y_offset), (x2, wave_y + y_offset)], fill='white', width=2)

img.save('icon.png', 'PNG')

sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
icons = []
for size_tuple in sizes:
    icon_img = img.resize(size_tuple, Image.Resampling.LANCZOS)
    icons.append(icon_img)

icons[0].save('icon.ico', format='ICO', sizes=[icon.size for icon in icons])

print("Icon files created: icon.png and icon.ico")
