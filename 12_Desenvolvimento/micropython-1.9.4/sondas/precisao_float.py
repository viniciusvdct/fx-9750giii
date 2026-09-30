#!/usr/bin/env python3
"""Mede a exatidão com que o MicroPython 1.9.4 LÊ (float("...") e literais) e
ESCREVE (repr/print) números de ponto flutuante, comparando com o CPython,
que arredonda corretamente nos dois sentidos.

Uso: python3 sondas/precisao_float.py [binario-micropython] [quantidade]
Grava resultados/precisao_float.md e .json.
"""
import json
import os
import random
import struct
import subprocess
import sys
import tempfile
from decimal import Decimal

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'bin', 'mpy194-teto')
N = int(sys.argv[2]) if len(sys.argv) > 2 else 20000

PROGRAMA_MP = r'''
import ustruct
def bits(x):
    return ustruct.unpack('<Q', ustruct.pack('<d', x))[0]
for s in open(ARQ):
    s = s.strip()
    x = float(s)
    r = repr(x)
    print(s, bits(x), r, bits(float(r)))
'''


def bits(x):
    return struct.unpack('<Q', struct.pack('<d', x))[0]


def de_bits(b):
    return struct.unpack('<d', struct.pack('<Q', b))[0]


def amostras(n, semente=1994):
    rnd = random.Random(semente)
    grupos = {}
    # Entradas "de calculadora": poucos dígitos, como o usuário digita.
    grupos['digitadas (1 a 6 dígitos)'] = [
        ('%.*f' % (rnd.randint(1, 4), rnd.uniform(0, 1000))).rstrip('0').rstrip('.') or '0'
        for _ in range(n)]
    # Números com 15 a 17 dígitos significativos em várias ordens de grandeza.
    grupos['longas (15 a 17 dígitos, 1e-10 a 1e10)'] = [
        '%.*e' % (rnd.randint(14, 16), rnd.uniform(1, 10) * 10 ** rnd.randint(-10, 10))
        for _ in range(n)]
    # Valores produzidos por contas: bits aleatórios em faixa moderada.
    grupos['resultados de contas (bits aleatórios)'] = [
        repr(de_bits(rnd.getrandbits(52) | ((1023 + rnd.randint(-30, 30)) << 52))) for _ in range(n)]
    return grupos


def rodar_mp(textos):
    with tempfile.TemporaryDirectory() as d:
        arq = os.path.join(d, 'numeros.txt')
        with open(arq, 'w') as f:
            f.write('\n'.join(textos))
        prog = os.path.join(d, 'p.py')
        with open(prog, 'w') as f:
            f.write('ARQ = %r\n' % arq + PROGRAMA_MP)
        out = subprocess.run([MP, '-X', 'heapsize=16M', prog], capture_output=True, text=True, timeout=600).stdout
    return [linha.split() for linha in out.splitlines()]


def analisar(textos):
    lidos_errados = ulps = escritos_errados = sem_volta = 0
    exemplos_leitura, exemplos_escrita = [], []
    linhas = rodar_mp(textos)
    if len(linhas) != len(textos):
        raise SystemExit('o MicroPython processou %d de %d números' % (len(linhas), len(textos)))
    for s, b_mp, r_mp, b_volta in linhas:
        b_mp, b_volta = int(b_mp), int(b_volta)
        certo = bits(float(s))
        if b_mp != certo:
            lidos_errados += 1
            ulps = max(ulps, abs(b_mp - certo))
            if len(exemplos_leitura) < 5:
                exemplos_leitura.append((s, repr(float(s)), repr(de_bits(b_mp))))
        # Escrita: o repr do MP deveria ser o valor (do próprio MP) arredondado a 16 dígitos.
        x_mp = de_bits(b_mp)
        if x_mp != 0 and Decimal(r_mp) != Decimal('%.15e' % x_mp):
            escritos_errados += 1
            if len(exemplos_escrita) < 5:
                exemplos_escrita.append((repr(x_mp), '%.15e' % x_mp, r_mp))
        if b_volta != b_mp:
            sem_volta += 1
    return {'n': len(textos), 'leitura_errada': lidos_errados, 'max_ulps': ulps,
            'escrita_errada_16dig': escritos_errados, 'repr_sem_ida_e_volta': sem_volta,
            'exemplos_leitura': exemplos_leitura, 'exemplos_escrita': exemplos_escrita}


def main():
    res = {nome: analisar(textos) for nome, textos in amostras(N).items()}
    os.makedirs(os.path.join(AQUI, 'resultados'), exist_ok=True)
    with open(os.path.join(AQUI, 'resultados', 'precisao_float.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    linhas = ['# Exatidão de leitura e escrita de floats — MicroPython 1.9.4', '',
              'Gerado por `sondas/precisao_float.py` com `%s`. Referência: CPython, que lê e escreve com '
              'arredondamento correto. "Leitura errada" = `float(texto)` do 1.9.4 difere do double mais próximo. '
              '"Escrita errada" = os 16 dígitos do `repr` do 1.9.4 diferem do valor arredondado corretamente. '
              '"Sem ida e volta" = `float(repr(x)) != x` no próprio 1.9.4.' % os.path.basename(MP), '',
              '| Amostra | n | Leitura errada | Máx. erro (ulps) | Escrita errada (16 díg.) | Sem ida e volta |',
              '|---|---|---|---|---|---|']
    for nome, r in res.items():
        pct = lambda k: '%d (%.1f%%)' % (r[k], 100.0 * r[k] / r['n'])
        linhas.append('| %s | %d | %s | %d | %s | %s |' % (
            nome, r['n'], pct('leitura_errada'), r['max_ulps'], pct('escrita_errada_16dig'),
            pct('repr_sem_ida_e_volta')))
    linhas += ['', '## Exemplos', '']
    for nome, r in res.items():
        for s, certo, mp in r['exemplos_leitura'][:3]:
            linhas.append('- Leitura (%s): `float("%s")` → CPython `%s`, 1.9.4 `%s`' % (nome, s, certo, mp))
        for x, certo, mp in r['exemplos_escrita'][:3]:
            linhas.append('- Escrita (%s): valor `%s`, 16 dígitos corretos `%s`, 1.9.4 escreve `%s`' % (
                nome, x, certo, mp))
    with open(os.path.join(AQUI, 'resultados', 'precisao_float.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas) + '\n')
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if not kk.startswith('exemplos')}
                      for k, v in res.items()}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
