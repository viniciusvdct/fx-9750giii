#!/usr/bin/env python3
"""Roda um .py no MicroPython 1.9.4 imitando o modo PYTHON da fx-9750GIII.

O que é imitado (e de onde vem):
  - execução por `from NOME import *`, como o SHELL mostra ao rodar um arquivo
    (manual SW350, PDF 367): __name__ é o nome do módulo, não "__main__";
  - heap pequeno (padrão 100 KB, ordem de grandeza medida pela comunidade);
  - só math, random, casioplot e arquivos .py da mesma pasta podem ser importados
    (manual 14-11 e 14-31). As linhas import são conferidas antes de rodar; e,
    como o `import` do 1.9.4 não consulta builtins.__import__, os demais módulos
    embutidos viram fantasmas em sys.modules que levantam ImportError no primeiro uso;
  - conferência dos limites do editor (manual 14-4, 14-26 e 14-27): ASCII,
    até 150 linhas de até 127 caracteres, nome de até 8 caracteres;
  - input(): aviso quando o texto do prompt passa de 16 caracteres (manual 14-16).

O que NÃO é imitado: velocidade, pilha de recursão da Casio, fonte da tela,
mensagens de erro exatas da Casio e a configuração de compilação da Casio (use
--teto para a porta unix completa, ou o padrão --piso para o núcleo mínimo).

Uso:
  python3 rodar_como_casio.py CAMINHO/NOME.py [--teto] [--heap 100k] [--entradas "100;0.02"] [--pbm prefixo]
"""
import argparse
import keyword
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(os.path.dirname(AQUI), 'bin')

# Módulos embutidos do 1.9.4 (e nomes comuns do CPython) que a calculadora não
# oferece. "builtins" fica de fora: não há evidência sobre ele no aparelho.
FANTASMAS = ('sys gc micropython uos os utime time ustruct struct uio io ucollections collections '
             'uarray array ujson json ure re uzlib zlib uhashlib hashlib ubinascii binascii uheapq heapq '
             'uerrno errno uselect select usocket socket termios ffi framebuf machine btree websocket '
             'uctypes _thread cmath urandom').split()
PERMITIDOS = ('math', 'random', 'casioplot')

BOOT = r'''
import builtins
import sys
import uos
builtins.__casioplot_pbm__ = uos.getenv('CASIOPLOT_PBM')
_input_original = builtins.input


class _Fantasma:
    def __init__(self, nome):
        self._nome = nome

    def __getattr__(self, atributo):
        raise ImportError("no module named '%%s' (nao existe na calculadora)" %% self._nome)


for _n in %(fantasmas)r:
    sys.modules[_n] = _Fantasma(_n)


def _entrada(prompt=''):
    p = str(prompt)
    if len(p) > 16:
        print('[bancada] prompt com %%d caracteres: a calculadora mostra "%%s~"' %% (len(p), p[:15]))
    return _input_original(p)


builtins.input = _entrada
del _n, sys, uos
from %(modulo)s import *
'''

RESERVADAS = set(keyword.kwlist)


def conferir(caminho):
    """Avisos sobre o que o editor da calculadora não aceita."""
    avisos = []
    nome = os.path.splitext(os.path.basename(caminho))[0]
    if len(nome) > 8:
        avisos.append('nome "%s" tem %d caracteres; a calculadora mostra até 8 (ex.: %s~1)'
                      % (nome, len(nome), nome[:6].upper()))
    if not re.fullmatch(r'[A-Za-z0-9]+', nome):
        avisos.append('nome "%s" deve ter só letras e números para ser criado no aparelho' % nome)
    if nome[:1].isdigit():
        avisos.append('nome começando por número não roda (manual 14-2)')
    if nome in RESERVADAS or nome.lower() in RESERVADAS:
        avisos.append('nome igual a palavra reservada não roda (manual 14-2)')
    dados = open(caminho, 'rb').read()
    if any(b > 126 or (b < 32 and b not in (9, 10, 13)) for b in dados):
        avisos.append('há caracteres fora do ASCII: o editor não mostra o arquivo corretamente')
    linhas = dados.decode('utf-8', 'replace').splitlines()
    if len(linhas) > 150:
        avisos.append('%d linhas: abre com "Invalid Data Size" (máx. 150), mas pode rodar' % len(linhas))
    longas = [i + 1 for i, l in enumerate(linhas) if len(l) > 127]
    if longas:
        avisos.append('linhas com mais de 127 caracteres: %s' % longas[:10])
    if b'\t' in dados:
        avisos.append('há tabulações: ao abrir no aparelho cada uma vira 2 espaços')
    pasta = os.path.dirname(caminho)
    for n, linha in enumerate(linhas, 1):
        m = re.match(r'\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.,\s]+?)(?:\s+as\s+\w+)?\s*$)', linha)
        if not m:
            continue
        modulos = [m.group(1)] if m.group(1) else [x.strip().split()[0] for x in m.group(2).split(',')]
        for mod in modulos:
            base = mod.split('.')[0]
            if base not in PERMITIDOS and not os.path.exists(os.path.join(pasta, base + '.py')):
                avisos.append('linha %d importa "%s": na calculadora só math, random, casioplot e .py da '
                              'mesma pasta (ImportError)' % (n, base))
    return nome, avisos


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('script')
    ap.add_argument('--teto', action='store_true', help='usa a variante com todos os recursos opcionais')
    ap.add_argument('--heap', default='100k')
    ap.add_argument('--entradas', help='respostas para input(), separadas por ;')
    ap.add_argument('--pbm', help='grava cada show_screen() em PREFIXO_NNN.pbm')
    a = ap.parse_args()

    script = os.path.abspath(a.script)
    nome, avisos = conferir(script)
    for av in avisos:
        print('[bancada] aviso: ' + av)
    binario = os.path.join(BIN, 'mpy194-teto' if a.teto else 'mpy194-piso')
    if not os.path.exists(binario):
        sys.exit('binário ausente: %s (rode ../compilar.sh)' % binario)

    with tempfile.TemporaryDirectory() as d:
        pasta = os.path.dirname(script)
        for arq in os.listdir(pasta):
            if arq.endswith('.py'):
                shutil.copy(os.path.join(pasta, arq), d)
        if not os.path.exists(os.path.join(d, 'casioplot.py')):
            shutil.copy(os.path.join(AQUI, 'casioplot.py'), d)
        with open(os.path.join(d, '_boot.py'), 'w') as f:
            f.write(BOOT % {'modulo': nome, 'fantasmas': FANTASMAS})
        env = dict(os.environ)
        if a.pbm:
            env['CASIOPLOT_PBM'] = os.path.abspath(a.pbm)
        entrada = (a.entradas.replace(';', '\n') + '\n') if a.entradas is not None else None
        print('[bancada] %s -X heapsize=%s  >>> from %s import *' % (os.path.basename(binario), a.heap, nome))
        proc = subprocess.run([binario, '-X', 'heapsize=' + a.heap, '_boot.py'], cwd=d, env=env,
                              input=entrada, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    saida = proc.stdout.replace('File "_boot.py", line %d, in <module>\n' % (BOOT.count('\n')), '')
    print(saida, end='')
    largas = [l for l in saida.splitlines()
              if len(l) > 21 and not l.startswith(('[bancada]', '[casioplot]', '|', '+'))]
    if largas:
        print('[bancada] %d linha(s) de saída com mais de 21 caracteres: na tela do SHELL exigem rolagem lateral'
              % len(largas))
    sys.exit(proc.returncode)


if __name__ == '__main__':
    main()
