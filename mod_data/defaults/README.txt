Bryan Forge X defaults — auto-copied to mod_data/ on first boot

user.cfg                  0.6mm stock nozzle baseline; includes
                           bfx_print_safe.cfg + bfx_material_macros.cfg.
bfx_print_safe.cfg        Moonraker-only safe print path (no stock zprint/LAN).
bfx_material_macros.cfg   Per-material PA/retraction tune macros
                           (BFX_TUNE_PLA, _PETG, _PETG_STD, _PETG_CF, and the
                           *_CONCH08 variants for the 0.8mm nozzle).
bfx_conch_0.8.cfg         Optional overlay for a Phaetus Conch + 0.8mm brass
                           nozzle install. Not included by default -- uncomment
                           `[include bfx_conch_0.8.cfg]` at the end of
                           user.cfg after installing the nozzle. See
                           docs/BRYAN_FORGE_X.md for details.
