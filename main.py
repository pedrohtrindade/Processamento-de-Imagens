"""Trabalho prático de PDI - Pedro Henrique Trindade.

Execute: python main.py. Interface Tkinter; processamento de imagens próprio.
Interface retrô separada dos algoritmos das listas e dos complementos.
"""
import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw
import processamento as pdi
from video import Camera, Audio
from interface_retro import montar_interface, desenhar_fundo


class PainelImagem(tk.Canvas):
    """Mostra uma prévia ajustada à tela sem alterar a resolução do cálculo."""
    def __init__(self, mestre, **kwargs):
        super().__init__(mestre, bg='#edede7', highlightthickness=0, **kwargs)
        self.img = None
        self.foto = None
        self.escala = 1.0
        self.origem = (0, 0)
        self.bind('<Configure>', lambda evento: self.desenhar())

    def mostrar(self, img):
        self.img = img
        self.desenhar()

    def desenhar(self):
        self.delete('imagem')
        desenhar_fundo(self)
        if self.img is None:
            return
        altura, largura = self.img.shape[:2]
        cw, ch = max(1, self.winfo_width()), max(1, self.winfo_height())
        self.escala = min(cw/largura, ch/altura)
        tamanho = (max(1, round(largura*self.escala)), max(1, round(altura*self.escala)))
        rgb = self.img if self.img.ndim == 2 else self.img[:, :, ::-1]
        pil = Image.fromarray(rgb).resize(tamanho, Image.Resampling.BILINEAR)
        self.foto = ImageTk.PhotoImage(pil)
        self.origem = ((cw-tamanho[0])/2, (ch-tamanho[1])/2)
        self.create_image(*self.origem, image=self.foto, anchor='nw', tags='imagem')
        self.tag_raise('imagem', 'fundo')

    def coordenada(self, x, y):
        if self.img is None:
            return None
        ox, oy = self.origem
        altura, largura = self.img.shape[:2]
        return (min(largura-1, max(0, int((x-ox)/self.escala))),
                min(altura-1, max(0, int((y-oy)/self.escala))))


class Aplicacao:
    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title('ImageLab 2000 — Pedro Trindade')
        largura = min(1320, raiz.winfo_screenwidth()-45)
        altura = min(900, raiz.winfo_screenheight()-80)
        raiz.geometry(f'{largura}x{altura}')
        raiz.minsize(980, 650)
        self.original = None
        self.atual = None
        self.visual_objetos = None
        self.objetos = []
        self.ocupado = False
        self.fechando = False
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.tarefas = queue.Queue()
        self.camera = None
        self.ultimo_frame = None
        self.ultimo_video = None
        self.selecionando = False
        self.semente = None
        self.referencia_rastro = None
        self.audio = Audio()
        self.status = tk.StringVar(value='Abra uma imagem ou vá à aba Câmera.')
        montar_interface(self, PainelImagem)
        raiz.protocol('WM_DELETE_WINDOW', self.fechar)
        raiz.after(40, self.atualizar)




    def disponivel(self):
        if self.ocupado:
            self.status.set('Aguarde a operação atual terminar.')
            return False
        if self.atual is None:
            messagebox.showinfo('Imagem', 'Abra uma imagem primeiro.')
            return False
        return True

    def limpar_medidas(self):
        self.objetos = []
        self.visual_objetos = None
        for item in self.tabela.get_children():
            self.tabela.delete(item)

    def carregar_array(self, img, origem):
        self.original = img.copy()
        self.atual = img.copy()
        self.limpar_medidas()
        self.canvas_original.mostrar(self.original)
        self.canvas_resultado.mostrar(self.atual)
        altura, largura = img.shape[:2]
        self.status.set(f'{origem} - {largura} x {altura} pixels. Cálculos na resolução original.')

    def abrir(self):
        if self.ocupado:
            self.status.set('Aguarde a operação atual terminar.')
            return
        caminho = filedialog.askopenfilename(title='Abrir imagem', filetypes=[('Imagens', '*.png *.jpg *.jpeg *.bmp *.tif *.tiff'), ('Todos', '*.*')])
        if not caminho:
            return
        try:
            # imdecode/fromfile evita problemas com acentos nos caminhos do Windows.
            img = cv2.imdecode(np.fromfile(caminho, dtype=np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError('O arquivo não é uma imagem válida ou está corrompido.')
            self.carregar_array(img, Path(caminho).name)
        except Exception as erro:
            messagebox.showerror('Abrir imagem', str(erro))

    def restaurar(self):
        if self.disponivel():
            self.atual = self.original.copy()
            self.limpar_medidas()
            self.canvas_resultado.mostrar(self.atual)
            self.status.set('Imagem original restaurada.')

    def executar(self, funcao, tipo):
        self.ocupado = True
        self.status.set('Processando com implementação própria... aguarde.')
        def tarefa():
            try:
                self.tarefas.put((tipo, funcao(), None))
            except Exception as erro:
                self.tarefas.put((tipo, None, str(erro)))
        self.executor.submit(tarefa)

    def parametros_imagem(self):
        op = self.op.get()
        tamanho = pdi.validar_tamanho(self.janela.get()) if op in ('Média', 'Mediana', 'Erosão', 'Dilatação', 'Abertura', 'Fechamento') else 3
        baixo, alto = (float(self.baixo.get()), float(self.alto.get())) if op == 'Canny' else (50, 150)
        if not 0 < baixo < alto:
            raise ValueError('Canny: use 0 < limiar baixo < limiar alto.')
        return op, tamanho, baixo, alto

    def aplicar(self):
        if not self.disponivel():
            return
        try:
            op, tamanho, baixo, alto = self.parametros_imagem()
        except ValueError as erro:
            messagebox.showerror('Parâmetros', str(erro))
            return
        entrada = (self.atual if self.encadear.get() else self.original).copy()
        self.executar(lambda: pdi.processar(entrada, op, tamanho, baixo, alto), 'operacao')

    def inverter(self):
        if not self.disponivel():
            return
        if self.atual.ndim != 2 or not np.all((self.atual == 0) | (self.atual == 255)):
            messagebox.showinfo('Binário', 'Aplique Otsu antes de inverter o binário.')
            return
        self.atual = pdi.negativo(self.atual)
        self.limpar_medidas()
        self.canvas_resultado.mostrar(self.atual)
        self.status.set('Binário invertido: objetos devem estar brancos.')

    def contar(self):
        if not self.disponivel():
            return
        try:
            conectividade = int(self.conexao.get())
            area = int(self.area_minima.get())
            if area < 1:
                raise ValueError('Área mínima deve ser >= 1.')
        except ValueError as erro:
            messagebox.showerror('Parâmetros', str(erro))
            return
        entrada = self.atual.copy()
        self.executar(lambda: pdi.rotular_componentes(entrada, conectividade, area), 'objetos')

    def salvar_array(self, img, titulo):
        caminho = filedialog.asksaveasfilename(title=titulo, defaultextension='.png', filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg'), ('BMP', '*.bmp')])
        if not caminho:
            return
        try:
            ok, dados = cv2.imencode(Path(caminho).suffix.lower(), img)
            if not ok:
                raise ValueError('Formato de saída não suportado.')
            dados.tofile(caminho)
            self.status.set(f'Salvo: {caminho}')
        except Exception as erro:
            messagebox.showerror('Salvar', str(erro))

    def salvar(self):
        if self.disponivel():
            self.salvar_array(self.visual_objetos if self.visual_objetos is not None else self.atual, 'Salvar resultado')

    def exportar(self):
        if not self.objetos:
            messagebox.showinfo('Medidas', 'Conte os objetos primeiro. Não há medidas para exportar.')
            return
        caminho = filedialog.asksaveasfilename(title='Exportar medidas', defaultextension='.csv', filetypes=[('CSV', '*.csv')])
        if caminho:
            try:
                with open(caminho, 'w', encoding='utf-8-sig', newline='') as arquivo:
                    escritor = csv.DictWriter(arquivo, fieldnames=tuple(self.objetos[0]), delimiter=';')
                    escritor.writeheader()
                    escritor.writerows(self.objetos)
                self.status.set(f'Medidas exportadas: {caminho}')
            except OSError as erro:
                messagebox.showerror('Exportar', str(erro))

    def histograma(self):
        if not self.disponivel():
            return
        entrada = self.atual.copy()
        def calcular():
            dados = [('Cinza', pdi.histograma(pdi.converter_para_cinza(entrada)), 'black')]
            if entrada.ndim == 3:
                dados.extend((nome, pdi.histograma(entrada[:, :, i]), cor)
                             for i, nome, cor in ((0, 'Azul', 'blue'), (1, 'Verde', 'green'), (2, 'Vermelho', 'red')))
            return dados
        self.executar(calcular, 'histograma')

    def mostrar_histograma(self, dados):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        janela = tk.Toplevel(self.raiz)
        janela.title('Histograma do resultado atual - contagem própria')
        janela.geometry('800x500')
        figura = Figure(figsize=(8, 4), dpi=100)
        eixo = figura.add_subplot(111)
        for nome, valores, cor in dados:
            eixo.plot(range(256), valores, color=cor, label=nome)
        eixo.set(xlabel='Intensidade (0 a 255)', ylabel='Quantidade de pixels', xlim=(0, 255))
        eixo.legend()
        eixo.grid(alpha=0.2)
        figura.tight_layout()
        canvas = FigureCanvasTkAgg(figura, master=janela)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        NavigationToolbar2Tk(canvas, janela).update()

    def abrir_camera(self):
        if self.camera is not None and self.camera.is_alive():
            self.status.set('A câmera já está aberta ou está sendo encerrada.')
            return
        try:
            indice = int(self.indice_camera.get())
            if indice < 0:
                raise ValueError('Índice da câmera deve ser >= 0.')
        except ValueError as erro:
            messagebox.showerror('Câmera', str(erro))
            return
        self.camera = Camera(indice)
        if not self.parametros_video():
            self.camera = None
            return
        self.ultimo_frame = None
        self.ultimo_video = None
        self.camera.start()
        self.status.set('Abrindo câmera...')

    def parametros_video(self):
        try:
            op = self.op_video.get()
            tamanho = pdi.validar_tamanho(self.janela_video.get()) if op in ('Média', 'Mediana', 'Erosão', 'Dilatação', 'Abertura', 'Fechamento') else 3
            baixo, alto = (float(self.baixo_video.get()), float(self.alto_video.get())) if op == 'Canny' else (50, 150)
            confianca = float(self.confianca.get())
            if not 0 < baixo < alto or not 0 < confianca < 1:
                raise ValueError('Use 0 < baixo < alto e confiança entre 0 e 1.')
            if self.camera:
                self.camera.configurar(operacao=op, tamanho=tamanho, baixo=baixo, alto=alto,
                                       detector=self.detector_ativo.get(), confianca=confianca)
            self.status.set('Parâmetros do vídeo atualizados.')
            return True
        except ValueError as erro:
            messagebox.showerror('Parâmetros do vídeo', str(erro))
            return False

    def parar_camera(self):
        self.cancelar_selecao()
        if self.camera:
            self.camera.encerrar()
        self.audio.parar()
        self.status.set('Encerrando câmera...')

    def capturar(self):
        if self.ultimo_frame is None:
            messagebox.showinfo('Câmera', 'Abra a câmera e aguarde um quadro.')
            return
        if self.ocupado:
            self.status.set('Aguarde o processamento da imagem terminar.')
            return
        self.carregar_array(self.ultimo_frame, 'Quadro capturado da câmera')
        self.aba.select(self.imagens)

    def salvar_video(self):
        if self.ultimo_video is not None:
            self.salvar_array(self.ultimo_video, 'Salvar quadro processado do vídeo')
        else:
            messagebox.showinfo('Vídeo', 'Abra a câmera primeiro.')

    def cancelar_selecao(self):
        self.selecionando = False
        self.semente = None
        self.referencia_rastro = None
        self.canvas_camera.delete('selecao')
        self.canvas_camera.configure(cursor='')
        if self.camera:
            self.camera.configurar(pausado=False)

    def selecionar_rastro(self):
        if self.selecionando:
            self.cancelar_selecao()
            self.status.set('Seleção cancelada.')
            return
        if not self.camera or not self.camera.is_alive() or self.ultimo_frame is None:
            messagebox.showinfo('Rastreamento', 'Abra a câmera primeiro.')
            return
        self.selecionando = True
        self.referencia_rastro = self.ultimo_frame.copy()
        self.camera.configurar(pausado=True)
        self.canvas_camera.configure(cursor='crosshair')
        self.status.set('Arraste um retângulo sobre o objeto na imagem da esquerda; o vídeo está pausado.')

    def inicio_retangulo(self, evento):
        if self.selecionando:
            self.semente = self.canvas_camera.coordenada(evento.x, evento.y)
            self.canvas_camera.delete('selecao')

    def mover_retangulo(self, evento):
        if self.selecionando and self.semente:
            ox, oy = self.canvas_camera.origem
            escala = self.canvas_camera.escala
            x, y = self.semente
            self.canvas_camera.delete('selecao')
            self.canvas_camera.create_rectangle(ox+x*escala, oy+y*escala, evento.x, evento.y,
                                                outline='cyan', width=2, tags='selecao')

    def fim_retangulo(self, evento):
        if not self.selecionando or self.semente is None:
            return
        fim = self.canvas_camera.coordenada(evento.x, evento.y)
        x1, y1 = self.semente
        x2, y2 = fim
        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2-x1)+1, abs(y2-y1)+1
        if w < 10 or h < 10:
            self.status.set('Selecione um retângulo de pelo menos 10 x 10 pixels.')
            self.semente = None
            self.canvas_camera.delete('selecao')
            return
        if self.camera:
            self.camera.comandos.put(('rastrear', (self.referencia_rastro.copy(), (x, y, w, h))))
        self.cancelar_selecao()
        self.status.set('Iniciando rastreamento CSRT...')

    def limpar_rastro(self):
        self.cancelar_selecao()
        if self.camera:
            self.camera.comandos.put(('limpar_rastro', None))
        self.status.set('Rastreamento removido.')

    def escolher_musica(self):
        caminho = filedialog.askopenfilename(title='Selecionar música', filetypes=[('Áudio', '*.mp3 *.wav *.ogg'), ('Todos', '*.*')])
        if caminho:
            try:
                self.audio.selecionar(caminho)
                self.nome_musica.set(Path(caminho).name)
                self.status.set('Música carregada. Use Testar música para conferir o som.')
            except Exception as erro:
                messagebox.showerror('Áudio', f'Não foi possível carregar a música: {erro}\nTente um arquivo WAV ou MP3 válido.')

    def testar_musica(self):
        try:
            if not self.audio.tocar():
                messagebox.showinfo('Música', 'Escolha um arquivo de música primeiro.')
        except Exception as erro:
            messagebox.showerror('Música', str(erro))

    def atualizar(self):
        if self.fechando:
            return
        try:
            tipo, resultado, erro = self.tarefas.get_nowait()
            self.ocupado = False
            if erro:
                self.status.set('Operação não concluída.')
                messagebox.showerror('Processamento', erro)
            elif tipo == 'operacao':
                self.atual, mensagem = resultado
                self.limpar_medidas()
                self.canvas_resultado.mostrar(self.atual)
                self.status.set(mensagem)
            elif tipo == 'objetos':
                _, objetos, visual = resultado
                self.limpar_medidas()
                self.objetos = objetos
                # Numeração na visualização; a imagem binária atual não é alterada.
                pil = Image.fromarray(visual[:, :, ::-1])
                desenhar = ImageDraw.Draw(pil)
                for obj in objetos:
                    desenhar.text((obj['x'], obj['y']), str(obj['id']), fill='white', stroke_width=1, stroke_fill='black')
                    self.tabela.insert('', 'end', values=(obj['id'], obj['area'], obj['perimetro'],
                                                         f"{obj['diametro']:.3f}", obj['x'], obj['y'], obj['largura'], obj['altura']))
                self.visual_objetos = np.asarray(pil)[:, :, ::-1].copy()
                self.canvas_resultado.mostrar(self.visual_objetos)
                self.status.set(f'{len(objetos)} objeto(s). Perímetro: lados expostos; diâmetro: distância máxima entre centros de pixels.')
            elif tipo == 'histograma':
                self.mostrar_histograma(resultado)
                self.status.set('Histograma calculado pelo algoritmo da Lista 1.')
        except queue.Empty:
            pass
        if self.camera:
            if not self.selecionando:
                try:
                    self.ultimo_frame, self.ultimo_video = self.camera.frames.get_nowait()
                    self.canvas_camera.mostrar(self.ultimo_frame)
                    self.canvas_video.mostrar(self.ultimo_video)
                except queue.Empty:
                    pass
            while True:
                try:
                    tipo, mensagem = self.camera.eventos.get_nowait()
                except queue.Empty:
                    break
                self.status.set(mensagem)
                if tipo in ('erro', 'erro_detector'):
                    if tipo == 'erro_detector':
                        self.detector_ativo.set(False)
                        self.camera.configurar(detector=False)
                        mensagem += '\nVerifique a instalação e o acesso à internet para baixar o modelo. Depois reabra a câmera.'
                    messagebox.showerror('Vídeo', mensagem)
                elif tipo == 'celular':
                    # Não executa eventos antigos ao encerrar a câmera.
                    if not self.camera.parar.is_set() and self.detector_ativo.get():
                        try:
                            tocou = self.audio.tocar()
                            self.status.set('Celular reconhecido: música acionada.' if tocou else 'Celular reconhecido. Escolha uma música para habilitar o som.')
                        except Exception as erro:
                            messagebox.showerror('Música', str(erro))
                elif tipo == 'camera_fechada':
                    self.cancelar_selecao()
                    self.audio.parar()
                    break
            if not self.camera.is_alive():
                self.camera = None
        self.raiz.after(40, self.atualizar)

    def fechar(self):
        self.fechando = True
        if self.camera:
            self.camera.encerrar()
        self.audio.encerrar()
        self.executor.shutdown(wait=False, cancel_futures=True)
        self.raiz.destroy()


if __name__ == '__main__':
    raiz = tk.Tk()
    Aplicacao(raiz)
    raiz.mainloop()
