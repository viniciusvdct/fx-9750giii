#!/usr/bin/env python3
"""Roda sondas/desempenho.py no MicroPython 1.9.4 e no CPython e grava
resultados/desempenho.md com os custos relativos ao laço vazio."""
import os
import platform
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'bin', 'mpy194-teto')
SONDA = os.path.join(AQUI, 'sondas', 'desempenho.py')


def rodar(cmd):
    out = subprocess.run(cmd + [SONDA], capture_output=True, text=True, timeout=900).stdout
    return [(l.split('\t')[0], float(l.split('\t')[1])) for l in out.splitlines() if '\t' in l]


mp = rodar([MP, '-X', 'heapsize=8M'])
cp = rodar([sys.executable])
b_mp, b_cp = mp[0][1], cp[0][1]
linhas = ['# Custo relativo de construções — MicroPython 1.9.4 × CPython %s' % platform.python_version(), '',
          'Gerado por `sondas/rodar_desempenho.py`. Tempo por iteração dividido pelo do laço vazio '
          '`for i in range(N): pass` do mesmo interpretador (melhor de 3). Valores absolutos do PC não '
          'se aplicam à calculadora: lá a CPU é muito mais lenta e o ponto flutuante é emulado em software, '
          'o que torna as contas com float proporcionalmente mais caras.', '',
          '| Construção | 1.9.4 (× laço vazio) | CPython (× laço vazio) |', '|---|---|---|']
for (nome, t_mp), (_, t_cp) in zip(mp, cp):
    linhas.append('| %s | %.1f | %.1f |' % (nome.replace('|', '\\|'), t_mp / b_mp, t_cp / b_cp))
with open(os.path.join(AQUI, 'resultados', 'desempenho.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(linhas) + '\n')
print('\n'.join(linhas))
