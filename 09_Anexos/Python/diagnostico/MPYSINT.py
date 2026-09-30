# MPYSINT - quais recursos da linguagem funcionam
# Cada teste roda com exec(); so os que FALHAM sao
# listados. Significado de cada codigo: tabela do
# estudo MicroPython 1.9.4 (secao Diagnostico).
# N = nucleo 1.9.4 (esperado falhar no aparelho)
# C = depende de como a Casio compilou
T = [
  ('N01', "r=f'{1}'"),
  ('N02', "r=[(y:=1)]"),
  ('N03', "r='abc'[::-1]"),
  ('N04', "r=next(iter([]),0)"),
  ('N05', "d={}\nfor k in 'zeta alfa mike bravo x a'.split():\n d[k]=1\nassert list(d)[0]=='zeta'"),
  ('N06', "assert isinstance(True,int)"),
  ('N07', "r='a'.ljust(3)"),
  ('N08', "assert round(1234,-2)==1200"),
  ('N09', "r='{0[1]}'.format([5,6])"),
  ('N10', "r=[*[1],*[2]]"),
  ('N11', "r=1_000"),
  ('N12', "class A:\n __slots__=('x',)\na=A()\ntry:\n a.y=1\nexcept AttributeError:\n pass\nelse:\n raise Exception"),
  ('N13', "def f():\n pass\nf.x=1"),
  ('N14', "r=format(3,'d')"),
  ('N15', "assert 'hi'.startswith(('h','x'))"),
  ('N16', "r=RecursionError"),
  ('N17', "class M:\n def __matmul__(s,o):\n  return 1\nr=eval('M()@M()')"),
  ('N18', "assert (1).bit_length()==1"),
  ('N19', "r=complex('1+2j')"),
  ('N20', "r=dict(a=1).keys()\nassert type(r).__name__=='dict_keys'"),
  ('C01', "class V:\n def __mul__(s,o):\n  return 7\nr=V()*2"),
  ('C02', "class V:\n def __neg__(s):\n  return 7\nr=-V()"),
  ('C03', "class V:\n def __radd__(s,o):\n  return 7\nr=2+V()"),
  ('C04', "class V:\n def __truediv__(s,o):\n  return 7\nr=V()/2"),
  ('C05', "class D:\n def __get__(s,o,t):\n  return 7\nclass A:\n x=D()\nassert A().x==7"),
  ('C06', "class S:\n def __getitem__(s,i):\n  return i.start\nr=S()[1:2]"),
  ('C07', "r=pow(2,10,7)"),
  ('C08', "r='ab'.center(6)"),
  ('C09', "r='a=b'.partition('=')"),
  ('C10', "r='a\\nb'.splitlines()"),
  ('C11', "r=frozenset([1])"),
  ('C12', "r=memoryview(b'ab')"),
  ('C13', "r=compile('1','s','eval')"),
  ('C14', "r=help"),
  ('C15', "r=NotImplemented"),
  ('C16', "def f():\n pass\nr=f.__name__"),
  ('C17', "try:\n int('xyz')\nexcept ValueError as e:\n assert 'xyz' in str(e)"),
  ('C18', "assert len(chr(233).encode())==2"),
  ('C19', "class G:\n def __setattr__(s,n,v):\n  object.__setattr__(s,n,v*2)\ng=G()\ng.x=2\nassert g.x==4"),
  ('C20', "async def f():\n return 1"),
  ('C21', "r=bytearray(3)"),
  ('C22', "r=[1,2,3][::2]"),
  ('C23', "r=(1).to_bytes(2,'big')"),
  ('C24', "r=abs(3+4j)"),
]


def curto(e):
  n = type(e).__name__
  for a, b in (('Error', ''), ('NotImplemented', 'NotImpl'),
               ('Attribute', 'Attr'), ('Syntax', 'Synt')):
    n = n.replace(a, b)
  return n[:9]


print('== MPYSINT ==')
ok = 0
falhas = []
for cod, prog in T:
  try:
    exec(prog, {})
    ok = ok + 1
  except Exception as e:
    falhas.append(cod + ' ' + curto(e))
print('ok %d de %d' % (ok, len(T)))
print('falharam:')
for f in falhas:
  print(f)
print('-- aviso de exec. --')
print('se a proxima linha')
print('mostrar Warning, os')
print('avisos estao ligados')
try:
  exec("try:\n 1/0\nexcept ZeroDivisionError as e:\n raise ValueError from e", {})
except ValueError:
  pass
print('== fim ==')
