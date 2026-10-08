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

# Dataset
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

# metodo de identificacao
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

# Grafico identificacao
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
