# Custo relativo de construções — MicroPython 1.9.4 × CPython 3.11.15

Gerado por `sondas/rodar_desempenho.py`. Tempo por iteração dividido pelo do laço vazio `for i in range(N): pass` do mesmo interpretador (melhor de 3). Valores absolutos do PC não se aplicam à calculadora: lá a CPU é muito mais lenta e o ponto flutuante é emulado em software, o que torna as contas com float proporcionalmente mais caras.

| Construção | 1.9.4 (× laço vazio) | CPython (× laço vazio) |
|---|---|---|
| for i in range(N): pass | 1.0 | 1.0 |
| while i < N: i += 1 | 1.0 | 3.3 |
| soma em variavel local | 2.9 | 1.9 |
| soma em variavel global | 4.1 | 1.9 |
| soma de float | 2.5 | 1.0 |
| leitura de atributo o.x | 1.7 | 1.2 |
| chamada de funcao vazia | 2.8 | 1.6 |
| chamada de metodo | 4.7 | 1.7 |
| math.sqrt(2.0) | 3.4 | 1.4 |
| raiz = math.sqrt; raiz(2.0) | 2.7 | 1.2 |
| x ** 2 | 1.9 | 1.4 |
| x * x | 1.7 | 0.8 |
| lista com append | 2.3 | 1.8 |
| lista por compreensao | 0.7 | 1.2 |
| lista pre-alocada [0]*N | 2.1 | 1.5 |
| texto: s = s + 'x' (N/10) | 2567.4 | 1.7 |
| texto: ''.join(partes) (N/10) | 3.8 | 1.0 |
| leitura d[2] em dict | 2.2 | 1.6 |
| leitura l[1] em lista | 2.0 | 1.2 |
| try/except sem excecao | 1.2 | 0.5 |
| try/except com excecao (N/10) | 12.4 | 4.3 |
| int grande 2**100 + i (N/10) | 3.3 | 1.4 |
