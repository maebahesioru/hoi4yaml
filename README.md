# hoi4yaml

JSONL → HoI4 mod files generator. Designed for AI-assisted modding with inline localisation and extensive validation.

[日本語版 README](README.ja.md)

## Install

```bash
pip install git+https://github.com/maebahesioru/hoi4yaml.git
```

## Usage

```bash
hoi4yaml mod.jsonl          # generate mod files
hoi4yaml mod.jsonl --clean  # clean output first
hoi4yaml mod.jsonl --check  # validate only
hoi4yaml --list             # show all sections, shorthands, and validations
```

## Quick example

```jsonl
{"mod":{"name":"My Mod","version":"1.0","supported_version":"1.14.*"}}
{"focus_tree":{"_file":"GER_focuses","id":"GER_focus_tree","country":{"factor":0,"modifier":{"add":10,"tag":"GER"}}}}
{"focus":{"id":"GER_rearm","cost":10,"reward":{"add_political_power":100}},"loc":{"GER_rearm":"Rearmament","GER_rearm_desc":"Germany begins its rearmament."}}
```

Each line is self-contained with inline localisation. All languages auto-generated from English.

## Features

- **190+ sections** covering all of `common/`, `history/`, `map/`, `interface/`, `gfx/`, `sound/`, `music/`
- **Inline localisation**: `"loc":{"KEY":"English","ja":{"KEY":"日本語"}}`
- **Auto-layout**: focus x/y positions calculated from prereq graph
- **Auto-icons**: focus icons and idea pictures guessed from ID keywords
- **Name resolution**: `"state":"Liberia"` → `7959`, `"target":"ethiopia"` → `ETH`
- **Shorthands**: `prereq`, `reward`, `rel_pos`, `hidden`, `ai_will_do`, `set_tech`, `timed_idea`, etc.
- **40+ validations**: ideology names, trait names, modifier names, building levels, missing loc keys, duplicate IDs — all checked against live game files

## JSONL Format

One JSON object per line. Objects are merged by section key.

```jsonl
// Focus with inline loc (English + Japanese)
{"focus":{"id":"GER_rearm","prereq":"GER_start","cost":10,"reward":{"add_political_power":100}},"loc":{"GER_rearm":"Rearmament","GER_rearm_desc":"Begin rearmament.","ja":{"GER_rearm":"再軍備","GER_rearm_desc":"再軍備を開始する。"}}}

// Idea with inline loc
{"idea":{"GER_spirit_militarism":{"modifier":{"army_attack_factor":0.1}}},"loc":{"GER_spirit_militarism":"Militarism","GER_spirit_militarism_desc":"A strong military tradition."}}

// Event with inline loc
{"country_event":{"id":"GER.1","title":"GER.1.t","desc":"GER.1.d","option":[{"name":"GER.1.a","add_political_power":50}]},"loc":{"GER.1.t":"Event Title","GER.1.d":"Event description.","GER.1.a":"Option A"}}
```

## Full reference

See [REFERENCE.md](REFERENCE.md) for complete documentation including all shorthands, sections, validations, and examples.

## Requirements

- Python 3.10+
- Hearts of Iron IV installed (auto-detected via Steam)
