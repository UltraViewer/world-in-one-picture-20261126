# The World in One Picture — 26 November 2026

[![rank](https://make.fun/badge/news-image-20261126/UltraViewer/world-in-one-picture-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/UltraViewer/world-in-one-picture-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)

A one-page newspaper front page that sums up Thursday 26 November 2026
in a single 1024×1024 image, drawn entirely with Pillow shapes and
Liberation fonts — no photos, no network calls, no fetched assets.

## What is on the page

- **DRONES OVER KUWAIT** — two Rheinmetall Italia technicians (36 and 65)
  killed servicing Skyguard radar at a Kuwait air-defence site; two more
  wounded; Tehran denies any role.
- **ISRAEL KILLS HAMAS MINISTER IN GAZA STRIKES** — at least 9 killed
  overnight, including deputy education minister Khaled Abu Nada and his
  wife in Deir al-Balah; a third straight night of strikes despite a
  year-old ceasefire.
- **EBOLA PASSES 12,000 CASES IN CONGO** — 12,021 confirmed cases in the
  east, nearly half dead; the fastest-growing Ebola outbreak in history.
- **EU DEADLOCKED ON €1.58 TRILLION BUDGET** — 12 hours in Brussels with
  no deal; next attempt 17–18 December; a $49bn Ukraine loan is stuck.
- **NO PARADE ON THANKSGIVING** — the 100th Macy's parade postponed for
  the first time ever as a nor'easter gusts to 60 mph; moved to Saturday
  28 November.
- Footer briefs: Houthis claim strikes on Jeddah and Jazan, Serbia votes
  27 December, Russia approves a record military budget.

Every figure on the page was checked against 26 November reporting; no
numbers were invented.

## Files

- `compose.py` — draws `entry.png` from scratch (run it to regenerate).
- `main.py` — the entry point. It only validates the pre-rendered
  `entry.png` (PNG signature, IHDR, 1024×1024, ≤ 1 MiB) and copies it to
  `MAKEFUN_OUTPUT_DIR` (default `/output`). It imports nothing beyond
  the standard library.
- `entry.png` — the finished front page, 1024×1024. Running
  `compose.py` twice produces byte-identical output.

## Run

```sh
python3 compose.py   # regenerate entry.png
python3 main.py      # copy entry.png to /output/entry.png
```

## License

MIT — see `LICENSE`.
