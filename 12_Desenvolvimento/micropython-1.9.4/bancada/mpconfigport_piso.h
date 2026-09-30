// Variante "piso" da porta unix do MicroPython 1.9.4.
//
// A porta unix liga muitos recursos opcionais que vêm DESLIGADOS no núcleo
// (py/mpconfig.h). A configuração da Casio não é pública. Esta variante devolve
// ao padrão do núcleo as opções visíveis ao programador, mantendo apenas o que o
// manual da fx-9750GIII documenta ou exige:
//   - float double, inteiros longos (mpz) e complexos (tecla SHIFT 0 -> 1j);
//   - math com log10 (tecla LOG), que no 1.9.4 só existe junto das funções
//     especiais (MICROPY_PY_MATH_SPECIAL_FUNCTIONS);
//   - random com randint/choice/... (categoria random do catálogo);
//   - input(), linha de origem nos erros e KeyboardInterrupt (tecla AC).
// Comparar "teto" (porta unix) com "piso" separa o que é do núcleo do que
// depende de configuração. Compilado por ../compilar.sh.

#include <mpconfigport_teto.h>

// Métodos de str opcionais
#undef MICROPY_PY_BUILTINS_STR_UNICODE
#define MICROPY_PY_BUILTINS_STR_UNICODE (0)
#undef MICROPY_PY_BUILTINS_STR_CENTER
#define MICROPY_PY_BUILTINS_STR_CENTER (0)
#undef MICROPY_PY_BUILTINS_STR_PARTITION
#define MICROPY_PY_BUILTINS_STR_PARTITION (0)
#undef MICROPY_PY_BUILTINS_STR_SPLITLINES
#define MICROPY_PY_BUILTINS_STR_SPLITLINES (0)

// Tipos e funções embutidas opcionais
#undef MICROPY_PY_BUILTINS_MEMORYVIEW
#define MICROPY_PY_BUILTINS_MEMORYVIEW (0)
#undef MICROPY_PY_BUILTINS_FROZENSET
#define MICROPY_PY_BUILTINS_FROZENSET (0)
#undef MICROPY_PY_BUILTINS_SLICE_ATTRS
#define MICROPY_PY_BUILTINS_SLICE_ATTRS (0)
#undef MICROPY_PY_BUILTINS_COMPILE
#define MICROPY_PY_BUILTINS_COMPILE (0)
#undef MICROPY_PY_BUILTINS_NOTIMPLEMENTED
#define MICROPY_PY_BUILTINS_NOTIMPLEMENTED (0)
#undef MICROPY_PY_BUILTINS_POW3
#define MICROPY_PY_BUILTINS_POW3 (0)
#undef MICROPY_PY_BUILTINS_EXECFILE
#define MICROPY_PY_BUILTINS_EXECFILE (0)

// Métodos especiais e atributos
#undef MICROPY_PY_ALL_SPECIAL_METHODS
#define MICROPY_PY_ALL_SPECIAL_METHODS (0)
#undef MICROPY_PY_REVERSE_SPECIAL_METHODS
#define MICROPY_PY_REVERSE_SPECIAL_METHODS (0)
#undef MICROPY_PY_ALL_INPLACE_SPECIAL_METHODS
#define MICROPY_PY_ALL_INPLACE_SPECIAL_METHODS (0)
#undef MICROPY_PY_DESCRIPTORS
#define MICROPY_PY_DESCRIPTORS (0)
#undef MICROPY_PY_DELATTR_SETATTR
#define MICROPY_PY_DELATTR_SETATTR (0)
#undef MICROPY_PY_FUNCTION_ATTRS
#define MICROPY_PY_FUNCTION_ATTRS (0)

// Mensagens de erro e avisos no padrão do núcleo
#undef MICROPY_ERROR_REPORTING
#define MICROPY_ERROR_REPORTING (MICROPY_ERROR_REPORTING_NORMAL)
#undef MICROPY_WARNINGS
#define MICROPY_WARNINGS (0)

// O que o manual documenta (math com log10) já vem do teto; cmath fica fora
#undef MICROPY_PY_CMATH
#define MICROPY_PY_CMATH (0)
