# Roadmap

Each milestone ends with something playable or provable. Don't start a milestone's
art before the previous one's gameplay works with placeholder art.

## M0 — Groundwork ✅

- Design pillars, systems translation, rosters, doctrine outlines
- Strings pipeline (`tools/modtool.py`), dev install script
- Repo conventions (LFS, ID ranges)

## M1 — It launches

- [ ] Rebuild `mod/City17.module` against the install's `RelicCOH.module`. The mod appears in the launcher and loads a skirmish
- [ ] Extract vanilla attribs with Corsix. Fill in `vanilla_bp` for every roster entry
- [ ] Run `check --vanilla` against the vanilla English `.ucs` and confirm there are no ID collisions
- [ ] Confirm `-dev` loose-file loading on Legacy Edition
- [ ] Rename both races and the three resources in-game with our strings

## M2 — Vanilla clothes, new rules

All units exist with their City 17 names and stats, using vanilla models.

- [ ] Clone and re-stat every roster unit. Point build menus at the clones and remove the leftover vanilla entries
- [ ] Rename and re-theme territory points
- [ ] Stub all six doctrine trees with renamed vanilla abilities
- [ ] First balance pass in skirmish against a human

## M3 — First real art

Prove the art pipeline end to end on one unit per side before scaling it up.

- [ ] Civil Protection officer: model → `.rgm` → animated in-game
- [ ] Rebel: same pipeline, plus a weapon swap upgrade
- [ ] Strider placeholder at full scale: test selection, pathing and camera
- [ ] Decide Blender vs 3ds Max pipeline and document it

## M4 — Doctrines, abilities, AI

- [ ] Implement doctrine abilities (SCAR + attribs)
- [ ] Off-map Gunship / Hunter-Chopper / Dropship
- [ ] Skirmish AI builds our rosters

## M5 — City 17

- [ ] Tileset and props for at least two maps (Canals, Plaza)
- [ ] UI reskin: taskbar, resource icons, faction emblems
- [ ] Unit voices and weapon audio (original or permitted, see the asset policy)

## M6 — Release 0.1

- [ ] Pack into `.sga` archives with Corsix
- [ ] Installer / ModDB page, version shown in-game
- [ ] Multiplayer sync test across two machines
