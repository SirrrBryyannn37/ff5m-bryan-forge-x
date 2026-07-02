#!/bin/bash
#
# Bryan Forge X — copy mod_data/defaults into mod_data/ once per install/OTA.

source /opt/config/mod/.shell/common.sh

BFX_MARKER="$MOD_DATA/.bfx_installed"
DEFAULTS_DIR="$MOD_DATA/defaults"
[ -d "$DEFAULTS_DIR" ] || DEFAULTS_DIR="/opt/config/mod/mod_data/defaults"

install_bfx_defaults() {
    [ -f "$BFX_MARKER" ] && return 0
    [ -d "$DEFAULTS_DIR" ] || return 0

    echo "// Bryan Forge X: installing defaults..."

    for f in "$DEFAULTS_DIR"/*; do
        [ -f "$f" ] || continue
        base=$(basename "$f")
        case "$base" in
            README.txt|variables.bfx.cfg|moonraker.conf|user.moonraker.conf)
                continue
                ;;
        esac
        if [ "$base" = "splash.img.xz" ]; then
            cp -f "$f" "$MOD_DATA/splash.img.xz"
            cp -f "$f" /opt/config/mod_data/splash.img.xz 2>/dev/null || true
            echo "//   installed splash.img.xz"
            continue
        fi
        dest="$MOD_DATA/$base"
        if [ ! -f "$dest" ]; then
            cp -f "$f" "$dest"
            echo "//   installed $base"
        fi
    done

    if [ -f "$DEFAULTS_DIR/variables.bfx.cfg" ]; then
        if [ ! -f "$VAR_PATH" ]; then
            echo "[Variables]" > "$VAR_PATH"
        fi
        while IFS= read -r line || [ -n "$line" ]; do
            line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            [ -z "$line" ] && continue
            [[ "$line" == \#* ]] && continue
            key="${line%%=*}"
            key=$(echo "$key" | sed 's/[[:space:]]*$//')
            val="${line#*=}"
            val=$(echo "$val" | sed 's/^[[:space:]]*//')
            "$CFG_SCRIPT" "$VAR_PATH" --set "$key=$val"
        done < "$DEFAULTS_DIR/variables.bfx.cfg"
        echo "//   merged variables.bfx.cfg"
    fi

    date -Iseconds > "$BFX_MARKER"
    sync
    echo "// Bryan Forge X defaults installed."
}

install_bfx_defaults