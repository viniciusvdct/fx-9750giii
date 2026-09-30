# Limites praticos com heap pequeno, um teste por processo:
#   mpy194-teto -X heapsize=100k sondas/limites_heap.py NOME_DO_TESTE
# Sem argumento, lista os testes. O driver e sondas/rodar_limites.py.
# (A comunidade mede ~100 KB de heap Python na Graph 35+E II / fx-9750GIII.)
import gc
import sys


def maior(teste, lo, hi):
    # maior n em [lo, hi] para o qual teste(n) nao levanta MemoryError
    while lo < hi:
        meio = (lo + hi + 1) // 2
        gc.collect()
        try:
            teste(meio)
            lo = meio
        except MemoryError:
            hi = meio - 1
    return lo


def conta_ate_estourar(passo):
    itens = []
    try:
        while True:
            passo(itens)
    except MemoryError:
        pass
    return len(itens)


def t_heap():
    gc.collect()
    return '%d livres de %d' % (gc.mem_free(), gc.mem_free() + gc.mem_alloc())


def t_lista_zeros():
    def f(n):
        x = [0] * n
    return maior(f, 0, 200000)


def t_texto():
    def f(n):
        x = 'x' * n
    return maior(f, 0, 400000)


def t_ints_append():
    return conta_ate_estourar(lambda l: l.append(len(l)))


def t_floats_append():
    return conta_ate_estourar(lambda l: l.append(len(l) * 0.5))


def t_floats_prealocados():
    # lista criada de uma vez; so os floats sao alocados depois
    n = 0
    l = [0] * 5000
    try:
        while n < 5000:
            l[n] = n * 0.5
            n += 1
    except MemoryError:
        pass
    return n


def t_textos_8():
    return conta_ate_estourar(lambda l: l.append('%08d' % len(l)))


def t_dict():
    d = {}
    try:
        while True:
            d[len(d)] = 0
    except MemoryError:
        pass
    return len(d)


def t_fragmentacao():
    blocos = []
    try:
        while True:
            blocos.append(bytearray(256))
    except MemoryError:
        pass
    for i in range(0, len(blocos), 2):
        blocos[i] = None
    gc.collect()
    livre = gc.mem_free()
    return '%d livres, maior bloco %d' % (livre, maior(lambda n: bytearray(n), 0, livre))


def _prof(f):
    prof = [0]
    try:
        f(prof, 1)
    except RuntimeError:
        pass
    return prof[0]


def _r_simples(p, n):
    p[0] = n
    _r_simples(p, n + 1)


def _r_locais(p, n):
    a = n; b = n + 1; c = n + 2; d = n + 3; e = n + 4
    p[0] = n
    _r_locais(p, n + 1)
    return a + b + c + d + e


def t_recursao():
    return 'simples %d, com 5 locais %d' % (_prof(_r_simples), _prof(_r_locais))


TESTES = {
    'heap': t_heap, 'lista_zeros': t_lista_zeros, 'texto': t_texto,
    'ints_append': t_ints_append, 'floats_append': t_floats_append,
    'floats_prealocados': t_floats_prealocados, 'textos_8': t_textos_8,
    'dict': t_dict, 'fragmentacao': t_fragmentacao, 'recursao': t_recursao,
}

if len(sys.argv) > 1:
    print(TESTES[sys.argv[1]]())
else:
    print(' '.join(sorted(TESTES)))
