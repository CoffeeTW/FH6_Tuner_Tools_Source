from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_payload_and_manifest_exist():
    payload_parts = sorted((ROOT / "recovery").glob("fh6_tuner.marshalled.zlib.b64.part*"))
    manifest = ROOT / "recovery" / "recovery_manifest.json"
    assert len(payload_parts) == 4
    assert sum(part.stat().st_size for part in payload_parts) > 380_000
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["python_version"] == "3.13"
    assert data["original_code_filename"] == "fh6_tuner.py"


def test_source_exe_hash_recorded():
    data = json.loads((ROOT / "recovery" / "recovery_manifest.json").read_text(encoding="utf-8"))
    assert data["source_sha256"] == "34b80e177144b904c39d489af57db82f565a8de88f9b63e1df1184ca4cda92b1"
