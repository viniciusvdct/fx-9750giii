# MPYNUM - como o Python da calculadora trata numeros
# Compare cada linha com a coluna "1.9.4 no PC" do
# estudo MicroPython 1.9.4 (secao Diagnostico).
import math


def mostra(rot, f):
  try:
    v = f()
  except Exception as e:
    v = type(e).__name__
  print(rot)
  print('  ' + str(v))


def bits_mantissa():
  x, n = 1.0, 0
  while 1.0 + x != 1.0:
    x, n = x / 2, n + 1
  return n


def exp_max():
  x, n = 1.0, 0
  while x * 2 != x * 4:
    x, n = x * 2, n + 1
  return n


def exp_min():
  x, n = 1.0, 0
  while x / 2 != 0:
    x, n = x / 2, n + 1
  return n


def soma_decimos():
  s = 0.0
  for i in range(10):
    s = s + 0.1
  return (s, s == 1.0)


print('== MPYNUM ==')
mostra('A bits mantissa', bits_mantissa)
mostra('B maior 2**n', exp_max)
mostra('C menor 2**-n', exp_min)
mostra('D 0.1+0.2', lambda: 0.1 + 0.2)
mostra('E 0.1+0.2==0.3', lambda: 0.1 + 0.2 == 0.3)
mostra('F 538.2', lambda: 538.2)
mostra('G 331.9 e 768.8', lambda: (331.9, 768.8))
mostra('H soma 10x 0.1', soma_decimos)
mostra('I round(2.675,2)', lambda: round(2.675, 2))
mostra('J round(0.5),(2.5)', lambda: (round(0.5), round(2.5)))
mostra('K round(1234,-2)', lambda: round(1234, -2))
mostra('L 2**100', lambda: 2 ** 100)
mostra('M float(2**53+1)', lambda: float(2 ** 53 + 1))
mostra('N 1e308*10', lambda: 1e308 * 10)
mostra('O 2.0**10000', lambda: 2.0 ** 10000)
mostra('P exp(1000)', lambda: math.exp(1000))
mostra('Q sqrt(2)', lambda: math.sqrt(2))
mostra('R sin(pi)', lambda: math.sin(math.pi))
mostra('S tan(pi/4)', lambda: math.tan(math.pi / 4))
mostra('T 1j*1j', lambda: 1j * 1j)
mostra('U (-8)**(1/3)', lambda: (-8) ** (1 / 3))
mostra('V 7//-2, 7%-2', lambda: (7 // -2, 7 % -2))
mostra('W %.3f e {:,}', lambda: ('%.3f' % (2 / 3), '{:,}'.format(10 ** 6)))
mostra('X 1/3', lambda: 1 / 3)
mostra('Y int(1e20)', lambda: int(1e20))
mostra('Z 0.1*3', lambda: 0.1 * 3)
print('== fim ==')
