"""
===============================================================================
 VERSAO DE DIAGNOSTICO - seguidor_linha_DEBUG.py
 Esta versao serve so para DESCOBRIR os valores reais que os sensores
 estao lendo na sua maquina, para calibrar o LIMIAR corretamente.
 NAO e' a versao final de entrega - depois de calibrar, volte a usar o
 seguidor_linha.py normal (so ajustando o LIMIAR).
===============================================================================
"""

from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

motorE = robot.getDevice('motorE')
motorD = robot.getDevice('motorD')
motorE.setPosition(float('inf'))
motorD.setPosition(float('inf'))
motorE.setVelocity(0.0)
motorD.setVelocity(0.0)

ds_esq = robot.getDevice('ds_esquerda')
ds_ctr = robot.getDevice('ds_centro')
ds_dir = robot.getDevice('ds_direita')
ds_esq.enable(timestep)
ds_ctr.enable(timestep)
ds_dir.enable(timestep)

contador = 0

print("=== INICIANDO DIAGNOSTICO ===")
print("O carro vai ficar PARADO (motores em 0) so para lermos os sensores.")
print("Copie e me mande as linhas 'LEITURA' que aparecerem no console.")

while robot.step(timestep) != -1:
    # Motores parados de propósito, so' para ler os sensores com calma
    motorE.setVelocity(0.0)
    motorD.setVelocity(0.0)

    contador += 1
    if contador % 32 == 0:  # imprime a cada ~0.5s (timestep 16ms * 32)
        v_e = ds_esq.getValue()
        v_c = ds_ctr.getValue()
        v_d = ds_dir.getValue()
        print(f"LEITURA -> esquerda: {v_e:.3f} | centro: {v_c:.3f} | direita: {v_d:.3f}")
