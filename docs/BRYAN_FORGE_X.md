# Bryan Forge X firmware fork

Fork of [DrA1ex/ff5m](https://github.com/DrA1ex/ff5m), branch `bryan-forge-x`.

## Differences from stock Forge-X

| Topic | Stock Forge-X | Bryan Forge X |
|-------|---------------|---------------|
| Branding | Forge-X | Bryan Forge X splash |
| Default display | STOCK | FEATHER |
| Print from touchscreen | LAN mode + zprint | **Disabled** — Moonraker only |
| START_PRINT | May shell / zprint | `bfx_print_safe.cfg` override |
| Moonraker | Full features | Lean buffers, no webcam |
| mod_params | DrA1ex defaults | `variables.bfx.cfg` |
| OTA origin | DrA1ex/ff5m | Your `ff5m-bryan-forge-x` repo |

## First-boot installer hook (fork-only change)

On first boot, copy `mod_data/defaults/*` → `mod_data/` if `mod_data/.bfx_installed` missing.

Implemented in fork `mod/sync.sh` patch (see `tools/sync_firmware.py`).

## Merge upstream

```bash
git fetch upstream
git merge upstream/main
# Resolve conflicts in mod/ only; keep overlays/ from bryan-forge-x repo
```