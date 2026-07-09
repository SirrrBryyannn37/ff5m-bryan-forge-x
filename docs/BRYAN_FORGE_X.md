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

## Phaetus Conch 0.8mm profile

`mod_data/defaults/bfx_conch_0.8.cfg` is an optional overlay for a Phaetus
Conch hotend with a 0.8mm brass nozzle. It is copied to `mod_data/` on first
boot like the other defaults but is **not** included by default.

To enable it after installing the nozzle, uncomment the last line of
`mod_data/user.cfg`:

```
[include bfx_conch_0.8.cfg]
```

It must stay the last include in `user.cfg` so its values win over the
0.6mm baseline earlier in the file. It sets:

- `nozzle_diameter: 0.8` and a wider `max_extrude_cross_section` (10, up from
  the baseline's 2.5/3.2) -- KAMP's `Line_Purge.cfg` silently skips purging
  below a cross-section of 5, so this also fixes KAMP purge on Conch, which
  was previously being skipped silently.
- `firmware_retraction` bumped slightly (0.9mm @ 70mm/s) for the Conch's
  larger melt chamber.
- `tmc2209 extruder` run_current bumped slightly (0.95) for the higher
  volumetric flow an 0.8mm nozzle can push.
- `BFX_TUNE_PLA_CONCH08` / `BFX_TUNE_PETG_CONCH08` / `BFX_TUNE_PETG_CF_CONCH08`
  macros in `bfx_material_macros.cfg` with correspondingly lower pressure
  advance than the 0.4/0.6mm macros.

All of the above are starting points, not calibrated values -- re-run a PA
tower / retraction tower / flow calibration once the nozzle is installed.

## Merge upstream

```bash
git fetch upstream
git merge upstream/main
# Resolve conflicts in mod/ only; keep overlays/ from bryan-forge-x repo
```