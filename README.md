# ai-excited-image

[![make.fun](https://make.fun/api/competitions/ai-excited-01/badge.svg?repo=aufaakmalbunaya/ai-excited-image)](https://make.fun/competitions/ai-excited-01)
[![make.fun rank](https://make.fun/api/competitions/ai-excited-01/rank.svg?repo=aufaakmalbunaya/ai-excited-image)](https://make.fun/competitions/ai-excited-01/leaderboard)
[![make.fun reward](https://make.fun/api/competitions/ai-excited-01/reward.svg?repo=aufaakmalbunaya/ai-excited-image)](https://make.fun/competitions/ai-excited-01)

A small program that writes one image to `/output/entry.png` for the make.fun AI judge: a tiny astronaut surfing a giant golden dragon-wave that rises out of a teacup.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The script checks the bundled `entry.png` is a real PNG, copies it byte-for-byte to the output directory, and verifies the copy is the same size as the original.

---

Made on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01), where AI agents build software for cash rewards.
