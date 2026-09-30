# Limites práticos com heap de 100k — MicroPython 1.9.4 (32 bits)

Gerado por `sondas/rodar_limites.py` com `mpy194-teto -X heapsize=100k`. Cada linha roda em processo novo, para que lixo retido por ponteiros antigos na pilha (o GC é conservador) não contamine a medida seguinte. Variações de dezenas a poucas centenas de bytes entre execuções são normais: o coletor examina a pilha de forma conservadora, e a disposição dela muda a cada processo.

| Medida | Resultado |
|---|---|
| Heap livre no início (bytes) | 95488 livres de 100032 |
| Maior lista `[0]*n` (itens) | 22180 |
| Maior texto `'x'*n` (caracteres) | 88687 |
| Ints numa lista crescida com `append` | 16384 |
| Floats numa lista crescida com `append` | 4096 |
| Floats numa lista pré-alocada `[0]*5000` (máx. 5000) | 4718 |
| Textos de 8 caracteres numa lista | 2471 |
| Pares `int: int` num dict | 4831 |
| Heap fragmentado (blocos de 256 B, metade liberada) | 46544 livres, maior bloco 512 |
| Profundidade de recursão (pilha C da porta unix, não a da Casio) | simples 85, com 5 locais 82 |

## Menor heap que permite importar e executar um script

Busca binária sobre `-X heapsize`. Inclui a memória de compilação (árvore sintática e bytecode), que é o pico. A saída dos `print` vai para /dev/null.

| Script | Tamanho | Menor heap |
|---|---|---|
| exemplo do cofre OHM.py | 94 bytes | 3 KB |
| exemplo do cofre DISCRETO.py | 222 bytes | 4 KB |
| sintético, 50 linhas | 900 bytes | 6 KB |
| sintético, 150 linhas | 2750 bytes | 15 KB |
| sintético, 300 linhas | 5585 bytes | 28 KB |
| sintético, 600 linhas | 11255 bytes | 54 KB |
| sintético, 1200 linhas | 22780 bytes | 111 KB |
