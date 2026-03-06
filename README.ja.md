# hoi4yaml

YAML → HoI4 modファイルジェネレーター。AIによるmod制作を前提に設計されており、ショートハンド構文と充実したバリデーションを備えています。

[English README](README.md)

## インストール

```bash
pip install git+https://github.com/maebahesioru/hoi4yaml.git
```

## 使い方

```bash
hoi4yaml mod.yaml          # modファイルを生成
hoi4yaml mod.yaml --clean  # 出力先を削除してから生成
hoi4yaml mod.yaml --check  # バリデーションのみ
hoi4yaml --list            # セクション・ショートハンド・バリデーション一覧
```

## クイックスタート

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

`english`のみ記述すれば、他の全言語は自動生成されます。

## 機能

- **190以上のセクション** — `common/`・`history/`・`map/`・`interface/`・`gfx/`・`sound/`・`music/`を完全網羅
- **ショートハンド** — `prereq`・`reward`・`rel_pos`・`hidden`・`ai_will_do`・`set_tech`・`set_ruling_party`・`add_pop`・`regiments`・`support_companies`・`sprites`・`timed_idea`・`add_state_building`・`add_state_manpower`
- **自動レイアウト** — prereqグラフからフォーカスのx/y座標を自動計算
- **アイコン自動設定** — フォーカスIDのキーワードからアイコンを自動推定
- **名前解決** — `target: ethiopia` → `ETH`、`state: berlin` → `64`
- **ローカライゼーション自動生成** — `english`のみ記述すれば全言語を自動生成
- **40以上のバリデーション** — イデオロギー名・トレイト名・モディファイア名・建物レベル・locキー欠落・ID重複など、ゲームファイルと照合してチェック

## 完全リファレンス

全ショートハンド・セクション・バリデーション・使用例は [REFERENCE.md](REFERENCE.md) を参照してください。

## 動作要件

- Python 3.10+
- Hearts of Iron IV インストール済み（Steamから自動検出）
