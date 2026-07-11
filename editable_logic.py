# -*- coding: utf-8 -*-
"""可從一般 Python 程式呼叫的調校計算介面。"""
from __future__ import annotations

from fh6_core import TuneInput, calculate_tune, default_gear_ratios


def calc_tune(**kwargs):
    """使用關鍵字參數建立 TuneInput 並回傳建議調校。"""
    return calculate_tune(TuneInput(**kwargs))


def corner_intent_strength(pct: float) -> float:
    """將 0～100 的轉向偏好正規化為 0～1。"""
    return max(0.0, min(100.0, float(pct))) / 100.0


__all__ = ["TuneInput", "calculate_tune", "calc_tune", "default_gear_ratios", "corner_intent_strength"]
