#!/usr/bin/env bash
# Host-only Lua module verification; see knowledge/contributions-koreader.md.
set -euo pipefail

if [[ $# -lt 3 ]]; then
    printf 'Usage: %s SOURCE_DIR RELEASE_RUNTIME_DIR SCRATCH_DIR [BUSTED_OPTIONS...]\n' "$0" >&2
    exit 2
fi

source_dir=$(realpath "$1")
runtime_dir=$(realpath "$2")
scratch_dir=$(realpath "$3")
shift 3

work=$(mktemp -d "$scratch_dir/koreader-test.XXXXXX")
mkdir -p "$work/run/koreader" "$work/settings"
cd "$work/run/koreader"

for entry in common ffi libs luajit data fonts l10n; do
    ln -s "$runtime_dir/$entry" "$entry"
done
for entry in frontend plugins resources datastorage.lua defaults.lua setupkoenv.lua; do
    ln -s "$source_dir/$entry" "$entry"
done

export KO_HOME="$work/settings"
export SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy
export TESSDATA_PREFIX="$runtime_dir/data"
export LUA_PATH="$source_dir/?.lua;$source_dir/frontend/?.lua;$source_dir/spec/unit/?.lua;./?.lua;./common/?.lua;/usr/share/lua/5.1/?.lua;/usr/share/lua/5.1/?/init.lua;;"
export LUA_CPATH='./?.so;./common/?.so;/usr/lib/x86_64-linux-gnu/lua/5.1/?.so;;'
export LD_LIBRARY_PATH="$runtime_dir/libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

printf 'Source: %s\nNative dependencies: %s\nIsolated run: %s\n' "$source_dir" "$runtime_dir" "$work"
./luajit -v
exec ./luajit /usr/bin/busted \
    -e 'require("ffi/loadlib")' \
    --loaders=lua --lazy --sort-files --exclude-tags=notest,internet --verbose \
    "$@" \
    "$source_dir/spec/unit/document_registry_spec.lua" \
    "$source_dir/spec/unit/opds_spec.lua"
