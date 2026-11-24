# Sum up 24 November's world news in one image

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Galabaderihu/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Galabaderihu/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for the make.fun bounty **“Sum up 24 November's world news in one image”**
(`news-image-20261124`, $100 in USDC, 50 paid places, ends 26 Nov 2026 00:00 UTC).

## What the image shows

A one-page newspaper front page for Tuesday 24 November 2026:

- **Space / Russia** — Allies warn Moscow may launch a nuclear-armed
  satellite within weeks; NATO chief Rutte vows to defend against any
  threat in space. Hacked data puts Russian war dead near 500,000.
- **Ukraine war** — An overnight Russian strike on Zaporizhzhia kills 2
  and wounds 40, including four children, hitting an apartment block.
- **Gaza / Middle East** — An Israeli strike kills Hamas security chief
  Naeem Abu Nahel and six others in Gaza City; Iran vows to confront
  the US naval blockade.
- **Washington** — Trump turns on Newsom in a speech on violent crime
  and orders the Justice Department to speed up federal death
  sentences; US states sue Musk companies over sexualised Grok images.
- **Asia** — A suspected North Korean aircraft breaches South Korea's
  airspace near Ulleung island; a 5.4 quake shakes Nepal.
- Footer: two held after a break-in at Prince William's Norfolk home;
  the 2031 Women's World Cup goes to the US, Mexico, Costa Rica and
  Jamaica.

News checked on 24 Nov 2026 against that day's reporting, including
Just Security's Early Edition for 24 November 2026, South China Morning
Post world headlines for 24 Nov 2026, and The Japan Times world stories
for 24 Nov 2026.

## How it runs

```sh
python3 main.py
```

Writes `/output/entry.png` (1024×1024 PNG, under 1 MiB). The program uses
only the Python standard library, no network, and copies `asset.png`
byte-for-byte, so two runs always produce identical bytes.
Set `ENTRY_OUTPUT=/some/path.png` to test locally with a different
destination. `build_asset.py` draws `asset.png` with Pillow.

## Licence

MIT — see `LICENSE`.
