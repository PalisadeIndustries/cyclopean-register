#!/usr/bin/env python3
"""Validate the faction rosters and build the mod's localisation file.

    py tools/modtool.py check [--vanilla RelicCOH.English.ucs]
    py tools/modtool.py build-ucs [--out PATH]
    py tools/modtool.py roster

Strings come from two places: names and blurbs in design/*.toml, and everything else in
locale/english.tsv. build-ucs merges them into the UTF-16 .ucs file the game reads.
"""

import argparse
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN_DIR = ROOT / "design"
LOCALE_TSV = ROOT / "locale" / "english.tsv"
DEFAULT_UCS = ROOT / "mod" / "City17" / "Locale" / "English" / "City17.ucs"

GENERAL_RANGE = (32000000, 32000999)
STATUSES = {"planned", "prototyped", "in-game", "final"}
UNIT_FIELDS = ("id", "name", "ucs", "blurb", "role", "tier", "clone_from", "vanilla_bp", "status")
DOCTRINE_FIELDS = ("id", "name", "ucs", "blurb", "clone_from", "abilities", "ultimate")


class Strings:
    """Collects ID -> text, remembering where each ID came from so clashes are traceable."""

    def __init__(self):
        self.text = {}
        self.origin = {}
        self.errors = []

    def add(self, ucs_id, text, origin):
        if ucs_id in self.text:
            self.errors.append(f"{origin}: ID {ucs_id} already used by {self.origin[ucs_id]}")
            return
        if "\t" in text or "\n" in text:
            self.errors.append(f"{origin}: text for {ucs_id} contains a tab or newline")
        self.text[ucs_id] = text
        self.origin[ucs_id] = origin


def load_factions():
    factions = []
    for path in sorted(DESIGN_DIR.glob("*.toml")):
        with path.open("rb") as f:
            factions.append((path.name, tomllib.load(f)))
    return factions


def load_tsv(strings):
    for lineno, line in enumerate(LOCALE_TSV.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        origin = f"{LOCALE_TSV.name}:{lineno}"
        key, sep, text = line.partition("\t")
        if not sep or not key.strip().isdigit():
            strings.errors.append(f"{origin}: expected '<id><TAB><text>'")
            continue
        ucs_id = int(key)
        if not GENERAL_RANGE[0] <= ucs_id <= GENERAL_RANGE[1]:
            strings.errors.append(f"{origin}: ID {ucs_id} outside general range {GENERAL_RANGE}")
        strings.add(ucs_id, text, origin)


def collect(factions):
    """Gather every string and every roster problem. Returns (strings, warnings)."""
    strings = Strings()
    warnings = []
    load_tsv(strings)
    seen_ids = {}

    for filename, data in factions:
        faction = data.get("faction", {})
        lo, hi = faction.get("ucs_range", (0, -1))
        retired = set(faction.get("retired_ucs", []))
        if lo > hi:
            strings.errors.append(f"{filename}: [faction] needs ucs_range = [low, high]")
        if not faction.get("name") or not isinstance(faction.get("ucs"), int):
            strings.errors.append(f"{filename}: [faction] needs a name and an integer ucs")
        else:
            strings.add(faction["ucs"], faction["name"], f"{filename} [faction]")
            if faction.get("blurb"):
                strings.add(faction["ucs"] + 1, faction["blurb"], f"{filename} [faction] blurb")

        entries = [("units", e, UNIT_FIELDS) for e in data.get("units", [])]
        entries += [("doctrines", e, DOCTRINE_FIELDS) for e in data.get("doctrines", [])]
        for kind, entry, required in entries:
            where = f"{filename} {kind}.{entry.get('id', '?')}"
            missing = [k for k in required if k not in entry]
            if missing:
                strings.errors.append(f"{where}: missing {', '.join(missing)}")
                continue
            if entry["id"] in seen_ids:
                strings.errors.append(f"{where}: id also used in {seen_ids[entry['id']]}")
            seen_ids[entry["id"]] = filename

            ucs_id = entry["ucs"]
            if not isinstance(ucs_id, int) or ucs_id % 10:
                strings.errors.append(f"{where}: ucs must be an integer multiple of 10")
                continue
            if not lo <= ucs_id < hi:
                strings.errors.append(f"{where}: ucs {ucs_id} outside faction range [{lo}, {hi}]")
            if {ucs_id, ucs_id + 1} & retired:
                strings.errors.append(f"{where}: ucs {ucs_id} is retired")
            strings.add(ucs_id, entry["name"], where)
            strings.add(ucs_id + 1, entry["blurb"], f"{where} blurb")

            if kind == "units":
                if entry["status"] not in STATUSES:
                    strings.errors.append(f"{where}: status must be one of {sorted(STATUSES)}")
                if not entry["vanilla_bp"] and entry["status"] != "planned":
                    strings.errors.append(f"{where}: status is {entry['status']} but vanilla_bp is empty")
                elif not entry["vanilla_bp"]:
                    warnings.append(where)

    return strings, warnings


def read_ucs(path):
    """Read a Relic .ucs file (UTF-16, '<id><TAB><text>' per line) into a dict."""
    out = {}
    for line in path.read_text(encoding="utf-16").splitlines():
        key, sep, text = line.partition("\t")
        if sep and key.strip().isdigit():
            out[int(key)] = text
    return out


def cmd_check(args):
    strings, warnings = collect(load_factions())
    if args.vanilla:
        vanilla = read_ucs(Path(args.vanilla))
        for ucs_id in sorted(strings.text.keys() & vanilla.keys()):
            strings.errors.append(f"ID {ucs_id} collides with vanilla string {vanilla[ucs_id]!r}")
    for err in strings.errors:
        print(f"error: {err}")
    if warnings:
        print(f"{len(warnings)} unit(s) still have no vanilla_bp (fine while planned)")
    print(f"{len(strings.text)} strings, {len(strings.errors)} error(s)")
    return 1 if strings.errors else 0


def cmd_build_ucs(args):
    strings, _ = collect(load_factions())
    if strings.errors:
        for err in strings.errors:
            print(f"error: {err}")
        print("not building: fix the errors above first (see `check`)")
        return 1
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(f"{k}\t{strings.text[k]}\r\n" for k in sorted(strings.text))
    # The game expects UTF-16 LE with a byte-order mark and Windows line endings.
    out.write_bytes(b"\xff\xfe" + body.encode("utf-16-le"))
    print(f"wrote {len(strings.text)} strings to {out}")
    return 0


def cmd_roster(args):
    for _, data in load_factions():
        faction = data["faction"]
        print(f"## {faction['name']} (vanilla slot: {faction['vanilla_race']})\n")
        print("| Tier | Unit | Role | Cloned from | Status |")
        print("|---|---|---|---|---|")
        for u in sorted(data.get("units", []), key=lambda u: u["tier"]):
            print(f"| {u['tier']} | {u['name']} | {u['role']} | {u['clone_from']} | {u['status']} |")
        print("\n| Doctrine | Cloned from | Ultimate |")
        print("|---|---|---|")
        for d in data.get("doctrines", []):
            print(f"| {d['name']} | {d['clone_from']} | {d['ultimate']} |")
        print()
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check", help="validate rosters and strings")
    p.add_argument("--vanilla", help="vanilla .ucs file to check for ID collisions")
    p.set_defaults(func=cmd_check)
    p = sub.add_parser("build-ucs", help="write the mod's .ucs file")
    p.add_argument("--out", default=str(DEFAULT_UCS))
    p.set_defaults(func=cmd_build_ucs)
    p = sub.add_parser("roster", help="print the rosters as Markdown tables")
    p.set_defaults(func=cmd_roster)
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
