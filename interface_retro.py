"""Interface ImageLab 2000. Apenas apresentação; algoritmos ficam nas listas.

Tkinter/ttk, ícones pixelados desenhados com Pillow e controles clássicos.
Nenhuma biblioteca ou serviço novo é necessário para o tema.
"""
import tkinter as tk
from tkinter import ttk, font as tkfont
from datetime import datetime
from PIL import Image, ImageDraw, ImageTk
import processamento as pdi

FUNDO = '#d4d0c8'
CLARO = '#f5f3ed'
AZUL = '#063e88'
TEXTO = '#222d38'
CINZA = '#66717c'
VERDE = '#167968'
FONTE = 'Tahoma'
MONO = 'Courier New'


def icone_pixel(tipo, tamanho=32):
    img = Image.new('RGBA', (16, 16))
    d = ImageDraw.Draw(img)
    if tipo == 'monitor':
        d.rectangle((1, 1, 14, 11), fill='#b6b9ba', outline='#25292d')
        d.line((2, 2, 13, 2), fill='white')
        d.rectangle((3, 3, 12, 8), fill='#083e79')
        d.line((4, 7, 6, 7, 7, 4, 9, 6, 11, 6), fill='#64ff79', width=1)
        d.rectangle((6, 12, 9, 13), fill='#6b757e')
        d.rectangle((3, 14, 12, 15), fill='#9ea4ab', outline='#25292d')
    elif tipo == 'folder':
        d.rectangle((1, 4, 7, 6), fill='#e9b746', outline='#776329')
        d.rectangle((1, 6, 14, 13), fill='#f8d674', outline='#776329')
        d.line((2, 7, 13, 7), fill='#fff5bd')
        d.polygon([(3, 9), (15, 9), (13, 14), (1, 14)], fill='#e9bb56', outline='#776329')
    elif tipo == 'save':
        d.rectangle((2, 1, 13, 14), fill='#52679d', outline='#26354e')
        d.rectangle((4, 2, 11, 6), fill='#d3d9de')
        d.rectangle((9, 2, 10, 5), fill='#748592')
        d.rectangle((4, 9, 11, 13), fill='#fffef3')
        d.line((5, 10, 10, 10), fill='#99a0a8')
    elif tipo == 'camera':
        d.rectangle((5, 3, 10, 5), fill='#74848d', outline='#273943')
        d.rectangle((1, 5, 14, 13), fill='#bec7cc', outline='#273943')
        d.line((2, 6, 13, 6), fill='white')
        d.ellipse((5, 7, 11, 13), fill='#174571', outline='#24313b')
        d.rectangle((2, 8, 3, 9), fill='#7cedab')
    elif tipo == 'phone':
        d.rectangle((4, 1, 11, 14), fill='#a7adb8', outline='#2b3448')
        d.rectangle((5, 3, 10, 8), fill='#8bc2e5')
        d.line((6, 4, 9, 4), fill='white')
        for y in (10, 12):
            for x in (5, 7, 9):
                d.rectangle((x, y, x+1, y), fill='#3c506d')
    elif tipo == 'chart':
        d.rectangle((1, 1, 14, 14), fill='#fffdf5', outline='#6d7b8a')
        d.rectangle((3, 9, 5, 12), fill='#368bce')
        d.rectangle((7, 6, 9, 12), fill='#519b74')
        d.rectangle((11, 3, 12, 12), fill='#db9760')
    elif tipo == 'music':
        d.rectangle((6, 3, 13, 4), fill='#344881')
        d.line((6, 4, 6, 11), fill='#344881', width=2)
        d.line((13, 4, 13, 10), fill='#344881', width=2)
        d.ellipse((2, 10, 6, 13), fill='#344881')
        d.ellipse((9, 9, 13, 12), fill='#344881')
    else:
        d.polygon([(3, 1), (10, 1), (13, 4), (13, 14), (3, 14)], fill='#fffdf7', outline='#68768a')
        d.line((10, 1, 10, 4, 13, 4), fill='#68768a')
        d.rectangle((5, 6, 11, 11), fill='#bed7e9')
        d.polygon([(5, 11), (7, 8), (9, 10), (10, 9), (11, 11)], fill='#388b69')
    return ImageTk.PhotoImage(img.resize((tamanho, tamanho), Image.Resampling.NEAREST))


class Dica:
    def __init__(self, widget, texto):
        self.widget, self.texto = widget, texto
        self.janela = None
        self.timer = None
        widget.bind('<Enter>', self.agendar, add='+')
        widget.bind('<Leave>', self.fechar, add='+')
        widget.bind('<ButtonPress>', self.fechar, add='+')

    def agendar(self, evento=None):
        self.timer = self.widget.after(650, self.mostrar)

    def mostrar(self):
        if not self.widget.winfo_exists():
            return
        self.janela = tk.Toplevel(self.widget)
        self.janela.overrideredirect(True)
        x = min(self.widget.winfo_rootx()+12, self.widget.winfo_screenwidth()-310)
        y = self.widget.winfo_rooty()+self.widget.winfo_height()+6
        self.janela.geometry(f'+{x}+{y}')
        tk.Label(self.janela, text=self.texto, bg='#fffbd7', fg=TEXTO, relief='solid',
                 bd=1, font=(FONTE, 9), padx=8, pady=5, wraplength=290).pack()

    def fechar(self, evento=None):
        if self.timer:
            self.widget.after_cancel(self.timer)
            self.timer = None
        if self.janela:
            self.janela.destroy()
            self.janela = None


def configurar_tema(raiz):
    global FONTE, MONO
    familias = set(tkfont.families(raiz))
    FONTE = 'Tahoma' if 'Tahoma' in familias else 'DejaVu Sans'
    MONO = 'Consolas' if 'Consolas' in familias else 'DejaVu Sans Mono'
    raiz.configure(bg='#236b72')
    raiz.option_add('*Font', (FONTE, 10))
    raiz.option_add('*Menu.background', FUNDO)
    raiz.option_add('*Menu.foreground', TEXTO)
    raiz.option_add('*Menu.activeBackground', AZUL)
    raiz.option_add('*Menu.activeForeground', 'white')
    estilo = ttk.Style(raiz)
    estilo.theme_use('clam')
    estilo.configure('.', background=FUNDO, foreground=TEXTO, font=(FONTE, 10))
    estilo.configure('TFrame', background=FUNDO)
    estilo.configure('TLabel', background=FUNDO)
    estilo.configure('TButton', padding=(8, 6), relief='raised', borderwidth=2,
                     background='#e8e5de', lightcolor='white', darkcolor='#7e8186')
    estilo.map('TButton', background=[('pressed', '#c3cbd4'), ('active', '#f7f5ee')],
               foreground=[('disabled', '#898e91')])
    estilo.configure('Primary.TButton', background=AZUL, foreground='white', padding=(8, 8))
    estilo.map('Primary.TButton', background=[('pressed', '#032755'), ('active', '#155ba4')],
               foreground=[('disabled', '#b8c4d0'), ('!disabled', 'white')])
    estilo.configure('TEntry', fieldbackground='white', padding=4)
    estilo.configure('TCombobox', fieldbackground='white', padding=4, arrowsize=14)
    estilo.map('TCombobox', fieldbackground=[('readonly', 'white')], selectbackground=[('readonly', 'white')],
               selectforeground=[('readonly', TEXTO)])
    estilo.configure('TSpinbox', fieldbackground='white', padding=4, arrowsize=12)
    estilo.configure('TCheckbutton', padding=3)
    estilo.configure('TNotebook', background=FUNDO, borderwidth=0, tabmargins=(8, 6, 0, 0))
    estilo.configure('TNotebook.Tab', padding=(18, 9), font=(FONTE, 10, 'bold'), background='#bfc5c9')
    estilo.map('TNotebook.Tab', background=[('selected', CLARO)], foreground=[('selected', AZUL)])
    estilo.configure('Treeview', background='white', fieldbackground='white', rowheight=26,
                     borderwidth=0, font=(FONTE, 9))
    estilo.configure('Treeview.Heading', background='#e5e8e9', font=(FONTE, 9, 'bold'), padding=5)
    estilo.map('Treeview', background=[('selected', AZUL)], foreground=[('selected', 'white')])
    estilo.configure('Horizontal.TProgressbar', troughcolor='#c3c7c9', background=VERDE, borderwidth=1)
    return estilo


def botao(app, mestre, texto, comando, icone=None, principal=False, dica=None):
    opcoes = dict(text=texto, command=comando, style='Primary.TButton' if principal else 'TButton')
    if icone:
        opcoes.update(image=app.icones[icone], compound='left')
    b = ttk.Button(mestre, **opcoes)
    if dica:
        Dica(b, dica)
    return b


def lateral(mestre):
    borda = tk.Frame(mestre, bg=FUNDO, width=276, bd=2, relief='groove')
    borda.pack(side='left', fill='y', padx=(0, 10))
    borda.pack_propagate(False)
    canvas = tk.Canvas(borda, bg=FUNDO, width=255, highlightthickness=0)
    scroll = ttk.Scrollbar(borda, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    corpo = ttk.Frame(canvas, padding=10)
    janela = canvas.create_window((0, 0), window=corpo, anchor='nw')
    corpo.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind('<Configure>', lambda e: canvas.itemconfigure(janela, width=e.width))
    def rolar(e):
        passo = -1 if getattr(e, 'num', None) == 4 else 1 if getattr(e, 'num', None) == 5 else -int(e.delta/120)
        canvas.yview_scroll(passo, 'units')
        return 'break'
    def vincular():
        def percorrer(w):
            if w.winfo_class() not in ('TEntry', 'TCombobox', 'TSpinbox'):
                w.bind('<MouseWheel>', rolar, add='+')
                w.bind('<Button-4>', rolar, add='+')
                w.bind('<Button-5>', rolar, add='+')
            for filho in w.winfo_children():
                percorrer(filho)
        percorrer(corpo)
    corpo.after_idle(vincular)
    return corpo


def secao(mestre, numero, titulo):
    caixa = ttk.Frame(mestre)
    caixa.pack(fill='x', pady=(0, 14))
    cab = tk.Frame(caixa, bg='#bcc6cc')
    cab.pack(fill='x', pady=(0, 8))
    tk.Label(cab, text=numero, bg=AZUL, fg='white', font=(FONTE, 9, 'bold'), padx=6, pady=4).pack(side='left')
    tk.Label(cab, text=titulo, bg='#bcc6cc', fg='#29404f', font=(FONTE, 9, 'bold'), padx=7).pack(side='left')
    return caixa


def legenda(mestre, texto, largura=220):
    l = tk.Label(mestre, text=texto, bg=FUNDO, fg=CINZA, font=(FONTE, 9),
                 justify='left', anchor='w', wraplength=largura)
    l.pack(fill='x', pady=(5, 0))
    return l


def parametros(app, mestre, video=False):
    op = tk.StringVar(value='Original' if video else 'Cinza')
    janela, baixo, alto = tk.StringVar(value='3'), tk.StringVar(value='50'), tk.StringVar(value='150')
    if video:
        app.op_video, app.janela_video, app.baixo_video, app.alto_video = op, janela, baixo, alto
    else:
        app.op, app.janela, app.baixo, app.alto = op, janela, baixo, alto
    ttk.Label(mestre, text='Operação ao vivo' if video else 'Operação').pack(anchor='w')
    combo = ttk.Combobox(mestre, textvariable=op, values=pdi.OPERACOES, state='readonly')
    combo.pack(fill='x', pady=(3, 8))
    grade = ttk.Frame(mestre)
    grade.pack(fill='x')
    ttk.Label(grade, text='Janela').grid(row=0, column=0, sticky='w')
    ttk.Label(grade, text='Canny baixo / alto').grid(row=0, column=1, columnspan=2, sticky='w', padx=(9, 0))
    kernel = ttk.Spinbox(grade, textvariable=janela, values=tuple(range(1, 32, 2)), width=4)
    e1, e2 = ttk.Entry(grade, textvariable=baixo, width=5), ttk.Entry(grade, textvariable=alto, width=5)
    kernel.grid(row=1, column=0, sticky='ew', pady=4)
    e1.grid(row=1, column=1, padx=(9, 3), pady=4)
    e2.grid(row=1, column=2, pady=4)
    # A escala usa índices para permitir somente janelas ímpares de 1 a 31.
    intensidade = ttk.Frame(mestre)
    intensidade.pack(fill='x', pady=(8, 0))
    valor = tk.StringVar(value='Intensidade: 3 × 3')
    ttk.Label(intensidade, textvariable=valor).pack(anchor='w')
    posicao = tk.DoubleVar(value=1)
    sincronizando = False
    pendente = None

    def mover(numero):
        nonlocal sincronizando
        if sincronizando:
            return
        tamanho = 2 * max(0, min(15, int(float(numero) + 0.5))) + 1
        janela.set(str(tamanho))

    barra = ttk.Scale(intensidade, from_=0, to=15, orient='horizontal',
                      variable=posicao, command=mover)
    barra.pack(fill='x', pady=4)
    extremos = ttk.Frame(intensidade)
    extremos.pack(fill='x')
    ttk.Label(extremos, text='Suave · 1').pack(side='left')
    ttk.Label(extremos, text='31 · Forte').pack(side='right')

    def sincronizar(*args):
        nonlocal sincronizando
        try:
            tamanho = int(janela.get())
        except ValueError:
            return
        if tamanho not in range(1, 32, 2):
            return
        sincronizando = True
        posicao.set((tamanho - 1) / 2)
        valor.set(f'Intensidade: {tamanho} × {tamanho}')
        sincronizando = False
        if video and getattr(app, 'camera', None):
            app.parametros_video()

    def aplicar_ajuste():
        nonlocal pendente
        pendente = None
        if video or getattr(app, 'original', None) is None:
            return
        if app.ocupado:
            pendente = mestre.after(150, aplicar_ajuste)
            return
        app.aplicar()

    def soltar(evento=None):
        nonlocal pendente
        if video:
            if getattr(app, 'camera', None):
                app.parametros_video()
        else:
            if pendente is not None:
                mestre.after_cancel(pendente)
            pendente = mestre.after(120, aplicar_ajuste)

    barra.bind('<ButtonRelease-1>', soltar)
    barra.bind('<KeyRelease>', soltar)
    janela.trace_add('write', sincronizar)
    def habilitar(*args):
        barra.configure(state='normal' if op.get() in ('Média', 'Mediana', 'Erosão', 'Dilatação', 'Abertura', 'Fechamento') else 'disabled')
        kernel.configure(state='normal' if op.get() in ('Média', 'Mediana', 'Erosão', 'Dilatação', 'Abertura', 'Fechamento') else 'disabled')
        for e in (e1, e2):
            e.configure(state='normal' if op.get() == 'Canny' else 'disabled')
    op.trace_add('write', habilitar)
    habilitar()
    legenda(mestre, 'Arraste para ajustar. Na imagem, solte para aplicar; no vídeo, o ajuste é ao vivo. Janelas maiores aumentam a ação do filtro, mas podem ser mais lentas.')


def janela_preview(app, mestre, classe, titulo, icone, mensagem, sub):
    quadro = tk.Frame(mestre, bg=FUNDO, bd=2, relief='raised')
    cab = tk.Frame(quadro, bg='#e8e9e5', height=34)
    cab.pack(fill='x')
    tk.Label(cab, image=app.icones[icone], bg='#e8e9e5').pack(side='left', padx=(8, 4), pady=5)
    tk.Label(cab, text=titulo, bg='#e8e9e5', fg=TEXTO, font=(FONTE, 10, 'bold')).pack(side='left')
    tk.Label(cab, text='PREVIEW', bg='#e8e9e5', fg='#78848c', font=(MONO, 8)).pack(side='right', padx=8)
    canvas = classe(quadro)
    canvas.mensagem_vazia, canvas.subtitulo_vazio = mensagem, sub
    canvas.icone_vazio = app.icones_grandes[icone]
    canvas.pack(fill='both', expand=True, padx=5, pady=(0, 5))
    meta = tk.StringVar(value='Aguardando entrada')
    tk.Label(quadro, textvariable=meta, bg=CLARO, fg=CINZA, anchor='w', padx=8,
             pady=5, font=(MONO, 9)).pack(fill='x')
    app.metadados.append((canvas, meta))
    return quadro, canvas


def montar_imagens(app, classe):
    corpo = ttk.Frame(app.imagens, padding=10)
    corpo.pack(fill='both', expand=True)
    lado = lateral(corpo)
    arquivo = secao(lado, '01', 'ARQUIVO')
    botao(app, arquivo, 'Abrir imagem', app.abrir, 'folder', dica='Abrir uma foto do computador · Ctrl+O').pack(fill='x')
    fila = ttk.Frame(arquivo)
    fila.pack(fill='x', pady=(6, 0))
    botao(app, fila, 'Restaurar', app.restaurar, dica='Restaurar a imagem original · Ctrl+R').pack(side='left', fill='x', expand=True, padx=(0, 3))
    botao(app, fila, 'Salvar', app.salvar, 'save', dica='Salvar o resultado · Ctrl+S').pack(side='left', fill='x', expand=True)
    botao(app, arquivo, 'Histograma', app.histograma, 'chart').pack(fill='x', pady=(6, 0))
    operacao = secao(lado, '02', 'PROCESSAMENTO')
    parametros(app, operacao)
    app.encadear = tk.BooleanVar(value=True)
    ttk.Checkbutton(operacao, text='Aplicar sobre resultado atual', variable=app.encadear).pack(anchor='w', pady=6)
    app.botao_aplicar = botao(app, operacao, 'Aplicar operação', app.aplicar, principal=True)
    app.botao_aplicar.pack(fill='x')
    objetos = secao(lado, '03', 'OBJETOS & MEDIDAS')
    grade = ttk.Frame(objetos)
    grade.pack(fill='x')
    app.conexao, app.area_minima = tk.StringVar(value='8'), tk.StringVar(value='1')
    ttk.Label(grade, text='Conectividade').grid(row=0, column=0, sticky='w')
    ttk.Label(grade, text='Área mínima (px)').grid(row=0, column=1, sticky='w', padx=10)
    ttk.Combobox(grade, textvariable=app.conexao, values=('4', '8'), state='readonly', width=6).grid(row=1, column=0, sticky='w', pady=5)
    ttk.Entry(grade, textvariable=app.area_minima, width=8).grid(row=1, column=1, padx=10, pady=5)
    botao(app, objetos, 'Inverter binário', app.inverter).pack(fill='x', pady=(2, 6))
    app.botao_contar = botao(app, objetos, 'Contar e medir objetos', app.contar, 'chart')
    app.botao_contar.pack(fill='x')
    botao(app, objetos, 'Exportar medidas CSV', app.exportar, 'save').pack(fill='x', pady=(6, 0))
    legenda(objetos, 'Use Otsu primeiro. Objetos brancos, fundo preto; inverta se necessário.')
    area = ttk.Frame(corpo)
    area.pack(side='left', fill='both', expand=True)
    intro = ttk.Frame(area)
    intro.pack(fill='x', pady=(0, 9))
    ttk.Label(intro, text='Seu laboratório de imagens', font=(FONTE, 15, 'bold'), foreground=AZUL).pack(anchor='w')
    ttk.Label(intro, text='Abra, transforme e compare. A imagem original fica sempre à esquerda.', foreground=CINZA).pack(anchor='w', pady=(3, 0))
    split = ttk.Panedwindow(area, orient='vertical')
    split.pack(fill='both', expand=True)
    previews = ttk.Frame(split)
    previews.columnconfigure((0, 1), weight=1, uniform='preview')
    previews.rowconfigure(0, weight=1)
    f, app.canvas_original = janela_preview(app, previews, classe, 'Original', 'file', 'Sua imagem começa aqui', 'Clique para abrir uma imagem')
    f.grid(row=0, column=0, sticky='nsew', padx=(0, 4))
    app.canvas_original.bind('<Button-1>', lambda e: app.abrir() if app.original is None else None)
    f, app.canvas_resultado = janela_preview(app, previews, classe, 'Resultado', 'monitor', 'Pronto para transformar', 'Escolha uma operação e clique em Aplicar')
    f.grid(row=0, column=1, sticky='nsew', padx=(4, 0))
    split.add(previews, weight=5)
    tabela = tk.Frame(split, bg=FUNDO, bd=2, relief='groove')
    cab = tk.Frame(tabela, bg='#e7e9e7')
    cab.pack(fill='x')
    tk.Label(cab, text='  OBJETOS DETECTADOS', bg='#e7e9e7', fg=AZUL, font=(FONTE, 9, 'bold'), pady=7).pack(side='left')
    app.contagem_texto = tk.StringVar(value='0 objetos')
    tk.Label(cab, textvariable=app.contagem_texto, bg='#e7e9e7', fg=CINZA, padx=10).pack(side='right')
    grade = ttk.Frame(tabela)
    grade.pack(fill='both', expand=True)
    colunas = ('id', 'area', 'perimetro', 'diametro', 'x', 'y', 'largura', 'altura')
    nomes = ('Objeto', 'Área (px)', 'Perímetro (px)', 'Diâmetro (px)', 'X', 'Y', 'Largura', 'Altura')
    app.tabela = ttk.Treeview(grade, columns=colunas, show='headings', height=4)
    for coluna, nome in zip(colunas, nomes):
        app.tabela.heading(coluna, text=nome)
        app.tabela.column(coluna, width=90 if coluna not in ('x', 'y', 'id') else 55, minwidth=45, anchor='center')
    vertical = ttk.Scrollbar(grade, orient='vertical', command=app.tabela.yview)
    horizontal = ttk.Scrollbar(grade, orient='horizontal', command=app.tabela.xview)
    app.tabela.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
    app.tabela.grid(row=0, column=0, sticky='nsew')
    vertical.grid(row=0, column=1, sticky='ns')
    horizontal.grid(row=1, column=0, sticky='ew')
    grade.columnconfigure(0, weight=1)
    grade.rowconfigure(0, weight=1)
    split.add(tabela, weight=1)


def montar_video(app, classe):
    corpo = ttk.Frame(app.videos, padding=10)
    corpo.pack(fill='both', expand=True)
    lado = lateral(corpo)
    entrada = secao(lado, '01', 'CÂMERA')
    linha = ttk.Frame(entrada)
    linha.pack(fill='x', pady=(0, 5))
    app.indice_camera = tk.StringVar(value='0')
    ttk.Label(linha, text='Índice da câmera').pack(side='left')
    indice = ttk.Spinbox(linha, textvariable=app.indice_camera, from_=0, to=10, width=4)
    indice.pack(side='right')
    Dica(indice, '0 costuma ser a câmera principal. Tente 1 se houver outra webcam.')
    linha = ttk.Frame(entrada)
    linha.pack(fill='x')
    botao(app, linha, 'Abrir câmera', app.abrir_camera, 'camera').pack(side='left', fill='x', expand=True, padx=(0, 4))
    botao(app, linha, 'Parar', app.parar_camera).pack(side='left')
    botao(app, entrada, 'Capturar para Imagens', app.capturar, 'file').pack(fill='x', pady=(6, 0))
    botao(app, entrada, 'Salvar quadro do vídeo', app.salvar_video, 'save').pack(fill='x', pady=(6, 0))
    op = secao(lado, '02', 'VÍDEO AO VIVO')
    parametros(app, op, video=True)
    botao(app, op, 'Atualizar parâmetros', app.parametros_video, principal=True).pack(fill='x', pady=(7, 0))
    rastreio = secao(lado, '03', 'RASTREAMENTO')
    app.botao_rastro = botao(app, rastreio, 'Selecionar objeto', app.selecionar_rastro)
    app.botao_rastro.pack(fill='x')
    botao(app, rastreio, 'Limpar rastreamento', app.limpar_rastro).pack(fill='x', pady=(6, 0))
    legenda(rastreio, 'Arraste sobre o objeto na prévia original. A caixa azul acompanha o alvo.')
    detector = secao(lado, '04', 'CELULAR & MÚSICA')
    app.detector_ativo = tk.BooleanVar(value=False)
    ttk.Checkbutton(detector, text='Reconhecer celular (YOLO)', variable=app.detector_ativo,
                    command=app.parametros_video).pack(anchor='w')
    linha = ttk.Frame(detector)
    linha.pack(fill='x', pady=5)
    app.confianca = tk.StringVar(value='0.40')
    ttk.Label(linha, text='Confiança mínima').pack(side='left')
    ttk.Spinbox(linha, textvariable=app.confianca, from_=0.05, to=0.95, increment=0.05,
                width=5, command=app.parametros_video).pack(side='right')
    botao(app, detector, 'Escolher música', app.escolher_musica, 'music').pack(fill='x', pady=(3, 0))
    app.nome_musica = tk.StringVar(value='Nenhuma música selecionada')
    tk.Label(detector, textvariable=app.nome_musica, bg=FUNDO, fg=CINZA, wraplength=215,
             justify='left', anchor='w', font=(FONTE, 9)).pack(fill='x', pady=6)
    linha = ttk.Frame(detector)
    linha.pack(fill='x')
    botao(app, linha, 'Testar música', app.testar_musica).pack(side='left', fill='x', expand=True, padx=(0, 4))
    botao(app, linha, 'Parar', app.audio.parar).pack(side='left')
    legenda(detector, 'Caixa verde: celular reconhecido. A música toca uma vez por aparição confirmada.')
    area = ttk.Frame(corpo)
    area.pack(side='left', fill='both', expand=True)
    ttk.Label(area, text='Um olhar em tempo real', font=(FONTE, 15, 'bold'), foreground=AZUL).pack(anchor='w')
    ttk.Label(area, text='Rastreie um objeto, experimente filtros e reconheça celulares.', foreground=CINZA).pack(anchor='w', pady=(3, 10))
    previews = ttk.Frame(area)
    previews.pack(fill='both', expand=True)
    previews.columnconfigure((0, 1), weight=1, uniform='preview')
    previews.rowconfigure(0, weight=1)
    f, app.canvas_camera = janela_preview(app, previews, classe, 'Câmera original', 'camera', 'Sua câmera está em espera', 'Clique em Abrir câmera para começar')
    f.grid(row=0, column=0, sticky='nsew', padx=(0, 4))
    f, app.canvas_video = janela_preview(app, previews, classe, 'Vídeo processado', 'phone', 'Imagem ao vivo, novas possibilidades', 'Filtros, rastreamento e reconhecimento')
    f.grid(row=0, column=1, sticky='nsew', padx=(4, 0))
    app.canvas_camera.bind('<ButtonPress-1>', app.inicio_retangulo)
    app.canvas_camera.bind('<B1-Motion>', app.mover_retangulo)
    app.canvas_camera.bind('<ButtonRelease-1>', app.fim_retangulo)
    faixa = tk.Frame(area, bg=CLARO, bd=1, relief='sunken')
    faixa.pack(fill='x', pady=(9, 0))
    tk.Label(faixa, text='■  Azul: rastreamento', fg=AZUL, bg=CLARO, padx=10, pady=7).pack(side='left')
    tk.Label(faixa, text='■  Verde: celular', fg=VERDE, bg=CLARO, padx=10).pack(side='left')


def mostrar_ajuda(app):
    if getattr(app, 'janela_ajuda', None) and app.janela_ajuda.winfo_exists():
        app.janela_ajuda.lift()
        return
    janela = tk.Toplevel(app.raiz)
    app.janela_ajuda = janela
    janela.title('ImageLab 2000 · Guia rápido')
    janela.geometry('590x530')
    janela.configure(bg=FUNDO)
    tk.Label(janela, text='Bem-vindo ao ImageLab 2000', font=(FONTE, 16, 'bold'),
             bg=AZUL, fg='white', padx=15, pady=15, anchor='w').pack(fill='x')
    conteudo = ttk.Frame(janela)
    conteudo.pack(fill='both', expand=True, padx=12, pady=12)
    texto = tk.Text(conteudo, bg=CLARO, fg=TEXTO, wrap='word', font=(FONTE, 11),
                    padx=20, pady=18, relief='sunken', bd=2)
    scroll = ttk.Scrollbar(conteudo, orient='vertical', command=texto.yview)
    texto.configure(yscrollcommand=scroll.set)
    scroll.pack(side='right', fill='y')
    texto.pack(side='left', fill='both', expand=True)
    texto.insert('1.0', 'IMAGENS\nAbra uma foto. Escolha uma operação e clique em Aplicar operação.\n'
                 'Marque “Aplicar sobre resultado atual” para encadear operações.\n\n'
                 'OBJETOS\nAplique Otsu. Os objetos devem estar brancos sobre fundo preto.\n'
                 'Se necessário, use Inverter binário. Clique em Contar e medir objetos.\n'
                 'A tabela pode ser exportada como CSV.\n\n'
                 'CÂMERA\nO índice 0 costuma ser a webcam principal. Abra a câmera, escolha\n'
                 'uma operação e clique em Atualizar parâmetros.\n\n'
                 'RASTREAMENTO\nClique em Selecionar objeto e arraste um retângulo na prévia esquerda.\n'
                 'O vídeo pausa durante a seleção. Se perder o alvo, selecione novamente.\n\n'
                 'CELULAR E MÚSICA\nEscolha e teste uma música. Ative Reconhecer celular e mostre um\n'
                 'celular à câmera. A confirmação em duas detecções aciona o áudio.\n\n'
                 'ATALHOS\nCtrl+O: abrir imagem · Ctrl+S: salvar resultado\nCtrl+R: restaurar original · F1: abrir este guia\n\n'
                 'Os algoritmos das listas continuam nos arquivos listas/.')
    texto.configure(state='disabled')
    botao(app, janela, 'Entendi', janela.destroy, principal=True).pack(pady=(0, 12))


def desenhar_fundo(canvas):
    """Prévia quadriculada e estado vazio; nunca altera os pixels da entrada."""
    w, h = max(1, canvas.winfo_width()), max(1, canvas.winfo_height())
    assinatura = (w, h, canvas.img is None)
    if getattr(canvas, '_fundo_assinatura', None) == assinatura:
        return
    canvas._fundo_assinatura = assinatura
    canvas.delete('fundo')
    canvas.delete('vazio')
    for y in range(0, h, 20):
        for x in range(0, w, 20):
            cor = '#f5f4ef' if (x//20+y//20) % 2 == 0 else '#edede7'
            canvas.create_rectangle(x, y, x+20, y+20, fill=cor, outline='', tags='fundo')
    canvas.tag_lower('fundo')
    if canvas.img is None:
        if getattr(canvas, 'icone_vazio', None):
            canvas.create_image(w/2, h/2-42, image=canvas.icone_vazio, tags='vazio')
        canvas.create_text(w/2, h/2+4, text=getattr(canvas, 'mensagem_vazia', 'Aguardando imagem'),
                           fill='#526477', font=(FONTE, 11, 'bold'), width=max(80, w-35), tags='vazio')
        canvas.create_text(w/2, h/2+39, text=getattr(canvas, 'subtitulo_vazio', ''),
                           fill='#7b8791', font=(FONTE, 9), width=max(80, w-35), tags='vazio')


def montar_interface(app, classe):
    raiz = app.raiz
    configurar_tema(raiz)
    app.icones = {tipo: icone_pixel(tipo, 20) for tipo in ('monitor', 'folder', 'save', 'camera', 'phone', 'chart', 'music', 'file')}
    app.icones_grandes = {tipo: icone_pixel(tipo, 64) for tipo in ('monitor', 'camera', 'phone', 'file')}
    raiz.iconphoto(True, app.icones_grandes['monitor'])
    app.metadados = []
    moldura = tk.Frame(raiz, bg=FUNDO, bd=3, relief='raised')
    moldura.pack(fill='both', expand=True, padx=12, pady=12)
    titulo = tk.Canvas(moldura, height=43, highlightthickness=0, bg=AZUL)
    titulo.pack(fill='x')
    def pintar(e):
        titulo.delete('all')
        for x in range(0, e.width, 4):
            t = x/max(1, e.width)
            cor = '#%02x%02x%02x' % (int(6+28*t), int(48+74*t), int(116+51*t))
            titulo.create_rectangle(x, 0, x+4, 43, fill=cor, outline='')
        titulo.create_image(22, 21, image=app.icones['monitor'])
        titulo.create_text(43, 13, text='ImageLab 2000', anchor='w', fill='white', font=(FONTE, 13, 'bold'))
        titulo.create_text(43, 31, text='Estúdio de imagens & vídeo', anchor='w', fill='#cfe0f5', font=(FONTE, 9))
        titulo.create_text(e.width-12, 21, text='PEDRO TRINDADE  /  PDI', anchor='e', fill='#e0edf8', font=(MONO, 9))
    titulo.bind('<Configure>', pintar)
    menu = tk.Frame(moldura, bg=FUNDO)
    menu.pack(fill='x')
    for nome, itens in [('Arquivo', [('Abrir imagem', app.abrir), ('Salvar resultado', app.salvar), ('Restaurar original', app.restaurar), ('Sair', app.fechar)]),
                        ('Exibir', [('Imagens', lambda: app.aba.select(app.imagens)), ('Câmera', lambda: app.aba.select(app.videos))]),
                        ('Ajuda', [('Guia rápido', lambda: mostrar_ajuda(app))])]:
        b = tk.Menubutton(menu, text=nome, bg=FUNDO, fg=TEXTO, activebackground='#eeeae2', relief='flat', padx=11, pady=5)
        m = tk.Menu(b, tearoff=False)
        for texto, comando in itens:
            m.add_command(label=texto, command=comando)
        b.configure(menu=m)
        b.pack(side='left')
    tk.Label(menu, text='ESTÚDIO DE IMAGENS', bg=FUNDO, fg=CINZA, font=(MONO, 8)).pack(side='right', padx=10)
    app.aba = ttk.Notebook(moldura)
    app.aba.pack(fill='both', expand=True, padx=4)
    app.imagens, app.videos = ttk.Frame(app.aba), ttk.Frame(app.aba)
    app.aba.add(app.imagens, text='  Imagens', image=app.icones['file'], compound='left')
    app.aba.add(app.videos, text='  Câmera', image=app.icones['camera'], compound='left')
    montar_imagens(app, classe)
    montar_video(app, classe)
    rodape = tk.Frame(moldura, bg=FUNDO, bd=1, relief='sunken')
    rodape.pack(side='bottom', fill='x', padx=5, pady=5, before=app.aba)
    botao(app, rodape, 'Ajuda', lambda: mostrar_ajuda(app), 'monitor').pack(side='left', padx=4, pady=4)
    app.estado_ui = tk.StringVar(value='PRONTO')
    tk.Label(rodape, textvariable=app.estado_ui, bg='#f1f1e9', fg=VERDE, font=(MONO, 9, 'bold'),
             relief='sunken', bd=1, padx=8, pady=8).pack(side='left', padx=4)
    mensagem = tk.Label(rodape, textvariable=app.status, bg=FUNDO, fg=TEXTO, anchor='w',
                        justify='left', padx=8, font=(FONTE, 9))
    mensagem.pack(side='left', fill='x', expand=True)
    mensagem.bind('<Configure>', lambda e: mensagem.configure(wraplength=max(100, e.width-20)))
    app.relogio = tk.StringVar()
    tk.Label(rodape, textvariable=app.relogio, bg=CLARO, fg=CINZA, relief='sunken', bd=1,
             font=(MONO, 9), padx=9, pady=8).pack(side='right', padx=4)
    app.progresso = ttk.Progressbar(rodape, mode='indeterminate', length=60)
    app.progresso.pack(side='right', padx=4)
    app._progresso_ativo = False
    def monitorar():
        if app.fechando:
            return
        ocupado = app.ocupado
        if ocupado != app._progresso_ativo:
            if ocupado:
                app.progresso.start(12)
            else:
                app.progresso.stop()
                app.progresso.configure(value=0)
            app._progresso_ativo = ocupado
        app.estado_ui.set('PROCESSANDO' if ocupado else 'CÂMERA ON' if app.camera and app.camera.is_alive() else 'PRONTO')
        app.botao_aplicar.configure(state='disabled' if ocupado else 'normal')
        app.botao_contar.configure(state='disabled' if ocupado else 'normal')
        app.botao_rastro.configure(text='Cancelar seleção' if app.selecionando else 'Selecionar objeto')
        app.contagem_texto.set(f'{len(app.objetos)} objeto(s)')
        for canvas, texto in app.metadados:
            if canvas.img is not None:
                h, w = canvas.img.shape[:2]
                canais = 'CINZA' if canvas.img.ndim == 2 else 'COR'
                texto.set(f'{w} × {h} px  |  {canais}')
        app.relogio.set(datetime.now().strftime('%H:%M'))
        raiz.after(200, monitorar)
    monitorar()
    raiz.bind('<Control-o>', lambda e: app.abrir())
    raiz.bind('<Control-s>', lambda e: app.salvar_video() if app.aba.select() == str(app.videos) else app.salvar())
    raiz.bind('<Control-r>', lambda e: app.restaurar())
    raiz.bind('<F1>', lambda e: mostrar_ajuda(app))
