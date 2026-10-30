# Technical plan

Target: **Company of Heroes 1 / Legacy Edition**, fully patched, on the Essence 1 engine.
Items marked **(verify)** are community knowledge we haven't yet confirmed on our
own install. Confirm them during M1 and update this file.

## Core decision: reskin race slots, don't add races

The four CoH 1 races (`allies`, `axis`, `allies_commonwealth`, `axis_panzer_elite`) are
handled inside the game DLL, `WW2Mod.dll`. Mods can rewrite each race's units, buildings,
doctrines, UI and audio through attribute files, but adding a fifth race needs DLL work
that the mod tools don't support **(verify)**. So:

- **Combine** replaces the Wehrmacht (`axis`).
- **Resistance** replaces the US (`allies`).
- Commonwealth and Panzer Elite are untouched for now (see open questions in `design.md`).

Each mod unit is **cloned from** a vanilla blueprint that already behaves roughly the way
we want, then renamed, re-statted and eventually given a new model. The `clone_from`
field in `design/*.toml` records which one. Matching the blueprint *kind* matters: a
crewed weapon (HMG, mortar, AT gun) must clone a team-weapon blueprint, infantry clones
infantry, and vehicles clone vehicles.

## How the game loads the mod

```
<CoH install>\
  RelicCOH.exe
  RelicCOH.module      vanilla module, our reference for the format
  City17.module        ours, copied from mod/City17.module
  City17\              ours, a junction to mod/City17 during development
    Data\attrib\       .rgd attribute files that override vanilla ones at the same path
    Data\scar\         SCAR (Lua) scripts: win conditions, abilities, scenarios
    Art\               models (.rgm), textures, FX
    Locale\English\    City17.ucs (built by tools/modtool.py)
  WW2\                 vanilla data the mod falls through to
```

Launch with `RelicCOH.exe -dev -mod City17`. `-dev` makes the game read loose files
from the mod folder instead of only packed `.sga` archives **(verify on Legacy Edition)**.

Override, don't edit: never change files under `WW2\`. Everything the mod changes is
a file at the same relative path inside `City17\`.

## Toolchain

| Job | Tool |
|---|---|
| Extracting vanilla data, editing `.rgd` attributes, packing `.sga` | [Corsix's Mod Studio](https://modstudio.corsix.org/) |
| Models, animations (`.rgm`) | Relic CoH Mod Tools (Object Editor plus 3ds Max exporter). Investigate community Blender importers/exporters in M3 |
| Maps | Relic World Builder (ships with the Mod Tools) |
| Textures | Any editor that exports DDS, then convert to Relic's formats via the Mod Tools **(verify)** |
| Strings | `tools/modtool.py` (this repo) |
| Scripting | SCAR (Lua 5.0 dialect) in any text editor |

## Version control

- `.rgd` files are binary and don't diff. Describe each stat change in the commit message.
  If this gets painful, we'll write a dump/compare script using Corsix's RGD
  Lua macros.
- Art sources and outputs (`.rgm`, textures, `.blend`, `.max`, `.psd`, audio) go through
  **Git LFS** (see `.gitattributes`). Run `git lfs install` once before cloning.
- `mod/City17/Locale/English/City17.ucs` is generated and ignored by git.
  Strings are edited in `design/*.toml` and `locale/english.tsv`.

## String IDs

`.ucs` files are UTF-16 LE with a BOM, CRLF line endings, and `<id><TAB><text>` per line.
IDs are global across vanilla and mods, so ours live in reserved blocks:

| Range | Owner |
|---|---|
| 32000000 – 32000999 | General / UI (`locale/english.tsv`) |
| 32001000 – 32001999 | Combine (`design/combine.toml`) |
| 32002000 – 32002999 | Resistance (`design/resistance.toml`) |
| 32003000 + | Reserved for future factions / maps / campaign |

When the vanilla `.ucs` has been extracted, run
`py tools/modtool.py check --vanilla <path to vanilla English .ucs>` to prove there are no
collisions.

## Known risks

| Risk | Impact | Plan |
|---|---|---|
| `.module` format changed in patch 2.400; Mod Studio writes the old one | Mod won't launch | First task of M1: rebuild ours from `RelicCOH.module` |
| Fifth race impossible without DLL work | Locks us to slot reskins | Accepted. Design already assumes it |
| Tall units (Strider) | Selection boxes, garrison/cover checks and camera framing assume WW2-sized vehicles | Prototype the Strider early in M3 with a scaled placeholder |
| Flying units (Scanners, Manhacks, Gunship) | No air layer in CoH 1 | Gunship/Chopper as off-map abilities like vanilla planes; Scanners as ground units with a height offset. Prototype |
| Skirmish AI references vanilla blueprints | AI can't build our units | Update AI build tables in `Data\ai` **(verify location)** after the roster stabilises (M4) |
| Multiplayer requires identical mod versions | Desyncs | Bump `ModVersion` on every release. Release only packed `.sga` builds |
| Valve IP | Takedown risk | `docs/asset-policy.md` |
