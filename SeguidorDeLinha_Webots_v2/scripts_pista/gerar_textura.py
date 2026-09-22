import numpy as np
from PIL import Image, ImageDraw

FLOOR_X = 2.0
FLOOR_Y = 1.2
TRACK_WIDTH = 0.035

x = np.load('/home/claude/work/build/path_x.npy')
y = np.load('/home/claude/work/build/path_ang.npy') if False else np.load('/home/claude/work/build/path_y.npy')

# resolução da textura (pixels por metro)
PPM = 700
W = int(FLOOR_X * PPM)
H = int(FLOOR_Y * PPM)

img = Image.new('RGB', (W, H), (235, 235, 230))  # piso claro
draw = ImageDraw.Draw(img)

def world_to_px(wx, wy):
    # origem do mundo no centro do chao; eixo Y do mundo para "cima" -> linha da
    # imagem para "baixo", por isso inverte o Y na conversao
    px = (wx + FLOOR_X/2) / FLOOR_X * W
    py = (FLOOR_Y/2 - wy) / FLOOR_Y * H
    return px, py

pts = [world_to_px(xx, yy) for xx, yy in zip(x, y)]
pts.append(pts[0])  # fecha o laco

width_px = max(2, int(TRACK_WIDTH * PPM))
draw.line(pts, fill=(15, 15, 15), width=width_px, joint='curve')
# bolinhas nas juntas para nao deixar "dentes" nas curvas
r = width_px / 2
for (px, py) in pts:
    draw.ellipse([px-r, py-r, px+r, py+r], fill=(15, 15, 15))

img.save('/home/claude/work/build/pista_textura.png')
print("textura salva:", img.size)
