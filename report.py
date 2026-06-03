import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import io
import logger
from datetime import datetime

def generate():
    rows = logger.read_all()
    if len(rows) < 2:
        return None

    times   = list(range(1, len(rows) + 1))
    duties  = [float(r["duty_%"])   for r in rows]
    powers  = [float(r["power_mw"]) for r in rows]
    savings = [float(r["saved_mw"]) for r in rows]
    freqs   = [float(r["freq_hz"])  for r in rows]

    fig = plt.figure(figsize=(10, 7))
    fig.patch.set_facecolor('#ffffff')
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    # Plot 1 — duty cycle over session
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(times, duties, color='#3266ad', linewidth=2, marker='o', markersize=3)
    ax1.fill_between(times, duties, alpha=0.1, color='#3266ad')
    ax1.set_title('Duty cycle over session', fontsize=11, color='#333', pad=8)
    ax1.set_ylabel('Duty (%)', fontsize=9)
    ax1.set_xlabel('Reading #', fontsize=9)
    ax1.set_ylim(0, 110)
    ax1.spines[['top', 'right']].set_visible(False)
    ax1.set_facecolor('#fafafa')

    # Plot 2 — power consumed vs saved
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(times, powers,  color='#E24B4A', linewidth=2, label='Consumed')
    ax2.plot(times, savings, color='#1D9E75', linewidth=2, label='Saved')
    ax2.fill_between(times, powers,  alpha=0.08, color='#E24B4A')
    ax2.fill_between(times, savings, alpha=0.08, color='#1D9E75')
    ax2.set_title('Power consumed vs saved (mW)', fontsize=11, color='#333', pad=8)
    ax2.set_ylabel('Power (mW)', fontsize=9)
    ax2.set_xlabel('Reading #', fontsize=9)
    ax2.legend(fontsize=8)
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.set_facecolor('#fafafa')

    # Plot 3 — frequency over session
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(times, freqs, color='#e67e00', linewidth=2, marker='s', markersize=3)
    ax3.fill_between(times, freqs, alpha=0.08, color='#e67e00')
    ax3.set_title('Frequency over session (Hz)', fontsize=11, color='#333', pad=8)
    ax3.set_ylabel('Frequency (Hz)', fontsize=9)
    ax3.set_xlabel('Reading #', fontsize=9)
    ax3.spines[['top', 'right']].set_visible(False)
    ax3.set_facecolor('#fafafa')

    # Plot 4 — duty vs power scatter
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.scatter(duties, powers, color='#3266ad', alpha=0.6, s=30)
    ax4.set_title('Duty cycle vs power (scatter)', fontsize=11, color='#333', pad=8)
    ax4.set_xlabel('Duty (%)', fontsize=9)
    ax4.set_ylabel('Power (mW)', fontsize=9)
    ax4.spines[['top', 'right']].set_visible(False)
    ax4.set_facecolor('#fafafa')

    fig.suptitle(
        f'PWM Session Report — {datetime.now().strftime("%Y-%m-%d %H:%M")}  |  {len(rows)} readings',
        fontsize=13, color='#222', y=1.01
    )

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=130)
    plt.close(fig)
    buf.seek(0)
    return buf