# Sondas de linguagem — CPython × MicroPython 1.9.4

Gerado por `comparar.py`. CPython 3.11.15; MicroPython 1.9.4 compilado em 32 bits nas variantes *teto* (porta unix) e *piso* (opções no padrão do núcleo). Texto em **negrito** = exceção levantada.

Resumo: 268 sondas — 136 iguais ao CPython, 113 diferenças do núcleo 1.9.4, 19 dependentes da configuração.

| ID | Recurso | CPython | 1.9.4 teto | 1.9.4 piso | Classe |
|---|---|---|---|---|---|
| S01 | f-string (PEP 498, Python 3.6) | '2' | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| S02 | operador morsa := (3.8) | [5, 5] | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| S03 | parametro so-posicional / (3.8) | 3 | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| S04 | anotacao de funcao (3.0) | 6 | 6 | 6 | igual ao CPython |
| S05 | anotacao de variavel x: int = 5 (3.6) | 5 | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| S06 | separador _ em numeros 1_000 (3.6) | 1000000 | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| S07 | async def / await (3.5) | 'compilou' | 'compilou' | 'compilou' | igual ao CPython |
| S08 | nonlocal | 2 | 2 | 2 | igual ao CPython |
| S09 | yield from | [0, 1, 2] | [0, 1, 2] | [0, 1, 2] | igual ao CPython |
| S10 | argumento so-nomeado (*, b) | 6 | 6 | 6 | igual ao CPython |
| S11 | desempacotamento estendido a, *b, c | (1, [2, 3, 4], 5) | (1, [2, 3, 4], 5) | (1, [2, 3, 4], 5) | igual ao CPython |
| S12 | PEP 448: [*a, *b] | [1, 2, 3] | **SyntaxError: *x must be assignment target** | **SyntaxError: *x must be assignment target** | núcleo 1.9.4 |
| S13 | PEP 448: {**d1, **d2} | [('a', 1), ('b', 2)] | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| S14 | PEP 448: f(*a, *b) | (1, 2) | **SyntaxError: can't have multiple *x** | **SyntaxError: can't have multiple *x** | núcleo 1.9.4 |
| S15 | operador @ (__matmul__, 3.5) | 42 | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| S16 | compreensao de conjunto | [0, 1, 2] | [0, 1, 2] | [0, 1, 2] | igual ao CPython |
| S17 | compreensao de dicionario | [(0, 0), (1, 1), (2, 4)] | [(0, 0), (1, 1), (2, 4)] | [(0, 0), (1, 1), (2, 4)] | igual ao CPython |
| S18 | expressao condicional em lambda | 'impar' | 'impar' | 'impar' | igual ao CPython |
| S19 | comparacao encadeada 1 < 2 < 3 | True | True | True | igual ao CPython |
| S20 | raise ... from ... (encadeamento) | ('ValueError', ZeroDivisionError('division by zero')) | ('ValueError', 'sem __cause__') | ('ValueError', 'sem __cause__') | núcleo 1.9.4 |
| S21 | with + gerenciador de contexto proprio | ['in', 'corpo', 'out'] | ['in', 'corpo', 'out'] | ['in', 'corpo', 'out'] | igual ao CPython |
| S22 | decorador de funcao e de classe | (20, 1) | (20, 1) | (20, 1) | igual ao CPython |
| S23 | match/case (3.10) | 'um' | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| S24 | literais 0b 0o 0x | (5, 15, 31) | (5, 15, 31) | (5, 15, 31) | igual ao CPython |
| S25 | literal complexo 1j | (5+5j) | (5+5j) | (5+5j) | igual ao CPython |
| S26 | prefixos r b u rb | ('\\n', b'ab', 'x', b'\\d') | ('\\n', b'ab', 'x', b'\\d') | ('\\n', b'ab', 'x', b'\\d') | igual ao CPython |
| S27 | escape \N{nome unicode} | 'α' | **NotImplementedError: unicode name escapes** | **NotImplementedError: unicode name escapes** | núcleo 1.9.4 |
| S28 | return *a, 3 (3.8) | (1, 2, 3) | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| S29 | for ... else / while ... else | ('for-else', 'while-else') | ('for-else', 'while-else') | ('for-else', 'while-else') | igual ao CPython |
| S30 | docstring acessivel em __doc__ | 'documentacao' | **AttributeError: 'function' object has no attribute '__doc__'** | **AttributeError: 'function' object has no attribute '__doc__'** | núcleo 1.9.4 |
| S31 | identificador nao ASCII | 1 | 1 | 1 | igual ao CPython |
| S32 | metaclass= | 'M' | **TypeError: function does not take keyword arguments** | **TypeError: function does not take keyword arguments** | núcleo 1.9.4 |
| S33 | global dentro de funcao | 2 | 2 | 2 | igual ao CPython |
| S34 | Ellipsis ... | Ellipsis | Ellipsis | Ellipsis | igual ao CPython |
| S35 | type hints com default | 3 | 3 | 3 | igual ao CPython |
| N01 | 0.1 + 0.2 == 0.3 | False | True | True | núcleo 1.9.4 |
| N02 | repr(0.1 + 0.2) | 0.30000000000000004 | 0.3 | 0.3 | núcleo 1.9.4 |
| N03 | str(0.1 + 0.2) | '0.30000000000000004' | '0.3' | '0.3' | núcleo 1.9.4 |
| N04 | 2 ** 0.5 | 1.4142135623730951 | 1.414213562373095 | 1.414213562373095 | núcleo 1.9.4 |
| N05 | 1 / 3 e 2 / 3 | (0.3333333333333333, 0.6666666666666666) | (0.3333333333333333, 0.6666666666666666) | (0.3333333333333333, 0.6666666666666666) | igual ao CPython |
| N06 | sum([0.1] * 10) | 0.9999999999999999 | 1.0 | 1.0 | núcleo 1.9.4 |
| N07 | str() de floats variados | ['1e+16', '1000000000000000.0', '123456789.12345679', '100.0', '-0.0', '1e+22', '12345678.9', '1e-05', '0.0001', '1e+100'] | ['1e+16', '1000000000000000.0', '123456789.1234568', '100.0', '-0.0', '1e+22', '12345678.9', '1e-05', '0.0001', '1e+100'] | ['1e+16', '1000000000000000.0', '123456789.1234568', '100.0', '-0.0', '1e+22', '12345678.9', '1e-05', '0.0001', '1e+100'] | núcleo 1.9.4 |
| N08 | transbordo 1e308 * 10 | (inf, -inf) | (inf, -inf) | (inf, -inf) | igual ao CPython |
| N09 | subnormais 5e-324 e 1e-324 | (5e-324, 0.0, 0.0) | (4.940656458412466e-324, 0.0, 0.0) | (4.940656458412466e-324, 0.0, 0.0) | núcleo 1.9.4 |
| N10 | inteiros grandes 2 ** 100 | 1267650600228229401496703205376 | 1267650600228229401496703205376 | 1267650600228229401496703205376 | igual ao CPython |
| N11 | (2**64 + 1) - 2**64 | 1 | 1 | 1 | igual ao CPython |
| N12 | divisao / // % com negativos | (3.5, 3, -4, 1, 2, -2, 3.0, (-4, 1)) | (3.5, 3, -4, 1, 2, -2, 3.0, (-4, 1)) | (3.5, 3, -4, 1, 2, -2, 3.0, (-4, 1)) | igual ao CPython |
| N13 | 1 / 0 | **ZeroDivisionError: division by zero** | **ZeroDivisionError: division by zero** | **ZeroDivisionError: division by zero** | igual ao CPython |
| N14 | 1.0 / 0 | **ZeroDivisionError: float division by zero** | **ZeroDivisionError: division by zero** | **ZeroDivisionError: division by zero** | núcleo 1.9.4 |
| N15 | 1 % 0 | **ZeroDivisionError: integer modulo by zero** | **ZeroDivisionError: division by zero** | **ZeroDivisionError: division by zero** | núcleo 1.9.4 |
| N16 | 0 ** 0, 0.0 ** 0 | (1, 1.0) | (1, 1.0) | (1, 1.0) | igual ao CPython |
| N17 | 0 ** -1 | **ZeroDivisionError: 0.0 cannot be raised to a negative power** | **ZeroDivisionError: division by zero** | **ZeroDivisionError: division by zero** | núcleo 1.9.4 |
| N18 | 2.0 ** 10000 | **OverflowError: (34, 'Numerical result out of range')** | inf | inf | núcleo 1.9.4 |
| N19 | float(10 ** 400) | **OverflowError: int too large to convert to float** | inf | inf | núcleo 1.9.4 |
| N20 | int(1e300) exato | False | False | False | igual ao CPython |
| N21 | int(float("inf")) | **OverflowError: cannot convert float infinity to integer** | **OverflowError: can't convert inf to int** | **OverflowError: can't convert inf to int** | núcleo 1.9.4 |
| N22 | int(float("nan")) | **ValueError: cannot convert float NaN to integer** | **ValueError: can't convert NaN to int** | **ValueError: can't convert NaN to int** | núcleo 1.9.4 |
| N23 | round(): meio-a-par e casas | (2, 4, 0, 0, 2.67, 1200, 2) | (2, 4, 0, 0, 2.68, 1234, 2) | (2, 4, 0, 0, 2.68, 1234, 2) | núcleo 1.9.4 |
| N24 | round(x) devolve int | 'int' | 'int' | 'int' | igual ao CPython |
| N25 | int() de textos | (12, 12, 255, 31, 5, 3, -3) | (12, 12, 255, 31, 5, 3, -3) | (12, 12, 255, 31, 5, 3, -3) | igual ao CPython |
| N26 | int("1_0") | 10 | **ValueError: invalid syntax for integer with base 10: '1_0'** | **ValueError: invalid syntax for integer with base 10** | depende da configuração |
| N27 | int("3.5") | **ValueError: invalid literal for int() with base 10: '3.5'** | **ValueError: invalid syntax for integer with base 10: '3.5'** | **ValueError: invalid syntax for integer with base 10** | depende da configuração |
| N28 | float() de textos | (2.5, 1000.0, inf, -inf, -0.0) | (2.5, 1000.0, inf, -inf, -0.0) | (2.5, 1000.0, inf, -inf, -0.0) | igual ao CPython |
| N29 | float("nan") != float("nan") | (True, 'nan') | (True, 'nan') | (True, 'nan') | igual ao CPython |
| N30 | pow() 3 argumentos e negativos | (24, 0.5, 2) | (24, 0.5, 2) | **NotImplementedError: 3-arg pow() not supported** | depende da configuração |
| N31 | (-8) ** (1/3) | (1.0000000000000002+1.7320508075688772j) | (1+1.732050807568877j) | (1+1.732050807568877j) | núcleo 1.9.4 |
| N32 | (-1) ** 0.5 | (6.123233995736766e-17+1j) | (6.123233995736767e-17+1j) | (6.123233995736767e-17+1j) | núcleo 1.9.4 |
| N33 | abs() de float e complexo | (3.5, 5.0) | (3.5, 5.0) | (3.5, 5.0) | igual ao CPython |
| N34 | complexos: atributos e metodos | (3.0, 4.0, (3-4j), (-1+0j), (1+2j)) | **AttributeError: 'complex' object has no attribute 'conjugate'** | **AttributeError: 'complex' object has no attribute 'conjugate'** | núcleo 1.9.4 |
| N35 | complex("1+2j") | (1+2j) | **ValueError: invalid syntax for number** | **ValueError: invalid syntax for number** | núcleo 1.9.4 |
| N36 | int.to_bytes / from_bytes | (b'\x00\xff', 256) | (b'\x00\xff', 256) | (b'\x00\xff', 256) | igual ao CPython |
| N37 | int.bit_length() | 3 | **AttributeError: 'int' object has no attribute 'bit_length'** | **AttributeError: 'int' object has no attribute 'bit_length'** | núcleo 1.9.4 |
| N38 | float.is_integer() | True | **AttributeError: 'float' object has no attribute 'is_integer'** | **AttributeError: 'float' object has no attribute 'is_integer'** | núcleo 1.9.4 |
| N39 | float.as_integer_ratio() | (1, 2) | **AttributeError: 'float' object has no attribute 'as_integer_ratio'** | **AttributeError: 'float' object has no attribute 'as_integer_ratio'** | núcleo 1.9.4 |
| N40 | float.hex() / fromhex | '0x1.0000000000000p+0' | **AttributeError: 'float' object has no attribute 'hex'** | **AttributeError: 'float' object has no attribute 'hex'** | núcleo 1.9.4 |
| N41 | True + True, bool e int | (2, True) | (2, False) | (2, False) | núcleo 1.9.4 |
| N42 | 2**53 + 1 vs float | (False, 9007199254740992.0) | (True, 9007199254740993.0) | (True, 9007199254740993.0) | núcleo 1.9.4 |
| N43 | 1e16 + 1 e 1e16 + 2 | (1e+16, 1.0000000000000002e+16) | (1e+16, 1e+16) | (1e+16, 1e+16) | núcleo 1.9.4 |
| N44 | int(0.1 * 3 * 10) | 3 | 3 | 3 | igual ao CPython |
| N45 | hash(1.5), hash(-1) | ('int', -2) | ('int', -1) | ('int', -1) | núcleo 1.9.4 |
| N46 | comparacao int grande x float | (True, True) | (True, True) | (True, True) | igual ao CPython |
| N47 | len(range(10**10)) | 10000000000 | **OverflowError: overflow converting long int to machine word** | **OverflowError: overflow converting long int to machine word** | núcleo 1.9.4 |
| N48 | divmod(7.5, 2), 7.5 % 2 | ((3.0, 1.5), 1.5, 0.5) | ((3.0, 1.5), 1.5, 0.5) | ((3.0, 1.5), 1.5, 0.5) | igual ao CPython |
| M01 | math.floor/ceil/trunc devolvem int | (2, 'int', -2, -2) | (2, 'int', -2, -2) | (2, 'int', -2, -2) | igual ao CPython |
| M02 | math.sqrt, pow, exp, e, pi | (1.4142135623730951, 1.4142135623730951, 2.718281828459045, 2.718281828459045, 3.141592653589793) | (1.414213562373095, 1.414213562373095, 2.718281828459045, 2.718281828459045, 3.141592653589793) | (1.414213562373095, 1.414213562373095, 2.718281828459045, 2.718281828459045, 3.141592653589793) | núcleo 1.9.4 |
| M03 | math.log(x) e math.log(x, base) | (1.0, 3.0, 2.0) | (1.0, 3.0, 2.0) | (1.0, 3.0, 2.0) | igual ao CPython |
| M04 | math.log10 e math.log2 | (3.0, 3.0) | (3.0, 3.0) | (3.0, 3.0) | igual ao CPython |
| M05 | math.sin(pi), cos, tan | (1.2246467991473532e-16, -1.0, 0.9999999999999999) | (1.224646799147353e-16, -1.0, 1.0) | (1.224646799147353e-16, -1.0, 1.0) | núcleo 1.9.4 |
| M06 | asin, acos, atan, atan2 | (1.5707963267948966, 1.5707963267948966, 0.7853981633974483, 2.356194490192345) | (1.570796326794897, 1.570796326794897, 0.7853981633974483, 2.356194490192345) | (1.570796326794897, 1.570796326794897, 0.7853981633974483, 2.356194490192345) | núcleo 1.9.4 |
| M07 | degrees, radians | (180.0, 3.141592653589793) | (180.0, 3.141592653589793) | (180.0, 3.141592653589793) | igual ao CPython |
| M08 | hiperbolicas sinh cosh tanh asinh acosh atanh | (1.1752011936438014, 1.5430806348152437, 0.7615941559557649, 0.881373587019543, 1.3169578969248166, 0.5493061443340548) | (1.175201193643801, 1.543080634815244, 0.7615941559557649, 0.881373587019543, 1.316957896924817, 0.5493061443340549) | (1.175201193643801, 1.543080634815244, 0.7615941559557649, 0.881373587019543, 1.316957896924817, 0.5493061443340549) | núcleo 1.9.4 |
| M09 | especiais erf erfc gamma lgamma expm1 | (0.8427007929497149, 0.15729920705028513, 24.0, 3.178053830347945, 1.00000000005e-10) | (0.8427007929497149, 0.1572992070502851, 24.0, 3.178053830347946, 1.00000000005e-10) | (0.8427007929497149, 0.1572992070502851, 24.0, 3.178053830347946, 1.00000000005e-10) | núcleo 1.9.4 |
| M10 | fabs fmod copysign modf frexp ldexp | (2.0, -1.0, -1.0, (0.5, 2.0), (0.5, 4), 1024.0) | (2.0, -1.0, -1.0, (0.5, 2.0), (0.5, 4), 1024.0) | (2.0, -1.0, -1.0, (0.5, 2.0), (0.5, 4), 1024.0) | igual ao CPython |
| M11 | isfinite isinf isnan | (True, True, True) | (True, True, True) | (True, True, True) | igual ao CPython |
| M12 | math.factorial | 2432902008176640000 | **AttributeError: 'module' object has no attribute 'factorial'** | **AttributeError: 'module' object has no attribute 'factorial'** | núcleo 1.9.4 |
| M13 | math.gcd | 6 | **AttributeError: 'module' object has no attribute 'gcd'** | **AttributeError: 'module' object has no attribute 'gcd'** | núcleo 1.9.4 |
| M14 | math.isclose | True | **AttributeError: 'module' object has no attribute 'isclose'** | **AttributeError: 'module' object has no attribute 'isclose'** | núcleo 1.9.4 |
| M15 | math.inf e math.nan | (inf, nan) | **AttributeError: 'module' object has no attribute 'inf'** | **AttributeError: 'module' object has no attribute 'inf'** | núcleo 1.9.4 |
| M16 | math.tau | 6.283185307179586 | **AttributeError: 'module' object has no attribute 'tau'** | **AttributeError: 'module' object has no attribute 'tau'** | núcleo 1.9.4 |
| M17 | math.hypot | 5.0 | **AttributeError: 'module' object has no attribute 'hypot'** | **AttributeError: 'module' object has no attribute 'hypot'** | núcleo 1.9.4 |
| M18 | math.fsum | 1.0 | **AttributeError: 'module' object has no attribute 'fsum'** | **AttributeError: 'module' object has no attribute 'fsum'** | núcleo 1.9.4 |
| M19 | math.comb / perm / prod / isqrt / dist | ['comb', 'perm', 'prod', 'isqrt', 'dist', 'lcm', 'cbrt', 'exp2', 'remainder', 'ulp', 'nextafter'] | [] | [] | núcleo 1.9.4 |
| M20 | math.sqrt(-1) | **ValueError: math domain error** | **ValueError: math domain error** | **ValueError: math domain error** | igual ao CPython |
| M21 | math.log(0) | **ValueError: math domain error** | **ValueError: math domain error** | **ValueError: math domain error** | igual ao CPython |
| M22 | math.acos(2) | **ValueError: math domain error** | **ValueError: math domain error** | **ValueError: math domain error** | igual ao CPython |
| M23 | math.exp(1000) | **OverflowError: math range error** | **ValueError: math domain error** | **ValueError: math domain error** | núcleo 1.9.4 |
| M24 | math.floor(1e300) exato | True | True | True | igual ao CPython |
| M25 | math.pow(-8, 1/3) | **ValueError: math domain error** | **ValueError: math domain error** | **ValueError: math domain error** | igual ao CPython |
| R01 | funcoes do random | ['BPF', 'LOG4', 'NV_MAGICCONST', 'RECIP_BPF', 'Random', 'SG_MAGICCONST', 'SystemRandom', 'TWOPI', 'betavariate', 'choice', 'choices', 'expovariate', 'gammavariate', 'gauss', 'getrandbits', 'getstate', 'lognormvariate', 'normalvariate', 'paretovariate', 'randbytes', 'randint', 'random', 'randrange', 'sample', 'seed', 'setstate', 'shuffle', 'triangular', 'uniform', 'vonmisesvariate', 'weibullvariate'] | ['choice', 'getrandbits', 'randint', 'random', 'randrange', 'seed', 'uniform'] | ['choice', 'getrandbits', 'randint', 'random', 'randrange', 'seed', 'uniform'] | núcleo 1.9.4 |
| R02 | random.seed(1) reproduz sequencia | True | True | True | igual ao CPython |
| R03 | random.shuffle / sample / gauss / choices | ['shuffle', 'sample', 'gauss', 'choices', 'triangular', 'normalvariate'] | [] | [] | núcleo 1.9.4 |
| R04 | randrange com passo | True | True | True | igual ao CPython |
| R05 | random.seed() sem argumento | 'aceito' | **TypeError: function takes 1 positional arguments but 0 were given** | **TypeError: function takes 1 positional arguments but 0 were given** | núcleo 1.9.4 |
| F01 | % com .2f d s r | " 3.14\|42\|a\|'b'" | " 3.14\|42\|a\|'b'" | " 3.14\|42\|a\|'b'" | igual ao CPython |
| F02 | % com x o e g | 'ff 10 1.234568e+04 1e-05' | 'ff 10 1.234568e+04 1e-05' | 'ff 10 1.234568e+04 1e-05' | igual ao CPython |
| F03 | % alinhamento e zeros | 'ab   \|00042\|+5' | 'ab   \|00042\|+5' | 'ab   \|00042\|+5' | igual ao CPython |
| F04 | % com dicionario %(a)s | 'x-2' | 'x-2' | 'x-2' | igual ao CPython |
| F05 | format posicional e nomeado | ('1 2', 'aba', '1') | ('1 2', 'aba', '1') | ('1 2', 'aba', '1') | igual ao CPython |
| F06 | format alinhamento < > ^ e preenchimento | ('      ab\|', 'ab      \|', '   ab   \|', '***ab****') | ('      ab\|', 'ab      \|', '   ab   \|', '***ab****') | ('      ab\|', 'ab      \|', '   ab   \|', '***ab****') | igual ao CPython |
| F07 | format f e g % | ('0.667', '    3.1416', '1.234568e+04', '1e-05', '25.000000%') | ('0.667', '    3.1416', '1.234568e+04', '1e-05', '25.000000%') | ('0.667', '    3.1416', '1.234568e+04', '1e-05', '25.000000%') | igual ao CPython |
| F08 | format separador de milhar {:,} | '1,234,567' | '1,234,567' | '1,234,567' | igual ao CPython |
| F09 | format sinal e zeros | ('-003.142', '+5', '00042') | ('-003.142', '+5', '00042') | ('-003.142', '+5', '00042') | igual ao CPython |
| F10 | format b x #x o | ('1010', 'ff', '0xff', '10') | ('1010', 'ff', '0xff', '10') | ('1010', 'ff', '0xff', '10') | igual ao CPython |
| F11 | format com indice {0[1]} | '6' | **NotImplementedError: attributes not supported yet** | **NotImplementedError: attributes not supported yet** | núcleo 1.9.4 |
| F12 | format com atributo {a.real} | '3' | **NotImplementedError: attributes not supported yet** | **NotImplementedError: attributes not supported yet** | núcleo 1.9.4 |
| F13 | format !r e !s | ("'x'", '1.5') | ("'x'", '1.5') | ("'x'", '1.5') | igual ao CPython |
| F14 | format() embutido | ('3.14', 'ff', '007') | **NameError: name 'format' is not defined** | **NameError: name 'format' is not defined** | núcleo 1.9.4 |
| F15 | format de largura padrao numero x texto | ('    3\|', 'a    \|') | ('    3\|', 'a    \|') | ('    3\|', 'a    \|') | igual ao CPython |
| F16 | str.ljust / rjust | ('ab   \|', '   ab') | **AttributeError: 'str' object has no attribute 'ljust'** | **AttributeError: 'str' object has no attribute 'ljust'** | núcleo 1.9.4 |
| F17 | str.center / zfill | ('  ab  \|', '00042') | **AttributeError: 'str' object has no attribute 'zfill'** | **AttributeError: 'str' object has no attribute 'center'** | depende da configuração |
| F18 | str.title / capitalize / swapcase | ('Ola Mundo', 'Ola', 'aB') | **AttributeError: 'str' object has no attribute 'title'** | **AttributeError: 'str' object has no attribute 'title'** | núcleo 1.9.4 |
| F19 | split basico | (['a', 'b', '', 'c'], ['a', 'b', 'c'], ['a', 'b c']) | (['a', 'b', '', 'c'], ['a', 'b', 'c'], ['a', 'b c']) | (['a', 'b', '', 'c'], ['a', 'b', 'c'], ['a', 'b c']) | igual ao CPython |
| F20 | rsplit(None, 1) | ['a b', 'c'] | **NotImplementedError: rsplit(None,n)** | **NotImplementedError: rsplit(None,n)** | núcleo 1.9.4 |
| F21 | rsplit(',', 1) | ['a,b', 'c'] | ['a,b', 'c'] | ['a,b', 'c'] | igual ao CPython |
| F22 | strip com caracteres | ('x', 'hi', 'a', 'a') | ('x', 'hi', 'a', 'a') | ('x', 'hi', 'a', 'a') | igual ao CPython |
| F23 | find rfind index count replace | (2, 3, 1, 2, 'heLlo') | (2, 3, 1, 2, 'heLlo') | (2, 3, 1, 2, 'heLlo') | igual ao CPython |
| F24 | startswith(tupla) | True | **TypeError: can't convert 'tuple' object to str implicitly** | **TypeError: can't convert 'tuple' object to str implicitly** | núcleo 1.9.4 |
| F25 | endswith com inicio e fim | True | **TypeError: function expected at most 3 arguments, got 4** | **TypeError: function expected at most 3 arguments, got 4** | núcleo 1.9.4 |
| F26 | partition / rpartition | (('a', '=', 'b=c'), ('a=b', '=', 'c')) | (('a', '=', 'b=c'), ('a=b', '=', 'c')) | **AttributeError: 'str' object has no attribute 'partition'** | depende da configuração |
| F27 | isdigit isalpha isspace isupper islower | (True, True, True, True, True) | (True, True, True, True, True) | (True, True, True, True, True) | igual ao CPython |
| F28 | isalnum isdecimal isnumeric isidentifier | ['isalnum', 'isdecimal', 'isnumeric', 'isidentifier', 'isprintable', 'istitle'] | [] | [] | núcleo 1.9.4 |
| F29 | fatiamento com passo s[::-1] e s[1:5:2] | ('fedcba', 'bd') | **NotImplementedError: only slices with step=1 (aka None) are supported** | **NotImplementedError: only slices with step=1 (aka None) are supported** | núcleo 1.9.4 |
| F30 | join, * e in | ('a-b', 'ababab', True) | ('a-b', 'ababab', True) | ('a-b', 'ababab', True) | igual ao CPython |
| F31 | len de texto acentuado | 1 | 1 | 1 | igual ao CPython |
| F32 | encode / decode | (b'\xc3\xa9', 'ab', 'ab') | (b'\xc3\xa9', 'ab', 'ab') | (b'\xe9', 'ab', 'ab') | depende da configuração |
| F33 | str.format_map | '1' | **AttributeError: 'str' object has no attribute 'format_map'** | **AttributeError: 'str' object has no attribute 'format_map'** | núcleo 1.9.4 |
| F34 | str.casefold / expandtabs / splitlines | ['casefold', 'expandtabs', 'splitlines', 'translate', 'maketrans', 'removeprefix'] | ['splitlines'] | [] | depende da configuração |
| F35 | '%.20f' % 0.1 (digitos alem da precisao) | '0.10000000000000000555' | '0.10000000000000000000' | '0.10000000000000000000' | núcleo 1.9.4 |
| F36 | '{:.17g}'.format(0.1) | '0.10000000000000001' | '0.1' | '0.1' | núcleo 1.9.4 |
| F37 | str() e repr() de complexo | ('(3+4j)', '1j', '(1+0j)') | ('(3+4j)', '1j', '(1+0j)') | ('(3+4j)', '1j', '(1+0j)') | igual ao CPython |
| F38 | ord / chr / chr(233) | (65, 'A', 'é') | (65, 'A', '\xe9') | (65, 'A', '�') | depende da configuração |
| F39 | bin oct hex | ('0b1010', '0o10', '0xff', '-0x1') | ('0b1010', '0o10', '0xff', '-0x1') | ('0b1010', '0o10', '0xff', '-0x1') | igual ao CPython |
| F40 | splitlines | ['a', 'b', 'c'] | ['a', 'b', 'c'] | **AttributeError: 'str' object has no attribute 'splitlines'** | depende da configuração |
| C01 | ordem de insercao do dict (texto) | ['zeta', 'alfa', 'mike', 'bravo', 'x', 'a', 'kilo', 'eco'] | ['mike', 'zeta', 'kilo', 'eco', 'a', 'x', 'bravo', 'alfa'] | ['mike', 'zeta', 'kilo', 'eco', 'a', 'x', 'bravo', 'alfa'] | núcleo 1.9.4 |
| C02 | ordem de insercao do dict (inteiros) | [50, 3, 9, 1, 27, 100] | [100, 1, 50, 9, 3, 27] | [100, 1, 50, 9, 3, 27] | núcleo 1.9.4 |
| C03 | ordem de iteracao do set | [1, 50, 3, 100, 9, 27] | [100, 1, 50, 3, 9, 27] | [100, 1, 50, 3, 9, 27] | núcleo 1.9.4 |
| C04 | visoes keys/items | ('dict_keys', True, [('a', 1)]) | ('dict_view', True, [('a', 1)]) | ('dict_view', True, [('a', 1)]) | núcleo 1.9.4 |
| C05 | dict: setdefault get pop popitem | (2, 0, 1, 'padrao', ('b', 2), {}) | (2, 0, 1, 'padrao', ('b', 2), {}) | (2, 0, 1, 'padrao', ('b', 2), {}) | igual ao CPython |
| C06 | dict: update(chaves) fromkeys copy | ({'a': 1}, [('a', 0), ('b', 0)], True) | ({'a': 1}, [('a', 0), ('b', 0)], True) | ({'a': 1}, [('a', 0), ('b', 0)], True) | igual ao CPython |
| C07 | dict(a=1), dict(pares), dict(zip()) | ([('a', 1), ('b', 2)], {'a': 1}, [('a', 1), ('b', 2)]) | ([('a', 1), ('b', 2)], {'a': 1}, [('a', 1), ('b', 2)]) | ([('a', 1), ('b', 2)], {'a': 1}, [('a', 1), ('b', 2)]) | igual ao CPython |
| C08 | list: sort(key, reverse), copy, clear | (['ccc', 'bb', 'a'], []) | (['ccc', 'bb', 'a'], []) | (['ccc', 'bb', 'a'], []) | igual ao CPython |
| C09 | list: index(x, inicio), insert, pop(0) | (2, None, [2, 1, 9, 3], 1, [2, 1, 9, 3]) | (2, None, [2, 1, 9, 3], 1, [2, 1, 9, 3]) | (2, None, [2, 1, 9, 3], 1, [2, 1, 9, 3]) | igual ao CPython |
| C10 | atribuicao em fatia l[1:3] = [...] | [0, 'a', 3, 4] | [0, 'a', 3, 4] | [0, 'a', 3, 4] | igual ao CPython |
| C11 | atribuicao em fatia com passo l[::2] | [9, 1, 9, 3, 9] | **NotImplementedError: ** | **NotImplementedError: ** | núcleo 1.9.4 |
| C12 | del l[::2] | [1, 3] | **NotImplementedError: ** | **NotImplementedError: ** | núcleo 1.9.4 |
| C13 | lista aninhada com * (aliasing) | [[1, 0], [1, 0]] | [[1, 0], [1, 0]] | [[1, 0], [1, 0]] | igual ao CPython |
| C14 | tupla: count index e fatia com passo | (2, 3, (1, 1)) | **NotImplementedError: only slices with step=1 (aka None) are supported** | **NotImplementedError: only slices with step=1 (aka None) are supported** | núcleo 1.9.4 |
| C15 | set: operadores e metodos | ([1, 2, 3, 4], [2, 3], [1], [1, 4], True, True) | ([1, 2, 3, 4], [2, 3], [1], [1, 4], True, True) | ([1, 2, 3, 4], [2, 3], [1], [1, 4], True, True) | igual ao CPython |
| C16 | set.remove de ausente | **KeyError: 9** | **KeyError: 9** | **KeyError: 9** | igual ao CPython |
| C17 | frozenset | [1, 2, 3] | [1, 2, 3] | **NameError: name 'frozenset' is not defined** | depende da configuração |
| C18 | sorted estavel com key | [('c', 0), ('b', 1), ('a', 1)] | [('c', 0), ('b', 1), ('a', 1)] | [('c', 0), ('b', 1), ('a', 1)] | igual ao CPython |
| C19 | sorted de tipos mistos | **TypeError: '<' not supported between instances of 'str' and 'int'** | **TypeError: unsupported types for __lt__: 'int', 'str'** | **TypeError: unsupported types for __lt__: 'int', 'str'** | núcleo 1.9.4 |
| C20 | range: fatia, in, len, indice negativo, == | (range(2, 5), True, 4, 9, True) | (range(2, 5), True, 4, 9, False) | (range(2, 5), True, 4, 9, False) | núcleo 1.9.4 |
| C21 | bytes e bytearray | (b'Ab', [97, 122], b'abc') | (b'Ab', [97, 122], b'abc') | (b'Ab', [97, 122], b'abc') | igual ao CPython |
| C22 | memoryview | b'bc' | b'bc' | **NameError: name 'memoryview' is not defined** | depende da configuração |
| C23 | slice() objeto | [1, 3] | **TypeError: cannot create 'slice' instances** | **TypeError: cannot create 'slice' instances** | núcleo 1.9.4 |
| C24 | lista: pop de vazia | **IndexError: pop from empty list** | **IndexError: pop from empty list** | **IndexError: pop from empty list** | igual ao CPython |
| C25 | dict: chave lista (nao hashavel) | **TypeError: unhashable type: 'list'** | **TypeError: unsupported type for __hash__: 'list'** | **TypeError: unsupported type for __hash__: 'list'** | núcleo 1.9.4 |
| B01 | enumerate(start=1) | [(1, 'a'), (2, 'b')] | [(1, 'a'), (2, 'b')] | [(1, 'a'), (2, 'b')] | igual ao CPython |
| B02 | zip de tamanhos diferentes | [(1, 'a'), (2, 'b')] | [(1, 'a'), (2, 'b')] | [(1, 'a'), (2, 'b')] | igual ao CPython |
| B03 | map com 2 iteraveis | [11, 22] | [11, 22] | [11, 22] | igual ao CPython |
| B04 | filter(None, ...) | [1, 'a'] | [1, 'a'] | [1, 'a'] | igual ao CPython |
| B05 | min(key=) max(default=) | ('a', -1) | ('a', -1) | ('a', -1) | igual ao CPython |
| B06 | sum com inicio (listas) | [1, 2] | [1, 2] | [1, 2] | igual ao CPython |
| B07 | any / all | (True, True) | (True, True) | (True, True) | igual ao CPython |
| B08 | reversed de lista, range e str | ([2, 1], [2, 1, 0], ['b', 'a']) | ([2, 1], [2, 1, 0], ['b', 'a']) | ([2, 1], [2, 1, 0], ['b', 'a']) | igual ao CPython |
| B09 | isinstance com tupla, issubclass | (True, True) | (True, False) | (True, False) | núcleo 1.9.4 |
| B10 | getattr/setattr/hasattr/delattr | (1, 'padrao', True, False) | (1, 'padrao', True, False) | (1, 'padrao', True, False) | igual ao CPython |
| B11 | type(nome, bases, dict) | (1, 'X') | (1, 'X') | (1, 'X') | igual ao CPython |
| B12 | vars() | {'x': 1} | **NameError: name 'vars' is not defined** | **NameError: name 'vars' is not defined** | núcleo 1.9.4 |
| B13 | callable, id, hash | (True, 'int', True) | (True, 'int', True) | (True, 'int', True) | igual ao CPython |
| B14 | eval e exec | (3, 5) | (3, 5) | (3, 5) | igual ao CPython |
| B15 | compile() | 2 | 2 | **NameError: name 'compile' is not defined** | depende da configuração |
| B16 | iter(callable, sentinela) | [3, 2, 1] | **TypeError: function takes 1 positional arguments but 2 were given** | **TypeError: function takes 1 positional arguments but 2 were given** | núcleo 1.9.4 |
| B17 | next(gerador, padrao) | 'vazio' | **TypeError: function takes 1 positional arguments but 2 were given** | **TypeError: function takes 1 positional arguments but 2 were given** | núcleo 1.9.4 |
| B18 | sorted(dict) e max(dict, key=dict.get) | (['a', 'b'], 'b') | (['a', 'b'], 'b') | (['a', 'b'], 'b') | igual ao CPython |
| B19 | print aceita sep, end e file | 'print(sep=, end=) ok' | 'print(sep=, end=) ok' | 'print(sep=, end=) ok' | igual ao CPython |
| B20 | ascii() | "'\\xe9'" | **NameError: name 'ascii' is not defined** | **NameError: name 'ascii' is not defined** | núcleo 1.9.4 |
| B21 | divmod de float | (3.0, 1.5) | (3.0, 1.5) | (3.0, 1.5) | igual ao CPython |
| B22 | globals() e locals() na funcao | (True, True) | (False, True) | (False, True) | núcleo 1.9.4 |
| B23 | __import__ | 1 | 1 | 1 | igual ao CPython |
| B24 | help() existe | True | **NameError: name 'help' is not defined** | **NameError: name 'help' is not defined** | núcleo 1.9.4 |
| B25 | open() existe | True | True | True | igual ao CPython |
| O01 | super() sem argumentos | 'BA' | 'BA' | 'BA' | igual ao CPython |
| O02 | property com setter | 10 | 10 | 10 | igual ao CPython |
| O03 | classmethod e staticmethod | (1, 2, 1) | (1, 2, 1) | (1, 2, 1) | igual ao CPython |
| O04 | __str__ e __repr__ | ('str', 'repr', '[repr]') | ('str', 'repr', '[repr]') | ('str', 'repr', '[repr]') | igual ao CPython |
| O05 | __eq__ e __lt__ (ordenar objetos) | ([1, 2, 3], True) | ([1, 2, 3], True) | ([1, 2, 3], True) | igual ao CPython |
| O06 | __eq__ sem __hash__ torna nao hashavel? | **TypeError: unhashable type: 'V'** | **TypeError: unsupported type for __hash__: 'V'** | **TypeError: unsupported type for __hash__: 'V'** | núcleo 1.9.4 |
| O07 | __radd__ (operador refletido) | 'radd' | 'radd' | **TypeError: unsupported types for __add__: 'int', 'V'** | depende da configuração |
| O08 | __add__ e __iadd__ | (3, 101) | (3, 101) | (3, 101) | igual ao CPython |
| O09 | __len__ __getitem__ __contains__ __iter__ | (3, 10, True, [0, 10, 20]) | (3, 10, True, [0, 10, 20]) | (3, 10, True, [0, 10, 20]) | igual ao CPython |
| O10 | __call__ e __bool__ | (8, False) | (8, False) | (8, False) | igual ao CPython |
| O11 | __getattr__ (fallback) | 'auto_qualquer' | 'auto_qualquer' | 'auto_qualquer' | igual ao CPython |
| O12 | __setattr__ sobrescrito | 4 | 2 | 2 | núcleo 1.9.4 |
| O13 | __del__ chamado ao apagar | ['del'] | [] | [] | núcleo 1.9.4 |
| O14 | heranca multipla (MRO em diamante) | 'C' | 'A' | 'A' | núcleo 1.9.4 |
| O15 | __slots__ restringe atributos? | **AttributeError: 'A' object has no attribute 'y'** | 1 | 1 | núcleo 1.9.4 |
| O16 | name mangling de __x | True | False | False | núcleo 1.9.4 |
| O17 | atributo em funcao f.x = 1 | 1 | **AttributeError: 'function' object has no attribute 'x'** | **AttributeError: 'function' object has no attribute 'x'** | núcleo 1.9.4 |
| O18 | __dict__ da instancia | {'x': 1} | {'x': 1} | {'x': 1} | igual ao CPython |
| O19 | __class__ e __name__ | ('A', 'A') | ('A', 'A') | ('A', 'A') | igual ao CPython |
| O20 | __qualname__ e __module__ | ('A', '__sonda__') | ('A', '__sonda__') | ('A', '__sonda__') | igual ao CPython |
| O21 | subclasse de int | 6 | 6 | 6 | igual ao CPython |
| O22 | subclasse de list com metodo | 6 | 6 | 6 | igual ao CPython |
| O23 | __init_subclass__ | ['B'] | [] | [] | núcleo 1.9.4 |
| O24 | __neg__ __abs__ __mul__ __truediv__ | (-2, 'abs', 6, 1.5) | (-2, 'abs', 6, 1.5) | **TypeError: unsupported type for : 'V'** | depende da configuração |
| O25 | __getitem__ com fatia | ('slice', 1, 3) | ('slice', 1, 3) | **AttributeError: 'slice' object has no attribute 'start'** | depende da configuração |
| O26 | __hash__ proprio em dict | 'a' | 'a' | 'a' | igual ao CPython |
| O27 | descritor __get__ | 'desc' | 'desc' | <D object> | depende da configuração |
| O28 | variavel de classe x de instancia | [1] | [1] | [1] | igual ao CPython |
| E01 | repr de excecao com argumento | "ValueError('x')" | "ValueError('x',)" | "ValueError('x',)" | núcleo 1.9.4 |
| E02 | str(KeyError("k")) | "'k'" | 'k' | 'k' | núcleo 1.9.4 |
| E03 | excecao propria com atributos | (7, 'codigo 7', ('codigo 7',)) | (7, 'codigo 7', ('codigo 7',)) | (7, 'codigo 7', ('codigo 7',)) | igual ao CPython |
| E04 | e.__traceback__ | True | False | False | núcleo 1.9.4 |
| E05 | RecursionError existe | 'RecursionError' | **NameError: name 'RecursionError' is not defined** | **NameError: name 'RecursionError' is not defined** | núcleo 1.9.4 |
| E06 | tipo e mensagem ao estourar recursao | ('RecursionError', 'maximum recursion depth exceeded') | ('RuntimeError', 'maximum recursion depth exceeded') | ('RuntimeError', 'maximum recursion depth exceeded') | núcleo 1.9.4 |
| E07 | SystemExit e BaseException | (True, False) | (True, False) | (True, False) | igual ao CPython |
| E08 | KeyboardInterrupt fora de Exception | False | False | False | igual ao CPython |
| E09 | mensagem NameError | **NameError: name 'nao_definida' is not defined** | **NameError: name 'nao_definida' is not defined** | **NameError: name 'nao_definida' is not defined** | igual ao CPython |
| E10 | mensagem TypeError 'a' + 1 | **TypeError: can only concatenate str (not "int") to str** | **TypeError: can't convert 'int' object to str implicitly** | **TypeError: can't convert 'int' object to str implicitly** | núcleo 1.9.4 |
| E11 | mensagem AttributeError | **AttributeError: 'int' object has no attribute 'xyz'** | **AttributeError: 'int' object has no attribute 'xyz'** | **AttributeError: 'int' object has no attribute 'xyz'** | igual ao CPython |
| E12 | mensagem IndexError | **IndexError: list index out of range** | **IndexError: list index out of range** | **IndexError: list index out of range** | igual ao CPython |
| E13 | mensagem KeyError | **KeyError: 'k'** | **KeyError: k** | **KeyError: k** | núcleo 1.9.4 |
| E14 | mensagem ValueError int("x") | **ValueError: invalid literal for int() with base 10: 'x'** | **ValueError: invalid syntax for integer with base 10: 'x'** | **ValueError: invalid syntax for integer with base 10** | depende da configuração |
| E15 | mensagem ImportError | **ModuleNotFoundError: No module named 'modulo_que_nao_existe'** | **ImportError: no module named 'modulo_que_nao_existe'** | **ImportError: no module named 'modulo_que_nao_existe'** | núcleo 1.9.4 |
| E16 | mensagem de argumentos errados | **TypeError: f() missing 1 required positional argument: 'a'** | **TypeError: f() takes 1 positional arguments but 0 were given** | **TypeError: function takes 1 positional arguments but 0 were given** | depende da configuração |
| E17 | UnboundLocalError | **UnboundLocalError: cannot access local variable 'x' where it is not associated with a value** | **NameError: local variable referenced before assignment** | **NameError: local variable referenced before assignment** | núcleo 1.9.4 |
| E18 | SyntaxError via exec | **SyntaxError: invalid syntax (<string>, line 1)** | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| E19 | IndentationError via exec | **IndentationError: expected an indented block after 'if' statement on line 1 (<string>, line 2)** | **SyntaxError: invalid syntax** | **SyntaxError: invalid syntax** | núcleo 1.9.4 |
| E20 | finally roda no return | ('ret', ['fin']) | ('ret', ['fin']) | ('ret', ['fin']) | igual ao CPython |
| E21 | except (A, B) as e | 'IndexError' | 'IndexError' | 'IndexError' | igual ao CPython |
| E22 | excecoes embutidas presentes | [] | ['UnboundLocalError', 'FileNotFoundError', 'RecursionError', 'TimeoutError', 'ModuleNotFoundError', 'Warning', 'UserWarning', 'IOError', 'EnvironmentError', 'PermissionError', 'FloatingPointError', 'ReferenceError'] | ['UnboundLocalError', 'FileNotFoundError', 'RecursionError', 'TimeoutError', 'UnicodeError', 'ModuleNotFoundError', 'Warning', 'UserWarning', 'IOError', 'EnvironmentError', 'PermissionError', 'FloatingPointError', 'ReferenceError'] | depende da configuração |
| E23 | excecao dentro de except (contexto) | ZeroDivisionError('division by zero') | 'sem __context__' | 'sem __context__' | núcleo 1.9.4 |
| E24 | str() de excecao sem argumentos | ('', 'ValueError()') | ('', 'ValueError()') | ('', 'ValueError()') | igual ao CPython |
| E25 | mensagem OverflowError int grande em float | **OverflowError: int too large to convert to float** | inf | inf | núcleo 1.9.4 |
| G01 | gerador send | 42 | 42 | 42 | igual ao CPython |
| G02 | gerador close e throw | 'capturou' | 'capturou' | 'capturou' | igual ao CPython |
| G03 | return em gerador (StopIteration.value) | 'fim' | 'fim' | 'fim' | igual ao CPython |
| G04 | protocolo de iterador proprio | [1, 2, 3] | [1, 2, 3] | [1, 2, 3] | igual ao CPython |
| G05 | zip(*matriz) transposicao | [(1, 3), (2, 4)] | [(1, 3), (2, 4)] | [(1, 3), (2, 4)] | igual ao CPython |
| G06 | expressao geradora em max/sum | (16, 4) | (16, 4) | (16, 4) | igual ao CPython |
| G07 | StopIteration dentro de gerador (PEP 479) | **RuntimeError: generator raised StopIteration** | [1] | [1] | núcleo 1.9.4 |
| V01 | lambda em laco (late binding) | [2, 2, 2] | [2, 2, 2] | [2, 2, 2] | igual ao CPython |
| V02 | argumento padrao mutavel | [1, 2] | [1, 2] | [1, 2] | igual ao CPython |
| V03 | __name__ no namespace do exec | '__sonda__' | '__sonda__' | '__sonda__' | igual ao CPython |
| V04 | variavel de compreensao nao vaza | 'fora' | 'fora' | 'fora' | igual ao CPython |
| V05 | del de variavel e reuso | 2 | 2 | 2 | igual ao CPython |
