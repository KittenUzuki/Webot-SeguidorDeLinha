# Robô Seguidor de Linha — Simulação Webots

**Aluno:** `Matheus Ferreira Fagundes`
**RA:** `23149`
**Disciplina/Turma:** `<PREENCHER>`
**Repositório GitHub:** `<COLOQUE_AQUI_O_LINK_DO_SEU_GITHUB>`

Projeto desenvolvido a partir do material de aula fornecido pelo professor
(`Robo_Webot_base1` e `Robo - Sensor`), estendendo o carro de duas rodas
para um **seguidor de linha** completo, com pista própria.

## O que foi alterado em relação ao modelo da aula

- **Design do carro**: chassi azul com um "nariz" cônico laranja na frente
  (no lugar da caixa lisa original), rodas escurecidas.
- **Sensores**: em vez de 1 sensor de distância lateral (usado na aula para
  bater e ricochetear), foram adicionados **3 sensores infravermelhos**
  (`ds_esquerda`, `ds_centro`, `ds_direita`) apontados para baixo, na frente
  do robô, para detectar a linha da pista.
- **Pista própria**: pista em formato de "estádio" (retângulo com cantos
  arredondados) com um **trecho ondulado exclusivo** no lado superior —
  ver `preview_pista.png` para uma prévia do formato. A linha é aplicada
  de **duas formas ao mesmo tempo**, para garantir que funcione mesmo sem
  ajustes finos:
  1. **Textura da pista** (`worlds/textures/pista_textura.png`), aplicada
     como imagem do chão (`RectangleArena → floorAppearance → baseColorMap`),
     na mesma técnica do exemplo de imagem que o professor indicou
     (`.../mapas/oval_line.png` — uma imagem PNG do desenho da pista,
     referenciada por URL). A pista usada aqui é **outra, autoral**, no
     formato "estádio ondulado" (não é uma cópia da imagem de referência).
  2. **Relevo físico de 1 cm** exatamente sobre o mesmo traçado da textura,
     para que os sensores de distância detectem a linha de forma confiável
     por proximidade, independente de ajuste fino de sensibilidade de cor.
     Se quiser, você pode aumentar `redColorSensitivity` nos sensores e
     depender só da cor (mais fiel ao exemplo do professor), mas o relevo
     já garante que o seguidor funcione "out of the box".
- **Controlador novo** (`seguidor_linha.py`): implementa o algoritmo
  clássico *bang-bang* de seguidor de linha com 3 sensores, totalmente
  comentado em português.

## Estrutura do projeto

```
SeguidorDeLinha_Webots/
├── worlds/
│   └── carro.wbt                  # mundo Webots (pista + robô)
├── controllers/
│   └── seguidor_linha/
│       └── seguidor_linha.py      # controlador comentado
├── preview_pista.png              # prévia 2D da pista (fora do Webots)
└── README.md
```

## Como abrir e rodar

1. Instale o **Webots R2025a** (mesma versão usada no material de aula).
2. Abra o Webots → *File → Open World...* → selecione
   `worlds/carro.wbt`.
3. Na primeira abertura, o Webots vai baixar automaticamente os PROTOs
   externos (fundo e chão) — é necessário estar conectado à internet
   nesse primeiro carregamento.
4. Clique em **▶ (Play/Real-time)** na barra de ferramentas para iniciar
   a simulação. O carro deve seguir a linha preta automaticamente.

### Ajustando o seguidor (se necessário)

Se o carro não seguir bem a linha na sua máquina (pequenas diferenças de
física entre versões do Webots podem exigir ajuste fino), altere no
início do `seguidor_linha.py`:

- `LIMIAR`: aumente/diminua se o robô não detectar a linha ou detectar
  o piso por engano.
- `VEL_BASE` / `VEL_CURVA`: velocidade em reta e intensidade da correção
  nas curvas.
- Se o carro andar de marcha-ré pela pista, gire o robô 180° no campo
  `rotation` do nó `Robot` em `carro.wbt` (some `3.14159` ao ângulo).

## Como gravar o vídeo pedido (o próprio Webots gera)

O Webots grava vídeos da simulação nativamente, sem precisar de programas
externos:

1. Com a simulação já aberta, vá em **File → Export... → Movie...**
   (ou no menu **Simulation**, dependendo da versão).
2. Escolha resolução, tempo de gravação (ex.: 20–30 s, tempo suficiente
   para dar uma volta completa na pista) e o arquivo de saída (`.mp4`).
3. Clique em **Start** — o Webots roda a simulação e grava
   automaticamente o vídeo do robô seguindo a linha.
4. Guarde o `.mp4` gerado junto com a entrega do trabalho.

## Como publicar no GitHub (para o link pedido pelo professor)

No terminal, dentro da pasta `SeguidorDeLinha_Webots`:

```bash
git init
git add .
git commit -m "Projeto seguidor de linha - Webots"
git branch -M main
git remote add origin https://github.com/<SEU_USUARIO>/<NOME_DO_REPO>.git
git push -u origin main
```

Depois, copie o link do repositório e cole:
- No topo deste `README.md` (`Repositório GitHub`);
- No cabeçalho de `worlds/carro.wbt` (comentário `Repositorio GitHub do projeto`);
- No cabeçalho de `controllers/seguidor_linha/seguidor_linha.py`.

### Link "raw" da imagem da pista (igual ao exemplo do professor)

O link que o professor mandou (`.../mapas/oval_line.png`) é o formato
**raw** de uma imagem hospedada no GitHub — é assim que o Webots consegue
baixar a textura da pista pela internet. Depois de publicar seu
repositório, gere o link raw da SUA imagem:

1. No GitHub, abra `worlds/textures/pista_textura.png` no seu repositório.
2. Clique em **Raw** (ou botão de "..." → *Download raw file* / *Copy raw
   link*, dependendo da interface do GitHub).
3. Copie a URL — ela terá o formato:
   `https://raw.githubusercontent.com/<SEU_USUARIO>/<REPO>/refs/heads/main/worlds/textures/pista_textura.png`
4. Cole essa URL no lugar de
   `<COLOQUE_AQUI_O_LINK_RAW_GITHUB_DA_SUA_IMAGEM_DE_PISTA>` dentro de
   `worlds/carro.wbt` (campo `url` do `ImageTexture`).

Como o campo `url` do `ImageTexture` já tem o caminho local
(`textures/pista_textura.png`) como primeira opção, a simulação funciona
mesmo antes de você publicar no GitHub — o link remoto é usado como
"prova" de que a pista é sua e está publicada, conforme pedido no
enunciado.

Não esqueça de subir também o vídeo `.mp4` gerado pelo Webots (ou um link
para ele, caso o GitHub recuse arquivos muito grandes — nesse caso, uma
opção é usar o *Git LFS* ou anexar o vídeo separadamente na entrega).

## Antes de entregar, confira nos dois arquivos:

- `worlds/carro.wbt` → nome, RA e link do GitHub já preenchidos.
- `controllers/seguidor_linha/seguidor_linha.py` → mesmos dados no
  cabeçalho do arquivo.
- Falta só substituir `<COLOQUE_AQUI_O_LINK_RAW_GITHUB_DA_SUA_IMAGEM_DE_PISTA>`
  e `<COLOQUE_AQUI_O_LINK_DO_SEU_GITHUB>` depois de publicar o repositório.

## Se o carro se comportar de forma estranha (tremendo, afundando, voando)

Isso normalmente é sinal de conflito na física das rodas (posição/rotação
das juntas). Nesta versão do projeto, a estrutura das rodas foi corrigida
para ficar **idêntica** à do arquivo original do professor — só foram
adicionados sensores, corpo e cor novos, sem tocar nas juntas
(`HingeJoint`) nem na geometria das rodas. Se mesmo assim algo parecer
estranho:

1. Feche o Webots **sem salvar** e abra `carro.wbt` de novo (às vezes o
   Webots salva no arquivo a posição "instável" em que a simulação parou).
2. Confira se você não moveu nenhuma peça sem querer dentro do Webots
   (arrastando com o mouse) antes de dar play.
3. Sempre use a versão mais recente do `.zip` — se você já tinha extraído
   uma versão anterior, apague a pasta antiga e extraia de novo.
