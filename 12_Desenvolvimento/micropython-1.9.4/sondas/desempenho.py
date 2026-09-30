# Custo RELATIVO de construcoes comuns no MicroPython 1.9.4 (e no CPython).
# Valores absolutos do PC nao valem para a calculadora; as proporcoes indicam
# o que evitar em lacos. Saida: NOME<TAB>MICROSSEGUNDOS_POR_ITERACAO
try:
    from utime import ticks_us, ticks_diff
except ImportError:
    from time import perf_counter

    def ticks_us():
        return int(perf_counter() * 1000000)

    def ticks_diff(a, b):
        return a - b

import math
N = 200000
G = 0


class Obj:
    def __init__(self):
        self.x = 1

    def metodo(self):
        return 1


def nada():
    return 1


def b_for_vazio():
    for i in range(N):
        pass


def b_while():
    i = 0
    while i < N:
        i += 1


def b_local_soma():
    s = 0
    for i in range(N):
        s = s + i


def b_global_soma():
    global G
    G = 0
    for i in range(N):
        G = G + i


def b_float_soma():
    s = 0.0
    for i in range(N):
        s = s + 1.5


def b_atributo():
    o = Obj()
    s = 0
    for i in range(N):
        s = s + o.x


def b_chamada_funcao():
    for i in range(N):
        nada()


def b_chamada_metodo():
    o = Obj()
    for i in range(N):
        o.metodo()


def b_math_sqrt_modulo():
    for i in range(N):
        math.sqrt(2.0)


def b_math_sqrt_local():
    raiz = math.sqrt
    for i in range(N):
        raiz(2.0)


def b_potencia():
    x = 3
    for i in range(N):
        y = x ** 2


def b_multiplica():
    x = 3
    for i in range(N):
        y = x * x


def b_append():
    l = []
    for i in range(N):
        l.append(i)


def b_compreensao():
    l = [i for i in range(N)]


def b_prealoca():
    l = [0] * N
    for i in range(N):
        l[i] = i


def b_concat_texto():
    s = ''
    for i in range(N // 10):
        s = s + 'x'


def b_join_texto():
    p = []
    for i in range(N // 10):
        p.append('x')
    s = ''.join(p)


def b_dict_leitura():
    d = {1: 1, 2: 2, 3: 3}
    s = 0
    for i in range(N):
        s = s + d[2]


def b_lista_leitura():
    l = [1, 2, 3]
    s = 0
    for i in range(N):
        s = s + l[1]


def b_try_sem_excecao():
    for i in range(N):
        try:
            pass
        except ValueError:
            pass


def b_try_com_excecao():
    for i in range(N // 10):
        try:
            raise ValueError
        except ValueError:
            pass


def b_int_grande():
    x = 2 ** 100
    for i in range(N // 10):
        y = x + i


BENCH = [
    ('for i in range(N): pass', b_for_vazio, N),
    ('while i < N: i += 1', b_while, N),
    ('soma em variavel local', b_local_soma, N),
    ('soma em variavel global', b_global_soma, N),
    ('soma de float', b_float_soma, N),
    ('leitura de atributo o.x', b_atributo, N),
    ('chamada de funcao vazia', b_chamada_funcao, N),
    ('chamada de metodo', b_chamada_metodo, N),
    ('math.sqrt(2.0)', b_math_sqrt_modulo, N),
    ('raiz = math.sqrt; raiz(2.0)', b_math_sqrt_local, N),
    ('x ** 2', b_potencia, N),
    ('x * x', b_multiplica, N),
    ('lista com append', b_append, N),
    ('lista por compreensao', b_compreensao, N),
    ('lista pre-alocada [0]*N', b_prealoca, N),
    ("texto: s = s + 'x' (N/10)", b_concat_texto, N // 10),
    ("texto: ''.join(partes) (N/10)", b_join_texto, N // 10),
    ('leitura d[2] em dict', b_dict_leitura, N),
    ('leitura l[1] em lista', b_lista_leitura, N),
    ('try/except sem excecao', b_try_sem_excecao, N),
    ('try/except com excecao (N/10)', b_try_com_excecao, N // 10),
    ('int grande 2**100 + i (N/10)', b_int_grande, N // 10),
]

for nome, f, n in BENCH:
    melhor = None
    for rep in range(3):
        t0 = ticks_us()
        f()
        dt = ticks_diff(ticks_us(), t0)
        melhor = dt if melhor is None or dt < melhor else melhor
    print('%s\t%.4f' % (nome, melhor / n))
