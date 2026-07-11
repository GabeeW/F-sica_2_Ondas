import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, RadioButtons, Button

fig, (ax_phasor, ax_time, ax_space) = plt.subplots(1, 3, figsize=(16, 8))
plt.subplots_adjust(left=0.04, bottom=0.48, right=0.98, top=0.90, wspace=0.25)
fig.suptitle("Simulador Completo de Interferência de Ondas", fontsize=18, fontweight='bold')

class WaveState:
    def __init__(self):
        self.A1, self.phi1, self.w1 = 1.2, np.pi/4, 1.0
        self.A2, self.phi2, self.w2 = 0.8, 3*np.pi/4, 1.0
        self.anim_time = 0.0

state = WaveState()
t_array = np.linspace(0, 20, 1000)
x_array = np.linspace(0, 20, 1000)

is_updating = False 
is_paused = False

INITIALS = {
    "A1": 1.2, "phi1": np.pi/4, "w1": 1.0,
    "A2": 0.8, "phi2": 3*np.pi/4, "w2": 1.0,
    "anim_time": 0.0
}

ax_phasor.set_title("1. Diagrama de Fasores", fontsize=13)
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
    -3.95, 3.9, '', fontsize=8.5, verticalalignment='top',
    bbox=dict(facecolor='white', edgecolor='gray', alpha=0.85, boxstyle='round,pad=0.35')
)
ax_phasor.legend(loc='lower right', fontsize=8)

ax_time.set_title("2. Ondas no Tempo y(t) em x=0", fontsize=13)
ax_time.set_xlim(0, 20)
ax_time.set_ylim(-4, 4)
ax_time.set_xlabel("Tempo (s)")
ax_time.set_ylabel("Amplitude")
ax_time.grid(True, linestyle='--')

time_line1, = ax_time.plot([], [], 'b-', alpha=0.6, label='Onda 1')
time_line2, = ax_time.plot([], [], 'r-', alpha=0.6, label='Onda 2')
time_res, = ax_time.plot([], [], 'k-', lw=2, label='Resultante')
time_dot1, = ax_time.plot([], [], 'bo', ms=7)
time_dot2, = ax_time.plot([], [], 'ro', ms=7)
time_dotres, = ax_time.plot([], [], 'ko', ms=7)
ax_time.legend(loc='upper right', fontsize=8)

eq_time_box = ax_time.text(
    0.03, 0.95, '', transform=ax_time.transAxes, fontsize=9.5, verticalalignment='top', 
    bbox=dict(facecolor='lightyellow', edgecolor='orange', alpha=0.9, boxstyle='round,pad=0.4')
)

ax_space.set_title("3. Ondas no Espaço y(x) propagando", fontsize=13)
ax_space.set_xlim(0, 20)
ax_space.set_ylim(-4, 4)
ax_space.set_xlabel("Posição Espacial x (m)")
ax_space.grid(True, linestyle='--')

space_line1, = ax_space.plot([], [], 'b-', alpha=0.6, label='Onda 1')
space_line2, = ax_space.plot([], [], 'r-', alpha=0.6, label='Onda 2')
space_res, = ax_space.plot([], [], 'k-', lw=2, label='Resultante')
space_dot1, = ax_space.plot([], [], 'bo', ms=7)
space_dot2, = ax_space.plot([], [], 'ro', ms=7)
space_dotres, = ax_space.plot([], [], 'ko', ms=7)
ax_space.legend(loc='upper right', fontsize=8)

eq_space_box = ax_space.text(
    0.03, 0.95, '', transform=ax_space.transAxes, fontsize=9.5, verticalalignment='top', 
    bbox=dict(facecolor='lightcyan', edgecolor='teal', alpha=0.9, boxstyle='round,pad=0.4')
)


ax_A1 = plt.axes([0.08, 0.28, 0.22, 0.02], facecolor='lightcyan')
ax_phi1 = plt.axes([0.08, 0.20, 0.22, 0.02], facecolor='lightcyan')
ax_w1 = plt.axes([0.08, 0.12, 0.22, 0.02], facecolor='lightcyan')

ax_A2 = plt.axes([0.42, 0.28, 0.22, 0.02], facecolor='mistyrose')
ax_phi2 = plt.axes([0.42, 0.20, 0.22, 0.02], facecolor='mistyrose')
ax_w2 = plt.axes([0.42, 0.12, 0.22, 0.02], facecolor='mistyrose')

s_A1 = Slider(ax_A1, 'A1 (m)', 0.0, 2.0, valinit=state.A1, valstep=0.01)
s_phi1 = Slider(ax_phi1, 'phi1 (rad)', 0.0, 2*np.pi, valinit=state.phi1, valstep=0.01)
s_w1 = Slider(ax_w1, 'w1 (rad/s)', -3.0, 3.0, valinit=state.w1, valstep=0.1)

s_A2 = Slider(ax_A2, 'A2 (m)', 0.0, 2.0, valinit=state.A2, valstep=0.01)
s_phi2 = Slider(ax_phi2, 'phi2 (rad)', 0.0, 2*np.pi, valinit=state.phi2, valstep=0.01)
s_w2 = Slider(ax_w2, 'w2 (rad/s)', -3.0, 3.0, valinit=state.w2, valstep=0.1)

ax_scenarios = plt.axes([0.72, 0.12, 0.15, 0.18], facecolor='whitesmoke')
opcoes = ('Cenário Atual', 'Mesma Fase', 'Fases Opostas', 'Batimentos', 'Ondas Estacionárias', 'Variável')
scenarios = RadioButtons(ax_scenarios, opcoes, active=5)

ax_pause = plt.axes([0.89, 0.22, 0.08, 0.05])
btn_pause = Button(ax_pause, 'Pausar')

ax_reset = plt.axes([0.89, 0.14, 0.08, 0.05])
btn_reset = Button(ax_reset, 'Reset')

def update_plots():
    t_now = state.anim_time
    k = 1.0

    f1 = state.A1 * np.exp(1j * (state.w1 * t_now + state.phi1))
    f2 = state.A2 * np.exp(1j * (state.w2 * t_now + state.phi2))
    f_res = f1 + f2

    line1.set_data([0, f1.real], [0, f1.imag])
    line2.set_data([f1.real, f_res.real], [f1.imag, f_res.imag])
    line_res.set_data([0, f_res.real], [0, f_res.imag])
    line2_ref.set_data([0, f2.real], [0, f2.imag])

    dot1.set_data([f1.real], [f1.imag])
    dot_res.set_data([f_res.real], [f_res.imag])
    dot2.set_data([f2.real], [f2.imag])

    y1_time = state.A1 * np.cos(state.w1 * t_array + state.phi1)
    y2_time = state.A2 * np.cos(state.w2 * t_array + state.phi2)
    yres_time = y1_time + y2_time

    time_line1.set_data(t_array, y1_time)
    time_line2.set_data(t_array, y2_time)
    time_res.set_data(t_array, yres_time)

    t_dot_x = t_now % 20
    time_dot1.set_data([t_dot_x], [state.A1 * np.cos(state.w1 * t_dot_x + state.phi1)])
    time_dot2.set_data([t_dot_x], [state.A2 * np.cos(state.w2 * t_dot_x + state.phi2)])
    time_dotres.set_data([t_dot_x], [state.A1 * np.cos(state.w1 * t_dot_x + state.phi1) + state.A2 * np.cos(state.w2 * t_dot_x + state.phi2)])

    y1_space = state.A1 * np.cos(state.w1 * t_now - k * x_array + state.phi1)
    y2_space = state.A2 * np.cos(state.w2 * t_now - k * x_array + state.phi2)
    yres_space = y1_space + y2_space

    space_line1.set_data(x_array, y1_space)
    space_line2.set_data(x_array, y2_space)
    space_res.set_data(x_array, yres_space)

    space_dot1.set_data([0], [y1_space[0]])
    space_dot2.set_data([0], [y2_space[0]])
    space_dotres.set_data([0], [yres_space[0]])

    delta_phi = (state.phi2 - state.phi1) % (2*np.pi)
    info_box.set_text(
        f"Fasor 1 (Azul): A={state.A1:.2f} | w={state.w1:.1f}\n"
        f"Fasor 2 (Vermelho): A={state.A2:.2f} | w={state.w2:.1f}\n"
        f"RESULTANTE: A={np.abs(f_res):.2f} | Fase={np.angle(f_res):.2f} rad\n"
        f"Δphi: {delta_phi:.2f} rad ({np.degrees(delta_phi):.1f}°)"
    )

    eq_time_box.set_text(
        "Modelagem no Tempo $y(t)$:\n"
        f"$y_1(t) = {state.A1:.2f} \\cos({state.w1:.1f}t {'+' if state.phi1 >= 0 else '-'} {abs(state.phi1):.2f})$\n"
        f"$y_2(t) = {state.A2:.2f} \\cos({state.w2:.1f}t {'+' if state.phi2 >= 0 else '-'} {abs(state.phi2):.2f})$"
    )

    eq_space_box.set_text(
        "Modelagem no Espaço $y(x, t)$:\n"
        f"$y_1(x,t) = {state.A1:.2f} \\cos({abs(state.w1):.1f}t {'-' if state.w1 >= 0 else '+'} {k:.1f}x {'+' if state.phi1 >= 0 else '-'} {abs(state.phi1):.2f})$\n"
        f"$y_2(x,t) = {state.A2:.2f} \\cos({abs(state.w2):.1f}t {'-' if state.w2 >= 0 else '+'} {k:.1f}x {'+' if state.phi2 >= 0 else '-'} {abs(state.phi2):.2f})$"
    )

    return (line1, line2, line2_ref, line_res, dot1, dot2, dot_res,
            time_line1, time_line2, time_res, time_dot1, time_dot2, time_dotres,
            space_line1, space_line2, space_res, space_dot1, space_dot2, space_dotres,
            info_box, eq_time_box, eq_space_box)

def update_params(val):
    global is_updating
    state.A1, state.phi1, state.w1 = s_A1.val, s_phi1.val, s_w1.val
    state.A2, state.phi2, state.w2 = s_A2.val, s_phi2.val, s_w2.val

    if not is_updating:
        is_updating = True
        scenarios.set_active(0)
        is_updating = False
        
    update_plots()
    fig.canvas.draw_idle()

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
    elif label == 'Batimentos':
        s_A1.set_val(1.5); s_phi1.set_val(0.0); s_w1.set_val(1.2)
        s_A2.set_val(1.5); s_phi2.set_val(0.0); s_w2.set_val(1.0)
    elif label == 'Ondas Estacionárias':
        s_A1.set_val(1.5); s_phi1.set_val(0.0); s_w1.set_val(1.5)
        s_A2.set_val(1.5); s_phi2.set_val(0.0); s_w2.set_val(-1.5)
    elif label == 'Variável':
        s_A1.set_val(1.2); s_phi1.set_val(np.pi/4); s_w1.set_val(1.0)
        s_A2.set_val(0.8); s_phi2.set_val(3*np.pi/4); s_w2.set_val(1.0)
        
    is_updating = False
    update_plots()
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
    scenarios.set_active(5)

    if is_paused:
        ani.resume()
        is_paused = False
        btn_pause.label.set_text('Pausar')

    is_updating = False
    update_plots()
    fig.canvas.draw_idle()

btn_reset.on_clicked(reset_simulation)

def animate(frame):
    artists = update_plots()
    state.anim_time += 0.05
    return artists

ani = FuncAnimation(fig, animate, blit=True, interval=25, cache_frame_data=False)
plt.show()