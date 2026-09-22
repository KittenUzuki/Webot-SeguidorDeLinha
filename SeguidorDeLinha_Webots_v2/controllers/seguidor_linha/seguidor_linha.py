"""
===============================================================================
 CONTROLADOR: seguidor_linha.py
 PROJETO....: Robo Seguidor de Linha - Simulacao Webots (pista avancada / v2)
 ALUNO......: Matheus Ferreira Fagundes
 RA.........: 23149
 REPO GITHUB: https://github.com/KittenUzuki/Webot-SeguidorDeLinha

 DESCRICAO GERAL
 ----------------
 Este e' o mesmo algoritmo "bang-bang" de seguidor de linha da entrega
 anterior (pista em formato de estadio), agora testado numa pista MAIS
 DIFICIL: uma pista em formato de "oito" (dois lacos tangentes que se
 cruzam uma vez no meio do percurso). Como sugerido apos a primeira pista
 ter funcionado, o desafio foi aumentado sem trocar a logica de controle,
 apenas reafirmando/ajustando as constantes de velocidade, exatamente
 para provar que o mesmo seguidor "generico" funciona em qualquer tracado,
 desde que a pista seja continua e a largura da linha seja compativel com
 o espacamento entre os tres sensores.

 O robo usa TRES sensores infravermelhos de distancia (DistanceSensor)
 apontados para o chao, na frente do robo:

        ds_esquerda   ds_centro   ds_direita

 A pista e' uma linha PRETA, ligeiramente ELEVADA (1 cm) em relacao ao
 piso claro do chao (RectangleArena). Como os sensores estao a uma altura
 fixa acima do robo, quando um sensor esta EXATAMENTE sobre a linha ele
 fica mais PERTO do obstaculo (a linha) do que quando esta sobre o piso
 (mais longe). Ou seja:

        valor do sensor PEQUENO  -> sensor esta EM CIMA da linha
        valor do sensor GRANDE   -> sensor esta sobre o piso (sem linha)

 LOGICA DE CONTROLE (bang-bang com 3 sensores)
 ----------------------------------------------
   * Somente o sensor CENTRAL ve a linha  -> robo alinhado, segue reto
   * Sensor ESQUERDO ve a linha           -> a linha esta a esquerda do
                                              centro do robo -> vira p/ ESQUERDA
   * Sensor DIREITO ve a linha            -> a linha esta a direita do
                                              centro do robo -> vira p/ DIREITA
   * Todos veem (cruzamento do "oito")    -> segue reto mais devagar, ate
                                              o cruzamento passar
   * Nenhum sensor ve a linha (perdeu)    -> gira devagar no ultimo sentido
                                              de curva conhecido, procurando
                                              a linha novamente
===============================================================================
"""

from controller import Robot

# ---------------------------------------------------------------------------
# 1) INICIALIZACAO DO ROBO E DO TIMESTEP DA SIMULACAO
# ---------------------------------------------------------------------------
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# ---------------------------------------------------------------------------
# 2) OBTENDO E CONFIGURANDO OS MOTORES (rodas esquerda/direita)
#    setPosition(inf) coloca o motor em modo de velocidade (nao de posicao).
# ---------------------------------------------------------------------------
print("Iniciando rodas...")
motorE = robot.getDevice('motorE')
motorD = robot.getDevice('motorD')
motorE.setPosition(float('inf'))
motorD.setPosition(float('inf'))
motorE.setVelocity(0.0)
motorD.setVelocity(0.0)

# ---------------------------------------------------------------------------
# 3) OBTENDO E HABILITANDO OS TRES SENSORES INFRAVERMELHOS DE LINHA
# ---------------------------------------------------------------------------
print("Iniciando sensores de linha...")
ds_esq = robot.getDevice('ds_esquerda')
ds_ctr = robot.getDevice('ds_centro')
ds_dir = robot.getDevice('ds_direita')
ds_esq.enable(timestep)
ds_ctr.enable(timestep)
ds_dir.enable(timestep)

# ---------------------------------------------------------------------------
# 4) PARAMETROS DE CONTROLE (ajustaveis para "calibrar" o seguidor)
#    Na pista em oito as curvas sao mais fechadas que na pista estadio,
#    entao a velocidade de curva (VEL_CURVA) foi um pouco reduzida em
#    relacao a versao anterior, para o robo nao "derrapar" para fora do
#    laco nas curvas mais apertadas.
# ---------------------------------------------------------------------------
LIMIAR = 1.5          # abaixo disso o sensor considera que "ve" a linha
VEL_BASE = 3.6         # velocidade das rodas em linha reta (rad/s)
VEL_CURVA = 2.2        # intensidade da correcao de curva
VEL_BUSCA = 1.4        # velocidade usada ao "procurar" a linha perdida

# Guarda o ultimo sentido de curva (True = estava curvando p/ esquerda)
# Usado para decidir para que lado girar quando a linha e' perdida.
ultima_curva_esquerda = True

print("Iniciando seguidor de linha na pista em formato de oito...")

# ---------------------------------------------------------------------------
# 5) LOOP PRINCIPAL DE CONTROLE
# ---------------------------------------------------------------------------
while robot.step(timestep) != -1:

    # Leitura dos tres sensores de linha
    val_esq = ds_esq.getValue()
    val_ctr = ds_ctr.getValue()
    val_dir = ds_dir.getValue()

    # Converte a leitura bruta em booleano "esta sobre a linha?"
    linha_esq = val_esq < LIMIAR
    linha_ctr = val_ctr < LIMIAR
    linha_dir = val_dir < LIMIAR

    if linha_ctr and not linha_esq and not linha_dir:
        # -----------------------------------------------------------------
        # Caso 1: robo centralizado sobre a linha -> segue em frente
        # -----------------------------------------------------------------
        motorE.setVelocity(VEL_BASE)
        motorD.setVelocity(VEL_BASE)

    elif linha_esq and not linha_dir:
        # -----------------------------------------------------------------
        # Caso 2: linha detectada a esquerda -> corrige virando p/ ESQUERDA
        # (reduz a roda esquerda / aumenta a roda direita)
        # -----------------------------------------------------------------
        motorE.setVelocity(VEL_BASE - VEL_CURVA)
        motorD.setVelocity(VEL_BASE + VEL_CURVA)
        ultima_curva_esquerda = True

    elif linha_dir and not linha_esq:
        # -----------------------------------------------------------------
        # Caso 3: linha detectada a direita -> corrige virando p/ DIREITA
        # -----------------------------------------------------------------
        motorE.setVelocity(VEL_BASE + VEL_CURVA)
        motorD.setVelocity(VEL_BASE - VEL_CURVA)
        ultima_curva_esquerda = False

    elif linha_esq and linha_dir:
        # -----------------------------------------------------------------
        # Caso 4: os dois sensores das pontas veem a linha ao mesmo tempo.
        # Na pista em oito isso acontece exatamente no ponto de CRUZAMENTO
        # no meio do percurso -> segue reto, porem mais devagar, ate sair
        # da regiao do cruzamento.
        # -----------------------------------------------------------------
        motorE.setVelocity(VEL_BASE * 0.5)
        motorD.setVelocity(VEL_BASE * 0.5)

    else:
        # -----------------------------------------------------------------
        # Caso 5: nenhum sensor detecta a linha (o robo "perdeu" a pista)
        # -> gira lentamente no ultimo sentido de curva conhecido ate
        # reencontrar a linha
        # -----------------------------------------------------------------
        if ultima_curva_esquerda:
            motorE.setVelocity(-VEL_BUSCA)
            motorD.setVelocity(VEL_BUSCA)
        else:
            motorE.setVelocity(VEL_BUSCA)
            motorD.setVelocity(-VEL_BUSCA)

# Codigo de limpeza ao encerrar a simulacao (nao ha nada a liberar aqui).
