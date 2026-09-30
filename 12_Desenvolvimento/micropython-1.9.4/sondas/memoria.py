# Custo de memoria (heap) de objetos comuns no MicroPython 1.9.4.
# So roda no MicroPython (usa gc.mem_alloc). Rode no binario de 32 bits, que
# tem ponteiros de 4 bytes como o SH4 da calculadora.
# Saida: NOME<TAB>BYTES_RETIDOS
import gc


def retido(fabrica):
    gc.collect()
    a0 = gc.mem_alloc()
    obj = fabrica()
    gc.collect()
    a1 = gc.mem_alloc()
    obj = None
    return a1 - a0


class Vazia:
    pass


class Ponto:
    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = 3


class Metodo:
    def m(self):
        return 1


def gerador():
    yield 1


def cria_lista_append(n):
    l = []
    for i in range(n):
        l.append(i)
    return l


def cria_floats(n):
    return [i * 0.5 for i in range(n)]


def codigo(n_linhas):
    # Fonte de uma funcao com n linhas tipicas; compilada via exec.
    linhas = ['def f(a, b):']
    for i in range(n_linhas):
        linhas.append('    a = a + b * %d - (a // 3)' % (i + 2))
    linhas.append('    return a')
    return '\n'.join(linhas)


def compila(n):
    ns = {}
    exec(codigo(n), ns)
    return ns


CASOS = [
    ('int pequeno (ate 2**30-1)', lambda: 12345),
    ('int 2**40', lambda: 2 ** 40 + 1),
    ('int 2**100', lambda: 2 ** 100 + 1),
    ('int 2**1000', lambda: 2 ** 1000 + 1),
    ('float', lambda: 1.5 * 3.1),
    ('complex', lambda: complex(1.5, 2.5)),
    ('str de 1 caractere criada em execucao', lambda: str(7)),
    ('str de 10 caracteres', lambda: 'x' * 10),
    ('str de 11 caracteres', lambda: 'x' * 11),
    ('str de 100 caracteres', lambda: 'x' * 100),
    ('str de 1000 caracteres', lambda: 'x' * 1000),
    ('lista vazia []', lambda: []),
    ('lista [0]*10', lambda: [0] * 10),
    ('lista [0]*100', lambda: [0] * 100),
    ('lista [0]*1000', lambda: [0] * 1000),
    ('lista de 1000 ints por append', lambda: cria_lista_append(1000)),
    ('lista de 1000 floats', lambda: cria_floats(1000)),
    ('tupla de 10', lambda: tuple(range(10))),
    ('tupla de 1000', lambda: tuple(range(1000))),
    ('dict vazio', lambda: {}),
    ('dict com 10 pares int', lambda: {i: i for i in range(10)}),
    ('dict com 100 pares int', lambda: {i: i for i in range(100)}),
    ('dict com 1000 pares int', lambda: {i: i for i in range(1000)}),
    ('set com 100 ints', lambda: set(range(100))),
    ('range(1000000)', lambda: range(1000000)),
    ('bytearray(1000)', lambda: bytearray(1000)),
    ('instancia de classe vazia', lambda: Vazia()),
    ('instancia com 3 atributos', lambda: Ponto()),
    ('metodo ligado (obj.m)', lambda: Metodo().m),
    ('objeto gerador', lambda: gerador()),
    ('lambda (closure simples)', lambda: (lambda x: x + 1)),
    ('funcao compilada: 10 linhas', lambda: compila(10)),
    ('funcao compilada: 50 linhas', lambda: compila(50)),
    ('funcao compilada: 100 linhas', lambda: compila(100)),
]

for nome, fab in CASOS:
    print(nome + '\t' + str(retido(fab)))
