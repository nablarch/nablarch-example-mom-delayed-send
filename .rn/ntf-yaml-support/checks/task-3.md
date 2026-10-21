# task-3 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 変換対象の全 Excel に対応する YAML が生成されている | OK | 対象 Excel は `src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest.xlsx` の1ファイル（シート `setUpDb` / `testSendMessage`）。`mvn com.nablarch.framework:nablarch-testing-converter:1.0.0-SNAPSHOT:convert`（pom の `<configuration>` を使用）で `Converted 1 file(s).` / BUILD SUCCESS。`ProjectInsertMessageRequestTest/setUpDb.yaml`（0 バイト）と `ProjectInsertMessageRequestTest/testSendMessage.yaml` を生成。シート数とYAML数が一致 | OK | `src` 配下の `.xls`/`.xlsx` は `ProjectInsertMessageRequestTest.xlsx` 1件のみ（`.xls` 0件で併存なし）。シート `setUpDb`（`<sheetData/>`、セル0件）/ `testSendMessage` の2つに対し YAML 2つが1対1対応。0 バイト YAML は NTF の `YamlLoader.load` で空 Map 扱いとなり空シートと同等 |
| サンプリング比較で Excel と YAML の内容が一致している | OK | `scripts/compare_samples.py` で `testSendMessage.yaml` 9件（testShots / SETUP_TABLE / EXPECTED_REQUEST_HEADER_MESSAGES / EXPECTED_REQUEST_BODY_MESSAGES / EXPECTED_TABLE の各ブロックから抽出）と、データなしシート `setUpDb` の空 YAML を照合し全一致（rc=0）。下記 Sampling Comparison 参照 | OK | 独自スクリプトで `testSendMessage` シートの値ありセル全件と YAML（`BaseLoader` で文字列として読込）を比較し 87 項目で差異0件。改行（`\n\n`）、日付書式3種（原文のまま）、空値 `予備領域` / `FILLER2` の `""`、電文 fields の name/type/length、行数・キー順まで一致。`file-type: "Fixed"` は NTF の `DataFile` コンストラクタが `FixedLengthFile.getFileType()` を既定設定する値で、実行時は Excel と同一 |
| 変換後の YAML がコミットされている | OK | YAML 2ファイルと `scripts/`（`dump_xlsx.py` / `compare_samples.py`）を Task #3 コミットに含めた。Excel は未削除（Task #4 で削除） | OK | `a1c94ea` は YAML 2件・`checks/task-3.md`・`scripts/` 2件の追加と `steering.md` 更新のみ。Excel は追跡されたまま残存。`git diff 6932e57 a1c94ea` で YAML ディレクトリに差分なし |

## Sampling Comparison（task-3 のみ）
| YAML ファイル | 比較件数 | レコードキー/行 | Excel 値 | YAML 値 | 一致 |
| --- | --- | --- | --- | --- | --- |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | testShots no=1 / diConfig (testSendMessage!G4) | 'messaging-async-send-boot.xml' | 'messaging-async-send-boot.xml' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | testShots no=1 / description（改行含む） (testSendMessage!B4) | '正常系ケース\n\n電文が想定通り送信され、テーブルの処理ステータスが送信済みに更新されること。' | '正常系ケース\n\n電文が想定通り送信され、テーブルの処理ステータスが送信済みに更新されること。' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | SETUP_TABLE[1] SEND_MESSAGE_SEQUENCE (testSendMessage!A14) | '0000010001' | '0000010001' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | SETUP_TABLE[1] PROJECT_START_DATE (testSendMessage!E14) | '2010-9-18 00:00:00.0' | '2010-9-18 00:00:00.0' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_REQUEST_HEADER_MESSAGES[1] 電文連番 (testSendMessage!C24) | '0000010001' | '0000010001' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_REQUEST_BODY_MESSAGES[1] プロジェクト名 (testSendMessage!B32) | 'プロジェクト００１' | 'プロジェクト００１' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_REQUEST_BODY_MESSAGES[1] 備考 length (testSendMessage!K31) | '1024' | '1024' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_TABLE[1] STATUS (testSendMessage!P39) | '1' | '1' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/testSendMessage.yaml | 9 | EXPECTED_TABLE[1] UPDATED_DATE (testSendMessage!T39) | '2014-09-13 12:34:56.0' | '2014-09-13 12:34:56.0' | OK |
| src/test/java/com/nablarch/example/ProjectInsertMessageRequestTest/setUpDb.yaml | 0（元データ0件のため全件=0件。空ファイルであることを確認） | （元シートにデータなし） | （空） | （空） | OK |

- 比較方法: `python3 -I .rn/ntf-yaml-support/scripts/compare_samples.py <xlsx> <yaml-dir>`（Excel のセル値と YAML の値を文字列で完全一致比較。YAML は `BaseLoader` で読込。Excel シートと YAML ファイルの1対1対応も確認し `correspondence=OK`）。`dump_xlsx.py` で Excel 全セルをダンプし、目視でも YAML 全体と照合した。
- 補足: YAML の電文ブロックの `directives` に Excel に無い `file-type: "Fixed"` が出力される。converter が NTF の読み取り処理（`FixedLengthFile`）を通して電文を読むため付く暗黙の属性で、Excel 由来のデータ値の差異ではない（`text-encoding: "MS932"` は Excel と一致）。
- 参考: 生成 YAML は、旧移行コミット `6932e57` 時点の `testSendMessage.yaml` と `diff` で完全一致。

## .xls/.xlsx 併存チェック（該当時のみ）
- 併存の有無: なし（`find` で `.xls` 0件、`.xlsx` 1件のみ）
- 差分確認結果の保存先: 該当なし
- 未使用側（通常 `.xlsx`）の削除: 該当なし

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Meaningful tests/verification | OK | `compare_samples.py` は `==` の厳密比較で不一致時 rc=1、9件のセル番地と YAML パスの対応は正しい。ふりがな（`rPh`）は除外済み。改善点: YAML を `BaseLoader`（NTF と同じ YAML 1.2 相当の文字列読込）で読む、シートと YAML の過不足を確認する → 反映済み（再実行で全一致・対応 OK、rc=0） |
| Edge case coverage | OK | QA で全セル比較を行い、空値（`FILLER2` / `予備領域`）、`directives`、行数、改行入り文字列、日付書式3種、ゼロ埋め値、全角文字、空シート→0バイト YAML、YAML 1.1 で真偽値化する `no` キーまで一致を確認 |

## Expert Reviews (code changes only)

N/A — no code changes in this task.

## Overall Verdict

- Self-check: OK
- QA: OK
- Language expert: N/A
- Software-engineering expert: N/A
- Ready for user review: Yes
