# City 17 — a Company of Heroes total conversion

**Working title.** This is a fan-made total conversion of *Company of Heroes* (CoH 1 /
Legacy Edition) that turns the game into the Combine occupation of City 17 from
*Half-Life 2*: the Combine Overwatch against the Resistance.

Non-commercial fan project. Not affiliated with Relic, SEGA or Valve. See
[`docs/asset-policy.md`](docs/asset-policy.md) before adding any art or audio.

## Status

**M0 — Groundwork.** Design docs, unit rosters, the strings pipeline and the dev
install script are in place. Nothing has been loaded into the game yet. The first
job of M1 is getting `City17.module` to launch. See [`docs/roadmap.md`](docs/roadmap.md).

## How it works

CoH 1 has its four races built into the engine DLL, so this mod **reskins existing
race slots** instead of adding new ones:

| Mod faction | Uses the vanilla slot of | Why it fits |
|---|---|---|
| **Combine Overwatch** | Wehrmacht (`axis`) | Tiered, defensive, expensive elite units, veterancy bought centrally |
| **Resistance** | US Forces (`allies`) | Cheap flexible infantry, engineers, light vehicles, call-ins |

Commonwealth and Panzer Elite slots are left alone for now. See
[`docs/technical-plan.md`](docs/technical-plan.md).

## Repository layout

```
docs/            design and technical documents (start with design.md)
design/          faction rosters as TOML. These are the source of truth for unit names and string IDs
locale/          extra UI strings (UTF-8 TSV), compiled into the game's .ucs format
tools/           modtool.py (validate + build strings), install-dev.ps1 (link into the game)
mod/
  City17.module  module definition, copied to the game's root folder
  City17/        the mod folder the game loads (Data/, Art/, Locale/)
```

## Quick start (Windows, for contributors)

Requirements: CoH 1 / Legacy Edition installed and fully patched, Python 3.11+,
[Corsix's Mod Studio](https://modstudio.corsix.org/), and Git with
[Git LFS](https://git-lfs.com/) (`git lfs install` once, before cloning).

```powershell
git clone <this repo>
cd <repo>
py tools\modtool.py check                     # validate rosters and strings
.\tools\install-dev.ps1 -GamePath "C:\Program Files (x86)\Steam\steamapps\common\Company of Heroes Relaunch"
```

The install script builds the strings, links `mod\City17` into the game folder as a
junction (so edits show up in-game without copying), and copies `City17.module` next to
`RelicCOH.exe`. Then launch with:

```
RelicCOH.exe -dev -mod City17
```

or add `-dev -mod City17` to the game's Steam launch options.

## Contributing

- **Adding or renaming a unit:** edit `design/combine.toml` or
  `design/resistance.toml`, then run `py tools\modtool.py check`. Unit names and
  string IDs come from these files, so never type a unit name straight into a `.ucs` file.
- **Adding UI text:** add a line to `locale/english.tsv` in the general ID range.
- **Attribute (stat) changes:** made in Corsix's Mod Studio on the `.rgd` files under
  `mod/City17/Data/attrib`. Because `.rgd` is binary, say in the commit message what
  you changed and why.
- **Printing the roster for discussion:** `py tools\modtool.py roster` prints Markdown tables.
