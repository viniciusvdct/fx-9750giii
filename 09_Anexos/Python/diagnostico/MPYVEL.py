# MPYVEL - velocidade do Python da calculadora
# Nao ha modulo time: use um cronometro. Aperte EXE
# no prompt e dispare; pare quando aparecer "fim".
# Ajuste N para cada teste durar de 5 a 30 s.
import math
from casioplot import set_pixel, show_screen
N = 20000


def f(x):
  return x


def t1():
  for i in range(N):
    pass


def t2():
  s = 0
  for i in range(N):
    s = s + i * 3


def t3():
  s = 0.0
  for i in range(N):
    s = s + i * 0.5


def t4():
  r = math.sqrt
  for i in range(N):
    r(2.0)


def t5():
  for i in range(N):
    f(i)


def t6():
  # N//4: lista grande crescida por append dobra de
  # tamanho e pode estourar o heap (MemoryError)
  l = []
  for i in range(N // 4):
    l.append(i)


def t7():
  s = ''
  for i in range(N // 10):
    s = s + 'x'


def t8():
  p = []
  for i in range(N // 10):
    p.append('x')
  s = ''.join(p)


def t9():
  for y in range(64):
    for x in range(128):
      set_pixel(x, y)
  show_screen()


TESTES = [('T1 laco vazio', t1), ('T2 conta int', t2),
          ('T3 conta float', t3), ('T4 sqrt', t4),
          ('T5 chama funcao', t5), ('T6 append N/4', t6),
          ('T7 s=s+x N/10', t7), ('T8 join N/10', t8),
          ('T9 8192 pixels', t9)]
print('== MPYVEL N=%d ==' % N)
for nome, t in TESTES:
  print(nome)
  input('EXE inicia')
  t()
  print('fim')
print('== fim ==')
