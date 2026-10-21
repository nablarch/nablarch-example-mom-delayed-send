# nablarch-example-mom-delayed-send NTF YAML 対応 steering

## Overview
- 目的・背景: NTF（Nablarch Testing Framework）の AI 対応として、AI が読み書きできないバイナリ形式の Excel テストデータを YAML 形式に移行する（背景資料: https://github.com/Fintan-contents/nablarch-system-development-guide/pull/211）。
- Acceptance criteria 要約:
  - 既存 `ntf-yaml-support` ブランチの履歴を維持したまま（rebase / amend / hard reset なし）、先端の上に `develop` 一致ツリーのベースラインコミットを積み、その上に task-1〜5 を再実施する（過去の移行コミットがあってもスキップしない）
  - ベースライン（`develop` 同等）で全テスト PASS を確認する
  - `pom.xml` に `nablarch-testing-yaml:1.0.0-SNAPSHOT`（test scope）と `nablarch-testing-converter:1.0.0-SNAPSHOT`（`<build><plugins>` のビルドプラグイン）を追加する
  - `YamlTestDataParser`（`testDataParser`）を、`testDataParser` が参照される全フェーズで有効になる設定ファイルに追加する（`interpreters` は `dateTimeInterpreter` → `compositeInterpreter` の2つのみ）
  - 全テスト用 Excel を YAML に変換し（サンプリング比較で一致確認）、Excel を削除したうえで全テスト PASS
- 対象プロジェクト名: nablarch-example-mom-delayed-send（MOM 応答不要メッセージングの送信側 Example）
- 指示書: `.rn/ntf-yaml-support/ntf-yaml-support-instructions_mom-delayed-send_V1.6.md`（原本: `/home/k10949/instructions/ntf-yaml-support-instructions_mom-delayed-send_V1.6.md`）
- ベースライン: 旧先端 `6932e57`（過去の移行コミット Task #1〜5 を含む）の上に、ベースラインコミット `c6e1ed2`（ツリー = `develop`、tree `650dab9`）を新規に積んだ。

## Build / Test
- README 記載: Java 17 / Maven 3.9.9 以降。ビルドは `mvn package`。DB セットアップ及びエンティティクラス生成は `mvn package` に含まれ、`mvn generate-resources` で個別実行可能（gsp-dba-maven-plugin が `generate-sources` フェーズに `generate-ddl` / `execute-ddl` / `load-data` を束縛。プロファイル指定は不要）。
- 本作業での実行手順:
  1. エンティティ生成: `mvn clean generate-resources`
  2. テスト: `mvn test`
- 実行環境: OpenJDK 21.0.2 / Apache Maven 3.9.16。
- 補足: README は `.mvn/jvm.config` に言及しているが、`develop` には存在しない（上記環境では無しで成功）。

## Scripts
- `scripts/dump_xlsx.py`（Task #3）: サンプリング比較用。外部ライブラリなしで `.xlsx` の各シートのセル値をテキストダンプし、converter が生成した YAML と目視で比較できるようにする（`python3 -I dump_xlsx.py <xlsx>`）。
- `scripts/compare_samples.py`（Task #3）: サンプリング比較用。Excel の指定セル値と YAML の指定パスの値を突き合わせ、一致/不一致を Markdown 表で出力する（`python3 -I compare_samples.py <xlsx> <yaml-dir>`、全一致で rc=0）。データなしシートの YAML が空であること、Excel シートと YAML ファイルの1対1対応も確認する。YAML は NTF と同じく全スカラーを文字列として読む（`yaml.BaseLoader`）。

## Tasks

### #1: ベースライン化（developと同一状態）し、全PASSを確認する
**Purpose**: 既存 `ntf-yaml-support` ブランチ（履歴維持）上で、過去の移行コミットの有無にかかわらず、先端の上に `develop` 一致ツリーのコミットを1つ新規に積み、その状態で全テストがパスすることを確認する（完了済みでも再実施）。
**Prerequisites**: none
**Steps**:
- [x] 既存の `ntf-yaml-support` ブランチへ切り替える（新規作成なし。履歴維持）
- [x] 過去の移行コミット（`813c92a`〜`6932e57`）を巻き戻さず、現在の先端の上に処理を積む
- [x] `develop` の存在を確認し、`git read-tree -u --reset develop` → `git commit` でベースラインコミット `c6e1ed2` を積む（`git diff develop HEAD` 差分なし）
- [x] README を確認し、ビルド・テスト手順を把握する（上記 Build / Test）
- [x] steering.md の初版を作成する（scripts は Task #3 で作成）
- [x] 本指示書を `.rn/ntf-yaml-support/` 配下へ同名でコピーし、`cmp` で原本と同一であることを確認する
- [x] `mvn clean generate-resources` でエンティティクラスを生成する
- [x] `mvn test` で全テスト PASS を確認する（Tests run: 1, Failures: 0, Errors: 0, Skipped: 0 / BUILD SUCCESS）
- [x] 結果を `checks/task-1.md` に記録する
- [x] 変更ファイルをコミットする
- [x] self-check
- [x] QA expert review (Agent: general-purpose / Opus)
- [ ] user review（全 task 完了後にまとめて実施）
**Completion criteria**:
- 既存の `ntf-yaml-support` ブランチ上で作業しており、コミット履歴が維持されている（過去の移行コミットが残っている）
- ブランチの既存先端の上に、ワーキングツリー全体が `develop` と同一内容になる新規コミットが1つ積まれている
- `mvn test` が全テストパスで終了している（BUILD SUCCESS）
- 本指示書のコピーが `.rn/ntf-yaml-support/` 配下に原本と同一内容で配置され、コミットされている

### #2: 設定変更 — pom.xml と unit-test.xml にYAML対応を追加
**Purpose**: `pom.xml` に `nablarch-testing-yaml`（test 依存）と `nablarch-testing-converter`（ビルドプラグイン）を追加し、`YamlTestDataParser` を Rules の「全フェーズで有効化」方針に従って配置する。
**Prerequisites**: #1
**Steps**:
- [x] `pom.xml` に `nablarch-testing-yaml:1.0.0-SNAPSHOT`（test scope）を追加する
- [x] `pom.xml` の `<build><plugins>` に `nablarch-testing-converter:1.0.0-SNAPSHOT` を追加する（`<configuration>` に from=xls / to=yaml / input / output / overwrite。web/batch 準拠）
- [x] 応答電文（`response_*` / sendSync）の有無から、実行中にモックが `testDataParser` 経由でテストデータを読む構成かを判定する → 非該当（`RESPONSE_*` なし。送信のみの非同期・応答不要）
- [x] 判定結果に応じて `YamlTestDataParser` を配置する → `src/test/resources/unit-test.xml`（`interpreters` は `dateTimeInterpreter` → `compositeInterpreter` の2つのみ。`test-data.xml` の import・`dbInfo` 定義より後）
- [x] `mvn dependency:resolve` と `mvn help:describe -Dplugin=com.nablarch.framework:nablarch-testing-converter:1.0.0-SNAPSHOT` で解決を確認する
- [x] 変更したファイルをコミットする
- [x] self-check
- [x] QA / language / software-engineering expert review（いずれも OK） (Agent: general-purpose / Opus)
- [ ] user review（全 task 完了後にまとめて実施）
**Completion criteria**:
- `pom.xml` に `nablarch-testing-yaml:1.0.0-SNAPSHOT` が test スコープで追加されている
- `pom.xml` の `<build><plugins>` に `nablarch-testing-converter:1.0.0-SNAPSHOT` がビルドプラグインとして追加されている
- `YamlTestDataParser` が `testDataParser` の参照される全フェーズで有効になる設定ファイルに追加され、`interpreters` は `dateTimeInterpreter` → `compositeInterpreter` の2つのみ
- `mvn dependency:resolve` が成功し、converter の `convert` ゴールが `mvn help:describe` で解決できる

### #3: ExcelテストデータをYAMLに変換
**Purpose**: `nablarch-testing-converter` で Excel テストデータを YAML に変換し、ソースツリー内に配置してサンプリング比較で確認する。
**Prerequisites**: #2
**Steps**:
- [x] 対象 Excel の所在を確認する（`ProjectInsertMessageRequestTest.xlsx` の1件）
- [x] 同名 `.xls` / `.xlsx` の併存を確認する（併存なし）
- [x] converter README の手順で全対象 Excel を YAML 変換する（`mvn com.nablarch.framework:nablarch-testing-converter:1.0.0-SNAPSHOT:convert`、Converted 1 file(s)）
- [x] 各 YAML について Excel とサンプリング比較する（各ファイル最低3件。3件未満は全件）
- [x] 比較結果を `checks/task-3.md` の Sampling Comparison に記録する
- [x] YAML をコミットする（Excel はまだ削除しない）
- [x] self-check
- [x] QA expert review（OK。改善提案を compare_samples.py に反映） (Agent: general-purpose / Opus)
- [ ] user review（全 task 完了後にまとめて実施）
**Completion criteria**:
- 変換対象の全 Excel に対応する YAML が生成されている
- サンプリング比較で Excel と YAML の内容が一致している
- 変換後の YAML がコミットされている

### #4: Excelを削除する
**Purpose**: 変換対象だった Excel を削除してコミットする。
**Prerequisites**: #3
**Steps**:
- [x] 変換対象の Excel を削除する（`ProjectInsertMessageRequestTest.xlsx`）
- [x] 残存 Excel 0 件を `checks/task-4.md` に記録する
- [x] 削除をコミットする
- [x] self-check
- [ ] QA expert review (Agent: general-purpose / Opus)
- [ ] user review（全 task 完了後にまとめて実施）
**Completion criteria**:
- 変換対象だった全 Excel ファイルが削除されている
- 削除がコミットされている

### #5: YAMLテストデータで全テストをパスさせる
**Purpose**: Excel なしで全テストがパスすることを確認する。
**Prerequisites**: #4
**Steps**:
- [x] `mvn clean generate-resources` → `mvn test` が BUILD SUCCESS になることを確認する（Tests run: 1, Failures: 0, Errors: 0, Skipped: 0）
- [x] テストログで YamlTestDataParser が実際に使われていることを確認する（`testDataParser` の override WARN と `YamlTestDataParser` の INFO ログ）
- [x] self-check
- [ ] QA / language / software-engineering expert review (Agent: general-purpose / Opus)
- [ ] user review（全 task 完了後にまとめて実施）
**Completion criteria**:
- `mvn test` が BUILD SUCCESS で終了する（全テストパス、Excel ファイルなし）
- テストログで YamlTestDataParser が実際に使われていることが確認できる
