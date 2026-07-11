from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass
class TuneInput:
    drivetrain: str = 'AWD'
    weight_kg: float = 1400.0
    front_weight_pct: float = 55.0
    power_hp: float = 500.0
    goal: str = '公路平衡'
    tire: str = '半熱熔'


def cm_to_in(v: float) -> float: return v / 2.54
def in_to_cm(v: float) -> float: return v * 2.54
def kg_to_lb(v: float) -> float: return v * 2.2046226218
def lb_to_kg(v: float) -> float: return v / 2.2046226218
def kgm_to_lbft(v: float) -> float: return v * 7.233013851

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def default_gear_ratios(n: int = 6, goal: str = 'balance') -> list[float]:
    n = max(4, min(10, int(n)))
    first = 3.25 if goal != 'speed' else 2.90
    last = 0.72 if goal != 'accel' else 0.82
    ratio = (last / first) ** (1 / (n - 1))
    return [round(first * ratio ** i, 2) for i in range(n)]


def calculate_tune(inp: TuneInput) -> dict:
    fw = clamp(inp.front_weight_pct / 100.0, 0.35, 0.70)
    rw = 1.0 - fw
    offroad = '越野' in inp.goal or '拉力' in inp.goal
    drift = '甩尾' in inp.goal
    speed = '極速' in inp.goal

    tire_base = 27.5 if inp.tire in ('半熱熔', '光頭胎') else 29.0
    if offroad: tire_base = 25.0
    front_psi = tire_base + (fw - .5) * 4
    rear_psi = tire_base + (rw - .5) * 4

    arb_total = 48 if offroad else 62
    spring_total = max(70.0, inp.weight_kg * (0.095 if offroad else 0.13))
    ride = 15.0 if offroad else 9.0
    if drift: ride = 8.5

    if inp.drivetrain == 'FWD':
        diff = {'前加速': 45, '前減速': 12}
    elif inp.drivetrain == 'RWD':
        diff = {'後加速': 62 if not drift else 82, '後減速': 18 if not drift else 35}
    else:
        diff = {'前加速': 28, '前減速': 8, '後加速': 62 if not drift else 78, '後減速': 18, '中央': 68 if not drift else 75}

    goal_key = 'speed' if speed else ('accel' if drift else 'balance')
    final_drive = 3.15 if speed else (4.10 if drift else 3.65)
    return {
        '輸入': asdict(inp),
        '輪胎壓力_psi': {'前': round(front_psi, 1), '後': round(rear_psi, 1)},
        '終傳比': final_drive,
        '齒比': default_gear_ratios(6, goal_key),
        '定位': {'前外傾': -2.0 if not offroad else -1.2, '後外傾': -1.4 if not offroad else -0.8, '前束': 0.1 if drift else 0.0, '後束': 0.0, '後傾角': 6.0},
        '防傾桿': {'前': round(arb_total * fw, 1), '後': round(arb_total * rw, 1)},
        '彈簧_kgf_per_mm': {'前': round(spring_total * fw, 1), '後': round(spring_total * rw, 1)},
        '車高_cm': {'前': ride, '後': round(ride + (0.7 if offroad else 0.3), 1)},
        '減震器': {'前回彈': round(9.5 * fw + 3.5, 1), '後回彈': round(9.5 * rw + 3.5, 1), '前壓縮': round((9.5 * fw + 3.5) * .62, 1), '後壓縮': round((9.5 * rw + 3.5) * .62, 1)},
        '煞車': {'平衡': round(50 + (fw - .5) * 10), '壓力': 105},
        '差速器': diff,
    }


def format_tune_text(result: dict) -> str:
    lines = []
    for section, value in result.items():
        if section == '輸入': continue
        lines.append(f'【{section}】')
        if isinstance(value, dict):
            lines.extend(f'{k}：{v}' for k, v in value.items())
        elif isinstance(value, list):
            lines.append(' / '.join(f'{i+1}檔 {v:.2f}' for i, v in enumerate(value)))
        else:
            lines.append(str(value))
        lines.append('')
    return '\n'.join(lines).strip()
