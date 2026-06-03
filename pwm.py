def calculate(duty):
    full_power = 66.0
    power = round(full_power * duty / 100, 2)
    saved = round(full_power - power, 2)
    savings_pct = round(100 - duty, 2)
    return {
        "duty": duty,
        "power_mw": power,
        "saved_mw": saved,
        "savings_pct": savings_pct,
    }

def calculate_freq(duty, freq):
    period_ms = round(1000 / freq, 4)
    on_ms     = round(period_ms * duty / 100, 4)
    off_ms    = round(period_ms - on_ms, 4)

    if freq < 20:
        band = "Slow / visible flicker"
    elif freq < 1000:
        band = "Mid-range / audible buzz"
    elif freq < 5000:
        band = "Fast / inaudible"
    else:
        band = "Very fast / switching"

    return {
        "duty": duty,
        "freq_hz": freq,
        "period_ms": period_ms,
        "on_ms": on_ms,
        "off_ms": off_ms,
        "band": band
    }

def waveform_points(duty, freq):
    period = 1000 / freq
    on_t   = period * duty / 100
    cycles = 3
    total  = period * cycles
    pts = []
    for i in range(cycles):
        t = i * period
        pts += [(t, 0), (t, 3.3), (t + on_t, 3.3), (t + on_t, 0)]
    pts.append((total, 0))
    return pts

def power_curve_points():
    return [(i, round(66 * i / 100, 1)) for i in range(0, 101, 5)]