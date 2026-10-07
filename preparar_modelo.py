"""Baixa e valida o modelo ANTES da apresentação; não precisa da câmera."""
from pathlib import Path


def main():
    import numpy as np
    from ultralytics import YOLO
    pasta = Path(__file__).resolve().parent / 'modelos'
    pasta.mkdir(exist_ok=True)
    caminho = pasta / 'yolov8n.pt'
    print('Preparando YOLOv8n (internet necessária somente para baixar)...')
    modelo = YOLO(str(caminho))
    assert 'cell phone' in modelo.names.values(), 'Modelo sem classe de celular.'
    modelo.predict(np.zeros((480, 640, 3), dtype=np.uint8), imgsz=640, device='cpu', verbose=False)
    print('Modelo validado:', caminho)
    print('O reconhecimento agora pode funcionar sem internet, com o modelo nesta pasta.')


if __name__ == '__main__':
    try:
        main()
    except Exception as erro:
        print('Falha ao preparar o modelo:', erro)
        raise SystemExit(1)
