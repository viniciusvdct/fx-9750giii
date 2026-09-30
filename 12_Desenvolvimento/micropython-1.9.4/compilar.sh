#!/usr/bin/env bash
# Compila o MicroPython 1.9.4 (a versão da fx-9750GIII) para testes no PC.
#
# Gera em ./bin:
#   mpy194-teto   32 bits, porta unix com quase todos os recursos opcionais
#   mpy194-piso   32 bits, opções visíveis no padrão do núcleo (ver bancada/)
#   mpy194-64     64 bits, porta unix padrão (referência)
#
# Requisitos (Linux): git, make, gcc, python3; para 32 bits, gcc-multilib.
# Uso: ./compilar.sh [pasta-do-codigo]   (padrão: ./_fonte-micropython-1.9.4)
set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
FONTE="${1:-$AQUI/_fonte-micropython-1.9.4}"
BIN="$AQUI/bin"
mkdir -p "$BIN"

if [ ! -d "$FONTE/py" ]; then
  git clone --depth 1 --branch v1.9.4 https://github.com/micropython/micropython "$FONTE"
fi
test "$(git -C "$FONTE" describe --tags)" = "v1.9.4" || { echo "a pasta $FONTE não está na tag v1.9.4"; exit 1; }

# O código de 2018 gera avisos nos compiladores atuais; sem -Werror.
CWARN="-Wall -Wno-error -Wno-dangling-pointer -Wno-enum-int-mismatch"
# Recursos da porta unix que dependem de submódulos ou bibliotecas externas.
SEM_EXTRAS="MICROPY_PY_BTREE=0 MICROPY_PY_USSL=0 MICROPY_SSL_AXTLS=0 MICROPY_PY_FFI=0 MICROPY_PY_THREAD=0"
# Em 32 bits, o NLR em assembly x86 do 1.9.4 falha com gcc recente: usar setjmp.
# -mfpmath=sse evita a precisão estendida de 80 bits do x87: as contas em double
# ficam estritas, como no ponto flutuante por software do SH4 da calculadora.
X86="-DMICROPY_NLR_SETJMP=1 -DMICROPY_EMIT_X86=0 -fno-pie -msse2 -mfpmath=sse"

make -C "$FONTE/mpy-cross" CWARN="$CWARN" -j"$(nproc)" >/dev/null
cp "$AQUI/bancada/mpconfigport_teto.h" "$AQUI/bancada/mpconfigport_piso.h" "$FONTE/ports/unix/"

compila() {  # nome  build  cflags  ldflags  extras-make
  local nome="$1" build="$2" cflags="$3" ldflags="$4"; shift 4
  if ! make -C "$FONTE/ports/unix" -j"$(nproc)" BUILD="$build" PROG="$nome" CWARN="$CWARN" \
       CFLAGS_EXTRA="$cflags" LDFLAGS_EXTRA="$ldflags" $SEM_EXTRAS "$@" >"$BIN/$nome.log" 2>&1; then
    tail -20 "$BIN/$nome.log"; echo "falhou: $nome (log em bin/$nome.log)"; exit 1
  fi
  cp "$FONTE/ports/unix/$nome" "$BIN/$nome"
  echo "ok: bin/$nome"
}

compila mpy194-teto build-teto "-DMP_CONFIGFILE=\"<mpconfigport_teto.h>\" $X86" "-no-pie" MICROPY_FORCE_32BIT=1
compila mpy194-piso build-piso "-DMP_CONFIGFILE=\"<mpconfigport_piso.h>\" $X86" "-no-pie" MICROPY_FORCE_32BIT=1
compila mpy194-64   build-64   "-DMP_CONFIGFILE=\"<mpconfigport_teto.h>\"" ""

"$BIN/mpy194-teto" -c "import sys; print(sys.implementation, sys.maxsize)"
