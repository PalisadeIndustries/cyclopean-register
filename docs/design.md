# Design

## Pitch

City 17, during the uprising. The Combine Overwatch holds the city with checkpoints,
forcefields and synths. The Resistance holds the rubble, the canals and the
sympathy of the population. Company of Heroes' fight over territory, cover and
suppression maps well onto this: the uprising was a street-by-street fight for ground.

## Pillars

1. **Asymmetry over mirror-matching.** The Combine is expensive, armoured, precise and
   tiered. The Resistance is cheap, numerous, improvised and gets worse equipment that it
   uses cleverly. Neither side should have an exact counterpart for every unit.
2. **Keep what CoH does well.** Cover, suppression, retreat, reinforcement, territory,
   veterancy and doctrines all stay. We re-theme systems before replacing them.
3. **Recognisable at a glance.** Every unit needs a silhouette that a Half-Life player
   can name. If the read is ambiguous, gameplay clarity wins over lore precision.
4. **Lore is a guide, not a cage.** HL2's cut content (Crab Synth, Mortar Synth) and
   reasonable invention are fair game when a gameplay role needs filling.

## Systems translation

| CoH system | City 17 equivalent | Notes |
|---|---|---|
| Manpower | **Manpower** | Unchanged name. Combine flavour text: "Overwatch allocation" |
| Munitions | **Munitions** | Abilities, weapon upgrades |
| Fuel | **Power** | Tech and vehicles. Combine dark energy, Resistance salvaged cells |
| Strategic point | **Sector point** | |
| Munitions point | **Supply cache** | |
| Fuel point | **Power node** | Combine: a Citadel conduit. Resistance: a tapped generator |
| Victory point | Victory point | |
| Wehrmacht veterancy (Kampfkraft) | **Overwatch conditioning** | Bought centrally, fits Combine augmentation |
| US veterancy (in combat) | Earned in the field | Unchanged |
| Doctrines | **Protocols** (Combine) / **Cells** (Resistance) | 3 per side, cloned from vanilla doctrine trees |
| Aircraft call-ins | Gunship, Hunter-Chopper, Dropship | Off-map abilities, as vanilla does planes |
| Sandbags / wire / tank traps | Forcefields, Combine barricades / scrap barricades | |

## Factions

The full rosters, including the vanilla unit each one is cloned from, are in
[`design/combine.toml`](../design/combine.toml) and
[`design/resistance.toml`](../design/resistance.toml). Run
`py tools/modtool.py roster` for tables.

### Combine Overwatch (Wehrmacht slot)

Few units, each one strong. Tight build order, strong static defence, and the best late
game in the mod in the Strider. Weak early on against units in cover, since Civil
Protection is poor infantry, and dependent on Power.

Core loop: Stalkers fortify territory, Civil Protection and Pulse Turrets hold it,
Overwatch squads and Hunters push. Conditioning makes surviving units much stronger.

### Resistance (US slot)

Swarming and adaptable. Squads are cheap and gain weapons through upgrades, picking up
Combine weapons dropped on the field (vanilla weapon pick-up). Vortigaunts are the elite
infantry. Vehicles are light and fast. Heavy anti-armour comes from rocket squads and
Magnusson devices, not tanks.

## Protocols and Cells (doctrines)

| Side | Name | Clones | Theme | Ultimate |
|---|---|---|---|---|
| Combine | Sector Lockdown | Defensive | Forcefields, ceiling turrets, sentry emplacements | Citadel Suppression Field |
| Combine | Pacification | Blitzkrieg | Dropship deployments, Hunter-Chopper strafes | Strider deployment |
| Combine | Sterilization | Terror | Headcrab shells, Manhack swarms, Breen broadcasts | Gunship patrol |
| Resistance | Lambda Uprising | Infantry | Rally, supply drops, elite rebels | Freeman sighting (hero unit) |
| Resistance | Vortal Coalition | Airborne | Vortigaunt healing, vortal blasts, antlion lures | Antlion Guard |
| Resistance | White Forest | Armor | Magnusson devices, rocket artillery, hacked turrets | Magnusson strike team |

## Open questions

- Commonwealth and Panzer Elite slots: leave vanilla, hide them, or later use them for
  sub-factions (e.g. a Synth-heavy Combine and a Vortigaunt-led Resistance)?
- Should Civil Protection get a non-lethal stun baton melee as a way to deal with
  garrisoned units?
- How should flying units (Scanners, Manhacks) look and move? CoH has no air layer,
  so they'd be ground units drawn with a height offset, or abilities. Needs a prototype.
- Hero units (Freeman, Alyx, D0G): one per match, doctrine-gated?
