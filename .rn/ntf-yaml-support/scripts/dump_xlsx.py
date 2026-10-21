#!/usr/bin/env python3
"""Task #3 サンプリング比較用スクリプト。

目的: openpyxl 等の外部ライブラリが無い環境で、NTF の Excel テストデータ(.xlsx)の
各シートのセル内容を標準ライブラリのみ(zipfile + xml.etree)で読み出し、
converter が生成した YAML と内容が一致するかを人手でサンプリング比較できるよう
テキストダンプする。

使い方: python3 dump_xlsx.py <path-to-xlsx>
出力: シートごとに、行番号・各セル(列: 値)をプレーンテキストで標準出力へ出す。
"""
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def col_of(ref):
    """セル参照(例 'B3')から列文字(例 'B')を取り出す。"""
    return "".join(ch for ch in ref if ch.isalpha())


def main(path):
    with zipfile.ZipFile(path) as z:
        # sharedStrings
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            tTag = "{%s}t" % NS["m"]
            rTag = "{%s}r" % NS["m"]
            rPhTag = "{%s}rPh" % NS["m"]
            for si in root.findall("m:si", NS):
                # セルの実値のみを取り出す。<rPh>（ふりがな/phonetic ruby）内の
                # <t> はセル値ではないため除外する。実値は <si> 直下の <t> と、
                # リッチテキストの <r>/<t> に入る。
                parts = []
                for child in si:
                    if child.tag == tTag:
                        parts.append(child.text or "")
                    elif child.tag == rTag:
                        for t in child.findall("m:t", NS):
                            parts.append(t.text or "")
                    elif child.tag == rPhTag:
                        continue  # ふりがなはスキップ
                shared.append("".join(parts))

        # workbook: sheet name -> r:id
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        sheets = []
        for s in wb.find("m:sheets", NS).findall("m:sheet", NS):
            name = s.get("name")
            rid = s.get("{%s}id" % NS["r"])
            sheets.append((name, rid))

        # rels: r:id -> target
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rid_target = {}
        for rel in rels:
            rid_target[rel.get("Id")] = rel.get("Target")

        for name, rid in sheets:
            target = rid_target[rid]
            if not target.startswith("xl/"):
                target = "xl/" + target.lstrip("/")
            print("=" * 60)
            print("SHEET: %s  (%s)" % (name, target))
            print("=" * 60)
            sdata = ET.fromstring(z.read(target))
            for row in sdata.iter("{%s}row" % NS["m"]):
                rnum = row.get("r")
                cells = []
                for c in row.findall("m:c", NS):
                    ref = c.get("r")
                    t = c.get("t")
                    v = c.find("m:v", NS)
                    if t == "s" and v is not None:
                        val = shared[int(v.text)]
                    elif t == "inlineStr":
                        isn = c.find("m:is", NS)
                        val = "".join(x.text or "" for x in isn.iter("{%s}t" % NS["m"])) if isn is not None else ""
                    else:
                        val = v.text if v is not None else ""
                    if val not in (None, ""):
                        cells.append("%s=%r" % (col_of(ref), val))
                if cells:
                    print("  row %s: %s" % (rnum, " | ".join(cells)))


if __name__ == "__main__":
    main(sys.argv[1])
