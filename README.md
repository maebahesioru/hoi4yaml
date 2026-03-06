# hoi4yaml

YAML → HoI4 mod files generator. Designed for AI-assisted modding with shorthand syntax and extensive validation.

[日本語版 README](README.ja.md)

## Install

```bash
pip install git+https://github.com/maebahesioru/hoi4yaml.git
```

## Usage

```bash
hoi4yaml mod.yaml          # generate mod files
hoi4yaml mod.yaml --clean  # clean output first
hoi4yaml mod.yaml --check  # validate only
hoi4yaml --list            # show all sections, shorthands, and validations
```

## Quick example

```yaml
mod:
  name: My Mod
  version: "1.0"
  supported_version: "1.14.*"

national_focus:
  - _file: GER_focuses
    focus_tree:
      id: GER_focus_tree
      country:
        factor: 0
        modifier:
          add: 10
          tag: GER
      focus:
        - id: GER_rearm
          x: 0
          y: 0
          cost: 10
          reward:
            add_political_power: 100

localisation:
  english:
    GER_rearm: "Rearmament"
    GER_rearm_desc: "Germany begins its rearmament."
```

`english` only — all other languages are auto-generated.

## Features

- **190+ sections** covering all of `common/`, `history/`, `map/`, `interface/`, `gfx/`, `sound/`, `music/`
- **Shorthands**: `prereq`, `reward`, `rel_pos`, `hidden`, `ai_will_do`, `set_tech`, `set_ruling_party`, `add_pop`, `regiments`, `support_companies`, `sprites`, `timed_idea`, `add_state_building`, `add_state_manpower`
- **Auto-layout**: focus x/y positions calculated from prereq graph
- **Auto-icons**: focus icons and idea pictures guessed from ID keywords
- **Name resolution**: `target: ethiopia` → `ETH`, `state: berlin` → `64`
- **Auto-localisation**: write `english` only, all languages generated automatically
- **40+ validations**: ideology names, trait names, modifier names, building levels, missing loc keys, duplicate IDs, and more — all checked against live game files

## Full reference

See [REFERENCE.md](REFERENCE.md) for complete documentation including all shorthands, sections, validations, and examples.

## Requirements

- Python 3.10+
- Hearts of Iron IV installed (auto-detected via Steam)
