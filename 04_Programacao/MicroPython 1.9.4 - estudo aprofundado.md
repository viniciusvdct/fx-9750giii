---
title: "MicroPython 1.9.4 — estudo aprofundado do Python da fx-9750GIII"
model: fx-9750GIII
updated: 2026-09-30
status: sintese
firmware_reference: "3.50; consulte Sistema e firmware para 3.70"
micropython: "1.9.4 (tag v1.9.4, 11/05/2018)"
tags: [casio, fx9750giii, python, micropython]
---
# MicroPython 1.9.4 — estudo aprofundado do Python da fx-9750GIII

O modo PYTHON da fx-9750GIII roda uma adaptação do **MicroPython 1.9.4**, versão lançada em 11/05/2018 ([[08_Manuais/fx-9750GIII_Soft_v350_EN.pdf#page=351|SW350, PDF 351]]). Este estudo explica o que essa versão é, como a calculadora a executa e o que muda para quem escreve programas — com medições feitas no próprio MicroPython 1.9.4 oficial, compilado no PC, e scripts para confirmar no aparelho o que só ele pode responder.

Complementa [[Python]], [[casioplot]] e [[Exemplos Python]].

## Resumo em 15 pontos

1. **É Python 3.4 com cortes.** O 1.9.4 declara `sys.version == '3.4.0'`. Não há f-strings (chegaram ao MicroPython só na 1.17, em 2021), operador morsa `:=`, `match`, `1_000`, `x: int = 5` nem `[*a, *b]`. Use `%` ou `str.format`.
2. **A calculadora roda o arquivo com `from NOME import *`** (captura do manual, [[08_Manuais/fx-9750GIII_Soft_v350_EN.pdf#page=367|PDF 367]]). Então `__name__` vale `"NOME"`, não `"__main__"`: um bloco `if __name__ == "__main__":` **não executa**.
3. **Só três módulos documentados:** `math`, `random` e `casioplot`, além de arquivos `.py` da mesma pasta. Não há `sys`, `time`, `gc`, `os` nem leitura de teclado além de `input()`.
4. **`dict` e `set` não guardam a ordem de inserção.** `print({'b': 1, 'a': 2, 'c': 3})` mostra `{'a': 2, 'c': 3, 'b': 1}`. No CPython 3.7+ a ordem é garantida; aqui não.
5. **Fatiar texto com passo não funciona:** `'abc'[::-1]` levanta `NotImplementedError`. Listas aceitam `l[::-1]` na leitura, mas não em atribuição ou `del`.
6. **Faltam métodos e funções comuns:** `str.ljust/rjust/zfill/title/isalnum`, `format()`, `next(it, padrão)`, `vars()`, `math.factorial/gcd/isclose/hypot/inf`, `random.shuffle/sample/gauss`. Há substitutos na [seção 12](#12-receitas-substitutos-para-o-que-falta).
7. **Floats são `double` (53 bits), mas `print` mostra 16 dígitos** — e o 16º pode estar errado: digitar `538.2` e imprimir dá `538.2000000000001`. Em 22,5% dos decimais curtos testados o último dígito impresso diverge do correto.
8. **A leitura de decimais não é arredondada corretamente.** O literal `0.3` vira o double logo acima; por isso `0.1 + 0.2 == 0.3` dá **`True`** no 1.9.4 (no CPython dá `False`). Nunca compare floats com `==`.
9. **`round()` difere:** `round(2.675, 2)` dá `2.68` (CPython: `2.67`) e `round(1234, -2)` devolve `1234` sem arredondar. Para mostrar números, prefira `'%.6g' % x`.
10. **`isinstance(True, int)` é `False`** e estouros de float viram `inf` em vez de `OverflowError`.
11. **Sobrecarga de operadores é parcial.** `+`, `-`, `+=`, `-=`, comparações, `len`, `[]`, `in` e `()` sempre funcionam; `*`, `/`, `**`, `-x`, `abs()` e os refletidos (`2 * v`) dependem de uma opção de compilação que a Casio não documenta; `@`, `int(v)`, `float(v)` e `round(v)` nunca funcionam no 1.9.4.
12. **Memória é o limite real.** A comunidade mede ~100 KB de heap. Num heap assim cabem ~22 mil ints em `[0]*n`, mas só ~4,7 mil floats; compilar um script custa ~5× o tamanho do arquivo (150 linhas ≈ 15 KB).
13. **Concatenar texto em laço é desastroso:** `s = s + 'x'` custou ~2500× uma iteração vazia no 1.9.4; `''.join(partes)`, ~4×.
14. **Recursão rasa:** a comunidade relata ~82 níveis antes de `RuntimeError: maximum recursion depth exceeded` (não existe `RecursionError`).
15. **Muito depende de como a Casio compilou.** Das 268 sondas de linguagem, 113 diferenças são do núcleo 1.9.4 (valem com certeza no aparelho) e 19 dependem de opções de compilação. Os scripts em [`09_Anexos/Python/diagnostico`](../09_Anexos/Python/diagnostico/LEIA-ME.md) resolvem essas 19 no aparelho.

## 1. Escopo, método e níveis de evidência

### Como o estudo foi feito

- **Manual SW350** (capítulo 14, PDF 351–381, e apêndices) e **manual de hardware** (PDF 10), lidos e conferidos nas imagens das páginas.
- **Código-fonte oficial do MicroPython na tag `v1.9.4`**, incluindo as notas de versão gravadas na própria tag, a documentação e os casos `tests/cpydiff`.
- **Laboratório reprodutível** em [`12_Desenvolvimento/micropython-1.9.4`](../12_Desenvolvimento/micropython-1.9.4/README.md): o 1.9.4 oficial compilado em **32 bits** (ponteiros de 4 bytes, como o processador SH4 da calculadora) e com **double estrito** (SSE2, sem a precisão estendida de 80 bits do x87: cada conta arredonda para double, como num ponto flutuante por software correto), em duas variantes:
  - **teto** — a configuração da porta unix, com quase todos os recursos opcionais ligados;
  - **piso** — as opções visíveis ao programador no padrão do núcleo, mantendo só o que o manual documenta (double, inteiros longos, complexos, `log10`, `random` completo).
  O que teto e piso fazem igual é do **núcleo 1.9.4** e vale no aparelho qualquer que seja a configuração da Casio. O que difere entre eles **depende da compilação da Casio** e precisa do aparelho.
- A suíte oficial de testes do 1.9.4 passou em 494 de 508 arquivos no binário teto; as 14 falhas vêm de mudanças do CPython 3.11 usado como referência (por exemplo, o `repr` de exceções), não de defeitos da compilação ([`resultados/suite_oficial.txt`](../12_Desenvolvimento/micropython-1.9.4/resultados/suite_oficial.txt)).
- **Relatos da comunidade** (TI-Planet, Planète Casio, HP Museum, Cemetech). A rede deste ambiente bloqueou esses sites; os dados vieram de resumos de busca e estão marcados como relato, não como leitura integral.

### Legenda

| Marca | Significado |
|---|---|
| **[manual]** | Documentado no manual SW350 ou no de hardware; página indicada |
| **[código 1.9.4]** | Lido no código-fonte oficial da tag v1.9.4 |
| **[medido]** | Medido no 1.9.4 oficial compilado no PC. Vale para o núcleo; não é o firmware da Casio |
| **[comunidade]** | Relato de terceiros, não conferido aqui |
| **[a confirmar]** | Depende do aparelho: rode os scripts de diagnóstico |

O que este estudo **não** faz: não executou nada na calculadora nem no emulador oficial, não leu o firmware da Casio e não conhece as opções de compilação escolhidas por ela. A velocidade, a pilha de recursão e o tamanho exato do heap do aparelho só podem ser medidos nele.

## 2. O que é o MicroPython e onde a 1.9.4 se encaixa

O MicroPython é uma reimplementação do Python 3 escrita em C por Damien George a partir de 2013, pensada para microcontroladores com dezenas de kilobytes de RAM. Licença MIT — o manual reproduz o aviso "Copyright (c) 2013-2017 Damien P. George, and others" **[manual γ-1, PDF 404]**. Ele não é o CPython encolhido: compilador, máquina virtual, coletor de lixo e biblioteca foram escritos do zero, com escolhas próprias para economizar memória. Daí as diferenças deste estudo.

### Linha do tempo (tags oficiais conferidas no repositório)

| Versão | Data | Destaque |
|---|---|---|
| 1.9 | 26/05/2017 | Novo sistema de arquivos virtual |
| **1.9.4** | **11/05/2018** | **Versão da fx-9750GIII** |
| 1.10 | 26/01/2019 | Emissor nativo melhorado |
| 1.12 | 20/12/2019 | Módulos nativos dinâmicos, BLE e littlefs |
| 1.13 | 02/09/2020 | Novo `uasyncio` |
| 1.17 | 02/09/2021 | **f-strings** |
| 1.19 | 16/06/2022 | Novo formato de bytecode `.mpy` 6 |
| 1.20.0 | 26/04/2023 | Gerenciador de pacotes `mip` |
| 1.29.0 | 24/08/2026 | Versão estável mais recente nesta data |

A calculadora ficou oito anos e dezenas de versões atrás. Tutoriais e respostas atuais de MicroPython descrevem uma linguagem maior que a do aparelho.

### O que a 1.9.4 trouxe

Pelas notas da tag **[código 1.9.4]**: parser menor (tabelas de regras comprimidas), uma pilha Python opcional para alocações temporárias (`MICROPY_ENABLE_PYSTACK`), `dir()` capaz de listar todos os atributos, `ucollections.deque`, correções no algoritmo que converte float em texto e no `pow` de três argumentos, e o port para ESP32. Para quem programa a calculadora, o essencial é o que **ainda não** existia — o resto deste estudo.

### Nível de linguagem

O 1.9.4 se declara Python 3.4 (`sys.version == '3.4.0'`) **[medido]**. Acrescenta a sintaxe `async def`/`await` do 3.5, que compila mas não tem uso sem biblioteca assíncrona. Não inclui recursos do 3.5 em diante como o operador `@` e a generalização de desempacotamento (PEP 448), nem nada do 3.6+.

### O que a Casio fez

- Compilou o núcleo com um conjunto próprio de opções — não publicado.
- Escreveu o editor de scripts, o SHELL, o catálogo e o módulo `casioplot` **[manual 14-1 a 14-22]**.
- Limitou os módulos importáveis a `math`, `random`, `casioplot` e arquivos `.py` **[manual 14-11]**.
- Distribuiu depois `turtle.py` e `matplotl.py`, scripts sobre o `casioplot` **[comunidade]** (seção 7.5).

## 3. Como a calculadora executa um script

### O fluxo

1. Na lista de arquivos, RUN (ou EXE) abre o SHELL. Rodar pela lista ou pelo editor **reinicializa o SHELL**: variáveis, funções e módulos anteriores são apagados e a tela de desenho é limpa **[manual 14-16, 14-17, 14-22]**.
2. O SHELL executa **`from NOME import *`** — a captura do manual mostra `>>>from example3 impo…` logo abaixo de `* SHELL Initialized *` **[manual 14-17, PDF 367]**.
3. O arquivo é lido e **compilado no aparelho**, inteiro, antes de rodar. O pico de memória da compilação acontece aqui (seção 8.4).
4. A saída aparece no SHELL; ao final, as funções e variáveis do script ficam disponíveis no prompt `>>>`.

### Consequências práticas

| Fato | Efeito | Evidência |
|---|---|---|
| Execução por `import` | `__name__` é o nome do arquivo; `if __name__ == "__main__":` não roda. Chame `main()` direto no fim do arquivo | [manual 14-17] + [medido] na bancada |
| `from … import *` ignora nomes com `_` inicial | `_total` não aparece no prompt depois da execução | [manual 14-11] |
| Módulos ficam em cache | Um segundo `import NOME` no mesmo SHELL não roda o arquivo de novo; um import que falhou no meio continua registrado. Saia do SHELL (reinicialização) e rode de novo | [código 1.9.4], caso `core_import_prereg` |
| Import só da mesma pasta | O arquivo importado deve estar na pasta do principal | [manual 14-31] |
| Variáveis do SHELL são apagadas ao trocar de tela | Não conte com estado entre execuções | [manual 14-13, 14-16] |
| AC interrompe | Aparece `KeyboardInterrupt:` | [manual 14-15] |
| Modo exame | O modo PYTHON fica desativado | [manual β-1, PDF 399] |

### A tela do SHELL

| Item | Limite | Evidência |
|---|---|---|
| Largura visível | ~21 caracteres (`>>>from casioplot imp` ocupa a linha) | [manual 14-20, captura] |
| Linhas visíveis | 7, mais a barra de funções | [manual 14-20, captura] |
| Linha de resultado | até 255 caracteres; o excedente pede rolagem lateral | [manual 14-13] |
| Histórico | 100 linhas | [manual 14-13] |
| Linha de prompt | até 127 caracteres | [manual 14-13] |
| Prompt do `input()` | até 16 caracteres aparecem inteiros; acima disso, 15 e `~` | [manual 14-16] |
| Banner | "MicroPython …" e "CASIO COMPUTER CO.," no topo | [manual 14-20, captura; versão borrada] |

Imprima linhas curtas: `print('V=', v)` cabe; `print('A tensão calculada no resistor é', v)` exige rolagem lateral.

### Arquivos

| Regra | Detalhe | Evidência |
|---|---|---|
| Nome | até 8 caracteres A–Z, a–z, 0–9; sem diferenciar maiúsculas; não começar por número nem ser palavra reservada | [manual 14-2] |
| Nome vindo do PC | só ASCII; nomes longos aparecem abreviados (`AAAABBBBCC.py` → `AAAABB~1.py`) | [manual 14-26] |
| Conteúdo editável | ASCII, até 150 linhas de até 127 caracteres; arquivo maior pode rodar, mas abre com "Invalid Data Size" | [manual 14-4, 14-27] |
| Tabulação | vira 2 espaços ao abrir no editor | [manual 14-27] |
| Quebra de linha | LF, CR ou CRLF são aceitas; o editor salva CRLF | [manual 14-26, 14-27] |
| Onde ficam | memória de armazenamento (até 3 MB), não a principal (62.000 bytes) | [manual 14-25] + [manual HW, PDF 10] |
| Pastas | até 3 níveis | [manual 11, memória] |

Indente só com espaços. A conversão de tabulação em 2 espaços pode quebrar um arquivo que misture tabulações e espaços.

### O teclado digita Python

A tabela da página 14-6 **[manual, PDF 356]** mostra o que cada tecla insere:

| Tecla | Insere | Observação |
|---|---|---|
| `x²` | `**2` | potência |
| `^` | `**` | em Python `^` é XOR; a tecla já insere o certo |
| `log` | `log10()` | função do `math` |
| `ln` | `log()` | logaritmo natural |
| `SHIFT` `x²` (√) | `sqrt()` | do `math` |
| `SHIFT` `ln` (eˣ) | `exp()` | do `math` |
| `×10ˣ` | `e` | em `2e3` é notação científica; sozinho é o `e` do `math` |
| `SHIFT` `×10ˣ` (π) | `pi` | do `math` |
| `SHIFT` `0` (i) | `1j` | unidade imaginária: complexos existem |
| `SHIFT` `)` (x⁻¹) | `**-1` | inverso |
| `X,θ,T` | `X` | só a letra |

As funções saem **sem prefixo**: só funcionam depois de `from math import *` **[manual 14-7]**.

## 4. Por dentro: por que ele se comporta assim

### Do texto à execução

O MicroPython lê o arquivo, monta a árvore sintática inteira, compila para bytecode e só então executa na máquina virtual **[código 1.9.4]**. Não há cache `.pyc`: cada execução recompila. Em outras plataformas o MicroPython aceita bytecode pré-compilado (`.mpy`); o manual da calculadora só fala de arquivos `.py`.

### Objetos e memória

- **Inteiros pequenos** (de −2³⁰ a 2³⁰−1 em 32 bits) vivem dentro do próprio ponteiro: custam **0 bytes** de heap **[medido]**. Acima disso vira inteiro longo (`mpz`), alocado no heap.
- **Floats são objetos**: cada resultado de conta com float aloca **16 bytes** **[medido]**. Um laço com floats gera lixo a cada iteração.
- **Nomes e textos curtos do programa** são "internados" (qstr) numa tabela que só cresce até a reinicialização do SHELL.
- **Coletor de lixo** mark-sweep, **conservador**, em blocos de 16 bytes, sobre um heap de tamanho fixo **[código 1.9.4]**. Sem contagem de referências: `__del__` nunca roda, o lixo só some quando o coletor passa, e um ponteiro velho esquecido na pilha pode manter um objeto morto ocupando memória — isso apareceu nas medições (seção 8.5).
- **Recursão** é limitada por uma verificação da pilha C. Ao estourar: `RuntimeError: maximum recursion depth exceeded` **[medido]**.
- **`dict` e `set`** são tabelas de espalhamento sem registro da ordem de inserção **[medido]**.

### Floats: leitura e escrita

- **Leitura** (literais e `float('…')`): acumula os dígitos num double e multiplica por `pow(10, expoente)` — dois arredondamentos, erro de até 1–3 ulps **[código 1.9.4, `py/parsenum.c`]**.
- **Escrita** (`print`, `str`, `repr`): usa uma rotina derivada de `pdouble.c` de Fred Bayer, adaptada por Dave Hylands. Normaliza o número multiplicando por potências de 10 e extrai cada dígito com `f -= d; f *= 10`, acumulando erro. Imprime **16 algarismos significativos** **[código 1.9.4, `py/formatfloat.c`]**. O CPython imprime a menor representação que volta exatamente ao mesmo double (até 17 algarismos).
- **`round(x, n)`** calcula `nearbyint(x * 10**n) / 10**n`; com `x` inteiro, devolve `x` e ignora `n` **[código 1.9.4, `py/modbuiltins.c`]**.

A seção 6 mostra as consequências.

### Opções de compilação

Boa parte do que o programador vê é ligada ou desligada na compilação: métodos como `str.center`, `frozenset`, `memoryview`, `pow` com três argumentos, operadores `*`, `/`, `-x` em classes, descritores, o detalhamento das mensagens de erro, unicode e avisos. O arquivo [`mpconfigport_piso.h`](../12_Desenvolvimento/micropython-1.9.4/bancada/mpconfigport_piso.h) lista essas opções. A Casio não publicou as suas; o diagnóstico `MPYSINT` as revela.

## 5. A linguagem: o que funciona e o que não funciona

Tabela completa das 268 sondas, com o código de cada uma e os resultados no CPython 3.11, teto e piso: [`resultados/sondas_linguagem.md`](../12_Desenvolvimento/micropython-1.9.4/resultados/sondas_linguagem.md). Resumo: **136 iguais ao CPython, 113 diferenças do núcleo 1.9.4, 19 dependentes da configuração**.

### 5.1 Sintaxe

| Recurso | Python | 1.9.4 | Evidência |
|---|---|---|---|
| f-string `f"{x}"` | 3.6 | ❌ `SyntaxError` | [medido] |
| Morsa `(y := 5)` | 3.8 | ❌ `SyntaxError` | [medido] |
| Parâmetro só-posicional `def f(a, /)` | 3.8 | ❌ `SyntaxError` | [medido] |
| `match` / `case` | 3.10 | ❌ `SyntaxError` | [medido] |
| Anotação de variável `x: int = 5` | 3.6 | ❌ `SyntaxError` | [medido] |
| Separador `1_000` | 3.6 | ❌ `SyntaxError`; `int('1_0')` dá `ValueError` | [medido] |
| `[*a, *b]`, `{**d1, **d2}`, `f(*a, *b)` | 3.5 | ❌ `SyntaxError` | [medido] |
| Operador `@` | 3.5 | ❌ `SyntaxError` | [medido] |
| `return *a, 3` | 3.8 | ❌ `SyntaxError` | [medido] |
| `\N{nome}` em texto | 3.0 | ❌ `NotImplementedError` | [medido] |
| `class A(metaclass=M)` | 3.0 | ❌ `TypeError` | [medido] |
| `raise X from Y` | 3.0 | ⚠️ aceita, mas não encadeia (`__cause__` não existe) | [medido] |
| Anotação de função `def f(x: int) -> int` | 3.0 | ✅ ignorada | [medido] |
| `nonlocal`, `yield from`, `*, b` (só-nomeado), `a, *b = …` | 3.x | ✅ | [medido] |
| Compreensões de lista, conjunto e dicionário | — | ✅ | [medido] |
| `with`, decoradores, `lambda`, `for/while … else`, `try/except/else/finally` | — | ✅ | [medido] |
| Número colado em palavra-chave `1if x else 2` | — | ❌ exige espaço | [código 1.9.4] `syntax_spaces` |
| Docstring em `f.__doc__` | — | ❌ não guarda | [medido] |

Erros de sintaxe mostram arquivo e linha. Bloco sem indentação dá `SyntaxError: invalid syntax`; recuo inesperado ou inconsistente dá `IndentationError`; parêntese não fechado é acusado na **linha seguinte** **[medido]**.

### 5.2 Funções embutidas

Nomes presentes nas duas variantes **[medido]**: `abs all any bin bool bytearray bytes callable chr classmethod complex delattr dict dir divmod enumerate eval exec filter float getattr globals hasattr hash hex id input int isinstance issubclass iter len list locals map max min next object oct open ord pow print property range repr reversed round set setattr slice sorted staticmethod str sum super tuple type zip`, além das exceções e de `__import__`, `__build_class__` e `__repl_print__`.

| Ausente no núcleo 1.9.4 | Dependente da configuração | Existe, mas limitada |
|---|---|---|
| `format()`, `vars()`, `ascii()`, `breakpoint()` | `compile()`, `frozenset`, `memoryview`, `NotImplemented`, `help()` | `next(it)` sem padrão; `iter(f, sentinela)` não; `slice()` não cria objetos; `pow(a, b, m)` pode faltar; `locals()` dentro de função devolve os globais; `eval()` não enxerga variáveis locais; `open()` existe na porta unix, mas o manual não documenta arquivos na calculadora |

`print(..., sep=, end=)` funciona. `input()` devolve sempre texto — converta com `int()` ou `float()`; `int('3.5')` levanta `ValueError`.

### 5.3 Texto

| Método de `str` | 1.9.4 |
|---|---|
| `count decode encode endswith find format index isalpha isdigit islower isspace isupper join lower lstrip replace rfind rindex rsplit rstrip split startswith strip upper` | ✅ núcleo |
| `center partition rpartition splitlines` | ⚠️ depende da configuração |
| `ljust rjust zfill title capitalize swapcase casefold expandtabs translate maketrans format_map isalnum isdecimal isnumeric isidentifier isprintable istitle removeprefix` | ❌ |

- `'abc'[::-1]` e qualquer fatia de texto com passo ≠ 1: `NotImplementedError`. Use `''.join(reversed(s))`.
- `startswith(('a', 'b'))` com tupla: `TypeError`. `endswith(s, início, fim)`: `TypeError`.
- `'a b c'.rsplit(None, 1)`: `NotImplementedError`.
- `'{0[1]}'.format(l)` e `'{a.real}'.format(a=3)`: `NotImplementedError`.
- **Funciona:** `%` completo (`'%5.2f|%-6s|%05d|%x' % …`, `'%(a)s' % dic`), `str.format` com alinhamento, preenchimento, sinal e `{:,}`.
- Com unicode ligado, `len('é')` é 1; sem unicode (piso), 2 **[medido; a confirmar]**. O editor e a tela de desenho só aceitam ASCII **[manual 14-21, 14-26]**.

### 5.4 Coleções

- **Ordem de `dict` e `set` imprevisível.** Chaves inseridas como `zeta, alfa, mike, bravo, x, a, kilo, eco` saíram como `mike, zeta, kilo, eco, a, x, bravo, alfa` **[medido]**. Para uma ordem estável, percorra `sorted(d)` ou mantenha uma lista separada com as chaves.
- `d.keys()` é do tipo `dict_view`; funciona em `for` e `in`.
- Listas: `append clear copy count extend index insert pop remove reverse sort`. `l[::2]` e `l[::-1]` funcionam **na leitura**; `l[::2] = …` e `del l[::2]` levantam `NotImplementedError`; `l[1:3] = range(2)` exige lista ou tupla à direita.
- Tuplas não aceitam fatia com passo.
- `range(3) == range(3)` dá `False` (comparação de ranges desligada nas duas variantes); `len(range(10**10))` dá `OverflowError`.
- `sorted` é estável e aceita `key` e `reverse`; `min`/`max` aceitam `key` e `default`.
- `bytes` e `bytearray` existem.

### 5.5 Classes e sobrecarga de operadores

Sonda dedicada, um método por vez ([`sondas_operadores.py`](../12_Desenvolvimento/micropython-1.9.4/sondas/sondas_operadores.py)) **[medido]**:

| Situação no 1.9.4 | Métodos |
|---|---|
| ✅ Sempre | `__add__ __sub__ __iadd__ __isub__ __lt__ __le__ __gt__ __ge__ __eq__ __ne__ __contains__ __len__ __bool__ __hash__ __getitem__ __setitem__ __delitem__ __iter__ __call__ __str__ __repr__ __enter__ __exit__ __getattr__`; sem `__iadd__`, o `+=` usa `__add__` |
| ⚠️ Depende da configuração | `__mul__ __truediv__ __floordiv__ __mod__ __pow__ __and__ __or__ __xor__ __lshift__ __rshift__`, os unários `__neg__ __pos__ __abs__ __invert__` e todos os refletidos (`__radd__`, `__rmul__`…). `a *= 2` recorre a `__mul__` quando este funciona; `__imul__` e os demais in-place próprios dependem de outra opção, desligada até na porta unix |
| ❌ Nunca | `@`/`__matmul__` (o operador nem é reconhecido), `__int__`, `__float__`, `__index__`, `__round__` |

Sem a opção, `V(1) * 2` falha com a mensagem truncada `TypeError: unsupported types for : 'V', 'int'`. Uma classe `Vetor` ou `Fracao` que dependa de `*` ou de `-v` deve ser testada no aparelho (código `C01`–`C04` do `MPYSINT`); se falhar, use métodos com nome (`v.escala(2)`, `v.neg()`).

Outras diferenças **[medido]**:

- `super()` sem argumentos, `@property` com setter, `@classmethod`, `@staticmethod`, herança simples e subclasses de `int` e `list` funcionam.
- `__setattr__` sobrescrito é **ignorado** nas duas variantes.
- `__del__` nunca é chamado.
- `__slots__` é ignorado: atributos novos continuam permitidos.
- Não há *name mangling*: `self.__x` fica com esse nome.
- Funções não aceitam atributos (`f.x = 1` levanta `AttributeError`).
- `__init_subclass__` é ignorado.
- Herança múltipla usa busca em profundidade: no diamante `D(B, C)`, com `B` e `C` herdando de `A` e só `C` redefinindo o método, `D().f()` chama o de `A` (o CPython chama o de `C`).
- Descritores (`__get__`) e atributos de `slice` (`.start`) dependem da configuração.
- `isinstance(True, int)` e `issubclass(bool, int)` são `False` (mas `True + True == 2`).

### 5.6 Exceções e mensagens

| Situação | CPython 3.11 | MicroPython 1.9.4 |
|---|---|---|
| Recursão funda | `RecursionError` | `RuntimeError: maximum recursion depth exceeded` |
| Variável local lida antes de atribuir | `UnboundLocalError` | `NameError: local variable referenced before assignment` |
| Módulo inexistente | `ModuleNotFoundError: No module named 'x'` | `ImportError: no module named 'x'` |
| `'a' + 1` | `can only concatenate str (not "int") to str` | `can't convert 'int' object to str implicitly` |
| `int('x')` | `invalid literal for int() with base 10: 'x'` | `invalid syntax for integer with base 10: 'x'` (sem o texto, se o detalhamento estiver no nível normal) |
| `{}['k']` | `KeyError: 'k'` | `KeyError: k` |
| `sorted([1, 'a'])` | `'<' not supported between…` | `unsupported types for __lt__: 'int', 'str'` |
| `{[1]: 2}` | `unhashable type: 'list'` | `unsupported type for __hash__: 'list'` |
| `f()` sem argumento | `missing 1 required positional argument` | `f() takes 1 positional arguments but 0 were given` (ou `function takes…`) |
| `1.0 / 0`, `1 % 0`, `0 ** -1` | mensagens distintas | sempre `division by zero` |
| `math.exp(1000)` | `OverflowError: math range error` | `ValueError: math domain error` |
| `repr(ValueError('x'))` | `ValueError('x')` | `ValueError('x',)` |

Também **[medido]**:

- Não existem `RecursionError`, `UnboundLocalError`, `ModuleNotFoundError`, `FileNotFoundError`, `PermissionError`, `TimeoutError`, `IOError`, `Warning` nem `ReferenceError`; `UnicodeError` depende do unicode.
- Não há `__traceback__`, `__context__` nem `__cause__`.
- Exceções embutidas não aceitam atributos novos (`e.x = 1`); crie uma subclasse. Nela, chame `super().__init__(…)`, porque `Exception.__init__` não existe como atributo.
- `except Exception` não captura `KeyboardInterrupt` nem `SystemExit`, como no CPython.

### 5.7 Geradores, iteradores e escopo

- `send`, `throw`, `close` e o `return valor` (em `StopIteration.value`) funcionam **[medido]**.
- A PEP 479 não existe: um `StopIteration` escapando dentro de um gerador encerra-o em silêncio, em vez de virar `RuntimeError` **[medido]**.
- Um `with` dentro de gerador não chama `__exit__` se o gerador não for até o fim **[código 1.9.4]** `core_generator_noexit`.
- *Late binding* em `lambda` dentro de laço, argumento padrão mutável e variável de compreensão que não vaza: igual ao CPython **[medido]**.
- `const()` funciona **sem importar nada**: `N = const(10)` é resolvido na compilação e `_N = const(10)` nem ocupa variável global **[medido; a confirmar no aparelho]**. No CPython, `const` não existe (seção 10).

### 5.8 O que o próprio projeto documenta

O MicroPython mantém casos de diferença em `tests/cpydiff`. Os 43 casos do 1.9.4 rodados nas três variantes estão em [`resultados/cpydiff.md`](../12_Desenvolvimento/micropython-1.9.4/resultados/cpydiff.md). Os que tocam a calculadora já aparecem acima; os de `array`, `collections`, `json`, `struct` e `sys` não se aplicam, porque esses módulos não estão disponíveis nela.

## 6. Números: o ponto mais delicado numa calculadora

### 6.1 Dois sistemas numéricos no mesmo aparelho

| | Modos nativos (RUN·MAT etc.) | Modo PYTHON |
|---|---|---|
| Representação | decimal, mantissa de 15 dígitos **[manual HW, PDF 10]** | binária IEEE 754 double: 53 bits ≈ 15,95 dígitos **[medido; comunidade]** |
| Faixa | ±1 × 10⁻⁹⁹ a ±9,999999999 × 10⁹⁹ | ±1,8 × 10³⁰⁸; subnormais até 4,9 × 10⁻³²⁴ |
| `0,1 + 0,2` | exatamente 0,3 | um valor binário vizinho de 0,3 |
| Inteiros | limitados pela mantissa | exatos e ilimitados (`2**100` sai completo) |

Por isso o manual avisa que os resultados do PYTHON podem diferir dos outros modos **[manual 14-1, 14-15]**. Não é defeito: são duas aritméticas.

### 6.2 O que você vê não é o que você tem

O `print` mostra 16 algarismos, e isso esconde parte dos erros binários **[medido]**:

| Expressão | CPython 3.11 | MicroPython 1.9.4 | Valor real guardado |
|---|---|---|---|
| `0.1 + 0.2` | `0.30000000000000004` | `0.3` | 0.3000000000000000444… |
| `sum([0.1] * 10)` | `0.9999999999999999` | `1.0` | 0.9999999999999998889…; `== 1.0` é `False` nos dois |
| `2 ** 0.5` | `1.4142135623730951` | `1.414213562373095` | o mesmo double |
| `math.tan(math.pi / 4)` | `0.9999999999999999` | `1.0` | idem |
| `1e16 + 2` | `1.0000000000000002e+16` | `1e+16` | idem |

Conclusão: no 1.9.4, dois números impressos iguais podem ser diferentes.

### 6.3 A leitura de decimais não é exata

O literal `0.3` é lido como `0.30000000000000004` (1 ulp acima do double correto). Coincide com o resultado de `0.1 + 0.2`, então **`0.1 + 0.2 == 0.3` dá `True` no 1.9.4** — por acaso, não por precisão. `2.675` também é lido acima, por isso `round(2.675, 2)` dá `2.68` **[medido]**.

Medição com 20.000 textos por grupo ([`resultados/precisao_float.md`](../12_Desenvolvimento/micropython-1.9.4/resultados/precisao_float.md)) **[medido]**:

| Amostra | Leitura errada | Maior erro | 16º dígito impresso errado | `float(repr(x)) != x` |
|---|---|---|---|---|
| Digitados, 1 a 6 dígitos (ex.: `331.9`) | 23,7% | 1 ulp | 22,5% | 19,1% |
| 15 a 17 dígitos, de 1e-10 a 1e10 | 34,0% | 3 ulps | 32,0% | 36,8% |
| Resultados de contas | 36,2% | 2 ulps | 23,3% | 49,3% |

Um ulp perto de 1 vale 2,2 × 10⁻¹⁶. Mesmo 3 ulps ficam abaixo da última casa da mantissa de 15 dígitos dos modos nativos e centenas de milhares de vezes abaixo dos 10 dígitos que eles exibem. **Para engenharia, a exatidão é suficiente; o problema é de exibição e de comparação.**

### 6.4 A escrita erra o último dígito

`print(538.2)` mostra `538.2000000000001`; `print(768.8)`, `768.8000000000001`; `float(2**53 + 1)` aparece como `9007199254740993.0`, um valor que um double nem representa **[medido]**. No [[Exemplos Python|DISCRETO.py]] do cofre, `print(k, round(y, 6))` mostra `0.8823510000000001` e `0.9176459999999999` no 1.9.4, onde o CPython mostra `0.882351` e `0.917646` **[medido na bancada]**. `round()` não conserta a exibição; formatar conserta.

### 6.5 `round()`

| Chamada | CPython | 1.9.4 |
|---|---|---|
| `round(2.5)`, `round(0.5)`, `round(-0.5)` | `2`, `0`, `0` | iguais (meio para o par) |
| `round(2.675, 2)` | `2.67` | `2.68` |
| `round(1234, -2)` | `1200` | `1234` (ignora `n` para inteiros) |
| `type(round(2.7))` | `int` | `int` |

### 6.6 Estouros e domínios

| Expressão | CPython | 1.9.4 |
|---|---|---|
| `1e308 * 10` | `inf` | `inf` |
| `2.0 ** 10000` | `OverflowError` | `inf` |
| `float(10**400)` | `OverflowError` | `inf` |
| `math.exp(1000)` | `OverflowError` | `ValueError: math domain error` |
| `math.sqrt(-1)`, `math.log(0)`, `math.acos(2)` | `ValueError: math domain error` | igual |
| `int(float('inf'))` | `OverflowError` | `OverflowError: can't convert inf to int` |
| `(-8) ** (1/3)` | complexo | complexo, `(1+1.732050807568877j)` |

Um `inf` silencioso pode atravessar vários cálculos. Teste com `math.isinf(x)` quando houver risco.

### 6.7 Inteiros

- Inteiros de precisão arbitrária: `2**100` é exato e `int(1e20)` dá `100000000000000000000` **[medido]**.
- Até 2³⁰−1 custam 0 bytes; um `2**40` ou `2**100` ocupa 32 bytes e `2**1000`, 144 **[medido]**.
- A comparação entre inteiro grande e float converte o inteiro em float: `2**53 + 1 == float(2**53 + 1)` dá `True` (no CPython, `False`) **[medido]**.
- `//` e `%` seguem o piso, como no CPython: `-7 // 2 == -4`, `-7 % 3 == 2` **[medido]**.
- `(255).to_bytes(2, 'big')` e `int.from_bytes` existem; `bit_length()` não **[medido]**.

### 6.8 Complexos

`1j`, `complex(a, b)`, `.real`, `.imag`, `abs(z)` e as contas básicas funcionam. **Não existem** `z.conjugate()`, `complex('1+2j')` nem o módulo `cmath` **[medido; a confirmar para `cmath`]**. Fase: `math.atan2(z.imag, z.real)`; conjugado: `complex(z.real, -z.imag)`.

### 6.9 Regras práticas

1. **Mostre com formato, não com `round`:** `'%.6g' % x`, `'%.4f' % x` ou `'{:.3e}'.format(x)`. Seis a dez algarismos bastam e escondem o 16º dígito incerto.
2. **Compare com tolerância:** `abs(a - b) <= 1e-9 * max(abs(a), abs(b), 1)` (não há `math.isclose`).
3. **Conte com inteiros quando puder:** centavos, milésimos, passos de laço. Inteiros pequenos não alocam memória e são exatos.
4. **Não use float como chave de `dict`** nem como critério de parada exato (`while x != 1.0`).

## 7. Módulos

### 7.1 O que existe

| Módulo | Situação | Evidência |
|---|---|---|
| embutidos (`print`, `len`…) | ✅ sem `import` | [manual 14-10] |
| `math` | ✅ | [manual 14-11] |
| `random` | ✅ | [manual 14-11] |
| `casioplot` | ✅ desde o OS 3.40 na fx-9750GIII | [manual 14-17]; versão: [comunidade] |
| `turtle.py`, `matplotl.py` | scripts da Casio distribuídos à parte | [comunidade] |
| `sys`, `time`, `gc`, `os`, `cmath`, `collections`, `json`, `re`, `struct`, `micropython` | ❌ | manual lista só os três; [comunidade]; [a confirmar] com `MPYINFO` |

Sem `time` não há `sleep` nem cronômetro: pausas só com laço de espera ou com `input()`. Sem `sys` não há `sys.exit()`; organize o programa em funções e use `return`. Sem teclado além de `input()`, jogos com resposta imediata não são possíveis no Python original **[comunidade]**; a fx-CG100, modelo posterior, ganhou um `getkey` no `casioplot` **[comunidade]**.

### 7.2 `math`

Conjunto do `math` no 1.9.4 com as funções especiais (40 nomes) **[código 1.9.4]**: `e pi sqrt pow exp expm1 log log2 log10 cos sin tan acos asin atan atan2 cosh sinh tanh acosh asinh atanh ceil floor trunc fabs fmod modf frexp ldexp copysign isfinite isinf isnan degrees radians erf erfc gamma lgamma`.

- No 1.9.4, `log10` só existe junto das "funções especiais" (hiperbólicas, `log2`, `erf`, `gamma`). Como a tecla LOG da calculadora insere `log10()` **[manual 14-6]**, a Casio deve ter ligado esse grupo ou alterado o módulo. Um programa da comunidade para a fx-9750GIII importa `sinh, cosh, tanh` **[comunidade]**. Confirme a lista com `MPYINFO`.
- `math.log(x, base)` funciona; `floor`, `ceil` e `trunc` devolvem `int` **[medido]**.
- **Não existem no 1.9.4:** `factorial gcd lcm isclose inf nan tau hypot fsum prod comb perm isqrt dist cbrt exp2 remainder ulp nextafter` **[medido]**. Substitutos na seção 12.
- Ângulos sempre em **radianos**: `math.degrees`/`math.radians`. O SET UP de ângulo dos modos nativos não afeta o Python.

### 7.3 `random`

- Funções **[código 1.9.4, `urandom` com funções extras]**: `getrandbits seed randrange randint choice random uniform`. A comunidade conta 8 elementos no `random` da Graph 35+E II **[comunidade]**; no 1.9.4, `dir(random)` lista 9 (as 7 funções, `__name__` e `__class__`). Ou falta uma função no aparelho, ou a contagem usou outro critério — `MPYINFO` mostra a lista real.
- **Não existem:** `shuffle sample choices gauss normalvariate triangular` **[medido]**.
- `seed()` **exige argumento**; `random.seed()` sem valor dá `TypeError` **[medido]**.
- O gerador (Yasmarang, 32 bits) parte de um **estado inicial fixo** no código do 1.9.4. Na bancada, o primeiro `random.random()` é sempre `0.689459…` a cada início **[medido]**. Se a Casio não semeia o gerador ao iniciar o SHELL, toda execução repete a mesma sequência **[a confirmar]**: rode `MPYINFO` duas vezes e compare a linha `rand1`. Se repetir, peça uma "semente" ao usuário (`random.seed(int(input('semente? ')))`).

### 7.4 `casioplot`

Especificação do manual **[manual 14-17 a 14-22]**:

| Função | Uso | Detalhes |
|---|---|---|
| `show_screen()` | mostra a tela de desenho | dentro do laço, anima; fora, só o resultado final |
| `clear_screen()` | apaga o desenho | a tela também é apagada quando o SHELL reinicializa |
| `set_pixel(x, y[, cor])` | acende um pixel | `x` de 0 a 127 e `y` de 0 a 63, **inteiros**; fora da faixa, nada acontece e não há erro |
| `get_pixel(x, y)` | lê um pixel | devolve `(0, 0, 0)` ou `(255, 255, 255)`; fora da faixa, não devolve nada (`None`) |
| `draw_string(x, y, s[, cor[, tamanho]])` | escreve texto | `(x, y)` é o canto superior esquerdo; `"large"` ou `"medium"` (padrão); `"small"` vira `"medium"`; só ASCII; texto que sai da tela é cortado |

- **Cor:** lista ou tupla `(R, G, B)`, inteiros de 0 a 255. De `(248, 252, 248)` a `(255, 255, 255)` é branco; qualquer outro valor é preto. Sem cor, preto.
- **A área é a tela inteira, 128 × 64:** o manual escreve `0 ≦ x ≦ 127, 0 ≦ y ≦ 63` e marca os cantos `(0, 0)` e `(127, 63)` **[manual 14-19, PDF 369]**. A área útil de 127 × 63 citada em [[casioplot]] vale para os gráficos nativos, não para o `casioplot`. O `y` cresce para baixo.
- `input()`, um erro ou a tecla AC devolvem a tela ao SHELL; para ver o desenho de novo, chame `show_screen()`. J, AC ou SHIFT J (QUIT) saem da tela de desenho **[manual 14-18, 14-22]**.
- Desempenho: `show_screen()` copia a tela inteira. Desenhe tudo e chame uma vez, ou poucas vezes por quadro. O teste `T9` do `MPYVEL` mede quanto custa preencher os 8.192 pixels.

Para testar no PC, a bancada traz um [emulador do `casioplot`](../12_Desenvolvimento/micropython-1.9.4/bancada/casioplot.py) com as mesmas regras de coordenada, cor e faixa. Ele mostra a tela no terminal e, opcionalmente, grava PBM. Não reproduz o desenho das letras: marca a caixa de cada caractere (hipótese: 6 × 8 pixels no `large`, 4 × 6 no `medium`).

### 7.5 `turtle` e `matplotl`

A Casio publicou `turtle.py` (~8 KB) e `matplotl.py` (~23 KB), scripts em Python que imitam os módulos `turtle` e `matplotlib.pyplot` usando o `casioplot`. Pedem OS 3.40 ou superior na fx-9750GIII/9860GIII; nos modelos franceses o `turtle` passou depois a vir no sistema **[comunidade]**. O manual 3.50 da fx-9750GIII não os menciona.

**Cuidado com a memória:** compilar um script custa cerca de 5 vezes o tamanho do arquivo (seção 8.4). Um arquivo de 23 KB de código denso precisou de ~111 KB de heap na bancada — mais que os ~100 KB relatados para a calculadora. Scripts reais têm comentários e espaços, que não pesam na compilação; ainda assim, importe `matplotl` logo depois de abrir o SHELL e mantenha o seu programa pequeno **[medido + inferência; a confirmar]**.

## 8. Memória

### 8.1 Três memórias diferentes

| Memória | Tamanho | O que guarda |
|---|---|---|
| Principal | até 62.000 bytes **[manual HW, PDF 10]** | programas BASIC, listas, matrizes, variáveis A–Z |
| Armazenamento | até 3 MB **[manual HW, PDF 10]** | arquivos `.py`, eActivities, backups |
| Heap do Python | ~100 KB na Graph 35+E II **[comunidade]** | tudo o que o script cria enquanto roda, inclusive o próprio código compilado |

Um arquivo `.py` de 3 KB ocupa 3 KB do armazenamento, mas ~15 KB do heap para compilar e o que o programa alocar depois. `MPYMEM` estima o heap livre do seu aparelho.

### 8.2 Quanto custa cada objeto (32 bits)

Medido com `gc.mem_alloc()` no binário de 32 bits ([`sondas/memoria.py`](../12_Desenvolvimento/micropython-1.9.4/sondas/memoria.py)) **[medido]**:

| Objeto | Bytes | | Objeto | Bytes |
|---|---|---|---|---|
| int até 2³⁰−1 | 0 | | lista `[0]*1000` | 4.016 |
| int 2⁴⁰ ou 2¹⁰⁰ | 32 | | lista de 1000 ints por `append` | 4.112 |
| int 2¹⁰⁰⁰ | 144 | | **lista de 1000 floats** | **20.112** |
| float | 16 | | tupla de 1000 | 4.016 |
| complex | 32 | | dict vazio | 16 |
| str de 1 a 11 caracteres | 32 | | dict com 100 pares int | 1.040 |
| str de 100 caracteres | 128 | | dict com 1000 pares int | 9.808 |
| str de 1000 caracteres | 1.024 | | set com 100 ints | 528 |
| lista vazia | 32 | | `range(1000000)` | 16 |
| instância vazia | 16 | | instância com 3 atributos | 48 |
| método ligado (`obj.m`) | 32 | | gerador | 32 |
| função compilada, 10 linhas | 192 | | função compilada, 100 linhas | 1.280 |

Uma lista de floats custa cinco vezes a de inteiros: 16 bytes por float mais 4 da posição.

### 8.3 O que cabe em 100 KB

Cada medida em processo novo, com `-X heapsize=100k` ([`resultados/limites_heap.md`](../12_Desenvolvimento/micropython-1.9.4/resultados/limites_heap.md)) **[medido]**:

| Medida | Resultado |
|---|---|
| Heap livre no início | 95.488 bytes (~93 KB) |
| Maior `[0]*n` | 22.180 itens |
| Maior `'x'*n` | 88.687 caracteres |
| Ints numa lista crescida com `append` | 16.384 |
| Floats numa lista crescida com `append` | 4.096 |
| Floats numa lista pré-alocada | 4.718 |
| Textos de 8 caracteres numa lista | 2.471 |
| Pares `int: int` num dict | 4.831 |
| Heap fragmentado | 46.544 bytes livres, mas o maior bloco contíguo tem 512 bytes |

Os valores variam dezenas de bytes entre execuções, porque o coletor examina a pilha de forma conservadora (seção 8.5). O `append` para em 16.384 porque a lista **dobra de capacidade** ao crescer: para passar de 16.384 posições precisa de um bloco novo de 128 KB. Se o tamanho é conhecido, `l = [0] * n` e depois `l[i] = …`.

### 8.4 Compilar também custa

Menor heap que permite importar e rodar um script sintético, com funções, `if`, laços e `print` **[medido]**:

| Script | Arquivo | Heap mínimo |
|---|---|---|
| exemplo `OHM.py` do cofre | 94 bytes | 3 KB |
| 50 linhas | 900 bytes | 6 KB |
| 150 linhas (limite do editor) | 2.750 bytes | 15 KB |
| 300 linhas | 5.585 bytes | 28 KB |
| 600 linhas | 11.255 bytes | 54 KB |
| 1200 linhas | 22.780 bytes | 111 KB — não caberia em ~100 KB |

Regra prática: **~5 bytes de heap por byte de código** para compilar. Comentários, linhas em branco e indentação quase não pesam; nomes longos pesam, porque cada nome novo é guardado na tabela de qstrs. A própria documentação do 1.9.4 recomenda evitar código que rode no momento do import e deixar a inicialização para depois de todos os imports, quando a memória do compilador já foi liberada **[código 1.9.4, `docs/reference/constrained.rst`]**. Dividir um programa grande em módulos distribui o pico da compilação, mas o bytecode de todos continua ocupando o heap.

### 8.5 Fragmentação e coletor conservador

- **Fragmentação:** depois de encher o heap com blocos de 256 bytes e liberar metade deles, sobraram 46 KB livres, mas nenhum pedaço contíguo maior que 512 bytes: nem uma lista de 1000 elementos (4 KB) cabe. Crie as estruturas grandes **no começo** do programa e reutilize-as.
- **Lixo que não some:** medidas feitas em sequência no mesmo processo deram resultados falsos, porque um ponteiro antigo deixado na pilha mantinha vivo um texto de 90 KB. O coletor é conservador: não sabe se um valor na pilha é ponteiro ou número. Trabalhe dentro de funções — os objetos locais morrem quando a função retorna — e dê `x = None` antes de criar outro objeto grande no nível do módulo.

### 8.6 Técnicas

1. Pré-aloque (`[0] * n`) em vez de crescer com `append` quando o tamanho é conhecido.
2. Prefira inteiros a floats em listas grandes (escala fixa: milésimos em `int`).
3. Use `range` e geradores em vez de listas intermediárias: `sum(x * x for x in range(n))` não cria lista.
4. Monte texto com uma lista de partes e `''.join()`.
5. Apague estruturas que não servem mais (`del l` ou `l = None`).
6. Mantenha o arquivo pequeno; mova dados fixos grandes para cálculo sob demanda.
7. Evite recursão funda; prefira laços.

## 9. Desempenho

Os tempos absolutos do PC não valem para a calculadora. As **proporções** mostram o que evitar dentro de laços **[medido]** ([`resultados/desempenho.md`](../12_Desenvolvimento/micropython-1.9.4/resultados/desempenho.md); oscilam ±20% entre rodadas):

| Construção (por iteração) | × laço vazio |
|---|---|
| `for i in range(N): pass` | 1,0 |
| compreensão de lista | ~0,7 |
| leitura de atributo `o.x` | ~1,7 |
| `x * x` / `x ** 2` | ~1,7 / ~1,9 |
| lista pré-alocada / `append` | ~2,1 / ~2,3 |
| soma em variável **local** / **global** | ~2,9 / ~4,1 |
| chamada de **função** / **método** | ~2,8 / ~4,7 |
| `math.sqrt(x)` / `raiz = math.sqrt; raiz(x)` | ~3,4 / ~2,7 |
| `try` sem exceção / com exceção levantada | ~1,2 / ~12 |
| **`s = s + 'x'`** em laço | **~2.500** |
| `''.join(partes)` | ~3,8 |

- **Concatenação de texto em laço é quadrática** no MicroPython (cada `+` copia tudo e aloca de novo); no CPython é otimizada. É a maior armadilha de desempenho.
- Variáveis globais e chamadas de método custam mais: coloque o laço dentro de uma função e guarde em variável local o que for usado muitas vezes (`raiz = math.sqrt`).
- Exceções custam caro quando levantadas; não as use como controle de fluxo em laço.
- Na calculadora, o processador da família SH-4 não teria unidade de ponto flutuante, e o double seria emulado em software **[comunidade + inferência]**. Nesse caso, contas com float pesam proporcionalmente mais que no PC. `MPYVEL` compara `T2` (inteiros) com `T3` (floats) no aparelho.
- Sem `time`, cronometre `MPYVEL` à mão e anote na tabela do [LEIA-ME do diagnóstico](../09_Anexos/Python/diagnostico/LEIA-ME.md).

## 10. Portabilidade entre PC e calculadora

### Escrever uma vez, rodar nos dois

- **Não use:** f-strings, `:=`, `match`, `1_000`, anotações de variável, `[*a, *b]`, `@`, `format()`, `next(it, padrão)`, `str.ljust/zfill/title`, fatias de texto com passo, `math.isclose/inf/factorial`, `random.shuffle`, `sys`, `time`, `os`, arquivos.
- **Não dependa de:** ordem de `dict`/`set`, `isinstance(True, int)`, `__del__`, `__slots__`, `__setattr__`, mensagens exatas de erro, `round()` para exibir, `==` entre floats.
- **Teste antes no aparelho:** classes com `*`, `/`, `-x`, `abs()` ou operadores refletidos; `str.center/partition/splitlines`; `pow(a, b, m)`; `frozenset`.
- **No fim do arquivo,** chame a função principal direto, sem `if __name__ == "__main__":`. Se precisar do guarda no PC, use `if __name__ in ('__main__', 'NOMEARQ'):` com o nome do arquivo.
- **`const()`:** para o mesmo código rodar no CPython, defina antes `try: const` / `except NameError: const = lambda x: x`.
- **Arquivo:** ASCII, nome de até 8 caracteres, indentação com espaços, até 150 linhas de 127 caracteres para poder editar no aparelho, CRLF ou LF.

### Testar no PC antes de copiar

```sh
cd 12_Desenvolvimento/micropython-1.9.4
./compilar.sh                                  # uma vez: gera bin/mpy194-teto e bin/mpy194-piso
python3 bancada/rodar_como_casio.py MEU.py --entradas "100;0.02"
python3 bancada/rodar_como_casio.py MEU.py --teto   # variante com todos os recursos opcionais
```

A bancada ([`rodar_como_casio.py`](../12_Desenvolvimento/micropython-1.9.4/bancada/rodar_como_casio.py)):

- roda o arquivo com `from NOME import *` e heap de 100 KB;
- bloqueia módulos que não existem na calculadora;
- avisa sobre nome, ASCII, linhas, tabulações, imports e prompts de `input()` com mais de 16 caracteres;
- conta linhas de saída com mais de 21 colunas;
- emula o `casioplot`.

Rodar no piso e no teto mostra, antes do aparelho, se o programa depende de alguma opção de compilação.

## 11. Armadilhas frequentes

| Sintoma na calculadora | Causa | Solução |
|---|---|---|
| `SyntaxError: invalid syntax` numa linha com `f"..."` | f-strings não existem | `'%.2f' % x` ou `'{:.2f}'.format(x)` |
| O programa roda, mas a parte principal não | `if __name__ == "__main__":` com `__name__` igual ao nome do arquivo | chamar `main()` direto |
| `print` mostra `538.2000000000001` | 16º dígito impreciso na escrita | `'%.6g' % x` |
| `round(x, 2)` ainda mostra muitos dígitos | `round` devolve float; a escrita volta a errar | formatar com `%` |
| Comparação de floats falha ou acerta "por sorte" | leitura e escrita inexatas | comparar com tolerância |
| Tabela impressa de um dict sai embaralhada | `dict` sem ordem | `for k in sorted(d):` |
| `NotImplementedError: only slices with step=1` | `s[::-1]` em texto ou tupla | `''.join(reversed(s))` |
| `TypeError: function takes 1 positional arguments but 2 were given` em `next` | `next(it, padrão)` não existe | `try: v = next(it)` / `except StopIteration: v = padrão` |
| `AttributeError: 'str' object has no attribute 'ljust'` | método ausente | `'%-10s' % s`, `'{:>10}'.format(s)` |
| `NameError: name 'format' is not defined` | não há `format()` embutido | `'{:.3f}'.format(x)` |
| `TypeError: unsupported types for : 'V', 'int'` | sobrecarga de `*`/`/` desligada | métodos com nome |
| `RuntimeError: maximum recursion depth exceeded` | pilha rasa (~82 níveis, comunidade) | reescrever como laço |
| `MemoryError` ao importar | compilação passou do heap | dividir o arquivo, encurtar, importar primeiro os módulos grandes |
| `MemoryError` numa lista longa | crescimento por `append` dobra a capacidade | pré-alocar `[0] * n`; usar inteiros |
| Programa lento ao montar texto | `s = s + ...` em laço | lista + `''.join()` |
| `ImportError: no module named 'time'` | módulo inexistente | laço de espera; `input()` para pausar |
| Números aleatórios iguais a cada execução | estado inicial fixo, se a Casio não semear **[a confirmar]** | `random.seed(...)` com valor do usuário |
| Desenho some depois de `input()` | a tela volta ao SHELL | chamar `show_screen()` de novo |
| `set_pixel` não desenha e não dá erro | coordenada fora de 0–127 × 0–63 é ignorada | conferir a conversão para a tela |
| Erro em `set_pixel` com coordenada calculada | a coordenada é float; o manual aceita só `int` | `int(round(x))` |
| `IndentationError` depois de editar no aparelho | tabulações viraram 2 espaços | indentar só com espaços |
| Edição no aparelho recusada ("Invalid Data Size") | mais de 150 linhas ou de 127 colunas | editar no PC; o arquivo ainda pode rodar |

## 12. Receitas: substitutos para o que falta

Todas funcionam no 1.9.4 **e** no CPython. O script [`sondas/testar_receitas.py`](../12_Desenvolvimento/micropython-1.9.4/sondas/testar_receitas.py) extrai este bloco do estudo e confere cada função no CPython, no teto e no piso.

```python
# Texto
def ljust(s, n, c=' '):
    return s + c * (n - len(s))
def rjust(s, n, c=' '):
    return c * (n - len(s)) + s
def zfill(s, n):
    return ('-' + rjust(s[1:], n - 1, '0')) if s[:1] == '-' else rjust(s, n, '0')
def inverte(s):
    return ''.join(reversed(s))
def isalnum(s):
    return len(s) > 0 and all(c.isalpha() or c.isdigit() for c in s)

# Iteradores
def proximo(it, padrao=None):
    try:
        return next(it)
    except StopIteration:
        return padrao

# math
def fatorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r
def mdc(a, b):
    while b:
        a, b = b, a % b
    return abs(a)
def perto(a, b, rel=1e-9, abs_=0.0):
    return abs(a - b) <= max(rel * max(abs(a), abs(b)), abs_)
def hipot(x, y):
    return (x * x + y * y) ** 0.5
INF = float('inf')
NAN = float('nan')
TAU = 2 * 3.141592653589793

# random (depois de import random)
def embaralha(l):                # Fisher-Yates, no lugar
    for i in range(len(l) - 1, 0, -1):
        j = random.randint(0, i)
        l[i], l[j] = l[j], l[i]
def amostra(pop, k):
    p = list(pop)
    embaralha(p)
    return p[:k]
def normal(mu=0.0, sigma=1.0):   # Box-Muller
    u = 1.0 - random.random()
    return mu + sigma * math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * random.random())

# Exibir números sem o 16º dígito
def fmt(x, dig=6):
    return '%.*g' % (dig, x)
```

## 13. O que isso muda nos arquivos do cofre

- **[[Exemplos Python]]:** os casos foram conferidos no CPython (`12_Desenvolvimento/testes/resultado-python.json`). No 1.9.4:
  - `FILTRO.py` imprime `fc Hz= 159.1549430918954`, 16 dígitos, e a linha passa das 21 colunas;
  - `DISCRETO.py` imprime `0.8823510000000001` e `0.9176459999999999` nas amostras 6 e 7.

  Sugestão, sem alterar os arquivos originais: `print(k, '%.6g' % y)` e `print('fc Hz=', '%.6g' % (1/(2*math.pi*R*C)))`. Os demais exemplos (`OHM`, `ESCALA`, `DEGRAU`, `QUAD`) saíram iguais aos valores esperados, e `TELA.py` desenhou o título e o ponto no emulador do `casioplot` **[medido na bancada]**.
- **[[casioplot]]:** o `casioplot` usa a tela inteira, 0–127 × 0–63 (manual 14-19). A área de 127 × 63 citada na nota vale para os gráficos nativos.
- **[[Python]]:** os limites de edição da nota coincidem com o manual. Vale acrescentar a execução por `from NOME import *` e os três módulos importáveis.

## 14. Alternativas e evolução

- **Versões do sistema.** O cofre documenta o OS 3.50 e a Casio anuncia 3.70 ([[Sistema e firmware]]). Para a Graph 35+E II francesa, a comunidade descreve a 3.60 (09/2022) e a 3.70 (06/2023) como mudanças de tradução e de menu de cálculo, e cita uma 3.71 de correção **[comunidade]**. Não foi encontrada menção a troca da versão do MicroPython; confirme a do seu aparelho no banner do SHELL.
- **PythonExtra** (Planète Casio, Lephenixnoir): add-in da comunidade para fx-CG50 e fx-9860GIII/fx-9750GIII com um MicroPython mais novo, mais módulos, leitura de teclas e gráficos mais rápidos; um tópico do Cemetech anuncia "MicroPython 1.12 for the casio Prizm and fx-9750gIII" **[comunidade]**. É software de terceiros: a compatibilidade e o uso em provas precisam ser conferidos, como em [[Addins e desenvolvimento]].
- **CasioPython** (terceiros, mais antigo) chegou a milhares de níveis de recursão onde o Python oficial para em ~82 **[comunidade]**.
- **KhiCAS** traz linguagem própria, próxima do Python, com recursos que o Python oficial não tem, como leitura de teclas **[comunidade]** — ver [[KhiCAS e CAS]].
- **fx-CG100** (colorida, posterior) adicionou `getkey` ao `casioplot` **[comunidade]**; não se aplica à fx-9750GIII.

## 15. Diagnóstico no aparelho

Cinco scripts em [`09_Anexos/Python/diagnostico`](../09_Anexos/Python/diagnostico/LEIA-ME.md), cada um com até 150 linhas, ASCII e saída em linhas de até 21 colunas:

| Script | Responde |
|---|---|
| `MPYINFO` | módulos importáveis; nomes embutidos ausentes; conteúdo de `math`, `random` e `casioplot`; métodos de `str`; se a semente aleatória é fixa |
| `MPYSINT` | 20 diferenças do núcleo (esperado: todas falham) e 24 recursos que dependem da compilação da Casio |
| `MPYNUM` | aritmética: bits da mantissa, faixa, leitura e escrita de decimais, `round`, estouros, complexos |
| `MPYMEM` | heap livre estimado, maior lista possível e profundidade máxima de recursão |
| `MPYVEL` | velocidade relativa (com cronômetro): laço, inteiros × floats, funções, texto e pixels |

O [LEIA-ME](../09_Anexos/Python/diagnostico/LEIA-ME.md) traz o resultado esperado de cada linha no 1.9.4 e uma coluna em branco para anotar o do aparelho. Quando esses resultados existirem, este estudo pode trocar os **[a confirmar]** por **[aparelho, OS x.xx]**.

## 16. Fontes e cobertura

| Fonte | O que sustenta | Acesso |
|---|---|---|
| Manual SW350, cap. 14 e apêndices (PDF 351–381, 399, 404) | execução, SHELL, arquivos, teclas, módulos, `casioplot`, modo exame, licença | lido no PDF local; figuras conferidas |
| Manual de hardware (PDF 10) | memórias de 62.000 bytes e 3 MB, mantissa de 15 dígitos, faixa 10^±99 | lido no PDF anexado |
| MicroPython, tag `v1.9.4` ([github.com/micropython/micropython](https://github.com/micropython/micropython/tree/v1.9.4)) | notas de versão, código (`parsenum.c`, `formatfloat.c`, `modbuiltins.c`, `modmath.c`, `modurandom.c`, `runtime.c`), `docs/reference/constrained.rst`, `tests/cpydiff` | clonado e compilado |
| Tags 1.9 a 1.29.0 do mesmo repositório | linha do tempo | datas lidas nas tags |
| Laboratório deste estudo | todos os **[medido]** | [`12_Desenvolvimento/micropython-1.9.4`](../12_Desenvolvimento/micropython-1.9.4/README.md) |
| TI-Planet (QCC 2020 e artigos sobre OS 3.30/3.40, `turtle`, `matplotl`) | heap ~100 KB, recursão 82, double de 53 bits, inteiros longos, contagens de módulos | **bloqueado pela rede**; resumos de busca |
| HP Museum, "Casio Python updates" | OS 3.40 (25/11/2020) com `casioplot` na fx-9750GIII | bloqueado; resumo de busca |
| Planète Casio (PythonExtra; OS 3.60, 3.70 e 3.71 da Graph 35+E II) | alternativas e versões | bloqueado; resumo de busca |
| [P0pMan20/casioplot-documentation](https://github.com/P0pMan20/casioplot-documentation) | uso do `casioplot` visto pela comunidade (fx-CG50) | clonado |
| [AbdelRahmanRahal/Casio-fx-9750GIII-Programs](https://github.com/AbdelRahmanRahal/Casio-fx-9750GIII-Programs) | programas para a fx-9750GIII; importa `sinh, cosh, tanh`; testa num MicroPython 1.9.4 compilado para Windows | clonado |
| Blog "Eddie's Math and Calculator Blog" (fx-CG100 `getkey`) | `getkey` só no modelo novo | resumo de busca |

## Conferir

- [[08_Manuais/fx-9750GIII_Soft_v350_EN.pdf#page=351|SW350 — PDF 351, cap. 14 (Python)]]
- [[08_Manuais/fx-9750GIII_Soft_v350_EN.pdf#page=356|SW350 — PDF 356, teclas]]
- [[08_Manuais/fx-9750GIII_Soft_v350_EN.pdf#page=363|SW350 — PDF 363, SHELL]]
- [[08_Manuais/fx-9750GIII_Soft_v350_EN.pdf#page=367|SW350 — PDF 367, execução e casioplot]]
- [[08_Manuais/fx-9750GIII_Soft_v350_EN.pdf#page=369|SW350 — PDF 369, coordenadas do casioplot]]
- [[08_Manuais/fx-9750GIII_Soft_v350_EN.pdf#page=376|SW350 — PDF 376, arquivos]]
- [[08_Manuais/fx-9860GIII_9750GIII_7400GIII_Hard_EN.pdf#page=10|Hardware — PDF 10, especificações]]

[[00_Inicio/COMECE AQUI|Início]] · [[04_Programacao/Python|Python]] · [[07_Fontes/Registro de fontes|Fontes]]
