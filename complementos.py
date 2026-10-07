"""Complementos novos do trabalho. Os códigos das listas estão em listas/.

Canny e primitivas morfológicas próprios; rotulação completa e medidas.
Estas funções não são apresentadas como cópias intactas das listas.
"""
from collections import deque
import math
import numpy as np
from listas.lista1.conversao_niveis_cinza import converter_para_cinza as _cinza_lista

def converter_para_cinza(img):
    if img.ndim == 2:
        return img.copy()
    return _cinza_lista(img)

def validar_imagem(img):
    if not isinstance(img, np.ndarray) or img.size == 0:
        raise ValueError('A imagem está vazia.')
    if img.dtype != np.uint8 or img.ndim not in (2, 3):
        raise ValueError('Use imagem uint8, em cinza ou BGR.')
    if img.ndim == 3 and img.shape[2] != 3:
        raise ValueError('São esperados três canais BGR.')


def validar_tamanho(tamanho):
    tamanho = int(tamanho)
    if tamanho < 1 or tamanho > 31 or tamanho % 2 == 0:
        raise ValueError('O tamanho deve ser ímpar, entre 1 e 31.')
    return tamanho


def _por_canal(img, funcao):
    validar_imagem(img)
    if img.ndim == 2:
        return funcao(img)
    return np.stack([funcao(img[:, :, c]) for c in range(3)], axis=2)


def _convolucao(img, mascara):
    """Convolução/correlação própria; somas de vizinhança como na Lista 2.

    A soma é vetorizada por posição da máscara para reduzir o tempo do Canny.
    Borda repetida; mantém sinal e precisão dos gradientes em float64.
    """
    margem = mascara.shape[0] // 2
    borda = np.pad(img.astype(np.float64), margem, mode='edge')
    altura, largura = img.shape
    resultado = np.zeros(img.shape, np.float64)
    for i in range(mascara.shape[0]):
        for j in range(mascara.shape[1]):
            resultado += mascara[i, j] * borda[i:i+altura, j:j+largura]
    return resultado


def canny(img, limiar_baixo=50, limiar_alto=150):
    """Complementa Lista 4: Gaussian -> Sobel -> supressão -> histerese.

    O Sobel deriva das máscaras da Lista 2, agora mantendo gx e gy para a
    direção. A magnitude usa sqrt(gx²+gy²), sem normalização por imagem.
    Não chama cv2.Canny; resultados não precisam coincidir pixel a pixel.
    """
    if not 0 < limiar_baixo < limiar_alto:
        raise ValueError('Canny: use 0 < limiar baixo < limiar alto.')
    cinza = converter_para_cinza(img)
    coordenadas = np.arange(-2, 3, dtype=float)
    g = np.exp(-(coordenadas ** 2) / (2 * 1.0 ** 2))
    gaussiana = np.outer(g, g)
    gaussiana /= gaussiana.sum()
    suavizada = _convolucao(cinza, gaussiana)
    mascara_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    mascara_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    gx = _convolucao(suavizada, mascara_x)
    gy = _convolucao(suavizada, mascara_y)
    magnitude = np.hypot(gx, gy)
    angulo = np.degrees(np.arctan2(gy, gx)) % 180
    suprimida = np.zeros(cinza.shape, np.float64)
    centro = magnitude[1:-1, 1:-1]
    direcao = angulo[1:-1, 1:-1]
    # A coordenada y aumenta para baixo: 45° compara NO e SE.
    casos = [
        ((direcao < 22.5) | (direcao >= 157.5), magnitude[1:-1, :-2], magnitude[1:-1, 2:]),
        ((direcao >= 22.5) & (direcao < 67.5), magnitude[:-2, :-2], magnitude[2:, 2:]),
        ((direcao >= 67.5) & (direcao < 112.5), magnitude[:-2, 1:-1], magnitude[2:, 1:-1]),
        ((direcao >= 112.5) & (direcao < 157.5), magnitude[:-2, 2:], magnitude[2:, :-2]),
    ]
    for faixa, vizinho1, vizinho2 in casos:
        manter = faixa & (centro >= vizinho1) & (centro >= vizinho2)
        suprimida[1:-1, 1:-1][manter] = centro[manter]
    fortes = suprimida >= limiar_alto
    candidatos = suprimida >= limiar_baixo
    resultado = np.zeros(cinza.shape, np.uint8)
    resultado[fortes] = 255
    fila = deque(zip(*np.nonzero(fortes)))
    altura, largura = cinza.shape
    while fila:
        y, x = fila.popleft()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = y + dy, x + dx
                if (0 <= ny < altura and 0 <= nx < largura and
                        candidatos[ny, nx] and resultado[ny, nx] == 0):
                    resultado[ny, nx] = 255
                    fila.append((ny, nx))
    return resultado


def _morfologia(img, tamanho, dilatar):
    """Primitiva própria: máximo (dilatação) ou mínimo (erosão) por janela.

    Elemento estruturante quadrado. Fora da imagem: 0 na dilatação e 255
    na erosão (valores neutros). Funciona em cinza, binário e por canal BGR.
    """
    tamanho = validar_tamanho(tamanho)
    def calcular(canal):
        margem = tamanho // 2
        neutro = 0 if dilatar else 255
        borda = np.pad(canal, margem, mode='constant', constant_values=neutro)
        altura, largura = canal.shape
        resultado = np.full(canal.shape, neutro, np.uint8)
        for i in range(tamanho):
            for j in range(tamanho):
                vizinhos = borda[i:i+altura, j:j+largura]
                if dilatar:
                    resultado = np.maximum(resultado, vizinhos)
                else:
                    resultado = np.minimum(resultado, vizinhos)
        return resultado
    return _por_canal(img, calcular)


def erosao(img, tamanho=3):
    return _morfologia(img, tamanho, False)


def dilatacao(img, tamanho=3):
    return _morfologia(img, tamanho, True)


def abertura(img, tamanho=3):
    """Lista 5: erosão seguida de dilatação; primitivas agora próprias."""
    return dilatacao(erosao(img, tamanho), tamanho)


def fechamento(img, tamanho=3):
    """Lista 5: dilatação seguida de erosão; primitivas agora próprias."""
    return erosao(dilatacao(img, tamanho), tamanho)


def _produto_vetorial(o, a, b):
    return (a[0]-o[0]) * (b[1]-o[1]) - (a[1]-o[1]) * (b[0]-o[0])


def _envoltoria_convexa(pontos):
    """Monotone chain própria: elimina pontos internos antes do diâmetro."""
    pontos = sorted(set(pontos))
    if len(pontos) < 3:
        return pontos
    inferior, superior = [], []
    for p in pontos:
        while len(inferior) >= 2 and _produto_vetorial(inferior[-2], inferior[-1], p) <= 0:
            inferior.pop()
        inferior.append(p)
    for p in reversed(pontos):
        while len(superior) >= 2 and _produto_vetorial(superior[-2], superior[-1], p) <= 0:
            superior.pop()
        superior.append(p)
    return inferior[:-1] + superior[:-1]


def diametro(pontos):
    """Maior distância entre CENTROS dos pixels: Feret máximo discreto.

    Envoltória O(b log b), seguida de rotating calipers O(h).
    Um pixel isolado tem diâmetro zero nesta convenção.
    """
    hull = _envoltoria_convexa(pontos)
    n = len(hull)
    if n < 2:
        return 0.0
    def dist2(a, b):
        return (a[0]-b[0]) ** 2 + (a[1]-b[1]) ** 2
    if n == 2:
        return math.sqrt(dist2(*hull))
    maior = 0
    j = 1
    for i in range(n):
        ni = (i + 1) % n
        def area(k):
            return abs(_produto_vetorial(hull[i], hull[ni], hull[k]))
        while area((j+1) % n) > area(j):
            j = (j+1) % n
        maior = max(maior, dist2(hull[i], hull[j]), dist2(hull[ni], hull[j]))
        if area((j+1) % n) == area(j):
            nj = (j+1) % n
            maior = max(maior, dist2(hull[i], hull[nj]), dist2(hull[ni], hull[nj]))
    return math.sqrt(maior)


def rotular_componentes(img, conectividade=8, area_minima=1):
    """Amplia Lista 5/q6: busca com pilha para TODOS os componentes.

    Fundo=0; objeto=255. Área em pixels; perímetro conta os lados expostos
    na grade de quatro vizinhos (inclui bordas de buracos). Diâmetro em px.
    Rótulos menores que area_minima são descartados, com renumeração.
    """
    validar_imagem(img)
    if img.ndim != 2 or not np.all((img == 0) | (img == 255)):
        raise ValueError('A contagem exige imagem binária (0 e 255). Aplique Otsu primeiro.')
    if conectividade not in (4, 8) or area_minima < 1:
        raise ValueError('Conectividade deve ser 4 ou 8; área mínima >= 1.')
    altura, largura = img.shape
    rotulos = np.zeros(img.shape, dtype=np.int32)
    direcoes4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    vizinhos = direcoes4 if conectividade == 4 else [
        (dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0)]
    objetos = []
    # -1 marca objetos descartados sem precisar visitá-los novamente.
    for y in range(altura):
        for x in range(largura):
            if img[y, x] == 0 or rotulos[y, x] != 0:
                continue
            identificador = len(objetos) + 1
            pilha = [(y, x)]
            rotulos[y, x] = identificador
            pixels, borda = [], []
            perimetro = 0
            while pilha:
                py, px = pilha.pop()
                pixels.append((py, px))
                lados_expostos = 0
                for dy, dx in direcoes4:
                    ny, nx = py+dy, px+dx
                    if not (0 <= ny < altura and 0 <= nx < largura) or img[ny, nx] == 0:
                        lados_expostos += 1
                perimetro += lados_expostos
                if lados_expostos:
                    borda.append((px, py))
                for dy, dx in vizinhos:
                    ny, nx = py+dy, px+dx
                    if 0 <= ny < altura and 0 <= nx < largura:
                        if img[ny, nx] == 255 and rotulos[ny, nx] == 0:
                            rotulos[ny, nx] = identificador
                            pilha.append((ny, nx))
            if len(pixels) < area_minima:
                for py, px in pixels:
                    rotulos[py, px] = -1
                continue
            ys, xs = zip(*pixels)
            objetos.append(dict(id=identificador, area=len(pixels), perimetro=perimetro,
                                diametro=diametro(borda), x=min(xs), y=min(ys),
                                largura=max(xs)-min(xs)+1, altura=max(ys)-min(ys)+1))
    rotulos[rotulos < 0] = 0
    visualizacao = np.zeros((altura, largura, 3), np.uint8)
    for objeto in objetos:
        i = objeto['id']
        # Cores BGR determinísticas; nenhum rótulo de objeto fica preto.
        cor = (60+(i*73)%196, 60+(i*113)%196, 60+(i*151)%196)
        visualizacao[rotulos == i] = cor
    return rotulos, objetos, visualizacao


