import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, RadioButtons, Button



fig, (ax_phasor, ax_wave) = plt.subplots(1, 2, figsize=(13, 8))
plt.subplots_adjust(left=0.08, bottom=0.45, right=0.95, top=0.92, wspace=0.25)
fig.suptitle("Simulador de Interferência de Ondas com Fasores", fontsize=18, fontweight='bold')

class WaveState:
    def __init__(self):
        self.A1, self.phi1, self.w1 = 1.2, np.pi/4, 1.0
        self.A2, self.phi2, self.w2 = 0.8, 3*np.pi/4, 1.0
        self.anim_time = 0.0

state = WaveState()
time_array = np.linspace(0, 20, 1000)

is_updating = False 

is_paused = False

INITIALS = {
    "A1": 1.2,
    "phi1": np.pi/4,
    "w1": 1.0,
    "A2": 0.8,
    "phi2": 3*np.pi/4,
    "w2": 1.0,
    "anim_time": 0.0
}

ax_phasor.set_title("Diagrama de Fasores", fontsize=14)
ax_phasor.set_xlim(-4, 4)
ax_phasor.set_ylim(-4, 4)
ax_phasor.set_aspect('equal')
ax_phasor.grid(True, linestyle='--')
ax_phasor.set_xlabel('Parte Real')
ax_phasor.set_ylabel('Parte Imaginária')

line1, = ax_phasor.plot([], [], 'b-', lw=2, label='Fasor 1')
line2, = ax_phasor.plot([], [], 'r-', lw=2, label='Fasor 2')
line_res, = ax_phasor.plot([], [], 'k-', lw=3, label='Resultante')
line2_ref, = ax_phasor.plot([], [], 'r--', lw=1.5, alpha=0.5)

dot1, = ax_phasor.plot([], [], 'bo')
dot_res, = ax_phasor.plot([], [], 'ko')
dot2, = ax_phasor.plot([], [], 'ro')

info_box = ax_phasor.text(
    -3.95, 3.9, '',
    fontsize=8.5,
    verticalalignment='top',
    horizontalalignment='left',
    bbox=dict(facecolor='white', edgecolor='gray', alpha=0.85, boxstyle='round,pad=0.35')
)
ax_phasor.legend(loc='lower right', fontsize=9)

ax_wave.set_title("Gráfico de Ondas no Tempo (y(t))", fontsize=14)
ax_wave.set_xlim(0, 20)
ax_wave.set_ylim(-4, 4)
ax_wave.set_xlabel("Tempo (s)")
ax_wave.set_ylabel("Amplitude")
ax_wave.grid(True, linestyle='--')

wave1_line, = ax_wave.plot([], [], 'b-', alpha=0.7, label='Onda 1')
wave2_line, = ax_wave.plot([], [], 'r-', alpha=0.7, label='Onda 2')
wave_res_line, = ax_wave.plot([], [], 'k-', lw=2.5, label='Resultante')
ax_wave.legend(loc='upper right', fontsize=9)

eq_box = ax_wave.text(
    0.03, 0.95, '',
    transform=ax_wave.transAxes,
    fontsize=11, 
    verticalalignment='top', 
    bbox=dict(facecolor='lightyellow', edgecolor='orange', alpha=0.9, boxstyle='round,pad=0.5')
)

def recompute_curves():
    y1 = state.A1 * np.cos(state.w1 * time_array + state.phi1)
    y2 = state.A2 * np.cos(state.w2 * time_array + state.phi2)
    y_res = y1 + y2
    wave1_line.set_data(time_array, y1)
    wave2_line.set_data(time_array, y2)
    wave_res_line.set_data(time_array, y_res)
    fig.canvas.draw_idle()

recompute_curves()

wave1_dot, = ax_wave.plot([], [], 'bo', ms=8)
wave2_dot, = ax_wave.plot([], [], 'ro', ms=8)
wave_res_dot, = ax_wave.plot([], [], 'ko', ms=8)

texto_explicativo = (
    "O diagrama de fasores (esquerda) ilustra a soma vetorial de duas ondas.\n"
    "Cada onda é um vetor giratório. A Amplitude (A) é o raio, a Fase (phi) é o ângulo inicial e (w) é a velocidade de rotação no tempo.\n"
    "Fases opostas causam interferência destrutiva. Frequências (w) diferentes causam batimentos (a resultante cresce e diminui no tempo)."
)

fig.text(0.5, 0.38, texto_explicativo, ha='center', va='center', fontsize=11, wrap=True, 
         bbox=dict(boxstyle='round,pad=0.6', facecolor='wheat', edgecolor='tan', alpha=0.5))

ax_A1 = plt.axes([0.10, 0.28, 0.25, 0.02], facecolor='lightcyan')
ax_phi1 = plt.axes([0.10, 0.23, 0.25, 0.02], facecolor='lightcyan')
ax_w1 = plt.axes([0.10, 0.18, 0.25, 0.02], facecolor='lightcyan')

ax_A2 = plt.axes([0.45, 0.28, 0.25, 0.02], facecolor='mistyrose')
ax_phi2 = plt.axes([0.45, 0.23, 0.25, 0.02], facecolor='mistyrose')
ax_w2 = plt.axes([0.45, 0.18, 0.25, 0.02], facecolor='mistyrose')

s_A1 = Slider(ax_A1, 'A1 (m)', 0.0, 2.0, valinit=state.A1, valstep=0.01)
s_phi1 = Slider(ax_phi1, 'phi1 (rad)', 0.0, 2*np.pi, valinit=state.phi1, valstep=0.01)
s_w1 = Slider(ax_w1, 'w1 (rad/s)', 0.0, 3.0, valinit=state.w1, valstep=0.1)

s_A2 = Slider(ax_A2, 'A2 (m)', 0.0, 2.0, valinit=state.A2, valstep=0.01)
s_phi2 = Slider(ax_phi2, 'phi2 (rad)', 0.0, 2*np.pi, valinit=state.phi2, valstep=0.01)
s_w2 = Slider(ax_w2, 'w2 (rad/s)', 0.0, 3.0, valinit=state.w2, valstep=0.1)

ax_scenarios = plt.axes([0.78, 0.18, 0.20, 0.18], facecolor='whitesmoke')
opcoes = ('Cenário Atual', 'Mesma Fase', 'Fases Opostas', 'Batimentos (w diff)', 'Variável')
scenarios = RadioButtons(ax_scenarios, opcoes, active=4)

ax_pause = plt.axes([0.78, 0.12, 0.20, 0.04])
btn_pause = Button(ax_pause, 'Pausar')

ax_reset = plt.axes([0.78, 0.07, 0.20, 0.04])
btn_reset = Button(ax_reset, 'Reset')

def update_params(val):
    global is_updating
    state.A1, state.phi1, state.w1 = s_A1.val, s_phi1.val, s_w1.val
    state.A2, state.phi2, state.w2 = s_A2.val, s_phi2.val, s_w2.val

    recompute_curves()

    if not is_updating:
        is_updating = True
        scenarios.set_active(0)
        is_updating = False

s_A1.on_changed(update_params)
s_phi1.on_changed(update_params)
s_w1.on_changed(update_params)
s_A2.on_changed(update_params)
s_phi2.on_changed(update_params)
s_w2.on_changed(update_params)

def update_scenario(label):
    global is_updating
    is_updating = True 
    
    if label == 'Mesma Fase':
        s_A1.set_val(1.5); s_phi1.set_val(0.0); s_w1.set_val(1.0)
        s_A2.set_val(1.5); s_phi2.set_val(0.0); s_w2.set_val(1.0)
    elif label == 'Fases Opostas':
        s_A1.set_val(1.5); s_phi1.set_val(0.0); s_w1.set_val(1.0)
        s_A2.set_val(1.5); s_phi2.set_val(np.pi); s_w2.set_val(1.0)
    elif label == 'Batimentos (w diff)':
        s_A1.set_val(1.5); s_phi1.set_val(0.0); s_w1.set_val(1.2)
        s_A2.set_val(1.5); s_phi2.set_val(0.0); s_w2.set_val(1.0)
    elif label == 'Variável':
        s_A1.set_val(1.2); s_phi1.set_val(np.pi/4); s_w1.set_val(1.0)
        s_A2.set_val(0.8); s_phi2.set_val(3*np.pi/4); s_w2.set_val(1.0)
        
    is_updating = False
    recompute_curves()
    fig.canvas.draw_idle()

scenarios.on_clicked(update_scenario)

def toggle_pause(event):
    global is_paused
    if is_paused:
        ani.resume()
        btn_pause.label.set_text('Pausar')
    else:
        ani.pause()
        btn_pause.label.set_text('Retomar')
    is_paused = not is_paused
    fig.canvas.draw_idle()

btn_pause.on_clicked(toggle_pause)


def reset_simulation(event):
    global is_updating, is_paused

    is_updating = True

    s_A1.set_val(INITIALS["A1"])
    s_phi1.set_val(INITIALS["phi1"])
    s_w1.set_val(INITIALS["w1"])
    s_A2.set_val(INITIALS["A2"])
    s_phi2.set_val(INITIALS["phi2"])
    s_w2.set_val(INITIALS["w2"])

    state.anim_time = INITIALS["anim_time"]
    scenarios.set_active(4)

    if is_paused:
        ani.resume()
        is_paused = False
        btn_pause.label.set_text('Pausar')

    is_updating = False
    recompute_curves()
    fig.canvas.draw_idle()

btn_reset.on_clicked(reset_simulation)


def animate(frame):
    f1 = state.A1 * np.exp(1j * (state.w1 * state.anim_time + state.phi1))
    f2 = state.A2 * np.exp(1j * (state.w2 * state.anim_time + state.phi2))
    f_res = f1 + f2

    line1.set_data([0, f1.real], [0, f1.imag])
    line2.set_data([f1.real, f_res.real], [f1.imag, f_res.imag])
    line_res.set_data([0, f_res.real], [0, f_res.imag])
    line2_ref.set_data([0, f2.real], [0, f2.imag])

    dot1.set_data([f1.real], [f1.imag])
    dot_res.set_data([f_res.real], [f_res.imag])
    dot2.set_data([f2.real], [f2.imag])

    delta_phi = (state.phi2 - state.phi1) % (2*np.pi)
    delta_phi_deg = np.degrees(delta_phi)

    texto_info = (
        f"Fasor 1 (Azul):\n"
        f"  A: {state.A1:.2f} m | phi: {state.phi1:.2f} rad ({np.degrees(state.phi1):.1f}°) | w: {state.w1:.1f}\n"
        f"Fasor 2 (Vermelho):\n"
        f"  A: {state.A2:.2f} m | phi: {state.phi2:.2f} rad ({np.degrees(state.phi2):.1f}°) | w: {state.w2:.1f}\n"
        f"RESULTANTE (Preto):\n"
        f"  Amp Inst.: {np.abs(f_res):.2f} m | Fase Inst.: {np.angle(f_res):.2f} rad ({np.degrees(np.angle(f_res)):.1f}°)\n"
        f"Δphi: {delta_phi:.2f} rad ({delta_phi_deg:.1f}°)"
    )
    info_box.set_text(texto_info)
    
    phi_res = np.angle(f_res)

    if np.isclose(state.w1, state.w2, atol=1e-9):
        texto_resultado = (
            f"$y_{{res}}(t)$ mantém a mesma frequência angular, pois "
            f"$\\omega_1 = \\omega_2 = {state.w1:.1f}$ rad/s"
        )
    else:
        texto_resultado = (
            f"$y_{{res}}(t)$ apresenta batimentos, pois "
            f"$\\omega_1 \\neq \\omega_2$"
        )

    texto_eq = (
        "Equações no Tempo:\n"
        f"$y_1(t) = {state.A1:.2f} \\cos({state.w1:.1f}t {'+' if state.phi1 >= 0 else '-'} {abs(state.phi1):.2f})$\n"
        f"$y_2(t) = {state.A2:.2f} \\cos({state.w2:.1f}t {'+' if state.phi2 >= 0 else '-'} {abs(state.phi2):.2f})$\n"
        f"{texto_resultado}"
    )
    eq_box.set_text(texto_eq)

    t_now = state.anim_time % 20
    y1_now = state.A1 * np.cos(state.w1 * t_now + state.phi1)
    y2_now = state.A2 * np.cos(state.w2 * t_now + state.phi2)
    yres_now = y1_now + y2_now

    wave1_dot.set_data([t_now], [y1_now])
    wave2_dot.set_data([t_now], [y2_now])
    wave_res_dot.set_data([t_now], [yres_now])

    state.anim_time += 0.02

    return (line1, line2, line2_ref, line_res, dot1, dot2, dot_res,
        wave1_line, wave2_line, wave_res_line,
        wave1_dot, wave2_dot, wave_res_dot, info_box, eq_box)

ani = FuncAnimation(fig, animate, blit=True, interval=25, cache_frame_data=False)

plt.show()
