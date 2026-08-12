"""Deterministic and explainable context scoring."""

from __future__ import annotations

import re

from microcode.context.models import ContextCandidate, ScoredCandidate


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[\w.-]+", text.casefold()))


def score_candidate(candidate: ContextCandidate, user_text: str) -> ScoredCandidate:
    source_priority = {
        "system": 100.0,
        "current_user": 100.0,
        "project_instructions": 85.0,
        "history": 65.0,
        "working_set": 60.0,
        "memory": 55.0,
    }.get(candidate.source, 40.0)
    query_terms = tokenize(user_text)
    candidate_terms = tokenize(candidate.label + " " + (candidate.content.preview or ""))
    overlap = len(query_terms & candidate_terms) / max(1, len(query_terms))
    factors = {
        "source_priority": source_priority,
        "lexical_overlap": overlap * 20.0,
        "size_penalty": min(20.0, candidate.estimated_tokens / 2_000),
    }
    score = factors["source_priority"] + factors["lexical_overlap"] - factors["size_penalty"]
    return ScoredCandidate(candidate=candidate, score=score, factors=factors)
