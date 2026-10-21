#!/usr/bin/env python3
"""Task #3 サンプリング比較用スクリプト。

目的: 変換元 Excel(.xlsx) のセル値と、converter が生成した YAML の値を、
指定したサンプル（Excel のシート/セル ↔ YAML のパス）ごとに突き合わせ、
一致/不一致を表形式で出力する（checks/task-3.md の Sampling Comparison 記録用）。
Excel の読み出しは同ディレクトリの dump_xlsx.py と同じ方式（標準ライブラリのみ）。

使い方: python3 -I compare_samples.py <xlsx> <yaml-dir>
終了コード: 全一致なら 0、不一致があれば 1。
"""
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

import yaml

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

# (YAML ファイル, レコードキー/行の説明, Excel シート, Excel セル, YAML パス)
SAMPLES = [
    ("testSendMessage.yaml", "testShots no=1 / diConfig", "testSendMessage", "G4",
     ["list_maps", 0, "rows", 0, "diConfig"]),
    ("testSendMessage.yaml", "testShots no=1 / description（改行含む）", "testSendMessage", "B4",
     ["list_maps", 0, "rows", 0, "description"]),
    ("testSendMessage.yaml", "SETUP_TABLE[1] SEND_MESSAGE_SEQUENCE", "testSendMessage", "A14",
     ["setup_tables", 0, "rows", 0, "SEND_MESSAGE_SEQUENCE"]),
    ("testSendMessage.yaml", "SETUP_TABLE[1] PROJECT_START_DATE", "testSendMessage", "E14",
     ["setup_tables", 0, "rows", 0, "PROJECT_START_DATE"]),
    ("testSendMessage.yaml", "EXPECTED_REQUEST_HEADER_MESSAGES[1] 電文連番", "testSendMessage", "C24",
     ["expected_request_header_messages", 0, "records", 0, "rows", 0, 1]),
    ("testSendMessage.yaml", "EXPECTED_REQUEST_BODY_MESSAGES[1] プロジェクト名", "testSendMessage", "B32",
     ["expected_request_body_messages", 0, "records", 0, "rows", 0, 0]),
    ("testSendMessage.yaml", "EXPECTED_REQUEST_BODY_MESSAGES[1] 備考 length", "testSendMessage", "K31",
     ["expected_request_body_messages", 0, "records", 0, "fields", 9, "length"]),
    ("testSendMessage.yaml", "EXPECTED_TABLE[1] STATUS", "testSendMessage", "P39",
     ["expected_tables", 0, "rows", 0, "STATUS"]),
    ("testSendMessage.yaml", "EXPECTED_TABLE[1] UPDATED_DATE", "testSendMessage", "T39",
     ["expected_tables", 0, "rows", 0, "UPDATED_DATE"]),
]


def read_sheets(path):
    """シート名 -> {セル参照: 値} を返す。"""
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                parts = []
                for child in si:
                    if child.tag == "{%s}t" % NS["m"]:
                        parts.append(child.text or "")
                    elif child.tag == "{%s}r" % NS["m"]:
                        parts.extend(t.text or "" for t in child.findall("m:t", NS))
                shared.append("".join(parts))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
        sheets = {}
        for s in wb.find("m:sheets", NS).findall("m:sheet", NS):
            target = rels[s.get("{%s}id" % NS["r"])]
            if not target.startswith("xl/"):
                target = "xl/" + target.lstrip("/")
            cells = {}
            for c in ET.fromstring(z.read(target)).iter("{%s}c" % NS["m"]):
                v = c.find("m:v", NS)
                if c.get("t") == "s" and v is not None:
                    cells[c.get("r")] = shared[int(v.text)]
                elif c.get("t") == "inlineStr":
                    cells[c.get("r")] = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                elif v is not None:
                    cells[c.get("r")] = v.text
            sheets[s.get("name")] = cells
        return sheets


def dig(data, path):
    for key in path:
        data = data[key]
    return data


def main(xlsx, yaml_dir):
    sheets = read_sheets(xlsx)
    ok = True
    print("| YAML ファイル | レコードキー/行 | Excel 値 | YAML 値 | 一致 |")
    print("| --- | --- | --- | --- | --- |")
    for yfile, label, sheet, cell, ypath in SAMPLES:
        with open(os.path.join(yaml_dir, yfile), encoding="utf-8") as f:
            ydata = yaml.safe_load(f)
        xval = sheets[sheet].get(cell, "")
        yval = dig(ydata, ypath)
        match = xval == yval
        ok = ok and match
        print("| %s | %s (%s!%s) | %r | %r | %s |" % (yfile, label, sheet, cell, xval, yval, "OK" if match else "NG"))
    # データを持たないシートは YAML 側も空であることを確認する
    for sheet, cells in sheets.items():
        if not any(v not in (None, "") for v in cells.values()):
            ypath = os.path.join(yaml_dir, sheet + ".yaml")
            with open(ypath, encoding="utf-8") as f:
                empty = yaml.safe_load(f) is None
            ok = ok and empty
            print("| %s.yaml | （元シートにデータなし） | （空） | %s | %s |" % (sheet, "（空）" if empty else "（非空）", "OK" if empty else "NG"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
