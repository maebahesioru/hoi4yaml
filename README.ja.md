# hoi4yaml

JSONL → HoI4 modファイル生成ツール。AI支援modding向けに設計。インラインローカライゼーションと充実したバリデーション。

[English README](README.md)

## インストール

```bash
pip install git+https://github.com/maebahesioru/hoi4yaml.git
```

## 使い方

```bash
hoi4yaml mod.jsonl          # modファイル生成
hoi4yaml mod.jsonl --clean  # 出力先をクリーンしてから生成
hoi4yaml mod.jsonl --check  # バリデーションのみ
hoi4yaml --list             # 全セクション・ショートハンド・バリデーション一覧
```

## クイック例

```jsonl
{"mod":{"name":"My Mod","version":"1.0","supported_version":"1.14.*"}}
{"focus_tree":{"_file":"GER_focuses","id":"GER_focus_tree","country":{"factor":0,"modifier":{"add":10,"tag":"GER"}}}}
{"focus":{"id":"GER_rearm","cost":10,"reward":{"add_political_power":100}},"loc":{"GER_rearm":"再軍備","GER_rearm_desc":"ドイツは再軍備を開始する。"}}
```

1行1オブジェクト。ローカライゼーションはインラインで記述。英語から全言語を自動生成。

## 機能

- **190+セクション対応** — `common/`・`history/`・`map/`・`interface/`・`gfx/`・`sound/`・`music/`を網羅
- **インラインローカライゼーション** — `"loc":{"KEY":"English","ja":{"KEY":"日本語"}}`
- **自動レイアウト** — prereqグラフからフォーカスのx/y座標を自動計算
- **自動アイコン** — IDキーワードからフォーカスicon・国家精神pictureを推定
- **名前解決** — `"state":"Liberia"` → `7959`、`"target":"ethiopia"` → `ETH`
- **ショートハンド** — `prereq`・`reward`・`rel_pos`・`hidden`・`ai_will_do`・`set_tech`・`timed_idea`など
- **40+バリデーション** — ideology名・trait名・modifier名・建物レベル・loc漏れ・重複IDなど、ゲームファイルと照合

## JSONLフォーマット

1行1JSONオブジェクト。同じセクションキーは自動マージ。

```jsonl
// フォーカス（英語+日本語loc付き）
{"focus":{"id":"GER_rearm","prereq":"GER_start","cost":10,"reward":{"add_political_power":100}},"loc":{"GER_rearm":"Rearmament","GER_rearm_desc":"Begin rearmament.","ja":{"GER_rearm":"再軍備","GER_rearm_desc":"再軍備を開始する。"}}}

// 国家精神
{"idea":{"GER_spirit_militarism":{"modifier":{"army_attack_factor":0.1}}},"loc":{"GER_spirit_militarism":"Militarism","GER_spirit_militarism_desc":"A strong military tradition."}}

// イベント
{"country_event":{"id":"GER.1","title":"GER.1.t","desc":"GER.1.d","option":[{"name":"GER.1.a","add_political_power":50}]},"loc":{"GER.1.t":"Event Title","GER.1.d":"Event description.","GER.1.a":"Option A"}}
```

## 詳細リファレンス

全機能のドキュメントは[REFERENCE.md](REFERENCE.md)を参照。

## 要件

- Python 3.10+
- Hearts of Iron IV（Steam経由で自動検出）
