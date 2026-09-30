// Variante "teto" da porta unix do MicroPython 1.9.4: a configuração da porta
// unix (que liga quase todos os recursos opcionais) mais o que falta para
// imitar os módulos documentados da fx-9750GIII:
//   - o módulo se chama random (no 1.9.4 ele existe como urandom);
//   - random com randrange, randint, choice, random e uniform.
// Compilado por ../compilar.sh.

#include <mpconfigport.h>

#undef MICROPY_PY_URANDOM_EXTRA_FUNCS
#define MICROPY_PY_URANDOM_EXTRA_FUNCS (1)
#undef MICROPY_PY_MATH_SPECIAL_FUNCTIONS
#define MICROPY_PY_MATH_SPECIAL_FUNCTIONS (1)

// "import random" passa a achar o urandom embutido
#undef MICROPY_MODULE_WEAK_LINKS
#define MICROPY_MODULE_WEAK_LINKS (1)
#undef MICROPY_PORT_BUILTIN_MODULE_WEAK_LINKS
#define MICROPY_PORT_BUILTIN_MODULE_WEAK_LINKS \
    { MP_ROM_QSTR(MP_QSTR_random), MP_ROM_PTR(&mp_module_urandom) },
