#!/usr/bin/env python3
"""Extrai o bloco de código da seção 12 (Receitas) do estudo e confere que ele
roda e acerta no CPython e nas variantes teto e piso do MicroPython 1.9.4.
Mantém o texto do estudo honesto: se uma receita quebrar, este teste falha.

Uso: python3 sondas/testar_receitas.py
"""
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESTUDO = os.path.join(AQUI, '..', '..', '04_Programacao', 'MicroPython 1.9.4 - estudo aprofundado.md')

VERIFICACOES = '''
try:
    const
except NameError:
    const = lambda x: x
K = const(3)
assert K == 3
assert ljust('ab', 4) == 'ab  ' and rjust('ab', 4) == '  ab'
assert zfill('42', 5) == '00042' and zfill('-42', 5) == '-0042'
assert inverte('abc') == 'cba'
assert isalnum('a1') and not isalnum('a-1') and not isalnum('')
it = iter([1])
assert proximo(it) == 1 and proximo(it, 'fim') == 'fim'
assert fatorial(0) == 1 and fatorial(20) == 2432902008176640000
assert mdc(12, 18) == 6 and mdc(-12, 18) == 6
assert perto(0.1 + 0.2, 0.3) and not perto(1.0, 1.1)
assert hipot(3, 4) == 5.0
assert INF > 1e308 and NAN != NAN and abs(TAU - 6.283185307179586) < 1e-12
random.seed(7)
l = list(range(10))
embaralha(l)
assert sorted(l) == list(range(10))
a = amostra(range(10), 3)
assert len(a) == 3 and len(set(a)) == 3
v = [normal() for i in range(2000)]
assert abs(sum(v) / len(v)) < 0.15
assert fmt(538.2) == '538.2' and fmt(0.1 + 0.2) == '0.3' and fmt(159.15494309189535) == '159.155'
print('receitas ok')
'''


def main():
    texto = open(ESTUDO, encoding='utf-8').read()
    m = re.search(r'## 12\. Receitas.*?```python\n(.*?)```', texto, re.S)
    if not m:
        sys.exit('bloco de receitas não encontrado no estudo')
    programa = 'import math\nimport random\n' + m.group(1) + VERIFICACOES
    falhou = False
    with tempfile.TemporaryDirectory() as d:
        arq = os.path.join(d, 'receitas.py')
        with open(arq, 'w') as f:
            f.write(programa)
        for nome, cmd in (('cpython', [sys.executable]),
                          ('teto', [os.path.join(AQUI, 'bin', 'mpy194-teto')]),
                          ('piso', [os.path.join(AQUI, 'bin', 'mpy194-piso')])):
            p = subprocess.run(cmd + [arq], capture_output=True, text=True)
            ok = p.returncode == 0 and 'receitas ok' in p.stdout
            falhou = falhou or not ok
            print('%-8s %s' % (nome, 'ok' if ok else 'FALHOU\n' + p.stdout + p.stderr))
    sys.exit(1 if falhou else 0)


if __name__ == '__main__':
    main()
