# Sondas de linguagem: rodam igual no CPython 3 e no MicroPython 1.9.4.
# Cada sonda e um trecho executado com exec(); o resultado e o repr() da
# variavel r ou o nome e a mensagem da excecao. Saida: ID<TAB>STATUS<TAB>RESULTADO.
# Nao use f-strings neste arquivo: ele precisa ser lido pelo proprio 1.9.4.

SONDAS = [
# ---------------------------------------------------------------- sintaxe
('S01', 'sintaxe', 'f-string (PEP 498, Python 3.6)', '''r = f"{1+1}"'''),
('S02', 'sintaxe', 'operador morsa := (3.8)', '''r = [(y := 5), y]'''),
('S03', 'sintaxe', 'parametro so-posicional / (3.8)', '''
def f(a, /, b):
    return a + b
r = f(1, 2)'''),
('S04', 'sintaxe', 'anotacao de funcao (3.0)', '''
def f(x: int) -> int:
    return x * 2
r = f(3)'''),
('S05', 'sintaxe', 'anotacao de variavel x: int = 5 (3.6)', '''
x: int = 5
r = x'''),
('S06', 'sintaxe', 'separador _ em numeros 1_000 (3.6)', '''r = 1_000_000'''),
('S07', 'sintaxe', 'async def / await (3.5)', '''
async def f():
    return 1
r = 'compilou' '''),
('S08', 'sintaxe', 'nonlocal', '''
def contador():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc
c = contador(); c()
r = c()'''),
('S09', 'sintaxe', 'yield from', '''
def g():
    yield from range(3)
r = list(g())'''),
('S10', 'sintaxe', 'argumento so-nomeado (*, b)', '''
def f(a, *, b=2):
    return a + b
r = f(1, b=5)'''),
('S11', 'sintaxe', 'desempacotamento estendido a, *b, c', '''
a, *b, c = [1, 2, 3, 4, 5]
r = (a, b, c)'''),
('S12', 'sintaxe', 'PEP 448: [*a, *b]', '''r = [*[1], *[2, 3]]'''),
('S13', 'sintaxe', 'PEP 448: {**d1, **d2}', '''r = sorted({**{'a': 1}, **{'b': 2}}.items())'''),
('S14', 'sintaxe', 'PEP 448: f(*a, *b)', '''
def f(*a):
    return a
r = f(*[1], *[2])'''),
('S15', 'sintaxe', 'operador @ (__matmul__, 3.5)', '''
class M:
    def __matmul__(self, o):
        return 42
r = M() @ M()'''),
('S16', 'sintaxe', 'compreensao de conjunto', '''r = sorted({x % 3 for x in range(10)})'''),
('S17', 'sintaxe', 'compreensao de dicionario', '''r = sorted({x: x * x for x in range(3)}.items())'''),
('S18', 'sintaxe', 'expressao condicional em lambda', '''
f = lambda x: 'par' if x % 2 == 0 else 'impar'
r = f(3)'''),
('S19', 'sintaxe', 'comparacao encadeada 1 < 2 < 3', '''r = 1 < 2 < 3'''),
('S20', 'sintaxe', 'raise ... from ... (encadeamento)', '''
try:
    try:
        1 / 0
    except ZeroDivisionError as e:
        raise ValueError('x') from e
except ValueError as e2:
    r = (type(e2).__name__, getattr(e2, '__cause__', 'sem __cause__'))'''),
('S21', 'sintaxe', 'with + gerenciador de contexto proprio', '''
log = []
class CM:
    def __enter__(self):
        log.append('in'); return self
    def __exit__(self, *a):
        log.append('out'); return False
with CM() as c:
    log.append('corpo')
r = log'''),
('S22', 'sintaxe', 'decorador de funcao e de classe', '''
def dec(f):
    return lambda *a: f(*a) * 10
@dec
def g(x):
    return x
def cdec(c):
    c.marca = 1
    return c
@cdec
class K:
    pass
r = (g(2), K.marca)'''),
('S23', 'sintaxe', 'match/case (3.10)', '''
match 1:
    case 1:
        r = 'um' '''),
('S24', 'sintaxe', 'literais 0b 0o 0x', '''r = (0b101, 0o17, 0x1f)'''),
('S25', 'sintaxe', 'literal complexo 1j', '''r = (1 + 2j) * (3 - 1j)'''),
('S26', 'sintaxe', 'prefixos r b u rb', '''r = (r'\\n', b'ab', u'x', rb'\\d')'''),
('S27', 'sintaxe', 'escape \\N{nome unicode}', '''r = '\\N{GREEK SMALL LETTER ALPHA}' '''),
('S28', 'sintaxe', 'return *a, 3 (3.8)', '''
def f():
    a = [1, 2]
    return *a, 3
r = f()'''),
('S29', 'sintaxe', 'for ... else / while ... else', '''
for i in range(3):
    pass
else:
    a = 'for-else'
n = 0
while n < 2:
    n += 1
else:
    b = 'while-else'
r = (a, b)'''),
('S30', 'sintaxe', 'docstring acessivel em __doc__', '''
def f():
    "documentacao"
    return 1
r = f.__doc__'''),
('S31', 'sintaxe', 'identificador nao ASCII', '''
\u00e9 = 1
r = \u00e9'''),
('S32', 'sintaxe', 'metaclass=', '''
class M(type):
    pass
class A(metaclass=M):
    pass
r = type(A).__name__'''),
('S33', 'sintaxe', 'global dentro de funcao', '''
g = 1
def f():
    global g
    g = 2
f()
r = g'''),
('S34', 'sintaxe', 'Ellipsis ...', '''r = ...'''),
('S35', 'sintaxe', 'type hints com default', '''
def f(a: int = 3) -> int:
    return a
r = f()'''),
# ------------------------------------------------------------- numeros
('N01', 'numeros', '0.1 + 0.2 == 0.3', '''r = 0.1 + 0.2 == 0.3'''),
('N02', 'numeros', 'repr(0.1 + 0.2)', '''r = 0.1 + 0.2'''),
('N03', 'numeros', 'str(0.1 + 0.2)', '''r = str(0.1 + 0.2)'''),
('N04', 'numeros', '2 ** 0.5', '''r = 2 ** 0.5'''),
('N05', 'numeros', '1 / 3 e 2 / 3', '''r = (1 / 3, 2 / 3)'''),
('N06', 'numeros', 'sum([0.1] * 10)', '''r = sum([0.1] * 10)'''),
('N07', 'numeros', 'str() de floats variados', '''
r = [str(x) for x in (1e16, 1e15, 123456789.123456789, 100.0, -0.0, 1e22, 12345678.9, 1e-5, 0.0001, 1e100)]'''),
('N08', 'numeros', 'transbordo 1e308 * 10', '''r = (1e308 * 10, -1e308 * 10)'''),
('N09', 'numeros', 'subnormais 5e-324 e 1e-324', '''r = (5e-324, 1e-324, 5e-324 / 2)'''),
('N10', 'numeros', 'inteiros grandes 2 ** 100', '''r = 2 ** 100'''),
('N11', 'numeros', '(2**64 + 1) - 2**64', '''r = (2 ** 64 + 1) - 2 ** 64'''),
('N12', 'numeros', 'divisao / // % com negativos', '''r = (7 / 2, 7 // 2, -7 // 2, 7 % 3, -7 % 3, 7 % -3, 7.5 // 2, divmod(-7, 2))'''),
('N13', 'numeros', '1 / 0', '''r = 1 / 0'''),
('N14', 'numeros', '1.0 / 0', '''r = 1.0 / 0'''),
('N15', 'numeros', '1 % 0', '''r = 1 % 0'''),
('N16', 'numeros', '0 ** 0, 0.0 ** 0', '''r = (0 ** 0, 0.0 ** 0)'''),
('N17', 'numeros', '0 ** -1', '''r = 0 ** -1'''),
('N18', 'numeros', '2.0 ** 10000', '''r = 2.0 ** 10000'''),
('N19', 'numeros', 'float(10 ** 400)', '''r = float(10 ** 400)'''),
('N20', 'numeros', 'int(1e300) exato', '''r = int(1e300) == 10 ** 300'''),
('N21', 'numeros', 'int(float("inf"))', '''r = int(float('inf'))'''),
('N22', 'numeros', 'int(float("nan"))', '''r = int(float('nan'))'''),
('N23', 'numeros', 'round(): meio-a-par e casas', '''r = (round(2.5), round(3.5), round(-0.5), round(0.5), round(2.675, 2), round(1234, -2), round(1.5))'''),
('N24', 'numeros', 'round(x) devolve int', '''r = type(round(2.7)).__name__'''),
('N25', 'numeros', 'int() de textos', '''r = (int('12'), int(' 12 '), int('ff', 16), int('0x1f', 16), int('0b101', 0), int(3.99), int(-3.99))'''),
('N26', 'numeros', 'int("1_0")', '''r = int('1_0')'''),
('N27', 'numeros', 'int("3.5")', '''r = int('3.5')'''),
('N28', 'numeros', 'float() de textos', '''r = (float(' 2.5 '), float('1e3'), float('inf'), float('-inf'), float('-0'))'''),
('N29', 'numeros', 'float("nan") != float("nan")', '''n = float('nan'); r = (n != n, str(n))'''),
('N30', 'numeros', 'pow() 3 argumentos e negativos', '''r = (pow(2, 10, 1000), pow(2, -1), pow(3, 200, 7))'''),
('N31', 'numeros', '(-8) ** (1/3)', '''r = (-8) ** (1 / 3)'''),
('N32', 'numeros', '(-1) ** 0.5', '''r = (-1) ** 0.5'''),
('N33', 'numeros', 'abs() de float e complexo', '''r = (abs(-3.5), abs(3 + 4j))'''),
('N34', 'numeros', 'complexos: atributos e metodos', '''z = 3 + 4j; r = (z.real, z.imag, z.conjugate(), 1j ** 2, complex(1, 2))'''),
('N35', 'numeros', 'complex("1+2j")', '''r = complex('1+2j')'''),
('N36', 'numeros', 'int.to_bytes / from_bytes', '''r = ((255).to_bytes(2, 'big'), int.from_bytes(b'\\x01\\x00', 'big'))'''),
('N37', 'numeros', 'int.bit_length()', '''r = (5).bit_length()'''),
('N38', 'numeros', 'float.is_integer()', '''r = (3.0).is_integer()'''),
('N39', 'numeros', 'float.as_integer_ratio()', '''r = (0.5).as_integer_ratio()'''),
('N40', 'numeros', 'float.hex() / fromhex', '''r = (1.0).hex()'''),
('N41', 'numeros', 'True + True, bool e int', '''r = (True + True, isinstance(True, int))'''),
('N42', 'numeros', '2**53 + 1 vs float', '''r = (2 ** 53 + 1 == float(2 ** 53 + 1), float(2 ** 53 + 1))'''),
('N43', 'numeros', '1e16 + 1 e 1e16 + 2', '''r = (1e16 + 1, 1e16 + 2)'''),
('N44', 'numeros', 'int(0.1 * 3 * 10)', '''r = int(0.1 * 3 * 10)'''),
('N45', 'numeros', 'hash(1.5), hash(-1)', '''r = (type(hash(1.5)).__name__, hash(-1))'''),
('N46', 'numeros', 'comparacao int grande x float', '''r = (10 ** 20 == 1e20, 10 ** 30 < 1e31)'''),
('N47', 'numeros', 'len(range(10**10))', '''r = len(range(10 ** 10))'''),
('N48', 'numeros', 'divmod(7.5, 2), 7.5 % 2', '''r = (divmod(7.5, 2), 7.5 % 2, -7.5 % 2)'''),
# ---------------------------------------------------------------- math
('M01', 'math', 'math.floor/ceil/trunc devolvem int', '''
import math
r = (math.floor(2.5), type(math.floor(2.5)).__name__, math.ceil(-2.5), math.trunc(-2.7))'''),
('M02', 'math', 'math.sqrt, pow, exp, e, pi', '''
import math
r = (math.sqrt(2), math.pow(2, 0.5), math.exp(1), math.e, math.pi)'''),
('M03', 'math', 'math.log(x) e math.log(x, base)', '''
import math
r = (math.log(math.e), math.log(8, 2), math.log(100, 10))'''),
('M04', 'math', 'math.log10 e math.log2', '''
import math
r = (math.log10(1000), math.log2(8))'''),
('M05', 'math', 'math.sin(pi), cos, tan', '''
import math
r = (math.sin(math.pi), math.cos(math.pi), math.tan(math.pi / 4))'''),
('M06', 'math', 'asin, acos, atan, atan2', '''
import math
r = (math.asin(1), math.acos(0), math.atan(1), math.atan2(1, -1))'''),
('M07', 'math', 'degrees, radians', '''
import math
r = (math.degrees(math.pi), math.radians(180))'''),
('M08', 'math', 'hiperbolicas sinh cosh tanh asinh acosh atanh', '''
import math
r = (math.sinh(1), math.cosh(1), math.tanh(1), math.asinh(1), math.acosh(2), math.atanh(0.5))'''),
('M09', 'math', 'especiais erf erfc gamma lgamma expm1', '''
import math
r = (math.erf(1), math.erfc(1), math.gamma(5), math.lgamma(5), math.expm1(1e-10))'''),
('M10', 'math', 'fabs fmod copysign modf frexp ldexp', '''
import math
r = (math.fabs(-2), math.fmod(-7, 3), math.copysign(1, -0.0), math.modf(2.5), math.frexp(8), math.ldexp(1, 10))'''),
('M11', 'math', 'isfinite isinf isnan', '''
import math
r = (math.isfinite(1e308), math.isinf(1e308 * 10), math.isnan(float('nan')))'''),
('M12', 'math', 'math.factorial', '''import math; r = math.factorial(20)'''),
('M13', 'math', 'math.gcd', '''import math; r = math.gcd(12, 18)'''),
('M14', 'math', 'math.isclose', '''import math; r = math.isclose(0.1 + 0.2, 0.3)'''),
('M15', 'math', 'math.inf e math.nan', '''import math; r = (math.inf, math.nan)'''),
('M16', 'math', 'math.tau', '''import math; r = math.tau'''),
('M17', 'math', 'math.hypot', '''import math; r = math.hypot(3, 4)'''),
('M18', 'math', 'math.fsum', '''import math; r = math.fsum([0.1] * 10)'''),
('M19', 'math', 'math.comb / perm / prod / isqrt / dist', '''
import math
r = [n for n in ('comb', 'perm', 'prod', 'isqrt', 'dist', 'lcm', 'cbrt', 'exp2', 'remainder', 'ulp', 'nextafter') if hasattr(math, n)]'''),
('M20', 'math', 'math.sqrt(-1)', '''import math; r = math.sqrt(-1)'''),
('M21', 'math', 'math.log(0)', '''import math; r = math.log(0)'''),
('M22', 'math', 'math.acos(2)', '''import math; r = math.acos(2)'''),
('M23', 'math', 'math.exp(1000)', '''import math; r = math.exp(1000)'''),
('M24', 'math', 'math.floor(1e300) exato', '''import math; r = math.floor(1e300) == int(1e300)'''),
('M25', 'math', 'math.pow(-8, 1/3)', '''import math; r = math.pow(-8, 1 / 3)'''),
# -------------------------------------------------------------- random
('R01', 'random', 'funcoes do random', '''
import random
r = sorted(n for n in dir(random) if not n.startswith('_'))'''),
('R02', 'random', 'random.seed(1) reproduz sequencia', '''
import random
random.seed(1); a = [random.randint(1, 100) for i in range(5)]
random.seed(1); b = [random.randint(1, 100) for i in range(5)]
r = a == b'''),
('R03', 'random', 'random.shuffle / sample / gauss / choices', '''
import random
r = [n for n in ('shuffle', 'sample', 'gauss', 'choices', 'triangular', 'normalvariate') if hasattr(random, n)]'''),
('R04', 'random', 'randrange com passo', '''
import random
random.seed(3)
r = all(random.randrange(0, 10, 2) % 2 == 0 for i in range(50))'''),
('R05', 'random', 'random.seed() sem argumento', '''
import random
random.seed()
r = 'aceito' '''),
# -------------------------------------------------- texto e formatacao
('F01', 'texto', '% com .2f d s r', '''r = '%5.2f|%d|%s|%r' % (3.14159, 42, 'a', 'b')'''),
('F02', 'texto', '% com x o e g', '''r = '%x %o %e %g' % (255, 8, 12345.678, 0.00001)'''),
('F03', 'texto', '% alinhamento e zeros', '''r = '%-5s|%05d|%+d' % ('ab', 42, 5)'''),
('F04', 'texto', '% com dicionario %(a)s', '''r = '%(a)s-%(b)d' % {'a': 'x', 'b': 2}'''),
('F05', 'texto', 'format posicional e nomeado', '''r = ('{} {}'.format(1, 2), '{0}{1}{0}'.format('a', 'b'), '{x}'.format(x=1))'''),
('F06', 'texto', 'format alinhamento < > ^ e preenchimento', '''r = ('{:>8}|'.format('ab'), '{:<8}|'.format('ab'), '{:^8}|'.format('ab'), '{:*^9}'.format('ab'))'''),
('F07', 'texto', 'format f e g %', '''r = ('{:.3f}'.format(2 / 3), '{:10.4f}'.format(3.14159), '{:e}'.format(12345.678), '{:g}'.format(1e-5), '{:%}'.format(0.25))'''),
('F08', 'texto', 'format separador de milhar {:,}', '''r = '{:,}'.format(1234567)'''),
('F09', 'texto', 'format sinal e zeros', '''r = ('{:08.3f}'.format(-3.14159), '{:+d}'.format(5), '{:05d}'.format(42))'''),
('F10', 'texto', 'format b x #x o', '''r = ('{:b}'.format(10), '{:x}'.format(255), '{:#x}'.format(255), '{:o}'.format(8))'''),
('F11', 'texto', 'format com indice {0[1]}', '''r = '{0[1]}'.format([5, 6])'''),
('F12', 'texto', 'format com atributo {a.real}', '''r = '{a.real}'.format(a=3)'''),
('F13', 'texto', 'format !r e !s', '''r = ('{!r}'.format('x'), '{!s}'.format(1.5))'''),
('F14', 'texto', 'format() embutido', '''r = (format(3.14159, '.2f'), format(255, 'x'), format(7, '03d'))'''),
('F15', 'texto', 'format de largura padrao numero x texto', '''r = ('{:5}|'.format(3), '{:5}|'.format('a'))'''),
('F16', 'texto', 'str.ljust / rjust', '''r = ('ab'.ljust(5) + '|', 'ab'.rjust(5))'''),
('F17', 'texto', 'str.center / zfill', '''r = ('ab'.center(6) + '|', '42'.zfill(5))'''),
('F18', 'texto', 'str.title / capitalize / swapcase', '''r = ('ola mundo'.title(), 'ola'.capitalize(), 'Ab'.swapcase())'''),
('F19', 'texto', 'split basico', '''r = ('a,b,,c'.split(','), 'a b  c'.split(), 'a b c'.split(None, 1))'''),
('F20', 'texto', "rsplit(None, 1)", '''r = 'a b c'.rsplit(None, 1)'''),
('F21', 'texto', "rsplit(',', 1)", '''r = 'a,b,c'.rsplit(',', 1)'''),
('F22', 'texto', 'strip com caracteres', '''r = (' x '.strip(), 'xxhixx'.strip('x'), '..a'.lstrip('.'), 'a..'.rstrip('.'))'''),
('F23', 'texto', 'find rfind index count replace', '''s = 'hello'; r = (s.find('l'), s.rfind('l'), s.index('e'), s.count('l'), s.replace('l', 'L', 1))'''),
('F24', 'texto', 'startswith(tupla)', '''r = 'hello'.startswith(('he', 'x'))'''),
('F25', 'texto', 'endswith com inicio e fim', '''r = 'hello'.endswith('ll', 0, 4)'''),
('F26', 'texto', 'partition / rpartition', '''r = ('a=b=c'.partition('='), 'a=b=c'.rpartition('='))'''),
('F27', 'texto', 'isdigit isalpha isspace isupper islower', '''r = ('12'.isdigit(), 'ab'.isalpha(), ' '.isspace(), 'AB'.isupper(), 'ab'.islower())'''),
('F28', 'texto', 'isalnum isdecimal isnumeric isidentifier', '''r = [m for m in ('isalnum', 'isdecimal', 'isnumeric', 'isidentifier', 'isprintable', 'istitle') if hasattr('', m)]'''),
('F29', 'texto', 'fatiamento com passo s[::-1] e s[1:5:2]', '''s = 'abcdef'; r = (s[::-1], s[1:5:2])'''),
('F30', 'texto', 'join, * e in', '''r = ('-'.join(['a', 'b']), 'ab' * 3, 'b' in 'abc')'''),
('F31', 'texto', 'len de texto acentuado', '''r = len('\\u00e9')'''),
('F32', 'texto', 'encode / decode', '''r = ('\\u00e9'.encode(), b'ab'.decode(), str(b'ab', 'utf8'))'''),
('F33', 'texto', 'str.format_map', '''r = '{a}'.format_map({'a': 1})'''),
('F34', 'texto', 'str.casefold / expandtabs / splitlines', '''r = [m for m in ('casefold', 'expandtabs', 'splitlines', 'translate', 'maketrans', 'removeprefix') if hasattr('', m)]'''),
('F35', 'texto', "'%.20f' % 0.1 (digitos alem da precisao)", '''r = '%.20f' % 0.1'''),
('F36', 'texto', "'{:.17g}'.format(0.1)", '''r = '{:.17g}'.format(0.1)'''),
('F37', 'texto', 'str() e repr() de complexo', '''r = (str(3 + 4j), repr(1j), str(complex(1, 0)))'''),
('F38', 'texto', 'ord / chr / chr(233)', '''r = (ord('A'), chr(65), chr(233))'''),
('F39', 'texto', 'bin oct hex', '''r = (bin(10), oct(8), hex(255), hex(-1))'''),
('F40', 'texto', 'splitlines', '''r = 'a\\nb\\r\\nc'.splitlines()'''),
# ------------------------------------------------------------ colecoes
('C01', 'colecoes', 'ordem de insercao do dict (texto)', '''
d = {}
for k in ['zeta', 'alfa', 'mike', 'bravo', 'x', 'a', 'kilo', 'eco']:
    d[k] = 1
r = list(d)'''),
('C02', 'colecoes', 'ordem de insercao do dict (inteiros)', '''
d = {}
for k in [50, 3, 9, 1, 27, 100]:
    d[k] = 0
r = list(d)'''),
('C03', 'colecoes', 'ordem de iteracao do set', '''r = list({50, 3, 9, 1, 27, 100})'''),
('C04', 'colecoes', 'visoes keys/items', '''d = {'a': 1}; r = (type(d.keys()).__name__, 'a' in d.keys(), list(d.items()))'''),
('C05', 'colecoes', 'dict: setdefault get pop popitem', '''d = {'a': 1}; r = (d.setdefault('b', 2), d.get('z', 0), d.pop('a'), d.pop('q', 'padrao'), d.popitem(), d)'''),
('C06', 'colecoes', 'dict: update(chaves) fromkeys copy', '''d = {}; d.update(a=1); r = (d, sorted(dict.fromkeys('ab', 0).items()), d.copy() == d)'''),
('C07', 'colecoes', 'dict(a=1), dict(pares), dict(zip())', '''r = (sorted(dict(a=1, b=2).items()), dict([('a', 1)]), sorted(dict(zip('ab', [1, 2])).items()))'''),
('C08', 'colecoes', 'list: sort(key, reverse), copy, clear', '''
l = ['bb', 'a', 'ccc']
l.sort(key=len, reverse=True)
m = l.copy(); m.clear()
r = (l, m)'''),
('C09', 'colecoes', 'list: index(x, inicio), insert, pop(0)', '''l = [1, 2, 1, 3]; r = (l.index(1, 1), l.insert(-1, 9), l, l.pop(0), l)'''),
('C10', 'colecoes', 'atribuicao em fatia l[1:3] = [...]', '''l = [0, 1, 2, 3, 4]; l[1:3] = ['a']; r = l'''),
('C11', 'colecoes', 'atribuicao em fatia com passo l[::2]', '''l = [0, 1, 2, 3, 4]; l[::2] = [9, 9, 9]; r = l'''),
('C12', 'colecoes', 'del l[::2]', '''l = [0, 1, 2, 3, 4]; del l[::2]; r = l'''),
('C13', 'colecoes', 'lista aninhada com * (aliasing)', '''m = [[0] * 2] * 2; m[0][0] = 1; r = m'''),
('C14', 'colecoes', 'tupla: count index e fatia com passo', '''t = (1, 2, 1, 3); r = (t.count(1), t.index(3), t[::2])'''),
('C15', 'colecoes', 'set: operadores e metodos', '''a = {1, 2, 3}; b = {2, 3, 4}; r = (sorted(a | b), sorted(a & b), sorted(a - b), sorted(a ^ b), a <= a | b, {1}.issubset(a))'''),
('C16', 'colecoes', 'set.remove de ausente', '''s = {1}; s.remove(9)'''),
('C17', 'colecoes', 'frozenset', '''r = sorted(frozenset([3, 1, 2]))'''),
('C18', 'colecoes', 'sorted estavel com key', '''r = sorted([('b', 1), ('a', 1), ('c', 0)], key=lambda t: t[1])'''),
('C19', 'colecoes', 'sorted de tipos mistos', '''r = sorted([1, 'a'])'''),
('C20', 'colecoes', 'range: fatia, in, len, indice negativo, ==', '''x = range(10); r = (x[2:5], 5 in x, len(range(0, 10, 3)), x[-1], range(3) == range(3))'''),
('C21', 'colecoes', 'bytes e bytearray', '''b = bytearray(b'ab'); b[0] = 65; r = (bytes(b), list(b'az'), b'ab' + b'c')'''),
('C22', 'colecoes', 'memoryview', '''r = bytes(memoryview(b'abc')[1:])'''),
('C23', 'colecoes', 'slice() objeto', '''r = [0, 1, 2, 3, 4][slice(1, 4, 2)]'''),
('C24', 'colecoes', 'lista: pop de vazia', '''[].pop()'''),
('C25', 'colecoes', 'dict: chave lista (nao hashavel)', '''r = {[1]: 2}'''),
# ------------------------------------------------------- funcoes embutidas
('B01', 'builtins', 'enumerate(start=1)', '''r = list(enumerate('ab', start=1))'''),
('B02', 'builtins', 'zip de tamanhos diferentes', '''r = list(zip([1, 2, 3], 'ab'))'''),
('B03', 'builtins', 'map com 2 iteraveis', '''r = list(map(lambda a, b: a + b, [1, 2], [10, 20]))'''),
('B04', 'builtins', 'filter(None, ...)', '''r = list(filter(None, [0, 1, '', 'a', None]))'''),
('B05', 'builtins', 'min(key=) max(default=)', '''r = (min(['bb', 'a'], key=len), max([], default=-1))'''),
('B06', 'builtins', 'sum com inicio (listas)', '''r = sum([[1], [2]], [])'''),
('B07', 'builtins', 'any / all', '''r = (any([0, 0, 1]), all([]))'''),
('B08', 'builtins', 'reversed de lista, range e str', '''r = (list(reversed([1, 2])), list(reversed(range(3))), list(reversed('ab')))'''),
('B09', 'builtins', 'isinstance com tupla, issubclass', '''r = (isinstance(1, (int, float)), issubclass(bool, int))'''),
('B10', 'builtins', 'getattr/setattr/hasattr/delattr', '''
class A:
    pass
a = A(); setattr(a, 'x', 1)
r = (getattr(a, 'x'), getattr(a, 'y', 'padrao'), hasattr(a, 'x'))
delattr(a, 'x')
r = r + (hasattr(a, 'x'),)'''),
('B11', 'builtins', 'type(nome, bases, dict)', '''X = type('X', (), {'a': 1}); r = (X.a, X.__name__)'''),
('B12', 'builtins', 'vars()', '''
class A:
    pass
a = A(); a.x = 1
r = vars(a)'''),
('B13', 'builtins', 'callable, id, hash', '''r = (callable(len), type(id(1)).__name__, hash('a') == hash('a'))'''),
('B14', 'builtins', 'eval e exec', '''ns = {}; exec('z = 2 + 3', ns); r = (eval('1 + 2'), ns['z'])'''),
('B15', 'builtins', 'compile()', '''r = eval(compile('1 + 1', '<s>', 'eval'))'''),
('B16', 'builtins', 'iter(callable, sentinela)', '''
it = iter([3, 2, 1, 0, 5])
r = list(iter(lambda: next(it), 0))'''),
('B17', 'builtins', 'next(gerador, padrao)', '''r = next(iter([]), 'vazio')'''),
('B18', 'builtins', 'sorted(dict) e max(dict, key=dict.get)', '''d = {'a': 3, 'b': 5}; r = (sorted(d), max(d, key=d.get))'''),
('B19', 'builtins', 'print aceita sep, end e file', '''
import sys
r = 'print(sep=, end=) ok' '''),
('B20', 'builtins', 'ascii()', '''r = ascii('\\u00e9')'''),
('B21', 'builtins', 'divmod de float', '''r = divmod(7.5, 2)'''),
('B22', 'builtins', 'globals() e locals() na funcao', '''
def f():
    v = 1
    return 'v' in locals()
r = (f(), 'f' in globals())'''),
('B23', 'builtins', '__import__', '''r = __import__('math').floor(1.5)'''),
('B24', 'builtins', 'help() existe', '''r = callable(help)'''),
('B25', 'builtins', 'open() existe', '''r = callable(open)'''),
# -------------------------------------------------------------- classes
('O01', 'classes', 'super() sem argumentos', '''
class A:
    def f(self):
        return 'A'
class B(A):
    def f(self):
        return 'B' + super().f()
r = B().f()'''),
('O02', 'classes', 'property com setter', '''
class T:
    def __init__(self):
        self._c = 0
    @property
    def c(self):
        return self._c
    @c.setter
    def c(self, v):
        self._c = v * 2
t = T(); t.c = 5
r = t.c'''),
('O03', 'classes', 'classmethod e staticmethod', '''
class A:
    n = 1
    @classmethod
    def cm(cls):
        return cls.n
    @staticmethod
    def sm(x):
        return x + 1
r = (A.cm(), A.sm(1), A().cm())'''),
('O04', 'classes', '__str__ e __repr__', '''
class P:
    def __str__(self):
        return 'str'
    def __repr__(self):
        return 'repr'
r = (str(P()), repr(P()), str([P()]))'''),
('O05', 'classes', '__eq__ e __lt__ (ordenar objetos)', '''
class V:
    def __init__(self, v):
        self.v = v
    def __lt__(self, o):
        return self.v < o.v
    def __eq__(self, o):
        return self.v == o.v
r = ([x.v for x in sorted([V(2), V(1), V(3)])], V(1) == V(1))'''),
('O06', 'classes', '__eq__ sem __hash__ torna nao hashavel?', '''
class V:
    def __eq__(self, o):
        return True
r = len({V(), V()})'''),
('O07', 'classes', '__radd__ (operador refletido)', '''
class V:
    def __radd__(self, o):
        return 'radd'
r = 1 + V()'''),
('O08', 'classes', '__add__ e __iadd__', '''
class V:
    def __init__(self, v):
        self.v = v
    def __add__(self, o):
        return V(self.v + o.v)
    def __iadd__(self, o):
        self.v += 100 * o.v
        return self
a = V(1); b = a + V(2); a += V(1)
r = (b.v, a.v)'''),
('O09', 'classes', '__len__ __getitem__ __contains__ __iter__', '''
class S:
    def __len__(self):
        return 3
    def __getitem__(self, i):
        if i >= 3:
            raise IndexError
        return i * 10
    def __contains__(self, x):
        return x == 'q'
s = S()
r = (len(s), s[1], 'q' in s, list(s))'''),
('O10', 'classes', '__call__ e __bool__', '''
class F:
    def __call__(self, x):
        return x * 2
    def __bool__(self):
        return False
r = (F()(4), bool(F()))'''),
('O11', 'classes', '__getattr__ (fallback)', '''
class G:
    def __getattr__(self, n):
        return 'auto_' + n
r = G().qualquer'''),
('O12', 'classes', '__setattr__ sobrescrito', '''
class G:
    def __setattr__(self, n, v):
        object.__setattr__(self, n, v * 2)
g = G(); g.x = 2
r = g.x'''),
('O13', 'classes', '__del__ chamado ao apagar', '''
log = []
class D:
    def __del__(self):
        log.append('del')
d = D(); del d
r = log'''),
('O14', 'classes', 'heranca multipla (MRO em diamante)', '''
class A:
    def f(self):
        return 'A'
class B(A):
    pass
class C(A):
    def f(self):
        return 'C'
class D(B, C):
    pass
r = D().f()'''),
('O15', 'classes', '__slots__ restringe atributos?', '''
class A:
    __slots__ = ('x',)
a = A(); a.y = 1
r = a.y'''),
('O16', 'classes', 'name mangling de __x', '''
class A:
    def __init__(self):
        self.__x = 1
r = hasattr(A(), '_A__x')'''),
('O17', 'classes', 'atributo em funcao f.x = 1', '''
def f():
    pass
f.x = 1
r = f.x'''),
('O18', 'classes', '__dict__ da instancia', '''
class A:
    def __init__(self):
        self.x = 1
r = A().__dict__'''),
('O19', 'classes', '__class__ e __name__', '''
class A:
    pass
r = (A().__class__.__name__, A.__name__)'''),
('O20', 'classes', '__qualname__ e __module__', '''
class A:
    pass
r = (getattr(A, '__qualname__', 'ausente'), getattr(A, '__module__', 'ausente'))'''),
('O21', 'classes', 'subclasse de int', '''
class I(int):
    pass
r = I(5) + 1'''),
('O22', 'classes', 'subclasse de list com metodo', '''
class L(list):
    def soma(self):
        return sum(self)
r = L([1, 2, 3]).soma()'''),
('O23', 'classes', '__init_subclass__', '''
class A:
    reg = []
    def __init_subclass__(cls):
        A.reg.append(cls.__name__)
class B(A):
    pass
r = A.reg'''),
('O24', 'classes', '__neg__ __abs__ __mul__ __truediv__', '''
class V:
    def __init__(self, v):
        self.v = v
    def __neg__(self):
        return V(-self.v)
    def __abs__(self):
        return 'abs'
    def __mul__(self, k):
        return V(self.v * k)
    def __truediv__(self, k):
        return V(self.v / k)
r = ((-V(2)).v, abs(V(1)), (V(2) * 3).v, (V(3) / 2).v)'''),
('O25', 'classes', '__getitem__ com fatia', '''
class S:
    def __getitem__(self, i):
        return i
x = S()[1:3]
r = (type(x).__name__, x.start, x.stop)'''),
('O26', 'classes', '__hash__ proprio em dict', '''
class K:
    def __init__(self, v):
        self.v = v
    def __hash__(self):
        return self.v
    def __eq__(self, o):
        return self.v == o.v
r = {K(1): 'a'}[K(1)]'''),
('O27', 'classes', 'descritor __get__', '''
class D:
    def __get__(self, obj, tipo):
        return 'desc'
class A:
    x = D()
r = A().x'''),
('O28', 'classes', 'variavel de classe x de instancia', '''
class A:
    l = []
a, b = A(), A()
a.l.append(1)
r = b.l'''),
# ----------------------------------------------------------- excecoes
('E01', 'excecoes', 'repr de excecao com argumento', '''r = repr(ValueError('x'))'''),
('E02', 'excecoes', 'str(KeyError("k"))', '''r = str(KeyError('k'))'''),
('E03', 'excecoes', 'excecao propria com atributos', '''
class Erro(Exception):
    def __init__(self, cod):
        super().__init__('codigo %d' % cod)
        self.cod = cod
try:
    raise Erro(7)
except Erro as e:
    r = (e.cod, str(e), e.args)'''),
('E04', 'excecoes', 'e.__traceback__', '''
try:
    1 / 0
except Exception as e:
    r = hasattr(e, '__traceback__')'''),
('E05', 'excecoes', 'RecursionError existe', '''r = RecursionError.__name__'''),
('E06', 'excecoes', 'tipo e mensagem ao estourar recursao', '''
def f(n):
    return f(n + 1)
try:
    f(0)
except Exception as e:
    r = (type(e).__name__, str(e))'''),
('E07', 'excecoes', 'SystemExit e BaseException', '''r = (issubclass(SystemExit, BaseException), issubclass(SystemExit, Exception))'''),
('E08', 'excecoes', 'KeyboardInterrupt fora de Exception', '''r = issubclass(KeyboardInterrupt, Exception)'''),
('E09', 'excecoes', 'mensagem NameError', '''nao_definida'''),
('E10', 'excecoes', "mensagem TypeError 'a' + 1", '''r = 'a' + 1'''),
('E11', 'excecoes', 'mensagem AttributeError', '''r = (1).xyz'''),
('E12', 'excecoes', 'mensagem IndexError', '''r = [][0]'''),
('E13', 'excecoes', 'mensagem KeyError', '''r = {}['k']'''),
('E14', 'excecoes', 'mensagem ValueError int("x")', '''r = int('x')'''),
('E15', 'excecoes', 'mensagem ImportError', '''import modulo_que_nao_existe'''),
('E16', 'excecoes', 'mensagem de argumentos errados', '''
def f(a):
    pass
f()'''),
('E17', 'excecoes', 'UnboundLocalError', '''
x = 1
def f():
    x += 1
f()'''),
('E18', 'excecoes', 'SyntaxError via exec', '''exec('x = ')'''),
('E19', 'excecoes', 'IndentationError via exec', '''exec('if 1:\\nx = 1')'''),
('E20', 'excecoes', 'finally roda no return', '''
log = []
def f():
    try:
        return 'ret'
    finally:
        log.append('fin')
r = (f(), log)'''),
('E21', 'excecoes', 'except (A, B) as e', '''
try:
    [][1]
except (KeyError, IndexError) as e:
    r = type(e).__name__'''),
('E22', 'excecoes', 'excecoes embutidas presentes', '''
nomes = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'EOFError', 'Exception',
 'GeneratorExit', 'ImportError', 'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError',
 'MemoryError', 'NameError', 'NotImplementedError', 'OSError', 'OverflowError', 'RuntimeError', 'StopIteration',
 'SyntaxError', 'SystemExit', 'TypeError', 'UnboundLocalError', 'ValueError', 'ZeroDivisionError',
 'FileNotFoundError', 'RecursionError', 'TimeoutError', 'UnicodeError', 'ModuleNotFoundError', 'StopAsyncIteration',
 'Warning', 'UserWarning', 'IOError', 'EnvironmentError', 'PermissionError', 'FloatingPointError', 'ReferenceError']
r = [n for n in nomes if n not in dir(__import__('builtins'))]'''),
('E23', 'excecoes', 'excecao dentro de except (contexto)', '''
try:
    try:
        1 / 0
    except ZeroDivisionError:
        [][0]
except IndexError as e:
    r = getattr(e, '__context__', 'sem __context__')'''),
('E24', 'excecoes', 'str() de excecao sem argumentos', '''r = (str(ValueError()), repr(ValueError()))'''),
('E25', 'excecoes', 'mensagem OverflowError int grande em float', '''r = float(2 ** 2000)'''),
# ---------------------------------------------- geradores e iteradores
('G01', 'geradores', 'gerador send', '''
def g():
    x = yield 1
    yield x * 2
it = g(); next(it)
r = it.send(21)'''),
('G02', 'geradores', 'gerador close e throw', '''
def g():
    try:
        yield 1
    except ValueError:
        yield 'capturou'
it = g(); next(it)
r = it.throw(ValueError)
it.close()'''),
('G03', 'geradores', 'return em gerador (StopIteration.value)', '''
def g():
    yield 1
    return 'fim'
it = g(); next(it)
try:
    next(it)
except StopIteration as e:
    r = e.value'''),
('G04', 'geradores', 'protocolo de iterador proprio', '''
class C:
    def __init__(self):
        self.i = 0
    def __iter__(self):
        return self
    def __next__(self):
        self.i += 1
        if self.i > 3:
            raise StopIteration
        return self.i
r = list(C())'''),
('G05', 'geradores', 'zip(*matriz) transposicao', '''r = list(zip(*[[1, 2], [3, 4]]))'''),
('G06', 'geradores', 'expressao geradora em max/sum', '''r = (max(x * x for x in range(5)), sum(x for x in range(5) if x % 2))'''),
('G07', 'geradores', 'StopIteration dentro de gerador (PEP 479)', '''
def g():
    yield 1
    next(iter([]))
    yield 2
r = list(g())'''),
# ------------------------------------------------------ escopo e nomes
('V01', 'escopo', 'lambda em laco (late binding)', '''fs = [lambda: i for i in range(3)]; r = [f() for f in fs]'''),
('V02', 'escopo', 'argumento padrao mutavel', '''
def f(x, l=[]):
    l.append(x)
    return l
f(1)
r = f(2)'''),
('V03', 'escopo', '__name__ no namespace do exec', '''r = __name__'''),
('V04', 'escopo', 'variavel de compreensao nao vaza', '''
k = 'fora'
l = [k for k in range(3)]
r = k'''),
('V05', 'escopo', 'del de variavel e reuso', '''a = 1; del a; a = 2; r = a'''),
]


def rodar(codigo):
    ns = {'__name__': '__sonda__'}
    try:
        exec(codigo, ns)
    except BaseException as e:
        return 'ERRO', type(e).__name__ + ': ' + str(e)
    if 'r' in ns:
        try:
            return 'OK', repr(ns['r'])
        except BaseException as e:
            return 'OK', '<repr falhou: ' + type(e).__name__ + '>'
    return 'OK', ''


def main():
    for pid, cat, desc, cod in SONDAS:
        st, res = rodar(cod)
        res = res.replace('\n', '\\n').replace('\t', ' ')
        print(pid + '\t' + st + '\t' + res)


if __name__ == '__main__':
    main()
