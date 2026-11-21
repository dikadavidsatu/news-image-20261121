# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/dikadavidsatu/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/dikadavidsatu/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A single 1024×1024 poster summing up the world's news of Saturday
21 November 2026, for the make.fun competition
`news-image-20261121`. The judge sees only the image; everything a
viewer needs is drawn on it, including the date.

## The stories

- **Lead — Missiles fall on Poland.** Russia fired 400+ drones and
  110 missiles at Ukraine overnight — its biggest barrage this year.
  At least 8 people were killed in Kyiv as bridges and power lines
  were hit. Two missiles and a suspected drone came down in Poland;
  Warsaw calls it a deliberate provocation.
- **Markets — AI rout: S&P in correction.** The S&P 500 fell 3.7%
  and the Nasdaq 5.3%, erasing its 2026 gains; Nvidia fell about
  14% after a report of an SEC accounting probe.
- **Justice — Myanmar guilty of genocide.** The world court rules
  Myanmar committed genocide against the Rohingya — the first time
  it has held a state responsible.
- **Climate — COP31 runs into overtime.** Talks in Antalya extended
  past their deadline as nearly 200 nations stay deadlocked over
  fossil fuels.
- **Middle East — Missiles at Riyadh stopped.** The Saudi-led
  coalition intercepts three Houthi missiles aimed at the capital,
  the third night running.
- **Europe — UK–EU's biggest step since Brexit.** Three deals signed:
  food trade, carbon markets and youth mobility for 100,000 young
  Britons.
- **Also today:** Trump defends calling Putin "my friend" after the
  Shenzhen summit with Xi; the FBI criminal database was hacked,
  CNN reports; a pancreatic-cancer pill trial shows tumours
  undetectable in 1 in 12 patients; a 6.9 quake shakes Peru's Andes;
  a power-plant fire in Basra kills at least 4.

Sources: Reuters, AP, BBC, Al Jazeera, France 24, The Guardian, FT.

## How it is built

`build_poster.py` draws the poster with Pillow and the system DejaVu
fonts. Everything is fixed at authoring time — no network, no clock,
no unseeded randomness — so re-running it reproduces the same PNG
byte for byte:

```sh
python3 build_poster.py   # writes entry.png (1024x1024, < 1 MiB)
```

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` is the competition entrypoint (Python 3.13, standard library
only). It copies the shipped `entry.png` to the output folder.

## License

MIT — see `LICENSE`.
