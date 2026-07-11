# -*- coding: utf-8 -*-
"""載入從原始 EXE 精確抽出的 Python 3.13 code object。"""
from __future__ import annotations

import base64
import marshal
import sys
import zlib
from pathlib import Path
from types import CodeType
from typing import Any

PAYLOAD_DIR = Path(__file__).resolve().parent / "recovery"
PAYLOAD_GLOB = "fh6_tuner.marshalled.zlib.b64.part*"
_RUNTIME: dict[str, Any] | None = None


def load_runtime(*, force_reload: bool = False) -> dict[str, Any]:
    """載入原始程式邏輯，但不自動開啟 GUI。"""
    global _RUNTIME
    if _RUNTIME is not None and not force_reload:
        return _RUNTIME
    if sys.version_info[:2] != (3, 13):
        raise RuntimeError(
            "此恢復專案的原始位元碼需要 Python 3.13。"
            f"目前版本：{sys.version.split()[0]}"
        )
    parts = sorted(PAYLOAD_DIR.glob(PAYLOAD_GLOB))
    if not parts:
        raise FileNotFoundError(f"找不到恢復位元碼分割檔：{PAYLOAD_DIR / PAYLOAD_GLOB}")

    encoded = b"".join(part.read_bytes().strip() for part in parts)
    code = marshal.loads(zlib.decompress(base64.b64decode(encoded)))
    if not isinstance(code, CodeType):
        raise TypeError("恢復檔案不是有效的 Python code object")

    namespace: dict[str, Any] = {
        "__name__": "fh6_recovered_runtime",
        "__file__": str(Path(__file__).resolve().parent / "fh6_tuner.py"),
        "__package__": None,
        "__builtins__": __builtins__,
    }
    exec(code, namespace, namespace)
    _RUNTIME = namespace
    return namespace


def run_gui() -> None:
    runtime = load_runtime()
    app_type = runtime["TunerApp"]
    app = app_type()
    app.mainloop()
