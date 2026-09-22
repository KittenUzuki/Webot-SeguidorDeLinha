"""
Gera a pista em formato de "oito" (figura-8) para o seguidor de linha:
 - imagem da textura (worlds/textures/pista_textura.png)
 - trecho .wbt com os segmentos físicos (Pose+Box) que formam o relevo da pista
 - ponto inicial (posição/rotação) para posicionar o Robot no começo da pista
"""
import numpy as np
from PIL import Image, ImageDraw

# ------------------------------------------------------------------
# 1) Parâmetros geométricos da pista (dois laços tangentes na origem)
# ------------------------------------------------------------------
R = 0.35              # raio de cada laço (m)
TRACK_WIDTH = 0.035    # largura da linha (m) - igual ao projeto anterior
SEG_LEN = 0.024        # comprimento de cada "tijolinho" da pista (m)
SEG_SPACING = 0.014    # distância entre centros dos tijolinhos (m) - overlap nas curvas
FLOOR_X = 2.0          # tamanho do chão em X (m)
FLOOR_Y = 1.2          # tamanho do chão em Y (m)

N = 20000
u = np.linspace(0, 4*np.pi, N, endpoint=False)

x = np.empty(N)
y = np.empty(N)
for i, uu in enumerate(u):
    if uu <= 2*np.pi:
        theta = uu
        cx, cy = -R, 0.0
        x[i] = cx + R*np.cos(theta)
        y[i] = cy + R*np.sin(theta)
    else:
        theta = 3*np.pi - uu
        cx, cy = R, 0.0
        x[i] = cx + R*np.cos(theta)
        y[i] = cy + R*np.sin(theta)

# reamostragem por comprimento de arco uniforme
dx = np.diff(x, append=x[0])
dy = np.diff(y, append=y[0])
ds = np.sqrt(dx**2 + dy**2)
cs = np.cumsum(ds)
s = np.concatenate([[0], cs[:-1]])  # s[i] = comprimento acumulado até o ponto i
total_len = cs[-1]
print("comprimento total da pista:", total_len)

n_pts = int(total_len / SEG_SPACING)
s_uniform = np.linspace(0, total_len, n_pts, endpoint=False)
x_u = np.interp(s_uniform, s, x)
y_u = np.interp(s_uniform, s, y)

# ângulo (tangente) em cada ponto, via diferença central
x_next = np.roll(x_u, -1)
y_next = np.roll(y_u, -1)
ang = np.arctan2(y_next - y_u, x_next - x_u)

np.save('/home/claude/work/build/path_x.npy', x_u)
np.save('/home/claude/work/build/path_y.npy', y_u)
np.save('/home/claude/work/build/path_ang.npy', ang)

print("pontos gerados:", n_pts)
print("x range", x_u.min(), x_u.max())
print("y range", y_u.min(), y_u.max())
print("ponto inicial:", x_u[0], y_u[0], "angulo inicial (graus):", np.degrees(ang[0]))
