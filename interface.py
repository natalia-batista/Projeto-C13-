import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

_plt_show_original = plt.show
plt.show = lambda *args, **kwargs: None

plt.show = _plt_show_original
plt.close('all')

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

tempo_dados_interface = dados['t'].squeeze()
tempo_pid_interface = np.linspace(0, 400, 1000)

melhor_identificacao = 'Smith' if rmse_smith <= rmse_sundaresan else 'Sundaresan'
identificacao_ativa = {'metodo': melhor_identificacao}
figura_atual = {'fig': None}


def obter_identificacao(metodo):
    if metodo == 'Smith':
        return K, tau, theta, rmse_smith, saida_smith
    return K, tau_sun, theta_sun, rmse_sundaresan, saida_sundaresan


def obter_identificacao_ativa():
    return obter_identificacao(identificacao_ativa['metodo'])


root = tk.Tk()
root.title('Pneumático - Controle PID')
root.geometry('1180x760')
root.minsize(1000, 680)

style = ttk.Style(root)
try:
    style.theme_use('vista')
except tk.TclError:
    pass

container = ttk.Frame(root, padding=10)
container.pack(fill='both', expand=True)

cabecalho = ttk.Label(
    container,
    text='Projeto Pratico C13 - Sistemas Embarcados | Grupo 4 - Cilindro Pneumatico',
    font=('Segoe UI', 14, 'bold')
)
cabecalho.pack(anchor='w', pady=(0, 8))

abas = ttk.Notebook(container)
abas.pack(fill='both', expand=True)

aba_identificacao = ttk.Frame(abas, padding=10)
aba_controle = ttk.Frame(abas, padding=10)

abas.add(aba_identificacao, text='Identificacao')
abas.add(aba_controle, text='Controle PID', state='disabled')

painel_id = ttk.Frame(aba_identificacao)
painel_id.pack(side='left', fill='y', padx=(0, 12))

painel_grafico_id = ttk.Frame(aba_identificacao)
painel_grafico_id.pack(side='right', fill='both', expand=True)

frame_dataset = ttk.LabelFrame(painel_id, text='Conjunto de dados', padding=10)
frame_dataset.pack(fill='x', pady=(0, 10))

ttk.Label(frame_dataset, text='Dataset:').grid(row=0, column=0, sticky='w', padx=(0, 8), pady=4)
var_dataset = tk.StringVar(value='Pneumatico_G4.mat')
entry_dataset = ttk.Entry(frame_dataset, textvariable=var_dataset, state='readonly', width=26)
entry_dataset.grid(row=0, column=1, sticky='ew', pady=4)

ttk.Label(frame_dataset, text='Menor RMSE:').grid(row=1, column=0, sticky='w', padx=(0, 8), pady=4)
ttk.Label(frame_dataset, text=melhor_identificacao, font=('Segoe UI', 9, 'bold')).grid(
    row=1, column=1, sticky='w', pady=4
)

frame_metodo_id = ttk.LabelFrame(painel_id, text='Identificacao da planta', padding=10)
frame_metodo_id.pack(fill='x', pady=(0, 10))

var_metodo_id = tk.StringVar(value=melhor_identificacao)
combo_metodo_id = ttk.Combobox(
    frame_metodo_id,
    textvariable=var_metodo_id,
    values=['Smith', 'Sundaresan'],
    state='readonly',
    width=22
)
combo_metodo_id.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 8))

var_k_id = tk.StringVar()
var_tau_id = tk.StringVar()
var_theta_id = tk.StringVar()
var_rmse_id = tk.StringVar()

campos_id = [
    ('K:', var_k_id),
    ('Tau:', var_tau_id),
    ('Theta:', var_theta_id),
    ('RMSE:', var_rmse_id),
]

for linha, (rotulo, variavel) in enumerate(campos_id, start=1):
    ttk.Label(frame_metodo_id, text=rotulo).grid(row=linha, column=0, sticky='w', padx=(0, 8), pady=3)
    ttk.Entry(frame_metodo_id, textvariable=variavel, state='readonly', width=18).grid(
        row=linha, column=1, sticky='ew', pady=3
    )

botao_usar_id = ttk.Button(frame_metodo_id, text='Selecionar identificacao')
botao_usar_id.grid(row=5, column=0, columnspan=2, sticky='ew', pady=(10, 0))

fig_id = Figure(figsize=(7.2, 5.2), dpi=100)
ax_id = fig_id.add_subplot(111)
canvas_id = FigureCanvasTkAgg(fig_id, master=painel_grafico_id)
canvas_id.get_tk_widget().pack(fill='both', expand=True)
toolbar_id = NavigationToolbar2Tk(canvas_id, painel_grafico_id, pack_toolbar=False)
toolbar_id.update()
toolbar_id.pack(fill='x')


def atualizar_identificacao(*_):
    metodo = var_metodo_id.get()
    k_sel, tau_sel, theta_sel, rmse_sel, saida_sel = obter_identificacao(metodo)

    var_k_id.set(f'{float(k_sel):.6f}')
    var_tau_id.set(f'{float(tau_sel):.6f}')
    var_theta_id.set(f'{float(theta_sel):.6f}')
    var_rmse_id.set(f'{float(rmse_sel):.6f}')

    ax_id.clear()
    ax_id.plot(tempo_dados_interface, saida, label='Dados experimentais')
    ax_id.plot(tempo_dados_interface, saida_sel, label=metodo)
    ax_id.set_xlabel('Tempo (s)')
    ax_id.set_ylabel('Pressao (bar)')
    ax_id.set_title('Identificacao da planta')
    ax_id.grid()
    ax_id.legend()
    fig_id.tight_layout()
    canvas_id.draw_idle()


combo_metodo_id.bind('<<ComboboxSelected>>', atualizar_identificacao)

painel_pid = ttk.Frame(aba_controle)
painel_pid.pack(side='left', fill='y', padx=(0, 12))

painel_grafico_pid = ttk.Frame(aba_controle)
painel_grafico_pid.pack(side='right', fill='both', expand=True)

frame_sintonia = ttk.LabelFrame(painel_pid, text='Selecao de sintonia', padding=10)
frame_sintonia.pack(fill='x', pady=(0, 10))

var_modo = tk.StringVar(value='Metodo')
radio_metodo = ttk.Radiobutton(frame_sintonia, text='Metodo', variable=var_modo, value='Metodo')
radio_manual = ttk.Radiobutton(frame_sintonia, text='Manual', variable=var_modo, value='Manual')
radio_metodo.grid(row=0, column=0, sticky='w', padx=(0, 12))
radio_manual.grid(row=0, column=1, sticky='w')

var_metodo_pid = tk.StringVar(value='IMC')
combo_metodo_pid = ttk.Combobox(
    frame_sintonia,
    textvariable=var_metodo_pid,
    values=['IMC', 'CHR sem sobrevalor'],
    state='readonly',
    width=22
)
combo_metodo_pid.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(8, 0))

frame_pid = ttk.LabelFrame(painel_pid, text='Parametros PID', padding=10)
frame_pid.pack(fill='x', pady=(0, 10))

var_kp = tk.StringVar()
var_ti = tk.StringVar()
var_td = tk.StringVar()
var_lambda = tk.StringVar(value=str(float(lamb)))

entries_pid = {}
for linha, (rotulo, variavel, chave) in enumerate([
    ('Kp:', var_kp, 'kp'),
    ('Ti:', var_ti, 'ti'),
    ('Td:', var_td, 'td'),
    ('Lambda:', var_lambda, 'lambda'),
]):
    ttk.Label(frame_pid, text=rotulo).grid(row=linha, column=0, sticky='w', padx=(0, 8), pady=3)
    entry = ttk.Entry(frame_pid, textvariable=variavel, width=18)
    entry.grid(row=linha, column=1, sticky='ew', pady=3)
    entries_pid[chave] = entry

botao_limpar = ttk.Button(frame_pid, text='Limpar parametros')
botao_limpar.grid(row=4, column=0, columnspan=2, sticky='ew', pady=(8, 0))

frame_controle = ttk.LabelFrame(painel_pid, text='Parametros de controle', padding=10)
frame_controle.pack(fill='x', pady=(0, 10))

var_setpoint = tk.StringVar(value=str(float(setpoint)))
var_tr = tk.StringVar()
var_ts = tk.StringVar()
var_mp = tk.StringVar()

for linha, (rotulo, variavel, readonly) in enumerate([
    ('SetPoint:', var_setpoint, False),
    ('tr (s):', var_tr, True),
    ('ts (s):', var_ts, True),
    ('mp (%):', var_mp, True),
]):
    ttk.Label(frame_controle, text=rotulo).grid(row=linha, column=0, sticky='w', padx=(0, 8), pady=3)
    estado = 'readonly' if readonly else 'normal'
    ttk.Entry(frame_controle, textvariable=variavel, state=estado, width=18).grid(
        row=linha, column=1, sticky='ew', pady=3
    )

var_marcar_tr = tk.BooleanVar(value=False)
var_marcar_ts = tk.BooleanVar(value=False)
var_marcar_mp = tk.BooleanVar(value=False)

ttk.Checkbutton(frame_controle, text='Marcar tr', variable=var_marcar_tr).grid(row=4, column=0, sticky='w', pady=(6, 0))
ttk.Checkbutton(frame_controle, text='Marcar ts', variable=var_marcar_ts).grid(row=4, column=1, sticky='w', pady=(6, 0))
ttk.Checkbutton(frame_controle, text='Marcar mp', variable=var_marcar_mp).grid(row=5, column=0, sticky='w')

frame_botoes = ttk.Frame(painel_pid)
frame_botoes.pack(fill='x')

botao_sintonizar = ttk.Button(frame_botoes, text='Sintonizar')
botao_exportar = ttk.Button(frame_botoes, text='Exportar')
botao_sintonizar.pack(side='left', fill='x', expand=True, padx=(0, 4))
botao_exportar.pack(side='left', fill='x', expand=True, padx=(4, 0))

var_status = tk.StringVar(value='')
label_status = ttk.Label(painel_pid, textvariable=var_status, wraplength=280)
label_status.pack(fill='x', pady=(8, 0))

fig_pid = Figure(figsize=(7.2, 5.2), dpi=100)
ax_pid = fig_pid.add_subplot(111)
canvas_pid = FigureCanvasTkAgg(fig_pid, master=painel_grafico_pid)
canvas_pid.get_tk_widget().pack(fill='both', expand=True)
toolbar_pid = NavigationToolbar2Tk(canvas_pid, painel_grafico_pid, pack_toolbar=False)
toolbar_pid.update()
toolbar_pid.pack(fill='x')

def parametros_metodo_interface():
    k_sel, tau_sel, theta_sel, _, _ = obter_identificacao_ativa()

    if var_metodo_pid.get() == 'IMC':
        lamb_interface = float(var_lambda.get())
        kp = (2*tau_sel + theta_sel)/(k_sel * (2*lamb_interface + theta_sel))
        ti = tau_sel + theta_sel/2
        td = (tau_sel * theta_sel)/(2*tau_sel + theta_sel)
    else:
        kp = 0.6*theta_sel / (k_sel * theta_sel)
        ti = theta_sel
        td = theta_sel/2

    return float(kp), float(ti), float(td)


def escrever_parametros(kp, ti, td):
    var_kp.set(str(kp))
    var_ti.set(str(ti))
    var_td.set(str(td))


def atualizar_campos_sintonia(*_):
    if var_modo.get() == 'Metodo':
        combo_metodo_pid.configure(state='readonly')
        entries_pid['kp'].configure(state='readonly')
        entries_pid['ti'].configure(state='readonly')
        entries_pid['td'].configure(state='readonly')
        botao_limpar.configure(state='disabled')

        if var_metodo_pid.get() == 'IMC':
            entries_pid['lambda'].configure(state='normal')
        else:
            entries_pid['lambda'].configure(state='disabled')

        try:
            kp, ti, td = parametros_metodo_interface()
            escrever_parametros(kp, ti, td)
        except ValueError:
            pass
    else:
        combo_metodo_pid.configure(state='disabled')
        entries_pid['lambda'].configure(state='disabled')
        entries_pid['kp'].configure(state='normal')
        entries_pid['ti'].configure(state='normal')
        entries_pid['td'].configure(state='normal')
        botao_limpar.configure(state='normal')


def selecionar_identificacao():
    identificacao_ativa['metodo'] = var_metodo_id.get()
    abas.tab(1, state='normal')
    atualizar_campos_sintonia()
    var_status.set(f"Identificacao selecionada: {identificacao_ativa['metodo']}")
    abas.select(1)


def limpar_parametros():
    if var_modo.get() == 'Manual':
        var_kp.set('')
        var_ti.set('')
        var_td.set('')


def montar_planta_interface(k_sel, tau_sel, theta_sel):
    G_interface = ct.tf([k_sel], [tau_sel, 1])
    num_delay_interface, den_delay_interface = ct.pade(theta_sel, 1)
    Delay_interface = ct.tf(num_delay_interface, den_delay_interface)
    H_interface = G_interface * Delay_interface
    return H_interface


def montar_controlador_interface(kp, ti, td, planta):
    numKp_interface = np.array([kp])
    denKp_interface = np.array([1])
    HKp_interface = ct.tf(numKp_interface, denKp_interface)

    numKi_interface = np.array([kp])
    denKi_interface = np.array([ti,0])
    HKi_interface = ct.tf(numKi_interface, denKi_interface)

    numKd_interface = np.array([kp*td,0])
    denKd_interface = np.array([1])
    HKd_interface = ct.tf(numKd_interface, denKd_interface)

    Hctrl1_interface = ct.parallel(HKp_interface, HKi_interface)
    Hctrl_interface = ct.parallel(Hctrl1_interface, HKd_interface)

    Hdel_interface = ct.series(planta, Hctrl_interface)
    Hcl_interface = ct.feedback(Hdel_interface, 1)
    return Hcl_interface

