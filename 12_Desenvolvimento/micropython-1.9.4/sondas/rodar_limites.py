#!/usr/bin/env python3
"""Roda sondas/limites_heap.py (um teste por processo) e mede o menor heap que
permite importar scripts de tamanhos diferentes. Grava resultados/limites_heap.md.

Uso: python3 sondas/rodar_limites.py [binario] [heap, ex.: 100k]
"""
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'bin', 'mpy194-teto')
HEAP = sys.argv[2] if len(sys.argv) > 2 else '100k'
SONDA = os.path.join(AQUI, 'sondas', 'limites_heap.py')
# Pasta com os exemplos do cofre (09_Anexos/Python); ajuste com a variável COFRE_PYTHON.
EXEMPLOS = os.environ.get('COFRE_PYTHON', os.path.join(AQUI, '..', '..', '09_Anexos', 'Python'))

DESCRICAO = {
    'heap': 'Heap livre no início (bytes)',
    'lista_zeros': 'Maior lista `[0]*n` (itens)',
    'texto': "Maior texto `'x'*n` (caracteres)",
    'ints_append': 'Ints numa lista crescida com `append`',
    'floats_append': 'Floats numa lista crescida com `append`',
    'floats_prealocados': 'Floats numa lista pré-alocada `[0]*5000` (máx. 5000)',
    'textos_8': 'Textos de 8 caracteres numa lista',
    'dict': 'Pares `int: int` num dict',
    'fragmentacao': 'Heap fragmentado (blocos de 256 B, metade liberada)',
    'recursao': 'Profundidade de recursão (pilha C da porta unix, não a da Casio)',
}


def rodar(args, heap, cwd=None):
    # O caminho do script ocupa heap (sys.argv, sys.path): rodar com nome relativo
    # deixa as medidas iguais em qualquer pasta.
    p = subprocess.run([MP, '-X', 'heapsize=' + heap] + args, capture_output=True, text=True,
                       timeout=300, cwd=cwd)
    return p.returncode, (p.stdout + p.stderr).strip()


def script_tipico(n_linhas):
    """Script com cara de programa de calculadora: funções, ifs, laços e prints."""
    linhas, i = [], 0
    while len(linhas) < n_linhas:
        linhas += [
            'def calc%d(x, y):' % i,
            '  if x > y:',
            '    r = x * %d + y / 2' % (i + 1),
            '  else:',
            '    r = (y - x) ** 2 + %d' % i,
            '  for k in range(3):',
            '    r = r + k * 0.5',
            '  return r',
            'v%d = calc%d(%d, %d)' % (i, i, i + 3, i + 1),
            'print("resultado %d =", v%d)' % (i, i),
        ]
        i += 1
    return '\n'.join(linhas[:n_linhas]) + '\n'


def menor_heap(caminho):
    lo, hi = 2, 400  # em KB
    pasta, nome = os.path.split(caminho)
    if rodar([nome], '%dk' % hi, pasta)[0] != 0:
        return None
    while lo < hi:
        meio = (lo + hi) // 2
        if rodar([nome], '%dk' % meio, pasta)[0] == 0:
            hi = meio
        else:
            lo = meio + 1
    return lo


def main():
    linhas = ['# Limites práticos com heap de %s — MicroPython 1.9.4 (32 bits)' % HEAP, '',
              'Gerado por `sondas/rodar_limites.py` com `%s -X heapsize=%s`. Cada linha roda em processo '
              'novo, para que lixo retido por ponteiros antigos na pilha (o GC é conservador) não contamine '
              'a medida seguinte. Variações de dezenas a poucas centenas de bytes entre execuções são normais: '
              'o coletor examina a pilha de forma conservadora, e a disposição dela muda a cada processo.'
              % (os.path.basename(MP), HEAP), '',
              '| Medida | Resultado |', '|---|---|']
    for nome in ['heap', 'lista_zeros', 'texto', 'ints_append', 'floats_append', 'floats_prealocados',
                 'textos_8', 'dict', 'fragmentacao', 'recursao']:
        cod, saida = rodar([os.path.basename(SONDA), nome], HEAP, cwd=os.path.dirname(SONDA))
        linhas.append('| %s | %s |' % (DESCRICAO[nome], saida if cod == 0 else 'falhou: ' + saida[-80:]))

    linhas += ['', '## Menor heap que permite importar e executar um script', '',
               'Busca binária sobre `-X heapsize`. Inclui a memória de compilação (árvore sintática e '
               'bytecode), que é o pico. A saída dos `print` vai para /dev/null.', '',
               '| Script | Tamanho | Menor heap |', '|---|---|---|']
    with tempfile.TemporaryDirectory() as d:
        alvos = []
        if os.path.isdir(EXEMPLOS):
            for nome in ('OHM.py', 'DISCRETO.py'):
                caminho = os.path.join(EXEMPLOS, nome)
                if os.path.exists(caminho):
                    alvos.append(('exemplo do cofre ' + nome, caminho))
        for n in (50, 150, 300, 600, 1200):
            caminho = os.path.join(d, 'tipico%d.py' % n)
            with open(caminho, 'w') as f:
                f.write(script_tipico(n))
            alvos.append(('sintético, %d linhas' % n, caminho))
        for rotulo, caminho in alvos:
            if 'exemplo' in rotulo:
                # exemplos pedem input(); troca por valores fixos
                with open(caminho) as f:
                    src = f.read().replace('input(', 'str(1) or (')
                copia = os.path.join(d, os.path.basename(caminho))
                with open(copia, 'w') as f:
                    f.write(src)
                caminho = copia
            tam = os.path.getsize(caminho)
            kb = menor_heap(caminho)
            linhas.append('| %s | %d bytes | %s |' % (rotulo, tam, ('%d KB' % kb) if kb else 'não coube em 400 KB'))
    saida = os.path.join(AQUI, 'resultados', 'limites_heap.md')
    with open(saida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas) + '\n')
    print('\n'.join(linhas))


if __name__ == '__main__':
    main()
