import cv2
from pathlib import Path

PASTA = Path(__file__).parent
SAIDA = PASTA / 'resultados'
SAIDA.mkdir(exist_ok=True)

def detector_canny(img, limiar_baixo, limiar_alto):
    resultado = cv2.Canny(img, limiar_baixo, limiar_alto)
    return resultado

img = cv2.imread(str(PASTA / 'igreja.png'), cv2.IMREAD_GRAYSCALE)
assert img is not None, 'igreja.png nao foi carregada'

resultado = detector_canny(img, 100, 200)
cv2.imwrite(str(SAIDA / 'q4_canny.png'), resultado)

