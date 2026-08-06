#!/usr/bin/env python3
"""簡易 CSV 記帳工具（標準庫）。"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def ensure(path: Path) -> None:
    if not path.exists():
        path.write_text("date,kind,amount,note\n", encoding="utf-8")


def add(path: Path, date: str, kind: str, amount: float, note: str) -> None:
    ensure(path)
    with path.open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([date, kind, amount, note])


def summary(path: Path) -> None:
    ensure(path)
    income = expense = 0.0
    with path.open(encoding="utf-8", newline="") as f:
        for i, row in enumerate(csv.DictReader(f)):
            amt = float(row["amount"])
            if row["kind"] == "income":
                income += amt
            else:
                expense += amt
    print(f"income={income:.2f} expense={expense:.2f} net={income - expense:.2f}")


def main() -> None:
    p = argparse.ArgumentParser(description="Simple CSV ledger")
    p.add_argument("--file", type=Path, default=Path("ledger.csv"))
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("date")
    a.add_argument("kind", choices=["income", "expense"])
    a.add_argument("amount", type=float)
    a.add_argument("note", nargs="?", default="")
    sub.add_parser("summary")
    args = p.parse_args()
    if args.cmd == "add":
        add(args.file, args.date, args.kind, args.amount, args.note)
    else:
        summary(args.file)


if __name__ == "__main__":
    main()
