# Emulacao do modulo casioplot da fx-9750GIII para testes no PC.
# Roda no MicroPython 1.9.4 (bancada) e no CPython. Segue o manual SW350,
# paginas 14-17 a 14-22: tela 128x64 monocromatica, coordenadas 0..127 e 0..63,
# cor (R,G,B) de 0 a 255 em lista ou tupla; (248..255, 252..255, 248..255) e
# branco, qualquer outro valor e preto; fora da faixa: nada e desenhado.
#
# Limite conhecido: o desenho exato das letras da calculadora nao e reproduzido.
# draw_string marca a caixa de cada caractere (hipotese: large 6x8, medium 4x6
# pixels) e a previa mostra o proprio caractere no canto da caixa.
#
# show_screen() imprime a previa no terminal. Com a variavel de ambiente
# CASIOPLOT_PBM=prefixo, cada show_screen() tambem grava prefixo_NNN.pbm
# (a bancada repassa o valor em __casioplot_pbm__, porque bloqueia import os).

_LARGURA = 128
_ALTURA = 64
_CAIXA = {'large': (6, 8), 'medium': (4, 6)}

# 1 bit por pixel (1 KB): na calculadora a VRAM fica fora do heap Python,
# entao o emulador gasta o minimo do heap para nao distorcer os testes.
_vram = bytearray(_LARGURA * _ALTURA // 8)
_textos = {}                          # (x, y) -> caractere, para a previa
_quadros = [0]


def _pix(x, y):
    return (_vram[(y * _LARGURA + x) >> 3] >> (x & 7)) & 1


def _poe(x, y, tinta):
    i = (y * _LARGURA + x) >> 3
    if tinta:
        _vram[i] |= 1 << (x & 7)
    else:
        _vram[i] &= ~(1 << (x & 7)) & 0xFF


def _cor(color):
    if not isinstance(color, (tuple, list)) or len(color) != 3:
        raise TypeError('color deve ser (R, G, B)')
    for c in color:
        if not isinstance(c, int) or c < 0 or c > 255:
            raise ValueError('cada componente de color deve ser int de 0 a 255')
    r, g, b = color
    return 0 if (r >= 248 and g >= 252 and b >= 248) else 1


def _coord_ok(x, y):
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError('x e y devem ser int')
    return 0 <= x < _LARGURA and 0 <= y < _ALTURA


def clear_screen():
    for i in range(len(_vram)):
        _vram[i] = 0
    _textos.clear()


def set_pixel(x, y, color=(0, 0, 0)):
    tinta = _cor(color)
    if _coord_ok(x, y):
        _poe(x, y, tinta)


def get_pixel(x, y):
    if _coord_ok(x, y):
        return (0, 0, 0) if _pix(x, y) else (255, 255, 255)
    return None


def draw_string(x, y, s, color=(0, 0, 0), size='medium'):
    if not isinstance(s, str):
        raise TypeError('s deve ser str')
    tinta = _cor(color)
    if not _coord_ok(x, y):
        return
    if size not in _CAIXA:
        size = 'medium'   # 'small' (modelos coloridos) vira 'medium' neste aparelho
    w, h = _CAIXA[size]
    base = min(y + h - 2, _ALTURA - 1)   # linha que sublinha a caixa do caractere
    for i in range(len(s)):
        ch = s[i]
        if ord(ch) > 126:
            ch = '?'      # a tela de desenho so mostra ASCII
        x0 = x + i * w
        if x0 >= _LARGURA:
            break
        for xx in range(x0, min(x0 + w - 1, _LARGURA)):
            _poe(xx, base, tinta)
        if ch != ' ':
            _textos[(x0, y)] = ch


def _previa():
    # 2 linhas de pixels por linha de terminal, 1 coluna por pixel; imprime linha
    # a linha para gastar pouco heap. Caracteres UTF-8 literais (sem escapes):
    # funcionam mesmo no 1.9.4 compilado sem unicode.
    blocos = (' ', '▀', '▄', '█')
    rotulos = {}
    for chave in _textos:
        rotulos[(chave[0], chave[1] // 2)] = _textos[chave]
    borda = '+' + '-' * _LARGURA + '+'
    print(borda)
    for ly in range(_ALTURA // 2):
        partes = ['|']
        for x in range(_LARGURA):
            ch = rotulos.get((x, ly))
            partes.append(ch if ch else blocos[_pix(x, 2 * ly) + 2 * _pix(x, 2 * ly + 1)])
        partes.append('|')
        print(''.join(partes))
    print(borda)


def _grava_pbm():
    try:
        prefixo = __casioplot_pbm__
    except NameError:
        try:
            import os
            prefixo = os.getenv('CASIOPLOT_PBM')
        except ImportError:
            prefixo = None
    if not prefixo:
        return
    nome = '%s_%03d.pbm' % (prefixo, _quadros[0])
    f = open(nome, 'w')
    f.write('P1\n%d %d\n' % (_LARGURA, _ALTURA))
    for y in range(_ALTURA):
        f.write(' '.join(str(_pix(x, y)) for x in range(_LARGURA)) + '\n')
    f.close()


def show_screen():
    _quadros[0] += 1
    print('[casioplot] show_screen() #%d' % _quadros[0])
    _previa()
    _grava_pbm()
