"""VÍDEO: OpenCV permitido pelo enunciado; CSRT e YOLOv8n para celular.

As threads nunca chamam Tkinter. Filas limitadas descartam frames antigos.
O detector recebe somente frames locais; não envia imagens para serviços.
"""
import os
from pathlib import Path
import queue
import threading
import time
import cv2


PASTA = Path(__file__).resolve().parent


def colocar_recente(fila, item):
    try:
        fila.put_nowait(item)
    except queue.Full:
        try:
            fila.get_nowait()
        except queue.Empty:
            pass
        try:
            fila.put_nowait(item)
        except queue.Full:
            pass


def criar_rastreador():
    if hasattr(cv2, 'TrackerCSRT_create'):
        return cv2.TrackerCSRT_create()
    if hasattr(cv2, 'legacy') and hasattr(cv2.legacy, 'TrackerCSRT_create'):
        return cv2.legacy.TrackerCSRT_create()
    raise RuntimeError('CSRT indisponível. Instale opencv-contrib-python no ambiente do projeto.')


def processar_frame(frame, operacao, tamanho=3, baixo=50, alto=150):
    """Somente no vídeo usamos funções prontas do OpenCV."""
    if operacao == 'Original':
        return frame.copy()
    if operacao == 'Negativo':
        return cv2.bitwise_not(frame)
    if operacao == 'Cinza':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if operacao == 'Otsu':
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    if operacao == 'Média':
        return cv2.blur(frame, (tamanho, tamanho))
    if operacao == 'Mediana':
        return cv2.medianBlur(frame, tamanho)
    if operacao == 'Canny':
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(cinza, baixo, alto)
    import numpy as np
    elemento = np.ones((tamanho, tamanho), np.uint8)
    if operacao == 'Erosão':
        return cv2.erode(frame, elemento)
    if operacao == 'Dilatação':
        return cv2.dilate(frame, elemento)
    if operacao == 'Abertura':
        return cv2.morphologyEx(frame, cv2.MORPH_OPEN, elemento)
    if operacao == 'Fechamento':
        return cv2.morphologyEx(frame, cv2.MORPH_CLOSE, elemento)
    raise ValueError('Operação de vídeo desconhecida.')


class GatilhoPresenca:
    """Dispara uma vez após duas detecções; rearma após três ausências.

    Não conta repetições do mesmo resultado; deve ser atualizado somente
    quando uma nova inferência chega. Pause/stop/detector off reiniciam.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.acertos = 0
        self.ausencias = 0
        self.presente = False

    def atualizar(self, detectado):
        if detectado:
            self.acertos += 1
            self.ausencias = 0
            if not self.presente and self.acertos >= 2:
                self.presente = True
                return True
        else:
            self.acertos = 0
            self.ausencias += 1
            if self.ausencias >= 3:
                self.presente = False
        return False


class DetectorCelular(threading.Thread):
    def __init__(self, eventos):
        super().__init__(daemon=True)
        self.entrada = queue.Queue(maxsize=1)
        self.saida = queue.Queue(maxsize=1)
        self.eventos = eventos
        self.parar = threading.Event()

    def run(self):
        try:
            # Importação e download somente ao ativar o reconhecimento.
            from ultralytics import YOLO
            caminho = PASTA / 'modelos' / 'yolov8n.pt'
            caminho.parent.mkdir(exist_ok=True)
            self.eventos.put(('status', 'Carregando YOLOv8n; no primeiro uso o modelo será baixado.'))
            modelo = YOLO(str(caminho))
            nomes = modelo.names
            celulares = [i for i, nome in nomes.items() if nome == 'cell phone']
            if not celulares:
                raise RuntimeError('O modelo não possui a classe cell phone.')
            self.eventos.put(('detector_pronto', 'Detector de celular pronto.'))
            while not self.parar.is_set():
                try:
                    frame, instante, confianca, geracao = self.entrada.get(timeout=0.2)
                except queue.Empty:
                    continue
                resultados = modelo.predict(frame, classes=celulares, conf=confianca,
                                            imgsz=640, device='cpu', verbose=False)
                caixas = []
                for caixa in resultados[0].boxes:
                    x1, y1, x2, y2 = caixa.xyxy[0].cpu().tolist()
                    certeza = float(caixa.conf[0].cpu())
                    caixas.append((int(x1), int(y1), int(x2), int(y2), certeza))
                colocar_recente(self.saida, (caixas, instante, geracao))
        except Exception as erro:
            self.eventos.put(('erro_detector', str(erro)))


class Camera(threading.Thread):
    def __init__(self, indice=0):
        super().__init__(daemon=True)
        self.indice = indice
        self.frames = queue.Queue(maxsize=1)
        self.eventos = queue.Queue()
        self.comandos = queue.Queue()
        self.parar = threading.Event()
        self.lock = threading.Lock()
        self.parametros = dict(operacao='Original', tamanho=3, baixo=50, alto=150,
                               detector=False, confianca=0.40, pausado=False)
        self.detector = None
        self.rastreador = None
        self.caixa = None
        self.geracao = 0

    def configurar(self, **parametros):
        with self.lock:
            self.parametros.update(parametros)

    def encerrar(self):
        self.parar.set()
        if self.detector:
            self.detector.parar.set()

    def run(self):
        captura = None
        gatilho = GatilhoPresenca()
        caixas_celular = []
        ultimo_envio = 0
        ultimo_resultado = 0
        detector_anterior = False
        pausado_anterior = False
        try:
            # DirectShow costuma reduzir o tempo de abertura no Windows.
            captura = cv2.VideoCapture(self.indice, cv2.CAP_DSHOW) if os.name == 'nt' else cv2.VideoCapture(self.indice)
            if not captura.isOpened():
                captura.release()
                captura = cv2.VideoCapture(self.indice)
            if not captura.isOpened():
                raise RuntimeError('Não foi possível abrir a câmera. Confira o índice e a permissão do Windows.')
            captura.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            captura.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            captura.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.eventos.put(('status', 'Câmera aberta.'))
            falhas = 0
            while not self.parar.is_set():
                with self.lock:
                    p = self.parametros.copy()
                if p['detector'] != detector_anterior or p['pausado'] != pausado_anterior:
                    self.geracao += 1
                    gatilho.reset()
                    caixas_celular = []
                    ultimo_resultado = 0
                    detector_anterior = p['detector']
                    pausado_anterior = p['pausado']
                if p['pausado']:
                    self.parar.wait(0.03)
                    continue
                ok, frame = captura.read()
                if not ok:
                    falhas += 1
                    if falhas >= 10:
                        raise RuntimeError('A câmera deixou de fornecer imagens.')
                    self.parar.wait(0.1)
                    continue
                falhas = 0
                while True:
                    try:
                        comando, argumento = self.comandos.get_nowait()
                    except queue.Empty:
                        break
                    if comando == 'rastrear':
                        try:
                            # Usa exatamente o frame congelado na seleção.
                            referencia, caixa = argumento
                            self.rastreador = criar_rastreador()
                            ok_init = self.rastreador.init(referencia, tuple(map(int, caixa)))
                            if ok_init is False:
                                raise RuntimeError('Não foi possível iniciar o rastreamento.')
                            self.caixa = caixa
                            self.eventos.put(('status', 'Rastreamento CSRT iniciado.'))
                        except Exception as erro:
                            self.rastreador = None
                            self.eventos.put(('erro', str(erro)))
                    elif comando == 'limpar_rastro':
                        self.rastreador = None
                        self.caixa = None
                if self.rastreador is not None:
                    ok_rastro, caixa = self.rastreador.update(frame)
                    if ok_rastro:
                        self.caixa = tuple(map(int, caixa))
                    else:
                        self.rastreador = None
                        self.caixa = None
                        self.eventos.put(('status', 'Objeto perdido. Selecione novamente para rastrear.'))
                agora = time.monotonic()
                if p['detector']:
                    if self.detector is None:
                        self.detector = DetectorCelular(self.eventos)
                        self.detector.start()
                    if self.detector.is_alive() and agora - ultimo_envio >= 0.5:
                        colocar_recente(self.detector.entrada, (frame.copy(), agora, p['confianca'], self.geracao))
                        ultimo_envio = agora
                    try:
                        caixas, instante, geracao = self.detector.saida.get_nowait()
                        if geracao == self.geracao and agora - instante < 2.0:
                            caixas_celular = caixas
                            ultimo_resultado = agora
                            if gatilho.atualizar(bool(caixas)):
                                self.eventos.put(('celular', 'Celular reconhecido.'))
                    except queue.Empty:
                        pass
                    if ultimo_resultado and agora - ultimo_resultado > 2.0:
                        caixas_celular = []
                        gatilho.reset()
                        ultimo_resultado = 0
                resultado = processar_frame(frame, p['operacao'], p['tamanho'], p['baixo'], p['alto'])
                # Anotações são apenas visualização; frame bruto continua disponível.
                if resultado.ndim == 2:
                    resultado = cv2.cvtColor(resultado, cv2.COLOR_GRAY2BGR)
                if self.caixa is not None:
                    x, y, w, h = self.caixa
                    cv2.rectangle(resultado, (x, y), (x+w, y+h), (255, 160, 0), 2)
                    cv2.putText(resultado, 'CSRT', (x, max(20, y-8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 160, 0), 2)
                for x1, y1, x2, y2, confianca in caixas_celular:
                    cv2.rectangle(resultado, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(resultado, f'Celular {confianca:.0%}', (x1, max(20, y1-8)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                colocar_recente(self.frames, (frame.copy(), resultado))
                self.parar.wait(0.01)
        except Exception as erro:
            self.eventos.put(('erro', str(erro)))
        finally:
            if captura is not None:
                captura.release()
            if self.detector is not None:
                self.detector.parar.set()
            self.eventos.put(('camera_fechada', 'Câmera encerrada.'))


class Audio:
    def __init__(self):
        self.caminho = None
        self.pygame = None

    def selecionar(self, caminho):
        if self.pygame is None:
            os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
            import pygame
            pygame.mixer.init()
            self.pygame = pygame
        self.pygame.mixer.music.load(str(caminho))
        self.caminho = str(caminho)

    def tocar(self):
        if not self.caminho:
            return False
        # Uma presença prolongada não reinicia; nova aparição inicia se terminou.
        if not self.pygame.mixer.music.get_busy():
            self.pygame.mixer.music.play()
        return True

    def parar(self):
        if self.pygame:
            self.pygame.mixer.music.stop()

    def encerrar(self):
        if self.pygame:
            self.pygame.mixer.quit()
