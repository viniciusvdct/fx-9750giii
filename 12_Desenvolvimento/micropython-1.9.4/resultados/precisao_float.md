# Exatidão de leitura e escrita de floats — MicroPython 1.9.4

Gerado por `sondas/precisao_float.py` com `mpy194-teto`. Referência: CPython, que lê e escreve com arredondamento correto. "Leitura errada" = `float(texto)` do 1.9.4 difere do double mais próximo. "Escrita errada" = os 16 dígitos do `repr` do 1.9.4 diferem do valor arredondado corretamente. "Sem ida e volta" = `float(repr(x)) != x` no próprio 1.9.4.

| Amostra | n | Leitura errada | Máx. erro (ulps) | Escrita errada (16 díg.) | Sem ida e volta |
|---|---|---|---|---|---|
| digitadas (1 a 6 dígitos) | 20000 | 4742 (23.7%) | 1 | 4494 (22.5%) | 3815 (19.1%) |
| longas (15 a 17 dígitos, 1e-10 a 1e10) | 20000 | 6799 (34.0%) | 3 | 6396 (32.0%) | 7359 (36.8%) |
| resultados de contas (bits aleatórios) | 20000 | 7244 (36.2%) | 2 | 4668 (23.3%) | 9857 (49.3%) |

## Exemplos

- Leitura (digitadas (1 a 6 dígitos)): `float("331.9")` → CPython `331.9`, 1.9.4 `331.90000000000003`
- Leitura (digitadas (1 a 6 dígitos)): `float("158.2")` → CPython `158.2`, 1.9.4 `158.20000000000002`
- Leitura (digitadas (1 a 6 dígitos)): `float("768.8")` → CPython `768.8`, 1.9.4 `768.8000000000001`
- Escrita (digitadas (1 a 6 dígitos)): valor `449.2817`, 16 dígitos corretos `4.492817000000000e+02`, 1.9.4 escreve `449.2817000000001`
- Escrita (digitadas (1 a 6 dígitos)): valor `934.885`, 16 dígitos corretos `9.348850000000000e+02`, 1.9.4 escreve `934.8850000000001`
- Escrita (digitadas (1 a 6 dígitos)): valor `486.3897`, 16 dígitos corretos `4.863897000000000e+02`, 1.9.4 escreve `486.3897000000001`
- Leitura (longas (15 a 17 dígitos, 1e-10 a 1e10)): `float("9.1638683275706226e-08")` → CPython `9.163868327570623e-08`, 1.9.4 `9.163868327570621e-08`
- Leitura (longas (15 a 17 dígitos, 1e-10 a 1e10)): `float("9.848246261642167e+06")` → CPython `9848246.261642167`, 1.9.4 `9848246.26164217`
- Leitura (longas (15 a 17 dígitos, 1e-10 a 1e10)): `float("8.48423170531218e+10")` → CPython `84842317053.1218`, 1.9.4 `84842317053.12181`
- Escrita (longas (15 a 17 dígitos, 1e-10 a 1e10)): valor `0.0009862851835662158`, 16 dígitos corretos `9.862851835662158e-04`, 1.9.4 escreve `0.0009862851835662157`
- Escrita (longas (15 a 17 dígitos, 1e-10 a 1e10)): valor `9.45918318122943e-09`, 16 dígitos corretos `9.459183181229430e-09`, 1.9.4 escreve `9.459183181229431e-09`
- Escrita (longas (15 a 17 dígitos, 1e-10 a 1e10)): valor `9.163868327570621e-08`, 16 dígitos corretos `9.163868327570621e-08`, 1.9.4 escreve `9.163868327570622e-08`
- Leitura (resultados de contas (bits aleatórios)): `float("0.015934480717801423")` → CPython `0.015934480717801423`, 1.9.4 `0.015934480717801427`
- Leitura (resultados de contas (bits aleatórios)): `float("6.533241758515837e-08")` → CPython `6.533241758515837e-08`, 1.9.4 `6.533241758515836e-08`
- Leitura (resultados de contas (bits aleatórios)): `float("43.837014371217975")` → CPython `43.837014371217975`, 1.9.4 `43.83701437121798`
- Escrita (resultados de contas (bits aleatórios)): valor `78223192.70255777`, 16 dígitos corretos `7.822319270255777e+07`, 1.9.4 escreve `78223192.70255779`
- Escrita (resultados de contas (bits aleatórios)): valor `943237982.3200294`, 16 dígitos corretos `9.432379823200294e+08`, 1.9.4 escreve `943237982.3200295`
- Escrita (resultados de contas (bits aleatórios)): valor `6.533241758515836e-08`, 16 dígitos corretos `6.533241758515836e-08`, 1.9.4 escreve `6.533241758515835e-08`
