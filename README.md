# Cyclopean — Submissions Register

A collaborative workboard for the Cyclopean rules project. Contributors file
factions, units, and abilities into a branching register, propose mechanics on a
second board, and annotate anything.

---

## For contributors

1. Open the link.
2. Type your name into **Filed by** in the top bar. Everything you file or
   annotate is attributed to it.
That is the whole setup. The board connects to the shared database on its own —
the dot next to **Sync** in the top bar turns green once it has. If it does not,
you are working on a private copy in your own browser and nobody else can see
your records; reload and check your connection.

### Filing a record

The big **+** at the bottom starts a new faction. The small **+** on any row
files something underneath it — units under factions, abilities and wargear
under units. The **✕** deletes a record and everything beneath it.

Click a title to open the record on the right, where you can edit it, set its
status, and leave annotations. Annotations get resolved rather than deleted, so
an open objection stays visible until someone closes it.

**Move to…** reparents a record. It only offers destinations that legitimately
accept that kind, so a unit sees factions and an ability sees units.

### Importing from Order of Battle

Import / export → **Import an army list**, or drop the exported `.json` into the
normal file import. Order of Battle's format is recognised automatically: units
arrive with their full stat line, weapons become wargear children, and abilities
become ability children with their element cost resolved.

Before anything is filed you get an assignment table where you pick which
faction each unit belongs to. Units whose faction already exists on the board
are matched for you.

---

## For whoever maintains this

### Publishing

The site is a single self-contained `index.html`. To update it, replace that
file and commit. GitHub Pages redeploys within a minute or two.

### The database

Records live in a Firebase Realtime Database, not in this repository, so
deploying never touches anyone's work. Free tier covers this comfortably. The
config is compiled into `index.html`, which is why contributors have nothing to
set up. A Firebase web config is not a secret — the rules below are what protect
the data.

Rules should be scoped to the board path:

```json
{
  "rules": {
    "boards": {
      "$board": {
        ".read": true,
        ".write": true
      }
    }
  }
}
```

Do not leave the console's default test-mode rules in place — they expire after
a trial period and the board silently stops syncing.

To close the board to anyone who finds the database URL in this public
repository, enable **Anonymous** sign-in under Authentication and change both
rules to `"auth != null"`. The site already signs in anonymously on load, so
nothing needs rebuilding and contributors see no login screen.

### Backups

Import / export → **Export JSON** writes the whole board, both tabs, every
record and annotation. Import merges by last-edited timestamp, so restoring or
folding in someone else's export is safe. Worth doing before any large import.

**Export Markdown** gives the register as an indented outline for the rulebook
draft.
