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
