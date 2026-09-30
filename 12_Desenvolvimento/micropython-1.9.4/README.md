---
title: "Laboratório MicroPython 1.9.4"
model: fx-9750GIII
updated: 2026-09-30
status: experimental
tags: [casio, fx9750giii, python, micropython, desenvolvimento]
---
# Laboratório MicroPython 1.9.4

Material reprodutível do [[MicroPython 1.9.4 - estudo aprofundado|estudo do MicroPython 1.9.4]]. Compila o MicroPython 1.9.4 **oficial** — a versão do modo PYTHON da fx-9750GIII — e mede o comportamento da linguagem, dos números, da memória e do desempenho. Traz também uma bancada que roda um `.py` no PC imitando o jeito da calculadora.

Nada aqui é o firmware da Casio. O que o laboratório prova vale para o **núcleo** do MicroPython 1.9.4; o que depende de como a Casio compilou fica marcado e se confirma com os scripts de [`09_Anexos/Python/diagnostico`](../../09_Anexos/Python/diagnostico/LEIA-ME.md).

## Requisitos

Linux com `git`, `make`, `gcc`, `python3` (3.8+) e, para os binários de 32 bits, `gcc-multilib` (Debian/Ubuntu: `apt install gcc-multilib`). Testado com gcc 13.3 e CPython 3.11. No Windows, use o WSL.

## Passo a passo

```sh
./compilar.sh                          # baixa a tag v1.9.4 e gera bin/mpy194-{teto,piso,64}
python3 comparar.py                    # 268 sondas de linguagem → resultados/sondas_linguagem.md
python3 sondas/precisao_float.py       # leitura e escrita de floats → resultados/precisao_float.md
python3 sondas/rodar_limites.py        # limites com heap de 100 KB → resultados/limites_heap.md
python3 sondas/rodar_desempenho.py     # custo relativo → resultados/desempenho.md
python3 sondas/rodar_cpydiff.py _fonte-micropython-1.9.4   # casos oficiais → resultados/cpydiff.md
python3 sondas/testar_receitas.py      # confere as receitas da seção 12 do estudo
```

`compilar.sh` aceita uma pasta com o código já clonado (`./compilar.sh /caminho/micropython`); sem argumento, clona em `_fonte-micropython-1.9.4`. A pasta clonada e `bin/` não entram no repositório.

`rodar_limites.py` procura os exemplos do cofre em `09_Anexos/Python`; aponte outra pasta com a variável `COFRE_PYTHON`.

## As três variantes

| Binário | Configuração | Para quê |
|---|---|---|
| `mpy194-teto` | porta unix (quase todos os recursos opcionais ligados), 32 bits, double estrito, `random` completo | limite superior do que o aparelho pode ter |
| `mpy194-piso` | opções visíveis no padrão do núcleo, mais o que o manual documenta ([`bancada/mpconfigport_piso.h`](bancada/mpconfigport_piso.h)) | limite inferior; padrão da bancada |
| `mpy194-64` | porta unix em 64 bits | referência; não usada nos resultados |

Por que 32 bits: o SH4 da calculadora tem ponteiros de 4 bytes. O tamanho dos objetos no heap e a faixa de inteiros pequenos (±2³⁰) dependem disso. Por que `-msse2 -mfpmath=sse`: sem isso, o x87 do PC faz contas intermediárias com 80 bits e mascara os erros de leitura e escrita de floats. Com double estrito, o binário de 32 bits dá exatamente o mesmo resultado do de 64 bits.

Ajustes para compilar o código de 2018 com ferramentas atuais, todos em `compilar.sh`:

- avisos não viram erro;
- sem os submódulos opcionais (FFI, SSL, btree, threads);
- em 32 bits, NLR por `setjmp` e sem o emissor nativo x86 — o NLR em assembly quebra com gcc recente e causa falha de segmentação.

## Bancada: rodar um script como na calculadora

```sh
python3 bancada/rodar_como_casio.py CAMINHO/NOME.py [--teto] [--heap 100k] [--entradas "100;0.02"] [--pbm prefixo]
```

O que a bancada faz:

- executa `from NOME import *`, como o SHELL — então `__name__ == "NOME"`;
- usa heap de 100 KB;
- deixa importar só `math`, `random`, `casioplot` e arquivos `.py` da mesma pasta. Como o `import` do 1.9.4 não consulta `builtins.__import__`, os demais módulos viram fantasmas em `sys.modules` que levantam `ImportError` no primeiro uso, e as linhas `import` são conferidas antes;
- confere nome, ASCII, 150 linhas, 127 colunas, tabulações e prompts de `input()` com mais de 16 caracteres;
- conta as linhas de saída com mais de 21 colunas;
- emula o `casioplot` com [`bancada/casioplot.py`](bancada/casioplot.py): tela 128 × 64 no terminal e, com `--pbm`, arquivos PBM.

O que ela **não** reproduz: velocidade, pilha de recursão, fonte das letras, mensagens exatas e a configuração de compilação da Casio. Rode no piso (padrão) e no teto: se o resultado muda, o programa depende de uma opção que só o aparelho confirma.

## Resultados

| Arquivo | Conteúdo |
|---|---|
| [`resultados/sondas_linguagem.md`](resultados/sondas_linguagem.md) | 268 sondas: código, resultado no CPython, teto e piso, e classificação |
| [`resultados/sondas_linguagem.json`](resultados/sondas_linguagem.json) | o mesmo em JSON |
| [`resultados/precisao_float.md`](resultados/precisao_float.md) | taxa de erro na leitura e na escrita de floats |
| [`resultados/limites_heap.md`](resultados/limites_heap.md) | o que cabe em 100 KB e o heap para compilar scripts |
| [`resultados/desempenho.md`](resultados/desempenho.md) | custo relativo de construções comuns |
| [`resultados/cpydiff.md`](resultados/cpydiff.md) | os 43 casos de diferença documentados pelo projeto |
| [`resultados/suite_oficial.txt`](resultados/suite_oficial.txt) | suíte oficial: 494 de 508 no teto, com a explicação das 14 falhas |

`sondas/memoria.py` e `sondas/sondas_operadores.py` imprimem direto no terminal. Seus números estão nas seções 5.5 e 8.2 do estudo.

## Licenças

Os scripts deste laboratório seguem a licença MIT do cofre. O MicroPython é MIT (Damien P. George e outros) e não é redistribuído aqui: `compilar.sh` o baixa da fonte oficial. Os casos `tests/cpydiff` são lidos da cópia baixada.

[[00_Inicio/COMECE AQUI|Início]] · [[04_Programacao/MicroPython 1.9.4 - estudo aprofundado|Estudo MicroPython 1.9.4]]
