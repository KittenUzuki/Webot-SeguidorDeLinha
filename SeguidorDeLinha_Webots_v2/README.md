# Robô Seguidor de Linha — Pista Avançada (v2, formato de "oito")

**Aluno:** Matheus Ferreira Fagundes
**RA:** 23149
**Repositório GitHub:** https://github.com/KittenUzuki/Webot-SeguidorDeLinha

Esta é a evolução da entrega anterior (pista "estádio"). Como o seguidor de
3 sensores já funcionava, a pista foi trocada por uma **mais difícil**: um
formato de **oito** (dois laços tangentes que se cruzam uma vez no meio do
percurso), com curvas fechadas nos dois sentidos.

## O que mudou em relação à v1

- **Pista nova e autoral**: gerada por script próprio (`scripts_pista/`),
  a partir de dois círculos tangentes na origem — não é cópia de nenhuma
  imagem de referência do professor ou de colegas.
- **Mesmo carro** (chassi azul, nariz cônico laranja, 3 sensores
  infravermelhos `ds_esquerda` / `ds_centro` / `ds_direita`).
- **Mesmo algoritmo de controle** (bang-bang com 3 sensores), só com as
  constantes de velocidade reajustadas para as curvas mais fechadas da
  pista em oito (ver comentários no início de `seguidor_linha.py`).
- A pista continua sendo aplicada de duas formas ao mesmo tempo:
  1. **Textura do chão** (`worlds/textures/pista_textura.png`);
  2. **Relevo físico de 1 cm** sobre o mesmo traçado, para os sensores de
     distância detectarem a linha por proximidade (mesma técnica da v1).

## Estrutura do projeto

```
SeguidorDeLinha_Webots_v2/
├── worlds/
│   ├── carro.wbt                       # mundo Webots (pista em oito + robô)
│   └── textures/
│       └── pista_textura.png           # textura da pista (autoral)
├── controllers/
│   └── seguidor_linha/
│       └── seguidor_linha.py           # controlador comentado
├── scripts_pista/                      # scripts que geraram a pista (prova de autoria)
│   ├── gerar_pista.py                  # calcula os pontos do traçado em oito
│   ├── gerar_textura.py                # desenha a textura a partir do traçado
│   └── gerar_wbt_pista.py              # gera os blocos Pose/Box do relevo físico
└── README.md
```

## Como abrir e rodar

1. Instale o **Webots R2025a** (mesma versão do material de aula).
2. Abra o Webots → *File → Open World...* → selecione `worlds/carro.wbt`.
3. Na primeira abertura, o Webots baixa os PROTOs externos (fundo e chão) —
   é necessário estar conectado à internet nesse primeiro carregamento.
4. Clique em **▶ (Play/Real-time)**. O carro deve seguir a linha
   automaticamente, completando os dois laços do "oito".

### Ajustando o seguidor (se necessário)

No início de `seguidor_linha.py`:

- `LIMIAR`: aumente/diminua se o robô não detectar a linha ou detectar o
  piso por engano.
- `VEL_BASE` / `VEL_CURVA`: velocidade em reta e intensidade da correção
  nas curvas (curvas mais fechadas podem pedir `VEL_CURVA` um pouco maior
  ou `VEL_BASE` um pouco menor).
- Se o carro andar de marcha à ré, gire o robô 180° no campo `rotation`
  do nó `Robot` em `carro.wbt` (some `3.14159` ao ângulo).

## Como gravar o vídeo pedido (o próprio Webots gera)

1. Com a simulação já aberta e rodando, vá em **File → Export... → Movie...**
   (dependendo da versão, fica em **Simulation → Record Movie**).
2. Escolha resolução e duração (recomendo 30–40 s, tempo suficiente para
   o robô completar os dois laços do "oito").
3. Clique em **Start** — o Webots grava a simulação automaticamente e
   salva o `.mp4`.
4. Guarde o arquivo junto com a entrega do trabalho.

## Como publicar a versão nova no GitHub

No terminal, dentro da pasta do repositório já existente
(`Webot-SeguidorDeLinha`), copie os arquivos desta pasta
`SeguidorDeLinha_Webots_v2/` para dentro do repositório (substituindo os
arquivos da v1, ou em uma subpasta nova `_v2` — fica a seu critério) e
rode:

```bash
git add .
git commit -m "Pista v2: formato de oito, mais dificil"
git push
```

Como o nome do arquivo de textura (`pista_textura.png`) e o caminho
(`worlds/textures/`) foram mantidos iguais aos da v1, o link "raw" do
GitHub que já está dentro de `carro.wbt` continua funcionando sem precisar
trocar nada:

```
https://raw.githubusercontent.com/KittenUzuki/Webot-SeguidorDeLinha/main/SeguidorDeLinha_Webots/worlds/textures/pista_textura.png
```

Se você optar por colocar esta v2 em uma pasta diferente dentro do
repositório, lembre de atualizar essa URL em `carro.wbt` para apontar para
o caminho novo.

## Antes de entregar, confira:

- [ ] `worlds/carro.wbt` → nome, RA e link do GitHub no cabeçalho.
- [ ] `controllers/seguidor_linha/seguidor_linha.py` → mesmos dados no
      cabeçalho do arquivo.
- [ ] Vídeo `.mp4` gerado pelo Webots mostrando o carro completando os
      dois laços da pista em oito.
- [ ] Push feito no GitHub com a pista nova.
