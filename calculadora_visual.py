
import pygame
import math
import sys

LARGURA = 960
ALTURA = 720
FPS = 60

PRETO       = (0, 0, 0)
AZUL_BG     = (6, 6, 26)
AZUL_ESCURO = (12, 12, 50)
DOURADO     = (255, 200, 0)
DOURADO_DK  = (180, 140, 0)
CIANO       = (0, 255, 255)
CIANO_DK    = (0, 120, 140)
VERDE       = (0, 255, 80)
VERDE_DK    = (0, 130, 40)
VERMELHO    = (255, 60, 60)
AMARELO     = (255, 230, 0)
BRANCO      = (240, 240, 240)
CINZA       = (130, 130, 140)
CINZA_ESC   = (60, 60, 70)
ROXO        = (200, 80, 255)
LARANJA     = (255, 160, 40)

BAT_X = 130
LAMP_X = 830
FIO_Y_TOP = 140
FIO_Y_BOT = 380
BAT_Y = 260
LAMP_Y = 260

PONTOS_CIRCUITO = [
    (BAT_X, 224),
    (BAT_X, FIO_Y_TOP),
    (LAMP_X, FIO_Y_TOP),
    (LAMP_X, 224),
    (LAMP_X, 296),
    (LAMP_X, FIO_Y_BOT),
    (BAT_X, FIO_Y_BOT),
    (BAT_X, 296),
]


def distancia_p2p(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


class CaminhoCircuito:
    def __init__(self, pontos):
        self.pontos = pontos
        self.segmentos = []
        self.comprimento_total = 0.0

        n = len(pontos)
        for i in range(n):
            p_a = pontos[i]
            p_b = pontos[(i + 1) % n]
            seg_len = distancia_p2p(p_a, p_b)
            self.segmentos.append((p_a, p_b, seg_len, self.comprimento_total))
            self.comprimento_total += seg_len

    def posicao_no_caminho(self, dist):
        dist = dist % self.comprimento_total
        for p_a, p_b, seg_len, dist_ini in self.segmentos:
            if dist_ini + seg_len >= dist:
                fracao = (dist - dist_ini) / seg_len if seg_len > 0 else 0
                x = p_a[0] + (p_b[0] - p_a[0]) * fracao
                y = p_a[1] + (p_b[1] - p_a[1]) * fracao
                return (x, y)
        return self.pontos[0]


class ParticulaCorrente:
    def __init__(self, caminho, offset, velocidade=80):
        self.caminho = caminho
        self.dist = offset
        self.velocidade = velocidade
        self.tamanho = 5

    def atualizar(self, dt, velocidade_global):
        self.dist += velocidade_global * dt
        if self.dist > self.caminho.comprimento_total:
            self.dist %= self.caminho.comprimento_total

    def get_pos(self):
        return self.caminho.posicao_no_caminho(self.dist)


def desenhar_circuito(tela, tempo, velocidade_corrente):
    for i in range(len(PONTOS_CIRCUITO)):
        p_a = PONTOS_CIRCUITO[i]
        p_b = PONTOS_CIRCUITO[(i + 1) % len(PONTOS_CIRCUITO)]
        pygame.draw.line(tela, DOURADO_DK, p_a, p_b, 7)
        pygame.draw.line(tela, DOURADO, p_a, p_b, 4)

    bat_rect = pygame.Rect(BAT_X - 35, BAT_Y - 36, 70, 72)
    pygame.draw.rect(tela, CINZA_ESC, bat_rect, border_radius=4)
    pygame.draw.rect(tela, CINZA, bat_rect, 3, border_radius=4)
    font_bat = pygame.font.SysFont("consolas", 22, bold=True)
    mais = font_bat.render("+", True, VERMELHO)
    menos = font_bat.render("−", True, CIANO)
    tela.blit(mais, (BAT_X - 8, BAT_Y - 30))
    tela.blit(menos, (BAT_X - 8, BAT_Y + 12))
    pygame.draw.line(tela, CINZA, (BAT_X - 12, BAT_Y - 22), (BAT_X + 12, BAT_Y - 22), 3)
    pygame.draw.line(tela, CINZA, (BAT_X - 8, BAT_Y - 14), (BAT_X + 8, BAT_Y - 14), 2)
    pygame.draw.line(tela, CINZA, (BAT_X - 12, BAT_Y + 8), (BAT_X + 12, BAT_Y + 8), 3)
    pygame.draw.line(tela, CINZA, (BAT_X - 8, BAT_Y + 16), (BAT_X + 8, BAT_Y + 16), 2)

    pulso = 0.5 + 0.5 * math.sin(tempo * 3)
    raio_lamp = 28
    for r in range(raio_lamp + 20, raio_lamp, -2):
        alpha = max(0, int(60 * (1 - (r - raio_lamp) / 20) * (0.4 + 0.6 * pulso)))
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*AMARELO, alpha), (r, r), r)
        tela.blit(surf, (LAMP_X - r, LAMP_Y - r))
    pygame.draw.circle(tela, (255, 255, 200), (LAMP_X, LAMP_Y), raio_lamp)
    pygame.draw.circle(tela, AMARELO, (LAMP_X, LAMP_Y), raio_lamp, 3)
    pygame.draw.line(tela, DOURADO_DK,
                     (LAMP_X - 14, LAMP_Y - 14), (LAMP_X + 14, LAMP_Y + 14), 2)
    pygame.draw.line(tela, DOURADO_DK,
                     (LAMP_X - 14, LAMP_Y + 14), (LAMP_X + 14, LAMP_Y - 14), 2)

    caminho = CaminhoCircuito(PONTOS_CIRCUITO)
    n_particulas = 24
    for i in range(n_particulas):
        offset = (i / n_particulas) * caminho.comprimento_total
        p = ParticulaCorrente(caminho, offset)
        p.dist += velocidade_corrente * tempo * 0.001
        pos = p.get_pos()

        for t_offset in range(1, 4):
            trail_dist = p.dist - t_offset * 8
            trail_pos = caminho.posicao_no_caminho(trail_dist)
            trail_cor = (0, 255 - t_offset * 60, 255 - t_offset * 60)
            pygame.draw.rect(tela, trail_cor,
                             (trail_pos[0] - 2, trail_pos[1] - 2, 4, 4))

        glow = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*CIANO, 80), (8, 8), 7)
        tela.blit(glow, (pos[0] - 8, pos[1] - 8))
        pygame.draw.rect(tela, CIANO, (pos[0] - 2, pos[1] - 2, 5, 5))
        pygame.draw.rect(tela, BRANCO, (pos[0] - 1, pos[1] - 1, 3, 3))


class Botao:
    def __init__(self, x, y, w, h, texto, cor_base, cor_texto=BRANCO):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.cor_base = cor_base
        self.cor_texto = cor_texto
        self.hover = False
        self.pressionado = False
        self.font = pygame.font.SysFont("consolas", 16, bold=True)

    def atualizar(self, mx, my):
        self.hover = self.rect.collidepoint(mx, my)

    def desenhar(self, tela):
        cor = self.cor_base
        if self.hover:
            cor = tuple(min(255, c + 40) for c in self.cor_base)
        if self.pressionado:
            cor = tuple(max(0, c - 30) for c in self.cor_base)

        pygame.draw.rect(tela, cor, self.rect, border_radius=2)
        pygame.draw.rect(tela, BRANCO if self.hover else CINZA,
                         self.rect, 2, border_radius=2)

        txt = self.font.render(self.texto, True, self.cor_texto)
        tr = txt.get_rect(center=self.rect.center)
        tela.blit(txt, tr)

    def clicado(self, mx, my):
        return self.rect.collidepoint(mx, my)


class CampoInput:
    def __init__(self, x, y, w, h, rotulo, cor_rotulo=VERDE):
        self.rect = pygame.Rect(x, y, w, h)
        self.rotulo = rotulo
        self.texto = ""
        self.ativo = False
        self.cor_rotulo = cor_rotulo
        self.font = pygame.font.SysFont("consolas", 18, bold=True)
        self.font_rotulo = pygame.font.SysFont("consolas", 14, bold=True)
        self.cursor_piscando = 0

    def atualizar(self, dt, mx, my):
        self.cursor_piscando += dt

    def tratar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                self.ativo = self.rect.collidepoint(evento.pos)
        elif evento.type == pygame.KEYDOWN and self.ativo:
            if evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_TAB):
                self.ativo = False
            else:
                char = evento.unicode
                if char in "0123456789.,-":
                    char = char.replace(",", ".")
                    if char == "." and "." in self.texto:
                        return
                    self.texto += char

    def desenhar(self, tela):
        lbl = self.font_rotulo.render(self.rotulo, True, self.cor_rotulo)
        tela.blit(lbl, (self.rect.x, self.rect.y - 20))

        cor_borda = CIANO if self.ativo else CINZA_ESC
        cor_fundo = (10, 10, 40) if self.ativo else (5, 5, 20)
        pygame.draw.rect(tela, cor_fundo, self.rect, border_radius=2)
        pygame.draw.rect(tela, cor_borda, self.rect, 2, border_radius=2)

        txt = self.font.render(self.texto, True, BRANCO)
        tela.blit(txt, (self.rect.x + 8, self.rect.y + 8))

        if self.ativo and int(self.cursor_piscando * 2) % 2 == 0:
            cx = self.rect.x + 8 + txt.get_width() + 2
            pygame.draw.line(tela, CIANO,
                             (cx, self.rect.y + 6), (cx, self.rect.y + self.rect.h - 6), 2)

    def get_valor(self):
        if not self.texto or self.texto in (".", "-", "-."):
            return None
        try:
            return float(self.texto)
        except ValueError:
            return None


def func_corrente(valores):
    Q, t = valores
    if t == 0:
        return None, "Erro: tempo não pode ser zero (divisão por zero)."
    return Q / t, None

def func_tensao(valores):
    R, I = valores
    return R * I, None

def func_resistencia(valores):
    U, I = valores
    if I == 0:
        return None, "Erro: corrente não pode ser zero (divisão por zero)."
    return U / I, None

def func_potencia_a(valores):
    U, I = valores
    return U * I, None

def func_potencia_b(valores):
    R, I = valores
    return R * I ** 2, None

def func_potencia_c(valores):
    U, R = valores
    if R == 0:
        return None, "Erro: resistência não pode ser zero (divisão por zero)."
    return U ** 2 / R, None

def func_energia(valores):
    P, t = valores
    E_j = P * t
    E_kwh = E_j / 3_600_000
    return E_j, f"Energia = {E_j:.4g} J  |  {E_kwh:.6f} kWh"

def func_trabalho(valores):
    U, Q = valores
    return U * Q, None

def func_consumo(valores):
    P_w, t, dias = valores
    P_kw = P_w / 1000
    E = P_kw * t * dias
    return E, f"Potência = {P_kw} kW  |  Consumo = {E} kWh"

def func_custo(valores):
    E, tarifa = valores
    C = E * tarifa
    return C, f"Custo = R$ {C:.2f}"


FUNCIONALIDADES = {
    "1": {
        "nome": "Corrente Elétrica",
        "formula": "I = Q / t",
        "campos": ["Carga (C)", "Tempo (s)"],
        "funcao": func_corrente,
        "unidade": "A",
        "rotulo": "Corrente",
        "cor": CIANO,
    },
    "2": {
        "nome": "Tensão Elétrica",
        "formula": "U = R * I",
        "campos": ["Resistência (Ω)", "Corrente (A)"],
        "funcao": func_tensao,
        "unidade": "V",
        "rotulo": "Tensão",
        "cor": AMARELO,
    },
    "3": {
        "nome": "Resistência",
        "formula": "R = U / I",
        "campos": ["Tensão (V)", "Corrente (A)"],
        "funcao": func_resistencia,
        "unidade": "Ω",
        "rotulo": "Resistência",
        "cor": LARANJA,
    },
    "4": {
        "nome": "Potência",
        "formula": "P = U*I  |  P = R*I²  |  P = U²/R",
        "campos": None,
        "cor": ROXO,
    },
    "5": {
        "nome": "Energia",
        "formula": "E = P * t",
        "campos": ["Potência (W)", "Tempo (s)"],
        "funcao": func_energia,
        "unidade": "J",
        "rotulo": "Energia",
        "cor": VERDE,
    },
    "6": {
        "nome": "Trabalho Elétrico",
        "formula": "W = U * Q",
        "campos": ["Tensão (V)", "Carga (C)"],
        "funcao": func_trabalho,
        "unidade": "J",
        "rotulo": "Trabalho",
        "cor": VERMELHO,
    },
    "7": {
        "nome": "Consumo (kWh)",
        "formula": "E = P(kW) * t * dias",
        "campos": ["Potência (W)", "Tempo/dia (h)", "Dias"],
        "funcao": func_consumo,
        "unidade": "kWh",
        "rotulo": "Consumo",
        "cor": CIANO,
    },
    "8": {
        "nome": "Custo da Energia",
        "formula": "C = E * tarifa",
        "campos": ["Energia (kWh)", "Tarifa (R$/kWh)"],
        "funcao": func_custo,
        "unidade": "R$",
        "rotulo": "Custo",
        "cor": VERDE,
    },
}

POTENCIA_OPCOES = {
    "A": {
        "nome": "P = U * I",
        "campos": ["Tensão (V)", "Corrente (A)"],
        "funcao": func_potencia_a,
        "unidade": "W",
        "rotulo": "Potência",
    },
    "B": {
        "nome": "P = R * I²",
        "campos": ["Resistência (Ω)", "Corrente (A)"],
        "funcao": func_potencia_b,
        "unidade": "W",
        "rotulo": "Potência",
    },
    "C": {
        "nome": "P = U² / R",
        "campos": ["Tensão (V)", "Resistência (Ω)"],
        "funcao": func_potencia_c,
        "unidade": "W",
        "rotulo": "Potência",
    },
}


def desenhar_painel(tela, x, y, w, h, titulo=None, cor_titulo=CIANO):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(tela, AZUL_ESCURO, rect, border_radius=4)
    pygame.draw.rect(tela, cor_titulo, rect, 2, border_radius=4)
    if titulo:
        font = pygame.font.SysFont("consolas", 18, bold=True)
        txt = font.render(titulo, True, cor_titulo)
        tela.blit(txt, (x + 12, y + 6))
        pygame.draw.line(tela, cor_titulo,
                         (x + 8, y + 32), (x + w - 8, y + 32), 1)


def desenhar_titulo(tela, texto, y=12, cor=CIANO, tamanho=28):
    font = pygame.font.SysFont("consolas", tamanho, bold=True)
    txt = font.render(texto, True, cor)
    tr = txt.get_rect(center=(LARGURA // 2, y + tamanho // 2))
    sombra = font.render(texto, True, (0, 80, 80))
    tela.blit(sombra, (tr.x + 3, tr.y + 3))
    tela.blit(txt, tr)
    return tr.bottom


class Aplicacao:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Calculadora de Eletrodinâmica - Retro")
        self.clock = pygame.time.Clock()
        self.tempo = 0
        self.velocidade_corrente = 1.0

        self.cena = "menu"
        self.func_id = None
        self.pot_opcao = None
        self.campos = []
        self.resultado = None
        self.resultado_extra = None
        self.erro = None
        self.config_func = None

        self.font_grande = pygame.font.SysFont("consolas", 24, bold=True)
        self.font_media = pygame.font.SysFont("consolas", 18, bold=True)
        self.font_peq = pygame.font.SysFont("consolas", 14, bold=True)
        self.font_resultado = pygame.font.SysFont("consolas", 30, bold=True)

        self._criar_botoes_menu()
        self._criar_botoes_potencia()
        self._criar_botoes_navegacao()

    def _criar_botoes_menu(self):
        self.botoes_menu = {}
        itens = [
            ("1", "1 - Corrente",     CIANO_DK),
            ("2", "2 - Tensão",       AZUL_ESCURO),
            ("3", "3 - Resistência",  (100, 60, 0)),
            ("4", "4 - Potência",     (80, 30, 120)),
            ("5", "5 - Energia",      VERDE_DK),
            ("6", "6 - Trabalho",     (120, 30, 30)),
            ("7", "7 - Consumo",      (0, 80, 100)),
            ("8", "8 - Custo",        (30, 100, 50)),
            ("9", "9 - Sair",         (120, 20, 20)),
        ]
        bx, by = 60, 420
        bw, bh = 260, 46
        gap = 10
        colunas = 3
        for i, (id_, texto, cor) in enumerate(itens):
            col = i % colunas
            lin = i // colunas
            x = bx + col * (bw + gap)
            y = by + lin * (bh + gap)
            self.botoes_menu[id_] = Botao(x, y, bw, bh, texto, cor)

    def _criar_botoes_potencia(self):
        self.botoes_potencia = {}
        opcoes = [("A", "A - P = U * I"), ("B", "B - P = R * I²"), ("C", "C - P = U² / R")]
        bx, by = 180, 340
        bw, bh = 200, 50
        gap = 15
        for i, (id_, texto) in enumerate(opcoes):
            x = bx + i * (bw + gap)
            self.botoes_potencia[id_] = Botao(x, by, bw, bh, texto, (80, 30, 120), AMARELO)

    def _criar_botoes_navegacao(self):
        self.btn_calcular = Botao(360, 520, 240, 50, "CALCULAR", VERDE_DK, BRANCO)
        self.btn_voltar = Botao(360, 590, 240, 45, "VOLTAR", AZUL_ESCURO, BRANCO)
        self.btn_voltar_pot = Botao(380, 430, 200, 45, "VOLTAR", AZUL_ESCURO, BRANCO)

    def entrar_input(self, config):
        self.campos = []
        self.config_func = config
        self.resultado = None
        self.resultado_extra = None
        self.erro = None
        x_inicial = 310
        y_inicial = 360
        for i, rotulo in enumerate(config["campos"]):
            campo = CampoInput(x_inicial, y_inicial + i * 70, 340, 40, rotulo,
                              cor_rotulo=config.get("cor", VERDE))
            self.campos.append(campo)
        self.cena = "input"

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.cena == "input":
                for campo in self.campos:
                    campo.tratar_evento(evento)

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self._tratar_clique(evento.pos)

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.cena in ("input", "potencia", "resultado"):
                        self.cena = "menu"
                elif evento.key == pygame.K_RETURN and self.cena == "input":
                    self._calcular()

    def _tratar_clique(self, pos):
        mx, my = pos

        if self.cena == "menu":
            for id_, botao in self.botoes_menu.items():
                botao.atualizar(mx, my)
                if botao.clicado(mx, my):
                    if id_ == "9":
                        pygame.quit()
                        sys.exit()
                    elif id_ == "4":
                        self.cena = "potencia"
                    else:
                        config = FUNCIONALIDADES[id_]
                        self.func_id = id_
                        self.entrar_input(config)
                    return

        elif self.cena == "potencia":
            for id_, botao in self.botoes_potencia.items():
                if botao.clicado(mx, my):
                    config = POTENCIA_OPCOES[id_]
                    config["cor"] = ROXO
                    self.pot_opcao = id_
                    self.entrar_input(config)
                    return
            if self.btn_voltar_pot.clicado(mx, my):
                self.cena = "menu"

        elif self.cena == "input":
            if self.btn_calcular.clicado(mx, my):
                self._calcular()
            elif self.btn_voltar.clicado(mx, my):
                self.cena = "menu"

        elif self.cena == "resultado":
            if self.btn_voltar.clicado(mx, my):
                self.cena = "menu"

    def _calcular(self):
        valores = []
        for campo in self.campos:
            v = campo.get_valor()
            if v is None:
                self.erro = "Erro: preencha todos os campos com valores numéricos válidos."
                self.resultado = None
                self.resultado_extra = None
                return
            valores.append(v)

        resultado, extra = self.config_func["funcao"](valores)

        if resultado is None:
            self.erro = extra
            self.resultado = None
            self.resultado_extra = None
        else:
            self.erro = None
            self.resultado = resultado
            self.resultado_extra = extra
            self.cena = "resultado"

    def atualizar(self, dt):
        self.tempo += dt
        mx, my = pygame.mouse.get_pos()

        if self.cena == "menu":
            for botao in self.botoes_menu.values():
                botao.atualizar(mx, my)

        elif self.cena == "potencia":
            for botao in self.botoes_potencia.values():
                botao.atualizar(mx, my)
            self.btn_voltar_pot.atualizar(mx, my)

        elif self.cena == "input":
            for campo in self.campos:
                campo.atualizar(dt, mx, my)
            self.btn_calcular.atualizar(mx, my)
            self.btn_voltar.atualizar(mx, my)

        elif self.cena == "resultado":
            self.btn_voltar.atualizar(mx, my)

    def desenhar(self):
        self.tela.fill(AZUL_BG)

        for x in range(0, LARGURA, 20):
            pygame.draw.line(self.tela, (10, 10, 35), (x, 0), (x, ALTURA), 1)
        for y in range(0, ALTURA, 20):
            pygame.draw.line(self.tela, (10, 10, 35), (0, y), (LARGURA, y), 1)

        desenhar_titulo(self.tela, "CALCULADORA DE ELETRODINÂMICA", y=10,
                        cor=CIANO, tamanho=26)
        sub = self.font_peq.render("◆ Eletrodinâmica • Trabalho • Energia • Potência ◆",
                                   True, DOURADO)
        self.tela.blit(sub, sub.get_rect(center=(LARGURA // 2, 46)))

        desenhar_circuito(self.tela, self.tempo, self.velocidade_corrente * 120)

        vel_txt = self.font_peq.render(
            f"Corrente: {'∞' if self.velocidade_corrente > 999 else f'{self.velocidade_corrente:.1f}x'}",
            True, CIANO_DK)
        self.tela.blit(vel_txt, (LARGURA - 130, 400))

        if self.cena == "menu":
            self._desenhar_menu()
        elif self.cena == "potencia":
            self._desenhar_potencia()
        elif self.cena == "input":
            self._desenhar_input()
        elif self.cena == "resultado":
            self._desenhar_resultado()

        pygame.display.flip()

    def _desenhar_menu(self):
        desenhar_painel(self.tela, 30, 400, 900, 290, "MENU DE CÁLCULOS", CIANO)
        for botao in self.botoes_menu.values():
            botao.desenhar(self.tela)
        dica = self.font_peq.render("ESC: Sair  |  Clique numa opção para começar",
                                    True, CINZA)
        self.tela.blit(dica, dica.get_rect(center=(LARGURA // 2, 688)))

    def _desenhar_potencia(self):
        desenhar_painel(self.tela, 120, 300, 720, 200, "POTÊNCIA ELÉTRICA - Escolha a fórmula", ROXO)
        instrucao = self.font_media.render("Quais dados você possui?", True, AMARELO)
        self.tela.blit(instrucao, instrucao.get_rect(center=(LARGURA // 2, 325)))
        for botao in self.botoes_potencia.values():
            botao.desenhar(self.tela)
        self.btn_voltar_pot.desenhar(self.tela)

    def _desenhar_input(self):
        config = self.config_func
        cor = config.get("cor", CIANO)
        nome = config["nome"]
        if self.func_id == "4":
            nome = f"Potência - {self.pot_opcao}"
        desenhar_painel(self.tela, 200, 320, 560, 260, nome, cor)

        formula_txt = self.font_grande.render(config["formula"], True, DOURADO)
        self.tela.blit(formula_txt, formula_txt.get_rect(center=(LARGURA // 2, 355)))

        for campo in self.campos:
            campo.desenhar(self.tela)

        self.btn_calcular.desenhar(self.tela)
        self.btn_voltar.desenhar(self.tela)

        if self.erro:
            err_txt = self.font_media.render(self.erro, True, VERMELHO)
            self.tela.blit(err_txt, err_txt.get_rect(center=(LARGURA // 2, 480)))

    def _desenhar_resultado(self):
        config = self.config_func
        cor = config.get("cor", CIANO)

        nome = config["rotulo"]
        desenhar_painel(self.tela, 200, 320, 560, 260, "RESULTADO", cor)

        formula_txt = self.font_media.render(config["formula"], True, DOURADO)
        self.tela.blit(formula_txt, formula_txt.get_rect(center=(LARGURA // 2, 360)))

        unidade = config.get("unidade", "")
        if unidade == "R$":
            txt_resultado = f"R$ {self.resultado:.2f}"
        else:
            if self.resultado == int(self.resultado):
                txt_resultado = f"{int(self.resultado)} {unidade}"
            else:
                txt_resultado = f"{self.resultado:.4g} {unidade}"

        for offset in range(4, 0, -1):
            brilho = self.font_resultado.render(txt_resultado, True,
                                                 tuple(min(255, int(c * 0.3)) for c in cor))
            self.tela.blit(brilho, brilho.get_rect(center=(LARGURA // 2 + offset, 440)))
            self.tela.blit(brilho, brilho.get_rect(center=(LARGURA // 2 - offset, 440)))

        txt = self.font_resultado.render(txt_resultado, True, BRANCO)
        self.tela.blit(txt, txt.get_rect(center=(LARGURA // 2, 440)))

        if self.resultado_extra:
            extra_txt = self.font_media.render(self.resultado_extra, True, VERDE)
            self.tela.blit(extra_txt, extra_txt.get_rect(center=(LARGURA // 2, 490)))

        self.btn_voltar.desenhar(self.tela)

    def rodar(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.tratar_eventos()
            self.atualizar(dt)
            self.desenhar()


if __name__ == "__main__":
    app = Aplicacao()
    app.rodar()
