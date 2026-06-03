import logger

def analyze():
    rows = logger.read_all()

    if not rows:
        return {
            "status": "no_data",
            "message": "No log data yet. Change the duty cycle or frequency to start logging."
        }

    duties  = [float(r["duty_%"])   for r in rows]
    powers  = [float(r["power_mw"]) for r in rows]
    savings = [float(r["saved_mw"]) for r in rows]
    freqs   = [float(r["freq_hz"])  for r in rows]

    avg_power   = round(sum(powers)  / len(powers),  2)
    avg_saving  = round(sum(savings) / len(savings), 2)
    avg_duty    = round(sum(duties)  / len(duties),  2)
    peak_saving = round(max(savings), 2)
    peak_saving_duty = duties[savings.index(max(savings))]

    most_used_duty = max(set(duties), key=duties.count)
    most_used_freq = max(set(freqs),  key=freqs.count)

    total_mw_full   = 66.0 * len(rows)
    total_mw_actual = sum(powers)
    efficiency_pct  = round((1 - total_mw_actual / total_mw_full) * 100, 1) if total_mw_full > 0 else 0

    if efficiency_pct >= 50:
        grade = "A"
        grade_note = "Excellent — significant energy saved"
    elif efficiency_pct >= 30:
        grade = "B"
        grade_note = "Good — moderate savings achieved"
    elif efficiency_pct >= 15:
        grade = "C"
        grade_note = "Average — consider lower duty cycles"
    else:
        grade = "D"
        grade_note = "Poor — mostly running at full power"

    optimal_duty = round(100 - efficiency_pct, 1)

    return {
        "status": "ok",
        "total_readings": len(rows),
        "avg_power_mw":   avg_power,
        "avg_saving_mw":  avg_saving,
        "avg_duty_pct":   avg_duty,
        "peak_saving_mw": peak_saving,
        "peak_saving_duty": peak_saving_duty,
        "most_used_duty": most_used_duty,
        "most_used_freq": most_used_freq,
        "efficiency_pct": efficiency_pct,
        "grade":          grade,
        "grade_note":     grade_note,
        "optimal_duty":   optimal_duty,
        "recommendation": f"Run at {optimal_duty}% duty cycle for best efficiency balance"
    }