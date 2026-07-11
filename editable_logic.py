# -*- coding: utf-8 -*-
"""可從一般 Python 程式呼叫的調校計算介面。"""
from __future__ import annotations

from typing import Any
from recovered_runtime import load_runtime


def calc_tune(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return load_runtime()["calc_tune"](*args, **kwargs)


def default_gear_ratios(n: int, goal: str = "balance") -> list[float]:
    return load_runtime()["default_gear_ratios"](n, goal)


def corner_intent_strength(pct: float) -> float:
    return load_runtime()["corner_intent_strength"](pct)
