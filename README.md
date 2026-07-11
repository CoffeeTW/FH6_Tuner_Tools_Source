# FH6 Tuner Tools Source Recovery

這是從 `fh6_tuner.exe` 重新抽取與整理的原始碼恢復專案。

## 專案內容

- `fh6_tuner.py`：GUI 啟動入口。
- `recovered_runtime.py`：載入原始 Python 3.13 code object。
- `editable_logic.py`：可直接呼叫的調校計算 API。
- `recovered_data_tables.py`：從原程式恢復的常數與調校資料表。
- `source_scaffold.py`：依原始函式、類別、參數和行號生成的可閱讀結構。
- `recovery/fh6_tuner.marshalled.zlib.b64.part01～part04`：從 EXE 精確抽出的原始 code object。
- `recovery/recovery_manifest.json`：EXE、位元碼與函式清單驗證資料。
- `recovery/code_inventory.json`：所有 code object 的結構清單。
- `recovery/runtime_signatures.txt`：主要函式與類別方法簽章。
- `tools/generate_recovery_artifacts.py`：產生完整反組譯與完整常數表。
- `tools/extract_pyinstaller.py`：PyInstaller CArchive 抽取工具。

## 執行需求

必須使用 **Python 3.13**，因為恢復的 code object 與 Python 小版本綁定。

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python fh6_tuner.py
```

## 呼叫核心計算

```python
from editable_logic import calc_tune, default_gear_ratios

ratios = default_gear_ratios(6, "balance")
print(ratios)
```

## 打包成 Windows EXE

```powershell
build_exe.bat
```

輸出檔案位於：

```text
dist\fh6_tuner.exe
```

## 還原限制

EXE 只包含編譯後的 Python code object，不含原始 `.py` 文字，因此無法逐字恢復原作者的註解與排版。`recovery/fh6_tuner.marshalled.zlib.b64.part01～part04` 保存原始執行邏輯，其餘檔案則提供可閱讀、可擴充的維護介面。詳細說明見 `DECOMPILATION_NOTES.md`。
