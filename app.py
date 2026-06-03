from flask import Flask, render_template, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import pwm
import logger
import analyzer
import simulator
import report

app = Flask(__name__)
duty = 50
freq = 1000

logger.init()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/set", methods=["POST"])
def set_duty():
    global duty, freq
    data = request.get_json()
    duty = int(data.get("duty", duty))
    freq = int(data.get("freq", freq))
    result = pwm.calculate(duty)
    result.update(pwm.calculate_freq(duty, freq))
    logger.log(duty, freq, result)
    return jsonify(result)

@app.route("/api/status")
def status():
    result = pwm.calculate(duty)
    result.update(pwm.calculate_freq(duty, freq))
    return jsonify(result)

@app.route("/api/simulate")
def simulate():
    d = int(request.args.get("duty", duty))
    f = int(request.args.get("freq", freq))
    return jsonify(simulator.simulate(d, f))

@app.route("/api/analyze")
def analyze():
    return jsonify(analyzer.analyze())

@app.route("/api/clearlog", methods=["POST"])
def clearlog():
    logger.clear()
    return jsonify({"status": "cleared"})

@app.route("/chart/waveform")
def chart_waveform():
    d = int(request.args.get("duty", duty))
    f = int(request.args.get("freq", freq))
    pts = pwm.waveform_points(d, f)
    xs, ys = zip(*pts)
    period = 1000 / f
    total  = period * 3
    on_ms  = round(period * d / 100, 3)
    off_ms = round(period - on_ms, 3)

    fig, ax = plt.subplots(figsize=(6, 2))
    ax.step(xs, ys, where='post', color='#3266ad', linewidth=2)
    ax.fill_between(xs, ys, step='post', alpha=0.12, color='#3266ad')
    ax.set_xlim(0, total)
    ax.set_ylim(-0.4, 4.2)
    ax.set_yticks([0, 3.3])
    ax.set_yticklabels(['0V', '3.3V'], fontsize=10)
    ax.set_xlabel('Time (ms)', fontsize=10)
    ax.set_xticks([round(i * period, 3) for i in range(4)])
    ax.xaxis.set_tick_params(labelsize=9)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.set_title(
        f'{f} Hz  |  Period: {round(period,3)} ms  |  ON: {on_ms} ms  OFF: {off_ms} ms',
        fontsize=10, color='#444', pad=8
    )
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=130)
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route("/chart/power")
def chart_power():
    pts = pwm.power_curve_points()
    xs, ys = zip(*pts)
    cur = pwm.calculate(duty)

    fig, ax = plt.subplots(figsize=(6, 2.5))
    ax.plot(xs, ys, color='#3266ad', linewidth=2)
    ax.fill_between(xs, ys, alpha=0.08, color='#3266ad')
    ax.scatter([cur['duty']], [cur['power_mw']], color='#E24B4A', zorder=5, s=80)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.set_xlabel('Duty cycle (%)', fontsize=10)
    ax.set_ylabel('Power (mW)', fontsize=10)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.set_title('Average power vs duty cycle', fontsize=11, color='#444', pad=8)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=130)
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route("/chart/report")
def chart_report():
    buf = report.generate()
    if buf is None:
        return "Not enough data yet — change settings at least twice.", 400
    return send_file(buf, mimetype='image/png')

if __name__ == "__main__":
    print("=" * 40)
    print("  PWM Energy Dashboard")
    print("  http://127.0.0.1:5000")
    print("=" * 40)
    app.run(debug=True)