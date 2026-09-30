# MPYMEM - quanto heap Python sobra e quao funda
# pode ser a recursao. A calculadora nao tem o
# modulo gc: o heap e estimado enchendo a memoria
# com textos ate dar MemoryError (leva segundos).
# Rode logo apos abrir o SHELL (heap limpo).


def custo(n):
  # bytes de um texto 'x'*n no heap do 1.9.4 em
  # 32 bits: 16 do objeto + dados (n+1) em blocos
  # de 16, mais 4 da posicao na lista
  return 16 + (n + 16) // 16 * 16 + 4


def heap_estimado():
  guarda = [None] * 800
  i = 0
  total = 800 * 4 + 16
  for n in (8000, 2000, 500, 120, 20):
    try:
      while i < 800:
        guarda[i] = 'x' * n
        i = i + 1
        total = total + custo(n)
    except MemoryError:
      pass
  guarda = None
  return total


def cabe(n):
  try:
    x = [0] * n
    return True
  except MemoryError:
    return False


def maior_lista():
  # busca binaria; cada tentativa dentro de uma funcao
  # para a lista anterior virar lixo de verdade
  lo, hi = 0, 200000
  while lo < hi:
    m = (lo + hi + 1) // 2
    if cabe(m):
      lo = m
    else:
      hi = m - 1
  return lo


def profundidade():
  p = [0]

  def r(n):
    p[0] = n
    r(n + 1)
  try:
    r(1)
  except Exception as e:
    return p[0], type(e).__name__
  return p[0], '?'


print('== MPYMEM ==')
print('maior [0]*n')
print('  n = %d' % maior_lista())
d, tipo = profundidade()
print('recursao maxima')
print('  %d niveis' % d)
print('  erro: ' + tipo)
h = heap_estimado()
print('heap livre aprox.')
print('  %d bytes' % h)
print('  (%d KB)' % (h // 1024))
print('== fim ==')
