# 還原說明

這個程式是以 PyInstaller 封裝的 Python 3.13 Windows GUI 應用程式。

EXE 中沒有原始 `.py` 文字，因此無法逐字恢復原作者的註解、空白、排版與區域變數名稱。專案採用兩層方式保存：

1. `recovery/fh6_tuner.marshalled.zlib.b64.part01～part04`：從 EXE 精確抽出的 Python 3.13 code object，可保留原始執行邏輯。
2. `source_scaffold.py`、`recovered_data_tables.py` 與 `editable_logic.py`：提供可閱讀的結構、資料表與呼叫介面。

`recovered_runtime.py` 會以非 `__main__` 名稱載入原始 code object，因此不會在匯入時自動打開視窗；`fh6_tuner.py` 再明確啟動 `TunerApp`。

## 已確認資訊

- 原始入口檔名：`fh6_tuner.py`
- Python bytecode：3.13
- GUI：Tkinter / CustomTkinter
- 封裝：PyInstaller one-file Windows GUI
- EXE SHA-256：`34b80e177144b904c39d489af57db82f565a8de88f9b63e1df1184ca4cda92b1`
