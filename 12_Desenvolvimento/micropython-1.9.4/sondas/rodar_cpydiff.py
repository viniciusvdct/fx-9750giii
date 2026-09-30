#!/usr/bin/env python3
"""Roda os casos oficiais tests/cpydiff do MicroPython 1.9.4 (as diferenças em
relação ao CPython que o próprio projeto documenta) no CPython e nas variantes
teto e piso. Grava resultados/cpydiff.md.

Uso: python3 sondas/rodar_cpydiff.py PASTA_DO_CODIGO_1.9.4
"""
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, '_fonte-micropython-1.9.4'))
CASOS = os.path.join(FONTE, 'tests', 'cpydiff')
BIN = os.path.join(AQUI, 'bin')


def cabecalho(texto):
    m = re.match(r'\s*"""(.*?)"""', texto, re.S)
    campos = {}
    for linha in (m.group(1) if m else '').strip().splitlines():
        if ':' in linha:
            k, v = linha.split(':', 1)
            campos[k.strip()] = v.strip()
    return campos


def rodar(cmd, arq):
    # nome relativo (cwd = pasta dos casos): a saída não depende de onde o código foi clonado
    try:
        p = subprocess.run(cmd + [os.path.basename(arq)], capture_output=True, text=True, timeout=60, cwd=CASOS)
        saida = (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        saida = '(tempo esgotado)'
    saida = re.sub(r'File "[^"]*", ', '', saida)
    saida = re.sub(r' at 0x[0-9a-f]+>', '>', saida).replace(CASOS, '.')
    return saida.replace('\n', ' ⏎ ').replace('|', '\\|')[:300]


def main():
    linhas = ['# Diferenças documentadas pelo projeto (tests/cpydiff do 1.9.4)', '',
              'Gerado por `sondas/rodar_cpydiff.py`. Cada caso é um programa curto que o próprio projeto '
              'MicroPython mantém para documentar uma diferença em relação ao CPython. Descrição, causa e '
              'contorno vêm do cabeçalho original (em inglês).', '',
              '| Caso | Categoria | Descrição | Contorno | CPython | 1.9.4 teto | 1.9.4 piso |',
              '|---|---|---|---|---|---|---|']
    for nome in sorted(os.listdir(CASOS)):
        if not nome.endswith('.py'):
            continue
        arq = os.path.join(CASOS, nome)
        with open(arq, encoding='utf-8') as f:
            meta = cabecalho(f.read())
        res = [rodar([sys.executable], arq),
               rodar([os.path.join(BIN, 'mpy194-teto')], arq),
               rodar([os.path.join(BIN, 'mpy194-piso')], arq)]
        linhas.append('| `%s` | %s | %s | %s | %s | %s | %s |' % (
            nome[:-3], meta.get('categories', ''), meta.get('description', '').replace('|', '\\|'),
            meta.get('workaround', '').replace('|', '\\|'), *res))
    with open(os.path.join(AQUI, 'resultados', 'cpydiff.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas) + '\n')
    print('%d casos' % (len(linhas) - 6))


if __name__ == '__main__':
    main()
