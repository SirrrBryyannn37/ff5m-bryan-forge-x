# Starlink Mini pole-mount chain

Parametric rebuild of the pole-based mount chain:

```
arm (proxy) -> pole (48mm) -> pole_clamp_v3 -> polemount_v3_45deg -> tube_mount -> mini_cradle_v3
```

Generated with `build_mount.py` (requires `trimesh`, `numpy`, `manifold3d` for
booleans). Run:

```bash
python3 build_mount.py       # writes STL per part + assembly_preview.3mf to out/
python3 render_preview.py    # writes out/assembly_preview.png (6-view sheet)
```

## Reference files

`reference/` holds the uploaded inspiration files, used to measure real
envelope and bolt-pattern dimensions rather than guessing:

| File | What it is | Measured |
|------|-----------|----------|
| `starlink_mini_v3_mount_system.3mf` | Full community mount assembly (6 bodies) | quad-bolt adapter plate 60x60x3mm, 45mm bolt square, 6.5mm holes; pole-clamp halves 83.2x79.9x16mm w/ 2x ~6.5mm clamp bolts; Mini v3 cradle 166.3x92.0x19.4mm w/ 2 mounting ears |
| `40mm_45deg_polemount_v3.3mf` / `40mm_45deg_polemount_v2.stl` | Standalone 45-degree pole adapter | 60x50x123mm envelope |
| `remix_starlink_pole_mount_v2.3mf` | Alternative single-body pole mount (comparison reference) | 150.9x91.9x109.7mm |
| `starlink_mini_wall_mount.step` | Wall-mount variant (comparison reference) | ~300x100x100mm |

## Design assumptions

- **Nozzle**: Phaetus Conch, 0.8mm. Minimum wall thickness used throughout is
  `4 * 0.8mm = 3.2mm` (four 0.8mm perimeters). Clearance holes are sized for
  drill-out, not fine as-printed tolerance.
- **Pole diameter**: 48mm, per the existing arm (from the earlier session's
  chain, not the reference files — the reference clamp bore was NOT reused,
  only its footprint/bolt-spacing style).
- **Quad-bolt pattern**: 45mm square, 6.5mm clearance, matches the measured
  Starlink v3 OEM-style adapter plate. Used at every part-to-part interface
  in this chain so pieces are interchangeable/reprintable independently.
- **Ear span** (tube_mount <-> mini_cradle_v3): 111.2mm center-to-center,
  10.9mm holes, measured directly from the v3 cradle reference body.

## Known gaps / next steps

- **`arm_proxy` is NOT the real arm.** No STL for the printed grey+orange arm
  from the earlier session was available here — only its render. The proxy
  matches that render's rough envelope (48mm riser + ~220mm beam + foot) so
  the chain assembles for review. Swap in the real file (or re-derive exact
  dimensions from it) before printing anything downstream of it.
- `polemount_v3_45deg` currently only cosmetically angles its top plate; it
  doesn't yet kink the load path 45 degrees off the pole axis the way the
  reference part's name implies. Fine for a first-pass dimensional/bolt-
  pattern check, not yet a physically faithful copy.
- `mini_cradle_v3` is a simplified tray (box + center slot + two ear holes),
  not a shell contoured to the Mini's actual foot geometry — good enough to
  check bolt spacing against `tube_mount`, not print-ready as the final
  cradle.
