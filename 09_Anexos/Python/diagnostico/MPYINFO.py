# MPYINFO - inventario do Python da calculadora
# Mostra modulos, nomes embutidos, math, random e
# metodos de str que existem neste aparelho.
# Resultado: anote no estudo MicroPython 1.9.4.
TESTAR_TURTLE = False  # True: importa turtle/matplotl


def mostra(rot, itens):
  # imprime em linhas de ate 21 colunas
  lin = rot
  for it in itens:
    if len(lin) + len(it) + 1 > 21:
      print(lin)
      lin = ' '
    lin = lin + ' ' + it
  print(lin)


def tem_mod(nome):
  try:
    m = __import__(nome)
    m.__name__
    return True
  except ImportError:
    return False
  except Exception:
    return True


print('== MPYINFO ==')
try:
  import sys
  v = (sys.implementation, sys.version)
  print('sys ok')
  print(v[0])
  print(v[1])
except ImportError:
  print('sys: nao existe')

MODS = ['math', 'random', 'casioplot', 'builtins',
        'sys', 'gc', 'time', 'utime', 'cmath',
        'micropython', 'array', 'collections',
        'ucollections', 'struct', 'ustruct', 'io',
        'json', 're', 'os', 'uos', 'urandom']
if TESTAR_TURTLE:
  MODS = MODS + ['turtle', 'matplotl']
sim = []
nao = []
for m in MODS:
  if tem_mod(m):
    sim.append(m)
  else:
    nao.append(m)
mostra('mod sim:', sim)
mostra('mod nao:', nao)

NOMES = ['abs', 'all', 'any', 'bin', 'bool',
         'bytearray', 'bytes', 'callable', 'chr',
         'classmethod', 'compile', 'complex',
         'delattr', 'dict', 'dir', 'divmod',
         'enumerate', 'eval', 'exec', 'filter',
         'float', 'format', 'frozenset', 'getattr',
         'globals', 'hasattr', 'hash', 'help', 'hex',
         'id', 'input', 'int', 'isinstance',
         'issubclass', 'iter', 'len', 'list',
         'locals', 'map', 'max', 'memoryview', 'min',
         'next', 'object', 'oct', 'open', 'ord',
         'pow', 'print', 'property', 'range', 'repr',
         'reversed', 'round', 'set', 'setattr',
         'slice', 'sorted', 'staticmethod', 'str',
         'sum', 'super', 'tuple', 'type', 'vars',
         'zip', 'NotImplemented', 'Ellipsis',
         'RecursionError', 'UnicodeError']
falta = []
for n in NOMES:
  try:
    eval(n)
  except NameError:
    falta.append(n)
  except Exception:
    pass
mostra('sem:', falta)

import math
MATH = ['acos', 'acosh', 'asin', 'asinh', 'atan',
        'atan2', 'atanh', 'ceil', 'copysign', 'cos',
        'cosh', 'degrees', 'e', 'erf', 'erfc', 'exp',
        'expm1', 'fabs', 'floor', 'fmod', 'frexp',
        'gamma', 'isfinite', 'isinf', 'isnan',
        'ldexp', 'lgamma', 'log', 'log10', 'log2',
        'modf', 'pi', 'pow', 'radians', 'sin', 'sinh',
        'sqrt', 'tan', 'tanh', 'trunc', 'factorial',
        'gcd', 'isclose', 'inf', 'nan', 'tau', 'hypot']
print('dir(math): %d' % len(dir(math)))
mostra('math sem:', [n for n in MATH if not hasattr(math, n)])

import random
print('dir(random): %d' % len(dir(random)))
mostra('random:', sorted([n for n in dir(random) if n[0] != '_']))
print('rand1: %.6f' % random.random())
print('(rode 2x; se rand1')
print(' repetir, a semente')
print(' inicial e fixa)')

try:
  import casioplot
  mostra('casioplot:', sorted([n for n in dir(casioplot) if n[0] != '_']))
except ImportError:
  print('casioplot: nao')

STR = ['center', 'ljust', 'rjust', 'zfill', 'title',
       'capitalize', 'partition', 'rpartition',
       'splitlines', 'isalnum', 'format', 'encode']
mostra('str sem:', [n for n in STR if not hasattr('', n)])
print('== fim ==')
