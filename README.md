# fx-9750GIII — estudo do MicroPython 1.9.4

Estudo aprofundado do Python da Casio fx-9750GIII: o **MicroPython 1.9.4** adaptado pela Casio. O comportamento foi medido no MicroPython 1.9.4 oficial, compilado no PC, e acompanha scripts para confirmar no aparelho o que só ele responde.

As pastas repetem a estrutura do cofre Obsidian `Cofre_fx9750GIII`. Para integrar, copie cada arquivo para o mesmo caminho dentro do cofre. Os manuais da Casio e o restante do cofre não estão neste repositório.

| Caminho | Conteúdo |
|---|---|
| [`04_Programacao/MicroPython 1.9.4 - estudo aprofundado.md`](04_Programacao/MicroPython%201.9.4%20-%20estudo%20aprofundado.md) | **o estudo**: linguagem, números, módulos, `casioplot`, memória, desempenho, portabilidade, armadilhas e receitas |
| [`09_Anexos/Python/diagnostico/`](09_Anexos/Python/diagnostico/LEIA-ME.md) | cinco scripts para rodar na calculadora (`MPYINFO`, `MPYSINT`, `MPYNUM`, `MPYMEM`, `MPYVEL`) e a tabela com o resultado esperado de cada linha |
| [`12_Desenvolvimento/micropython-1.9.4/`](12_Desenvolvimento/micropython-1.9.4/README.md) | laboratório reprodutível: compilação do 1.9.4 em duas configurações, sondas, resultados e a bancada que roda um `.py` como a calculadora |

## Em uma linha cada

- Não há f-strings, `:=`, `match`, `1_000` nem `[*a, *b]`: é Python 3.4 com cortes.
- A calculadora roda o arquivo com `from NOME import *`, então `if __name__ == "__main__":` não executa.
- Só `math`, `random`, `casioplot` e `.py` da mesma pasta podem ser importados.
- `dict` não guarda a ordem de inserção; `'abc'[::-1]`, `next(it, padrão)`, `str.ljust` e `format()` não existem.
- `print(538.2)` mostra `538.2000000000001` e `0.1 + 0.2 == 0.3` dá `True`: leitura e escrita de floats não são exatas no 1.9.4.
- Heap de ~100 KB (relato da comunidade): compilar custa ~5× o tamanho do arquivo; concatenar texto em laço é quadrático.

Copiados para o cofre, os textos e scripts seguem a licença MIT dele (`LICENSE-MIT.txt`, na raiz do cofre). O MicroPython (MIT) é baixado da fonte oficial pelo `compilar.sh`, não redistribuído.
