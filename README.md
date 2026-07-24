# crisprradar

**Local CRISPR-Cas9 guide off-target scanner.**

![crisprradar cover](demo/cover.png)

Scan both strands for NGG-adjacent sites and rank exact, seed, and distal mismatch risk locally.

![crisprradar workbench](demo/dashboard.png)

## What ships

- A deterministic domain analysis engine with explicit scope
- JSON API and responsive local browser workbench
- CLI demo and file-driven analysis
- Docker image, unit tests, and GitHub Actions matrix
- No API keys and no uploaded user data

## Run it end to end

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e .
crisprradar demo
crisprradar serve
```

Open <http://127.0.0.1:8090>. Analyze your own JSON input with `crisprradar analyze input.json`.

## API

- `GET /api/demo` returns the committed fixture and result.
- `POST /api/analyze` runs the same engine on a JSON body.

## Current basis

- [CRISPRitz](https://github.com/pinellolab/CRISPRitz)

## Demo result

The scanner checks 149 bases on both strands and returns one exact SpCas9 site plus two NGG-adjacent off-targets. The highest-risk off-target has one seed mismatch and a specificity score of 85.

## Scope

This is a transparent mismatch-only SpCas9/NGG scanner for focused sequences and test fixtures. Genome-scale indexed search, DNA/RNA bulges, chromatin accessibility, allele-specific effects, and experimental validation are intentionally not claimed.

## Test

```bash
python -m unittest discover -s tests -v
```

MIT licensed.
