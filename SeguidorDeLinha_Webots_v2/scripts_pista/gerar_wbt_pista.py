import numpy as np

x = np.load('/home/claude/work/build/path_x.npy')
y = np.load('/home/claude/work/build/path_y.npy')
ang = np.load('/home/claude/work/build/path_ang.npy')

SEG_LEN = 0.024
SEG_WIDTH = 0.035
SEG_HEIGHT = 0.01
Z = 0.005

lines = []
lines.append('DEF PISTA Group {')
lines.append('  children [')
for xx, yy, aa in zip(x, y, ang):
    lines.append('    Pose {')
    lines.append(f'      translation {xx:.4f} {yy:.4f} {Z}')
    lines.append(f'      rotation 0 0 1 {aa:.5f}')
    lines.append('      children [')
    lines.append('        Shape {')
    lines.append('          appearance USE PISTA_APPEARANCE')
    lines.append('          geometry Box {')
    lines.append(f'            size {SEG_LEN} {SEG_WIDTH} {SEG_HEIGHT}')
    lines.append('          }')
    lines.append('        }')
    lines.append('      ]')
    lines.append('    }')
lines.append('  ]')
lines.append('}')

with open('/home/claude/work/build/pista_group.txt', 'w') as f:
    f.write('\n'.join(lines))

print("segmentos gerados:", len(x))
print("angulo inicial (rad):", ang[0], "posicao inicial:", x[0], y[0])
