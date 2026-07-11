# FH6 Tuner Tools Source

這是由 `fh6_tuner.exe` 分析後整理出的可維護重建版原始碼。

## 目前內容

- `fh6_tuner.py`：繁體中文 CustomTkinter 圖形介面。
- `fh6_core.py`：可維護的調校計算與單位換算核心。
- `editable_logic.py`：供其他 Python 程式呼叫的 API。
- `recovered_runtime.py`：原始 Python 3.13 位元碼載入器骨架，供後續深入還原使用。
- `DECOMPILATION_NOTES.md`：EXE 分析與還原限制說明。
- `build_exe.bat`：Windows EXE 打包腳本。
- `tests/test_recovery_files.py`：恢復資料驗證測試。

## 執行方式

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python fh6_tuner.py
```

## 打包成 Windows EXE

```powershell
build_exe.bat
```

完成後輸出：

```text
dist\fh6_tuner.exe
```

## 核心程式呼叫範例

```python
from fh6_core import TuneInput, calculate_tune

result = calculate_tune(
    TuneInput(
        drivetrain="AWD",
        weight_kg=1400,
        front_weight_pct=55,
        power_hp=500,
        goal="公路平衡",
        tire="半熱熔",
    )
)
print(result)
```

## 還原限制

原始 EXE 是以 PyInstaller 封裝的 Python 3.13 程式。封包內沒有原始 `.py` 文字，因此無法逐字恢復原作者的註解、排版與區域變數名稱。此儲存庫提供的是可執行、可繼續維護的重建版本，並保留已確認的還原資訊。

來源 EXE SHA-256：

```text
34b80e177144b904c39d489af57db82f565a8de88f9b63e1df1184ca4cda92b1
```
