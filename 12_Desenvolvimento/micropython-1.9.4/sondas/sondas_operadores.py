# Quais metodos especiais (sobrecarga de operadores) o interpretador honra.
# Roda no CPython e no MicroPython 1.9.4. Saida: METODO<TAB>OK|FALHA<TAB>detalhe

CASOS = [
    # (metodo, expressao usando o objeto a e o numero 2)
    ('__add__', 'a + 2'), ('__sub__', 'a - 2'), ('__mul__', 'a * 2'),
    ('__truediv__', 'a / 2'), ('__floordiv__', 'a // 2'), ('__mod__', 'a % 2'),
    ('__pow__', 'a ** 2'), ('__matmul__', None),
    ('__and__', 'a & 2'), ('__or__', 'a | 2'), ('__xor__', 'a ^ 2'),
    ('__lshift__', 'a << 2'), ('__rshift__', 'a >> 2'),
    ('__radd__', '2 + a'), ('__rsub__', '2 - a'), ('__rmul__', '2 * a'),
    ('__rtruediv__', '2 / a'), ('__rpow__', '2 ** a'),
    ('__iadd__', 'IADD'), ('__isub__', 'ISUB'), ('__imul__', 'IMUL'),
    ('__neg__', '-a'), ('__pos__', '+a'), ('__abs__', 'abs(a)'), ('__invert__', '~a'),
    ('__lt__', 'a < 2'), ('__le__', 'a <= 2'), ('__gt__', 'a > 2'), ('__ge__', 'a >= 2'),
    ('__eq__', 'a == 2'), ('__ne__', 'a != 2'),
    ('__contains__', '2 in a'), ('__len__', 'len(a)'), ('__bool__', 'bool(a)'),
    ('__hash__', 'hash(a)'), ('__getitem__', 'a[2]'), ('__setitem__', 'SETITEM'),
    ('__delitem__', 'DELITEM'), ('__iter__', 'ITER'), ('__call__', 'a(2)'),
    ('__str__', 'str(a)'), ('__repr__', 'repr(a)'), ('__int__', 'int(a)'),
    ('__float__', 'float(a)'), ('__index__', '[0, 1, 2][a]'), ('__round__', 'round(a)'),
]

RETORNO = {'__bool__': 'True', '__len__': '5', '__hash__': '7', '__str__': "'S'", '__repr__': "'R'",
           '__int__': '9', '__float__': '1.5', '__index__': '1', '__contains__': 'True',
           '__iter__': 'iter([1, 2])'}


def testar(metodo, expr):
    ret = RETORNO.get(metodo, "'ok'")
    if metodo in ('__setitem__', '__delitem__'):
        corpo = '    def %s(self, *a):\n        self.log = %s\n' % (metodo, "'ok'")
    elif metodo.startswith('__i') and metodo in ('__iadd__', '__isub__', '__imul__'):
        corpo = '    def %s(self, o):\n        self.log = %s\n        return self\n' % (metodo, "'ok'")
    else:
        corpo = '    def %s(self, *o):\n        return %s\n' % (metodo, ret)
    cod = 'class A:\n' + corpo + 'a = A()\n'
    if expr is None:
        cod += 'r = eval("a @ 2")\n'
    elif expr == 'IADD':
        cod += 'a += 2\nr = a.log\n'
    elif expr == 'ISUB':
        cod += 'a -= 2\nr = a.log\n'
    elif expr == 'IMUL':
        cod += 'a *= 2\nr = a.log\n'
    elif expr == 'SETITEM':
        cod += 'a[0] = 1\nr = a.log\n'
    elif expr == 'DELITEM':
        cod += 'del a[0]\nr = a.log\n'
    elif expr == 'ITER':
        cod += 'r = list(a)\n'
    else:
        cod += 'r = ' + expr + '\n'
    ns = {}
    try:
        exec(cod, ns)
        return 'OK', repr(ns.get('r'))
    except BaseException as e:
        return 'FALHA', type(e).__name__ + ': ' + str(e)


if __name__ == '__main__':
    for metodo, expr in CASOS:
        st, det = testar(metodo, expr)
        print(metodo + '\t' + st + '\t' + det)
