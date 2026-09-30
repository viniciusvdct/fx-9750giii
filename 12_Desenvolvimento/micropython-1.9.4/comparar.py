#!/usr/bin/env python3
"""Roda as sondas de linguagem no CPython e nas variantes do MicroPython 1.9.4
e grava a comparação em resultados/.

Classificação de cada sonda:
  igual      CPython, teto e piso dão o mesmo resultado
  nucleo     teto e piso concordam entre si e diferem do CPython: é do 1.9.4,
             independe de como a Casio configurou a compilação
  config     teto e piso discordam: depende de opção de compilação; só o
             aparelho decide (ver 09_Anexos/Python/diagnostico)

Uso: python3 comparar.py   (depois de ./compilar.sh)
"""
import importlib.util
import json
import os
import platform
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SONDAS = os.path.join(AQUI, 'sondas', 'sondas_linguagem.py')
SAIDA = os.path.join(AQUI, 'resultados')

INTERPRETES = [
    ('cpython', [sys.executable]),
    ('teto', [os.path.join(AQUI, 'bin', 'mpy194-teto')]),
    ('piso', [os.path.join(AQUI, 'bin', 'mpy194-piso')]),
]

ROTULO = {'igual': 'igual ao CPython', 'nucleo': 'núcleo 1.9.4', 'config': 'depende da configuração'}


def carregar_sondas():
    spec = importlib.util.spec_from_file_location('sondas', SONDAS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SONDAS


def rodar(cmd):
    proc = subprocess.run(cmd + [SONDAS], capture_output=True, text=True, timeout=300,
                          encoding='utf-8', errors='replace')
    res, avisos = {}, []
    # endereços de memória mudam a cada execução: <D object at f7b43e10> -> <D object>
    saida = re.sub(r' object at (0x)?[0-9a-f]+>', ' object>', proc.stdout)
    for linha in saida.splitlines():
        partes = linha.split('\t')
        if len(partes) == 3:
            res[partes[0]] = (partes[1], partes[2])
        elif linha.strip():
            avisos.append(linha)
    return res, avisos


def celula(par):
    if par is None:
        return '—'
    st, txt = par
    txt = txt if st == 'OK' else '**' + txt + '**'
    return txt.replace('|', '\\|') or '(sem valor)'


def main():
    os.makedirs(SAIDA, exist_ok=True)
    sondas = carregar_sondas()
    saidas, avisos = {}, {}
    for nome, cmd in INTERPRETES:
        saidas[nome], avisos[nome] = rodar(cmd)

    linhas, dados, contagem = [], [], {'igual': 0, 'nucleo': 0, 'config': 0}
    for pid, cat, desc, cod in sondas:
        cp, te, pi = (saidas[n].get(pid) for n in ('cpython', 'teto', 'piso'))
        if te != pi:
            classe = 'config'
        elif te == cp:
            classe = 'igual'
        else:
            classe = 'nucleo'
        contagem[classe] += 1
        dados.append({'id': pid, 'categoria': cat, 'recurso': desc, 'codigo': cod.strip(),
                      'cpython': cp, 'teto': te, 'piso': pi, 'classe': classe})
        linhas.append('| %s | %s | %s | %s | %s | %s |' % (
            pid, desc.replace('|', '\\|'), celula(cp), celula(te), celula(pi), ROTULO[classe]))

    cab = [
        '# Sondas de linguagem — CPython × MicroPython 1.9.4',
        '',
        'Gerado por `comparar.py`. CPython %s; MicroPython 1.9.4 compilado em 32 bits nas variantes '
        '*teto* (porta unix) e *piso* (opções no padrão do núcleo). Texto em **negrito** = exceção levantada.'
        % platform.python_version(),
        '',
        'Resumo: %d sondas — %d iguais ao CPython, %d diferenças do núcleo 1.9.4, %d dependentes da configuração.'
        % (len(sondas), contagem['igual'], contagem['nucleo'], contagem['config']),
        '',
    ]
    for nome in ('teto', 'piso'):
        if avisos[nome]:
            cab.append('Mensagens fora do formato impressas pela variante %s: %s' % (
                nome, '; '.join('`%s`' % a for a in avisos[nome])))
            cab.append('')
    cab += ['| ID | Recurso | CPython | 1.9.4 teto | 1.9.4 piso | Classe |', '|---|---|---|---|---|---|']
    with open(os.path.join(SAIDA, 'sondas_linguagem.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(cab + linhas) + '\n')
    with open(os.path.join(SAIDA, 'sondas_linguagem.json'), 'w', encoding='utf-8') as f:
        json.dump({'cpython': platform.python_version(), 'contagem': contagem, 'sondas': dados},
                  f, ensure_ascii=False, indent=1)
    print(contagem)


if __name__ == '__main__':
    main()
