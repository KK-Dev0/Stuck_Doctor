"""Test the report decoder on real photos and get a right/wrong table you can show judges.

How to use (on your own computer, after `pip install gradio_client`):

1. Make a folder called eval/ and put 15-20 photos of REAL reports in it
   (blurry ones, rotated ones, different labs and formats). Blur out names and phone numbers first.
2. Make eval/expected.json with the numbers YOU read by eye from each photo, like this:
   {
     "report1.jpg": {"Hemoglobin": "13.5", "WBC": "7200"},
     "report2.png": {"Glucose": "98"}
   }
3. Run:  python eval_reports.py https://stuck-doctor.onrender.com eval
4. It writes eval/results.csv and eval/results.md. Paste the markdown table into docs/TESTING.md.

A value counts as "right" only if the number matches exactly. Test names are matched loosely
(so "Hemoglobin" will match "Haemoglobin (Hb)").
"""
import sys, json, csv, re, pathlib
from gradio_client import Client, handle_file


def num(s):
    m = re.search(r"-?\d+(?:\.\d+)?", str(s).replace(",", ""))
    return float(m.group()) if m else None


def find(got, test):
    t = test.strip().lower()
    for name, value in got.items():
        if t in name or name in t:
            return value
    return None


def main(url, folder):
    folder = pathlib.Path(folder)
    expected = json.loads((folder / "expected.json").read_text(encoding="utf-8"))
    client = Client(url)
    rows = []
    for name, truth in expected.items():
        print("Reading", name, "...")
        try:
            res = client.predict(handle_file(str(folder / name)), "English", "yes", api_name="/read_document")
        except Exception as e:
            print("  failed:", e)
            res = {}
        got = {str(v.get("test", "")).strip().lower(): v.get("value")
               for v in (res.get("values") or []) if isinstance(v, dict)}
        for test, want in truth.items():
            have = find(got, test)
            ok = have is not None and num(have) is not None and num(have) == num(want)
            rows.append([name, test, want, have if have is not None else "(missed)", "right" if ok else "wrong"])

    right = sum(1 for r in rows if r[4] == "right")
    total = len(rows) or 1
    with open(folder / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["photo", "test", "expected", "got", "result"])
        w.writerows(rows)
    lines = ["| Photo | Test | I read | Stuck Doctor read | Result |", "|---|---|---|---|---|"]
    lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in rows]
    lines += ["", f"**{right} of {len(rows)} values right ({100 * right // total}%)** across {len(expected)} photos."]
    (folder / "results.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\n{right} of {len(rows)} values right ({100 * right // total}%). Saved results.csv and results.md in {folder}/")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python eval_reports.py <backend url> <folder with photos and expected.json>")
    main(sys.argv[1], sys.argv[2])
