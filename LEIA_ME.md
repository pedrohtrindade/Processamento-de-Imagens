# Trabalho prático de Processamento Digital de Imagens

Aluno: Pedro Henrique Trindade. Python, OpenCV e interface Tkinter.

## Códigos das listas preservados nesta revisão

A versão anterior reuniu e reescreveu funções em `processamento.py`. Esta revisão
restaura os arquivos separados e os passos originais das funções.

- **`originais/lista1` até `originais/lista5`:** os 33 arquivos Python fornecidos,
  copiados sem modificar seus bytes, inclusive os geradores de relatórios.
- **`listas/lista1` até `listas/lista5`:** cópias para integração. Todos os nomes
  de funções, laços, variáveis e etapas foram preservados. Os exemplos de execução
  ficam dentro de `if __name__ == "__main__":`, para importar as funções sem abrir
  imagens/janelas automaticamente. A criação de diretório `SAIDA` também foi movida
  para esse bloco. No negativo, a única correção do algoritmo é `250` para `255`.
- **`processamento.py`:** ligação da interface com as funções originais de cinza,
  negativo, histograma, média, mediana e Otsu. Para filtros coloridos, chama a mesma
  função original separadamente para azul, verde e vermelho.
- **`complementos.py`:** implementações novas, separadas dos códigos preservados:
  Canny próprio, primitivas de morfologia próprias, rotulação completa e medidas.

A comparação automática confirmou que 47 funções nas cópias de integração mantêm
exatamente a mesma estrutura do código original. A função de negativo tem a correção
explicitada acima. Esse número indica funções preservadas, não que todas elas sejam
utilizadas pelo programa. Por exemplo, a Lista 3 é incluída para consulta, mas os
filtros de Fourier não são exigidos pelo trabalho.

Os Canny e as operações morfológicas originais, que chamam OpenCV, continuam visíveis
em `listas/lista4/questao4_canny.py` e `listas/lista5/codigos/`. Na aba Imagens,
o programa usa os complementos próprios para seguir a interpretação estrita da
observação do professor. Os arquivos originais não foram substituídos por esses complementos.

Os exemplos dos scripts originais continuam dependendo de suas imagens e dos caminhos
usados nas listas. As imagens e resultados dessas listas continuam nos ZIPs que você
enviou; esta entrega inclui os seus arquivos Python. Para usar a janela, execute
`iniciar_windows.bat`, sem precisar executar os scripts de cada lista separadamente.

## Interface ImageLab 2000

O programa agora tem um tema inspirado nas interfaces de computadores dos anos 2000:
barras azuis, botões em relevo, ícones pixelados e painéis clássicos. A janela continua
sendo um aplicativo de desktop para Windows; não precisa de navegador.

- As abas **Imagens** e **Câmera** ficam na parte superior.
- Os controles ficam na **lateral esquerda**. Use a barra de rolagem ou a roda do
  mouse para acessar as opções inferiores, especialmente Celular & Música.
- As prévias ocupam a área central. O quadriculado é apenas o fundo da prévia:
  ele não é adicionado à imagem salva nem aos cálculos.
- Os campos de tamanho de janela e de limiares ficam habilitados conforme a operação.
- Na aba Imagens, **Restaurar** corresponde ao antigo botão Restaurar original,
  **Salvar** corresponde a Salvar resultado e **Aplicar operação** corresponde a Aplicar.
- A tabela de objetos fica abaixo das prévias. Arraste a divisão horizontal para
  ajustar o espaço entre a tabela e as imagens. Há rolagem horizontal e vertical.
- O rodapé mostra a mensagem da operação, o estado e um indicador de processamento.
- Os menus **Arquivo**, **Exibir** e **Ajuda** também dão acesso às ações principais.
- Passe o mouse sobre alguns controles para ler dicas.
- **F1** abre o guia rápido dentro do aplicativo.
- **Ctrl+O:** abrir imagem; **Ctrl+R:** restaurar original; **Ctrl+S:** salvar resultado
  na aba Imagens ou quadro processado na aba Câmera.

As alterações desta edição estão em `main.py` e no novo `interface_retro.py`.
Os arquivos das listas, de processamento, dos complementos e de vídeo foram comparados
com a versão anterior e preservados byte a byte. A instalação e a execução usam os
mesmos arquivos `.bat`; nenhuma biblioteca extra foi adicionada para o tema.

## Executar no Windows

1. Extraia **todo** o ZIP para uma pasta. Não execute os arquivos dentro do ZIP.
2. Instale Python **3.11 ou 3.12 de 64 bits**, de https://www.python.org/downloads/windows/.
   Inclua o Python Launcher na instalação (comando `py`). Tkinter vem com a instalação padrão.
3. Execute `instalar_windows.bat`. A instalação precisa de internet e pode demorar:
   YOLO utiliza PyTorch, que é uma dependência grande. O script cria um ambiente `.venv`
   isolado, instala as bibliotecas e garante a versão do OpenCV com CSRT.
4. Execute `iniciar_windows.bat` para abrir a janela.
5. O modelo `modelos/yolov8n.pt` já está incluído. Não é necessário treinar nem
   baixar um conjunto de imagens. `baixar_modelo_windows.bat` valida o modelo
   ou baixa outra cópia caso o arquivo seja removido.

A música não está incluída: escolha depois, na janela, um arquivo MP3, WAV ou OGG.
O processamento e o reconhecimento ocorrem localmente. Após instalar as bibliotecas,
o uso normal funciona sem internet, mantendo o arquivo do modelo.

## Como usar: imagens

- **Abrir imagem:** lê uma imagem colorida. A prévia é ajustada à tela; os cálculos
  preservam a resolução original. Caminhos com acentos são aceitos.
- Escolha uma operação e pressione **Aplicar**. O tamanho da janela deve ser ímpar,
  entre 1 e 31. O Canny utiliza `0 < limiar baixo < limiar alto`.
- **Aplicar sobre resultado atual** permite encadear operações. Desmarque para
  aplicar cada operação à imagem original. **Restaurar original** recomeça.
- **Histograma** mostra o histograma de cinza e, quando há cor, os três canais BGR.
  A frequência é calculada pelo código da lista; Matplotlib apenas desenha.
- Para medir objetos, aplique **Otsu**. Os objetos devem estar brancos e o fundo
  preto. Use **Inverter binário** se necessário. Aplique abertura/fechamento para
  reduzir ruídos antes da contagem, quando isso for adequado à imagem.
- Escolha conectividade **4** ou **8** e uma área mínima. Clique em
  **Contar e medir objetos**. A tabela apresenta todos os componentes aceitos.
- **Exportar medidas CSV** salva a tabela; **Salvar resultado** salva a imagem
  processada ou a visualização dos objetos com seus números.

Exemplos incluídos:

- `exemplos/objetos_binarios.png`: três objetos brancos, um deles com um buraco.
  Ao abrir, use Cinza antes de contar (a abertura de arquivos usa BGR).
  Com conectividade 8 e área mínima 1, o resultado esperado é **3 objetos**.
- `exemplos/objetos_coloridos.png`: imagem para testar operações, Otsu e inversão.

## Como usar: câmera

1. Vá à aba **Câmera** e pressione **Abrir câmera**. O índice padrão é 0.
   Caso não abra, teste 1. Permita o acesso a aplicativos de desktop nas
   configurações de privacidade da câmera no Windows e feche outros aplicativos
   que estejam usando o dispositivo.
2. Escolha uma operação e pressione **Atualizar parâmetros**. Os filtros são
   aplicados quadro a quadro. A esquerda mostra o vídeo original; a direita,
   o resultado com as anotações.
3. **Capturar para aba Imagens** copia um quadro bruto para realizar as operações
   próprias de imagem. **Salvar quadro do vídeo** salva o resultado visível.
4. Para rastrear, clique em **Selecionar objeto / cancelar** e arraste um retângulo
   na imagem da esquerda. O vídeo pausa durante a seleção e retoma automaticamente.
   CSRT acompanha o objeto, com caixa azul. Qualquer objeto pode ser selecionado,
   inclusive um celular. Se ele sair da cena e o rastreador perder o alvo, selecione novamente.
5. Para reconhecer a categoria celular, marque **Reconhecer celular (YOLO)**.
   Mostre um celular físico com boa iluminação e tamanho suficiente no quadro.
   A detecção aparece em verde. A confiança inicial é 0,40; ajuste e pressione
   **Atualizar parâmetros**. Reduzir a confiança aumenta sensibilidade e pode
   aumentar falsos positivos.
6. Clique em **Escolher música**, selecione um arquivo e use **Testar música**.
   Duas inferências consecutivas com celular confirmam a aparição e acionam a música.
   Enquanto houver presença contínua, ela não reinicia. Três inferências sem celular
   permitem um novo disparo numa nova aparição. Se a música ainda estiver tocando,
   uma nova aparição não a interrompe nem a reinicia. Ao terminar a faixa, uma
   presença contínua também não a reinicia.
7. **Parar música** interrompe o áudio; **Parar câmera** encerra o vídeo e o áudio.

Sem música selecionada, o celular continua sendo reconhecido e a janela informa
que falta selecionar o arquivo. O reconhecimento identifica a categoria "celular",
sem diferenciar o aparelho de uma pessoa de outro aparelho.

CSRT e YOLO resolvem requisitos diferentes: CSRT acompanha uma região escolhida;
YOLO identifica a categoria do objeto. Ambos usam o quadro original, mesmo quando
o vídeo exibido está em negativo, Canny ou outra operação. YOLO trabalha em outra
thread, permitindo que a janela continue respondendo durante o carregamento e a inferência.

## Relação com as listas

| Requisito | Base usada | Adaptação no trabalho |
|---|---|---|
| Cinza | Lista 1, `conversao_niveis_cinza.py` | Média dos canais mantida; aceita imagem já em cinza |
| Negativo | Lista 1, `negativo.py` | Corrigido `250 - img` para `255 - img` |
| Histograma | Lista 1, `exercicio7_histogramas.py` | Contagem própria; gráfico usa Matplotlib |
| Média e mediana | Lista 2, `filtro_media.py` e `filtro_mediana.py`; Lista 4, questão 1 | Janela e borda zero preservadas; opção colorida processa cada canal |
| Otsu | Lista 4, `questao6_otsu.py` | Histograma e maximização da variância entre classes preservados |
| Canny | Lista 4, questão 4; Sobel da Lista 2 | A chamada pronta foi substituída por Gaussian, Sobel, supressão e histerese próprios |
| Erosão e dilatação | Lista 5, questões 2, 3, 4 e 7 | Chamadas prontas substituídas por mínimo e máximo próprios |
| Abertura e fechamento | Lista 5, questão 3 | Ordem das operações mantida, usando as primitivas próprias |
| Rotulação de componentes | Lista 5, `questao6.py` | Busca com pilha ampliada para todos os objetos; conectividade 4/8 |
| Área, perímetro e diâmetro | Ampliação da rotulação | Contagem de pixels, lados expostos e distância máxima |

Os filtros de Fourier da Lista 3 não são necessários aos requisitos obrigatórios.
Não foram adicionados como extras para manter o programa fácil de explicar.

**Importante:** Canny e morfologia, nas listas enviadas, utilizavam funções prontas.
Por isso, esses trechos foram complementados: não seria correto dizer que as versões
próprias completas já estavam presentes nas listas. O trabalho identifica as adaptações.

As funções reutilizadas de cinza, negativo, histograma, média, mediana e Otsu
fazem os cálculos diretamente, como nas listas. Os algoritmos novos próprios ficam
em `complementos.py`. OpenCV, no `main.py`, somente
lê e salva imagens. Pillow ajusta as prévias e desenha os números dos objetos.
Em `video.py`, o processamento de vídeo usa funções prontas, conforme a exceção
expressa no enunciado. Não substitua as funções próprias por funções cv2 na aba Imagens.

## Convenções das medidas

- **Área:** número de pixels brancos pertencentes ao componente, em px (unidades
  de área de pixel). Não há calibração para cm².
- **Perímetro:** soma dos lados de pixels expostos ao fundo ou ao exterior da imagem,
  em px. Inclui fronteiras internas de buracos. É um perímetro na grade; pode diferir
  do comprimento de contorno estimado por funções do OpenCV.
- **Diâmetro:** maior distância euclidiana entre centros de pixels do objeto
  (Feret máximo discreto), em px. Uma envoltória convexa própria e rotating calipers
  evitam testar todos os pares. Um pixel isolado tem diâmetro 0 nesta convenção;
  um retângulo de 2 x 3 pixels tem diâmetro `sqrt(5)`.
- X e Y são coordenadas da caixa mínima do objeto, começando em **0**. Largura
  e altura incluem todos os pixels da caixa.
- Conectividade 4 não une pixels apenas na diagonal; conectividade 8 une.

Essas definições estão explícitas porque "diâmetro" e "perímetro" podem ter
outras convenções. Se o professor exigir outra, será necessário adaptar a medida.

## Arquivos e apresentação

- `main.py`: ações dos botões, leitura/salvamento e coordenação da janela.
- `interface_retro.py`: tema, ícones pixelados, layout, menus, dicas e atalhos.
- `processamento.py`: ligação com as funções das listas.
- `listas/`: códigos separados de cada lista, preparados para importação.
- `originais/`: cópias sem alterações dos arquivos Python enviados.
- `complementos.py`: algoritmos novos exigidos pelo trabalho.
- `video.py`: câmera, processamento pronto de vídeo, CSRT, YOLO e áudio.
- `preparar_modelo.py`: validação/download dos pesos.
- `testar_algoritmos.py`: verificações automáticas sem câmera física.
- `requirements.txt` e arquivos `.bat`: instalação e execução no Windows.
- `modelos/yolov8n.pt`: pesos oficiais do detector pré-treinado.

Antes da apresentação:

1. Instale e execute no computador que será usado.
2. Abra os exemplos e demonstre conversões, filtros, morfologia e histograma.
3. Conte os três objetos e mostre a tabela, o buraco e a exportação CSV.
4. Abra a câmera; demonstre pelo menos uma conversão e cada grupo de operações.
5. Selecione um objeto, mova-o lentamente e demonstre CSRT.
6. Selecione a música, confirme o som e mostre um celular até aparecer a caixa verde.
7. Retire o celular e aguarde algumas inferências antes de mostrar novamente.

Para repetir as verificações dos algoritmos no Windows:

```bat
.venv\Scripts\python.exe testar_algoritmos.py
```

Para enviar ao Moodle, compacte esta pasta, incluindo código e modelo. Exclua
`.venv`, `__pycache__` e arquivos temporários. Caso queira incluir a música,
copie o arquivo para a pasta e selecione essa cópia no programa.

## Limites e validação

Algoritmos próprios de média/mediana percorrem os pixels em Python. Imagens grandes
podem levar segundos; a janela continua respondendo. Canny próprio usa borda repetida,
Gaussian 5 x 5 com sigma 1 e magnitude euclidiana do Sobel. A versão da câmera usa
o Canny pronto do OpenCV, por isso resultados podem diferir.

Foram executados 12 testes dos algoritmos, incluindo comparações com OpenCV,
rotulação com buracos e bordas, conectividade, diâmetro comparado à força bruta,
operações de vídeo, regra de presença para a música e CSRT em sequência sintética.
O modelo real foi carregado e executado em quadro vazio; o áudio WAV foi testado
com dispositivo simulado. Isso não valida a taxa de acerto para um celular real.
Também foram exercitados os botões da interface, histogramas, contagem e exportações,
com inspeção visual das duas abas. Uma câmera simulada validou o fluxo de abertura,
filtro, seleção por retângulo, CSRT, captura e encerramento. Um detector simulado
validou a integração entre o evento de celular e o disparo único da música.
O teste com câmera, alto-falantes e celular físicos deve ser realizado no Windows.
Velocidade e reconhecimento dependem do hardware, iluminação, distância e oclusão.

## Referências técnicas

- Listas 1 a 5 fornecidas pelo aluno e enunciado do trabalho da disciplina.
- Ultralytics YOLOv8: https://docs.ultralytics.com/models/yolov8/
- API Python: https://docs.ultralytics.com/usage/python/
- COCO, incluindo a categoria `cell phone`: https://docs.ultralytics.com/datasets/detect/coco/
- OpenCV CSRT: https://docs.opencv.org/4.11.0/d2/da2/classcv_1_1TrackerCSRT.html
- Pesos oficiais: https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8n.pt
  (modelo Ultralytics, distribuído sob licença AGPL-3.0; veja https://ultralytics.com/license).

## Barra de intensidade dos filtros

As abas Imagens e Câmera possuem uma barra para Média, Mediana, Erosão,
Dilatação, Abertura e Fechamento. Ela ajusta o tamanho da janela/elemento
estruturante de 1 × 1 até 31 × 31, sempre em valores ímpares. O campo
numérico continua disponível e fica sincronizado com a barra.

Na aba Imagens, solte a barra para aplicar o filtro. No vídeo aberto,
o tamanho é atualizado durante o movimento. Uma janela 1 × 1 é neutra;
valores maiores geralmente tornam o efeito mais evidente. A mudança depende
do tamanho das estruturas presentes na imagem, especialmente em abertura
e fechamento. Imagens grandes e janelas grandes podem demorar.

Para comparar intensidades sobre a mesma imagem, desmarque “Aplicar sobre
resultado atual”. Com essa opção marcada, cada aplicação trabalha sobre
o resultado anterior e os efeitos podem se acumular. Nenhum algoritmo das
listas ou de processamento foi alterado para adicionar a barra.
