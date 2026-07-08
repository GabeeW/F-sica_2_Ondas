import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, RadioButtons

fig, (ax_phasor, ax_wave) = plt.subplots(1, 2, figsize=(12, 8))
plt.subplots_adjust(left=0.08, bottom=0.45, right=0.95, top=0.92, wspace=0.25)
fig.suptitle("Simulador de Interferência de Ondas com Fasores", fontsize=18, fontweight='bold')

class WaveState:
    def __init__(self):
        self.A1, self.phi1 = 1.2, np.pi/4
        self.A2, self.phi2 = 0.8, 3*np.pi/4
        self.omega = 1.0
        self.anim_time = 0.0

state = WaveState()
time_array = np.linspace(0, 20, 1000)

is_updating = False 

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

dot1, = ax_phasor.plot([], [], 'bo')
dot_res, = ax_phasor.plot([], [], 'ko')

info_box = ax_phasor.text(
    -3.85, 3.85, '',
    fontsize=10, 
    verticalalignment='top', 
    bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9, boxstyle='round,pad=0.5')
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

def recompute_curves():
    y1 = state.A1 * np.cos(state.omega * time_array + state.phi1)
    y2 = state.A2 * np.cos(state.omega * time_array + state.phi2)
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
    "O diagrama de fasores (esquerda) ilustra a soma vetorial de duas ondas no tempo em um único ponto espacial.\n"
    "Cada onda é representada por um vetor que gira. O comprimento do vetor é a Amplitude (A) e o ângulo inicial é a Fase (phi).\n"
    "Se as ondas tiverem fases opostas (diferença de pi), os vetores se anulam no centro, causando a interferência destrutiva vista no quadro."
)

fig.text(0.5, 0.36, texto_explicativo, ha='center', va='center', fontsize=11, wrap=True, 
         bbox=dict(boxstyle='round,pad=0.6', facecolor='wheat', edgecolor='tan', alpha=0.5))

ax_A1 = plt.axes([0.10, 0.22, 0.35, 0.03], facecolor='lightcyan')
ax_phi1 = plt.axes([0.10, 0.17, 0.35, 0.03], facecolor='lightcyan')
ax_A2 = plt.axes([0.10, 0.10, 0.35, 0.03], facecolor='mistyrose')
ax_phi2 = plt.axes([0.10, 0.05, 0.35, 0.03], facecolor='mistyrose')

s_A1 = Slider(ax_A1, 'A1 (m)', 0.0, 2.0, valinit=state.A1, valstep=0.01)
s_phi1 = Slider(ax_phi1, 'phi1 (rad)', 0.0, 2*np.pi, valinit=state.phi1, valstep=0.01)
s_A2 = Slider(ax_A2, 'A2 (m)', 0.0, 2.0, valinit=state.A2, valstep=0.01)
s_phi2 = Slider(ax_phi2, 'phi2 (rad)', 0.0, 2*np.pi, valinit=state.phi2, valstep=0.01)

ax_scenarios = plt.axes([0.55, 0.05, 0.35, 0.20], facecolor='whitesmoke')
opcoes = ('Cenário Atual', 'Mesma Direção e Fase', 'Mesma Direção e Fases Opostas (Quadro)', 'Variável')
scenarios = RadioButtons(ax_scenarios, opcoes, active=3)

def update_params(val):
    global is_updating
    state.A1, state.phi1 = s_A1.val, s_phi1.val
    state.A2, state.phi2 = s_A2.val, s_phi2.val

    recompute_curves()

    if not is_updating:
        is_updating = True
        scenarios.set_active(0)
        is_updating = False

s_A1.on_changed(update_params)
s_phi1.on_changed(update_params)
s_A2.on_changed(update_params)
s_phi2.on_changed(update_params)

def update_scenario(label):
    global is_updating
    is_updating = True 
    
    if label == 'Mesma Direção e Fase':
        s_A1.set_val(1.2)
        s_phi1.set_val(0.0)
        s_A2.set_val(1.2)
        s_phi2.set_val(0.0)
    elif label == 'Mesma Direção e Fases Opostas (Quadro)':
        s_A1.set_val(1.5)
        s_phi1.set_val(0.0)
        s_A2.set_val(1.5)
        s_phi2.set_val(np.pi)
    elif label == 'Variável':
        s_A1.set_val(1.2)
        s_phi1.set_val(np.pi/4)
        s_A2.set_val(0.8)
        s_phi2.set_val(3*np.pi/4)
        
    is_updating = False
    recompute_curves()
    fig.canvas.draw_idle()

scenarios.on_clicked(update_scenario)


def animate(frame):
    f1 = state.A1 * np.exp(1j * (state.omega * state.anim_time + state.phi1))
    f2 = state.A2 * np.exp(1j * (state.omega * state.anim_time + state.phi2))
    f_res = f1 + f2

    line1.set_data([0, f1.real], [0, f1.imag])
    line2.set_data([f1.real, f_res.real], [f1.imag, f_res.imag])
    line_res.set_data([0, f_res.real], [0, f_res.imag])

    dot1.set_data([f1.real], [f1.imag])
    dot_res.set_data([f_res.real], [f_res.imag])

    texto_info = (
        f"Fasor 1 (Azul):\n  Amp: {state.A1:.2f}m | Fase: {state.phi1:.2f} rad\n\n"
        f"Fasor 2 (Vermelho):\n  Amp: {state.A2:.2f}m | Fase: {state.phi2:.2f} rad\n\n"
        f"RESULTANTE (Preto):\n  Amp: {np.abs(f_res):.2f}m | Fase: {np.angle(f_res):.2f} rad"
    )
    info_box.set_text(texto_info)

    t_now = state.anim_time % 20
    y1_now = state.A1 * np.cos(state.omega * t_now + state.phi1)
    y2_now = state.A2 * np.cos(state.omega * t_now + state.phi2)
    yres_now = y1_now + y2_now

    wave1_dot.set_data([t_now], [y1_now])
    wave2_dot.set_data([t_now], [y2_now])
    wave_res_dot.set_data([t_now], [yres_now])

    state.anim_time += 0.02

    return (line1, line2, line_res, dot1, dot_res,
            wave1_line, wave2_line, wave_res_line,
            wave1_dot, wave2_dot, wave_res_dot, info_box)

ani = FuncAnimation(fig, animate, blit=True, interval=25, cache_frame_data=False)

plt.show()