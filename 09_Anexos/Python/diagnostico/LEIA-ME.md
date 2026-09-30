---
title: "Diagnóstico do Python na fx-9750GIII"
model: fx-9750GIII
updated: 2026-09-30
status: experimental
firmware_reference: "3.50; consulte Sistema e firmware para 3.70"
tags: [casio, fx9750giii, python, micropython, diagnostico]
---
# Diagnóstico do Python na fx-9750GIII

Cinco scripts que respondem, **no aparelho**, o que o [[MicroPython 1.9.4 - estudo aprofundado|estudo do MicroPython 1.9.4]] não pôde medir no PC: a configuração com que a Casio compilou o interpretador, o heap livre, a profundidade de recursão e a velocidade.

Foram testados na bancada do PC (MicroPython 1.9.4 oficial, variantes *piso* e *teto*, heap de 100 KB) e, `MPYSINT` e `MPYNUM`, também no CPython. **Ainda não rodaram numa calculadora.**

| Arquivo | Linhas | O que responde | Tempo esperado |
|---|---|---|---|
| `MPYINFO.py` | 115 | módulos, nomes embutidos, `math`, `random`, `casioplot`, métodos de `str`, semente aleatória | segundos |
| `MPYSINT.py` | 84 | 44 recursos da linguagem: 20 do núcleo e 24 dependentes da compilação | segundos |
| `MPYNUM.py` | 71 | aritmética de ponto flutuante, `round`, estouros, complexos | segundos |
| `MPYMEM.py` | 76 | maior lista, recursão máxima, heap livre estimado | alguns segundos |
| `MPYVEL.py` | 81 | velocidade relativa, com cronômetro | minutos |

Todos são ASCII, têm nome de até 8 caracteres, até 150 linhas de até 127 colunas e imprimem linhas de até 21 colunas — dá para abrir e editar no próprio aparelho.

## Como rodar

1. Anote a versão do sistema: SYSTEM → VERSION ([[Sistema e firmware]]).
2. Copie os `.py` para a calculadora pelo USB, na raiz ou numa pasta — não em `@MainMem` ([[USB e arquivos]]).
3. Entre em PYTHON, selecione o arquivo e aperte RUN (ou EXE). Rode cada um logo após abrir o PYTHON, para o heap estar limpo.
4. Role o SHELL com as setas e anote a saída. O histórico guarda 100 linhas; nenhum script passa disso.
5. `MPYINFO` tem uma chave no topo, `TESTAR_TURTLE = False`. Com `True`, também importa `turtle` e `matplotl`, se estiverem instalados na mesma pasta.

## MPYINFO — inventário

| Linha | Esperado no 1.9.4 | Observação | Aparelho |
|---|---|---|---|
| `sys:` | `nao existe` | a comunidade relata só `math`, `random`, `casioplot` | |
| `mod sim:` | `math random casioplot` | `builtins` é incerto | |
| `mod nao:` | `sys gc time utime cmath micropython array collections…` | qualquer módulo além dos documentados é novidade | |
| `sem:` | núcleo: `format vars RecursionError`; também `compile frozenset help memoryview NotImplemented UnicodeError` se a Casio usou o padrão do núcleo | cada nome a menos na lista indica uma opção ligada | |
| `dir(math):` | `42` com as funções especiais (40 nomes, mais `__name__` e `__class__`) | `log10` é documentado; outro número indica módulo alterado | |
| `math sem:` | `factorial gcd isclose inf nan tau hypot` | se aparecerem `log2`, `cosh`, `erf` ou `gamma`, as funções especiais foram cortadas | |
| `dir(random):` | `9` | | |
| `random:` | `choice getrandbits randint random randrange seed uniform` | | |
| `rand1:` | na bancada, `0.689459` em toda execução | rode duas vezes: se o valor se repetir, a semente inicial é fixa; se for igual ao da bancada, o gerador é o mesmo | |
| `casioplot:` | `clear_screen draw_string get_pixel set_pixel show_screen` | nomes a mais seriam funções não documentadas | |
| `str sem:` | núcleo: `ljust rjust zfill title capitalize isalnum`; também `center partition rpartition splitlines` no padrão do núcleo | | |

## MPYSINT — recursos da linguagem

Mostra `ok N de 44` e a lista do que **falhou**, com o tipo do erro abreviado (`Synt` = SyntaxError, `Attr` = AttributeError, `NotImpl` = NotImplementedError…). Na bancada: **5 de 44 no piso, 22 de 44 no teto, 44 de 44 no CPython**.

Os códigos `N` são diferenças do núcleo 1.9.4: se o aparelho roda o 1.9.4, **todos devem aparecer na lista de falhas**. Um `N` que passe indica código alterado pela Casio.

| Código | Recurso testado | Falha esperada |
|---|---|---|
| N01 | f-string | Synt |
| N02 | operador morsa `:=` | Synt |
| N03 | `'abc'[::-1]` | NotImpl |
| N04 | `next(it, padrão)` | Type |
| N05 | `dict` na ordem de inserção | Assertion |
| N06 | `isinstance(True, int)` | Assertion |
| N07 | `str.ljust` | Attr |
| N08 | `round(1234, -2) == 1200` | Assertion |
| N09 | `'{0[1]}'.format(...)` | NotImpl |
| N10 | `[*a, *b]` | Synt |
| N11 | `1_000` | Synt |
| N12 | `__slots__` restringe atributos | Exception |
| N13 | atributo em função `f.x = 1` | Attr |
| N14 | `format()` embutido | Name |
| N15 | `startswith` com tupla | Type |
| N16 | `RecursionError` existe | Name |
| N17 | operador `@` | Synt |
| N18 | `int.bit_length()` | Attr |
| N19 | `complex('1+2j')` | Value |
| N20 | `d.keys()` do tipo `dict_keys` | Assertion |

Os códigos `C` dependem de como a Casio compilou. Anote quais falham:

| Código | Recurso testado | Teto | Piso | Aparelho |
|---|---|---|---|---|
| C01 | `__mul__` em classe (`v * 2`) | ok | Type | |
| C02 | `__neg__` (`-v`) | ok | Type | |
| C03 | `__radd__` (`2 + v`) | ok | Type | |
| C04 | `__truediv__` (`v / 2`) | ok | Type | |
| C05 | descritor `__get__` | ok | Assertion | |
| C06 | `slice.start` em `__getitem__` | ok | Attr | |
| C07 | `pow(a, b, m)` | ok | NotImpl | |
| C08 | `str.center` | ok | Attr | |
| C09 | `str.partition` | ok | Attr | |
| C10 | `str.splitlines` | ok | Attr | |
| C11 | `frozenset` | ok | Name | |
| C12 | `memoryview` | ok | Name | |
| C13 | `compile()` | ok | Name | |
| C14 | `help()` | Name | Name | |
| C15 | `NotImplemented` | ok | Name | |
| C16 | `f.__name__` | ok | Attr | |
| C17 | mensagem de erro detalhada (`int('xyz')` cita `'xyz'`) | ok | Assertion | |
| C18 | texto unicode (`chr(233)` vira 2 bytes em UTF-8) | ok | Assertion | |
| C19 | `__setattr__` sobrescrito | Assertion | Assertion | |
| C20 | `async def` compila | ok | ok | |
| C21 | `bytearray` | ok | ok | |
| C22 | lista com passo `[1, 2, 3][::2]` | ok | ok | |
| C23 | `int.to_bytes` | ok | ok | |
| C24 | `abs()` de complexo | ok | ok | |

No fim, se aparecer a linha `Warning: exception chaining not supported`, os avisos do compilador estão ligados (na bancada, só no teto).

## MPYNUM — números

Cada teste imprime o rótulo numa linha e o valor na seguinte. No 1.9.4 o resultado é **igual no piso e no teto** (é do núcleo). As letras Q, R, S e U usam funções da biblioteca matemática da Casio e podem diferir no último dígito sem que isso indique outra versão.

| Linha | CPython 3.11 | 1.9.4 no PC | Aparelho |
|---|---|---|---|
| A bits mantissa | 53 | 53 | |
| B maior 2**n | 1023 | 1023 | |
| C menor 2**-n | 1074 | 1074 | |
| D 0.1+0.2 | 0.30000000000000004 | **0.3** | |
| E 0.1+0.2==0.3 | False | **True** | |
| F 538.2 | 538.2 | **538.2000000000001** | |
| G 331.9 e 768.8 | (331.9, 768.8) | **(331.9, 768.8000000000001)** | |
| H soma 10x 0.1 | (0.9999999999999999, False) | **(1.0, False)** | |
| I round(2.675,2) | 2.67 | **2.68** | |
| J round(0.5),(2.5) | (0, 2) | (0, 2) | |
| K round(1234,-2) | 1200 | **1234** | |
| L 2**100 | 1267650600228229401496703205376 | igual | |
| M float(2**53+1) | 9007199254740992.0 | **9007199254740993.0** | |
| N 1e308*10 | inf | inf | |
| O 2.0**10000 | OverflowError | **inf** | |
| P exp(1000) | OverflowError | **ValueError** | |
| Q sqrt(2) | 1.4142135623730951 | 1.414213562373095 | |
| R sin(pi) | 1.2246467991473532e-16 | 1.224646799147353e-16 | |
| S tan(pi/4) | 0.9999999999999999 | 1.0 | |
| T 1j*1j | (-1+0j) | (-1+0j) | |
| U (-8)**(1/3) | (1.0000000000000002+1.7320508075688772j) | (1+1.732050807568877j) | |
| V 7//-2, 7%-2 | (-4, -1) | (-4, -1) | |
| W %.3f e {:,} | ('0.667', '1,000,000') | igual | |
| X 1/3 | 0.3333333333333333 | igual | |
| Y int(1e20) | 100000000000000000000 | igual | |
| Z 0.1*3 | 0.30000000000000004 | **0.3** | |

Se D, E, F, G, H, I, K, M, O, P e Z saírem como na coluna do 1.9.4, a calculadora usa as mesmas rotinas de leitura, escrita e `round` do núcleo, e as regras da seção 6 do estudo valem sem ressalva.

## MPYMEM — memória e recursão

| Linha | Bancada (heap de 100 KB) | Comunidade | Aparelho |
|---|---|---|---|
| maior `[0]*n` | 16.664 (22.180 num processo sem o script) | — | |
| recursão máxima | 62 níveis, `RuntimeError` (pilha da porta unix, não a da Casio) | 82 na Graph 35+E II | |
| heap livre aprox. | ~93.750 bytes (91 KB) | ~100 KB de heap total | |

O heap é estimado enchendo a memória com textos até dar `MemoryError`. Na bancada a estimativa ficou ~5% abaixo do valor real do `gc`, diferença ocupada pelo próprio script. Rode logo após entrar no PYTHON.

## MPYVEL — velocidade

Não há relógio no Python da calculadora. Para cada teste: dispare o cronômetro ao apertar EXE no prompt `EXE inicia` e pare quando aparecer `fim`. Se um teste passar de 30 s ou ficar abaixo de 5 s, mude `N` no topo do arquivo (padrão 20.000) e anote o novo valor.

| Teste | Iterações | Tempo (s) | Iterações/s |
|---|---|---|---|
| T1 laço vazio | N | | |
| T2 conta com int | N | | |
| T3 conta com float | N | | |
| T4 `sqrt` | N | | |
| T5 chamada de função | N | | |
| T6 `append` | N/4 | | |
| T7 `s = s + 'x'` | N/10 | | |
| T8 `''.join` | N/10 | | |
| T9 8.192 `set_pixel` + `show_screen` | 8.192 | | |

Comparações que interessam:

- **T3 / T2:** custo do float emulado em software frente ao inteiro.
- **T5 / T1:** custo de uma chamada de função.
- **T7 / T8:** o desastre da concatenação de texto.
- **T9:** tempo para redesenhar a tela inteira pixel a pixel.

## Depois de rodar

Anote a versão do sistema e as colunas "Aparelho" nesta nota. Em seguida, no estudo, troque cada **[a confirmar]** resolvido por **[aparelho, OS x.xx]**. Se algum resultado contrariar o estudo, prevalece o aparelho: registre a divergência na seção de fontes.

[[00_Inicio/COMECE AQUI|Início]] · [[04_Programacao/MicroPython 1.9.4 - estudo aprofundado|Estudo MicroPython 1.9.4]]
