from __future__ import annotations

from typing import Any


COMPLEMENT = str.maketrans("ACGT", "TGCA")


def reverse_complement(sequence: str) -> str:
    return sequence.translate(COMPLEMENT)[::-1]


GUIDE = "GACCTGATCGTACGATCGTA"
DEMO = {
    "guide": GUIDE,
    "genome": "A" * 25 + GUIDE + "AGG" + "T" * 12 + "GACCTGATCGTACGATCGTT" + "TGG" + "C" * 18 + reverse_complement("GACCTGATCGTACGATTGTT" + "CGG") + "A" * 25,
    "max_mismatches": 4,
}


def _score(guide: str, candidate: str) -> tuple[int, int, int]:
    mismatches = [index for index, (left, right) in enumerate(zip(guide, candidate)) if left != right]
    seed = sum(index >= 12 for index in mismatches)
    score = max(0, 100 - 8 * len(mismatches) - 7 * seed)
    return len(mismatches), seed, score


def analyze(payload: dict[str, Any]) -> dict[str, Any]:
    guide = str(payload.get("guide", "")).upper().replace("U", "T")
    genome = "".join(str(payload.get("genome", "")).upper().split())
    if len(guide) != 20 or set(guide) - set("ACGT"):
        raise ValueError("guide must contain exactly 20 A/C/G/T bases")
    if len(genome) < 23 or set(genome) - set("ACGTN"):
        raise ValueError("genome must contain at least 23 DNA bases")
    maximum = int(payload.get("max_mismatches", 4))
    hits = []
    for strand, sequence in (("+", genome), ("-", reverse_complement(genome))):
        for index in range(len(sequence) - 22):
            candidate, pam = sequence[index:index + 20], sequence[index + 20:index + 23]
            if "N" in candidate or pam[1:] != "GG":
                continue
            mismatches, seed, score = _score(guide, candidate)
            if mismatches <= maximum:
                position = index + 1 if strand == "+" else len(genome) - index - 22
                hits.append({"position": position, "strand": strand, "sequence": candidate, "pam": pam, "mismatches": mismatches, "seed_mismatches": seed, "specificity": score})
    hits.sort(key=lambda hit: (hit["mismatches"], hit["seed_mismatches"], -hit["specificity"], hit["position"]))
    off_targets = [hit for hit in hits if hit["mismatches"] > 0]
    return {
        "guide": guide,
        "genome_bases_scanned": len(genome),
        "candidate_hits": len(hits),
        "exact_sites": sum(hit["mismatches"] == 0 for hit in hits),
        "off_target_sites": len(off_targets),
        "highest_off_target_risk": off_targets[0] if off_targets else None,
        "hits": hits,
        "scope": "Mismatch-only SpCas9 NGG scan; bulges, chromatin, and experimental validation are outside scope.",
    }
