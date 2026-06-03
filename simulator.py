import pwm

FAN_MAX_RPM    = 3000
BULB_MAX_LUMEN = 800
BULB_MAX_HEAT  = 5.0

def simulate(duty, freq):
    calc   = pwm.calculate(duty)
    timing = pwm.calculate_freq(duty, freq)

    fan_rpm    = round(FAN_MAX_RPM    * duty / 100)
    fan_power  = round(33.0 * duty / 100, 2)

    lumen      = round(BULB_MAX_LUMEN * duty / 100)
    bulb_power = round(33.0 * duty / 100, 2)
    heat       = round(BULB_MAX_HEAT  * (1 - duty / 100), 2)

    if duty == 0:
        fan_status  = "Off"
        bulb_status = "Off"
    elif duty <= 20:
        fan_status  = "Very slow"
        bulb_status = "Barely glowing"
    elif duty <= 50:
        fan_status  = "Half speed"
        bulb_status = "Medium brightness"
    elif duty <= 75:
        fan_status  = "Running fast"
        bulb_status = "Bright"
    else:
        fan_status  = "Full speed"
        bulb_status = "Full brightness"

    return {
        "duty":        duty,
        "freq_hz":     freq,
        "fan": {
            "rpm":     fan_rpm,
            "power_mw": fan_power,
            "status":  fan_status,
            "pct":     duty
        },
        "bulb": {
            "lumen":   lumen,
            "power_mw": bulb_power,
            "heat_mw": heat,
            "status":  bulb_status,
            "pct":     duty
        },
        "timing": timing,
        "total_power_mw": calc["power_mw"],
        "total_saved_mw": calc["saved_mw"]
    }