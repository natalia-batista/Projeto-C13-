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
aba_comparacao = ttk.Frame(abas, padding=10)

abas.add(aba_identificacao, text='Identificacao')
abas.add(aba_controle, text='Controle PID', state='disabled')
abas.add(aba_comparacao, text='Compara\u00e7\u00e3o', state='disabled')

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

frame_modelo_id = ttk.LabelFrame(
    painel_id,
    text='Modelo FOPDT',
    padding=10
)
frame_modelo_id.pack(fill='x', pady=(0, 10))

# Figura usada somente para renderizar a formula matematica
fig_funcao_id = Figure(
    figsize=(3.0, 0.8),
    dpi=100
)

ax_funcao_id = fig_funcao_id.add_subplot(111)

ax_funcao_id.axis('off')

texto_funcao_id = ax_funcao_id.text(
    0.5,
    0.5,
    '',
    ha='center',
    va='center',
    fontsize=14
)

canvas_funcao_id = FigureCanvasTkAgg(
    fig_funcao_id,
    master=frame_modelo_id
)

canvas_funcao_id.get_tk_widget().pack(
    fill='x',
    expand=True
)

var_fator_id = tk.StringVar()

ttk.Label(
    frame_modelo_id,
    textvariable=var_fator_id
).pack(
    anchor='center',
    pady=(4, 0)
)

fig_id = Figure(figsize=(7.2, 5.2), dpi=100)

ax_id = fig_id.add_subplot(111)

canvas_id = FigureCanvasTkAgg(
    fig_id,
    master=painel_grafico_id
)

canvas_id.get_tk_widget().pack(
    fill='both',
    expand=True
)

toolbar_id = NavigationToolbar2Tk(
    canvas_id,
    painel_grafico_id,
    pack_toolbar=False
)

toolbar_id.update()
toolbar_id.pack(fill='x')

def atualizar_identificacao(*_):
    metodo = var_metodo_id.get()
    k_sel, tau_sel, theta_sel, rmse_sel, saida_sel = obter_identificacao(metodo)

    var_k_id.set(f'{float(k_sel):.6f}')
    var_tau_id.set(f'{float(tau_sel):.6f}')
    var_theta_id.set(f'{float(theta_sel):.6f}')
    var_rmse_id.set(f'{float(rmse_sel):.6f}')
    formula = (rf"$G(s)="rf"\frac{{{float(k_sel):.4f}}}"rf"{{{float(tau_sel):.4f}s+1}}"rf"e^{{-{float(theta_sel):.4f}s}}$")
    texto_funcao_id.set_text(formula)

    canvas_funcao_id.draw_idle()
    if float(tau_sel) != 0:
        var_fator_id.set(
            f'Fator theta/tau = {float(theta_sel / tau_sel):.4f}'
        )
    else:
        var_fator_id.set('Fator theta/tau = indefinido')

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

painel_grafico_comparacao = ttk.Frame(aba_comparacao)
painel_grafico_comparacao.pack(fill='both', expand=True)

fig_comparacao = Figure(figsize=(9.0, 4.0), dpi=100)
ax_comparacao = fig_comparacao.add_subplot(111)
canvas_comparacao = FigureCanvasTkAgg(fig_comparacao, master=painel_grafico_comparacao)
canvas_comparacao.get_tk_widget().pack(fill='both', expand=True)
toolbar_comparacao = NavigationToolbar2Tk(
    canvas_comparacao,
    painel_grafico_comparacao,
    pack_toolbar=False
)
toolbar_comparacao.update()
toolbar_comparacao.pack(fill='x')

frame_acoes_comparacao = ttk.Frame(aba_comparacao)
frame_acoes_comparacao.pack(fill='x', pady=(8, 8))

botao_comparar = ttk.Button(frame_acoes_comparacao, text='Comparar m\u00e9todos')
botao_comparar.pack(side='left')

var_status_comparacao = tk.StringVar(value='')
ttk.Label(
    frame_acoes_comparacao,
    textvariable=var_status_comparacao
).pack(side='left', padx=(12, 0))

frame_tabela_comparacao = ttk.LabelFrame(
    aba_comparacao,
    text='Par\u00e2metros e m\u00e9tricas',
    padding=8
)
frame_tabela_comparacao.pack(fill='x')

tabela_comparacao = ttk.Treeview(
    frame_tabela_comparacao,
    columns=('parametro', 'imc', 'chr'),
    show='headings',
    height=6
)
tabela_comparacao.heading('parametro', text='Par\u00e2metro')
tabela_comparacao.heading('imc', text='IMC')
tabela_comparacao.heading('chr', text='CHR sem sobrevalor')
tabela_comparacao.column('parametro', width=280, anchor='w')
tabela_comparacao.column('imc', width=180, anchor='center')
tabela_comparacao.column('chr', width=180, anchor='center')
tabela_comparacao.pack(fill='x')

linhas_comparacao = {}
for chave, rotulo in [
    ('kp', 'Kp'),
    ('ti', 'Ti (s)'),
    ('td', 'Td (s)'),
    ('tr', 'Tempo de subida tr (s)'),
    ('ts', 'Tempo de acomoda\u00e7\u00e3o ts (s)'),
    ('mp', 'Sobressinal Mp (%)'),
]:
    linhas_comparacao[chave] = tabela_comparacao.insert(
        '',
        'end',
        values=(rotulo, '', '')
    )

def parametros_metodo_interface():
    k_sel, tau_sel, theta_sel, _, _ = obter_identificacao_ativa()

    if var_metodo_pid.get() == 'IMC':
        lamb_interface = float(var_lambda.get())
        kp = (2*tau_sel + theta_sel)/(k_sel * (2*lamb_interface + theta_sel))
        ti = tau_sel + theta_sel/2
        td = (tau_sel * theta_sel)/(2*tau_sel + theta_sel)
    else:
        kp = 0.6*tau_sel / (k_sel * theta_sel)
        ti = tau_sel
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
    abas.tab(2, state='normal')
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


def comparar_metodos_interface():
    try:
        k_sel, tau_sel, theta_sel, _, _ = obter_identificacao_ativa()
        k_sel = float(k_sel)
        tau_sel = float(tau_sel)
        theta_sel = float(theta_sel)
        lamb_interface = float(var_lambda.get())
        setpoint_interface = float(var_setpoint.get())

        if not np.all(np.isfinite([k_sel, tau_sel, theta_sel])):
            raise ValueError('K, tau e theta devem ser valores finitos.')
        if k_sel == 0:
            raise ValueError('K deve ser diferente de zero.')
        if tau_sel <= 0:
            raise ValueError('Tau deve ser maior que zero.')
        if theta_sel <= 0:
            raise ValueError('Theta deve ser maior que zero.')
        if not np.isfinite(lamb_interface) or lamb_interface <= 0:
            raise ValueError('Lambda deve ser um valor finito e positivo.')
        if not np.isfinite(setpoint_interface):
            raise ValueError('SetPoint deve ser um valor finito.')

        denominador_imc_kp = k_sel * (2*lamb_interface + theta_sel)
        denominador_imc_td = 2*tau_sel + theta_sel
        denominador_chr_kp = k_sel * theta_sel
        if denominador_imc_kp == 0 or denominador_imc_td == 0:
            raise ValueError('Os parametros selecionados invalidam o calculo IMC.')
        if denominador_chr_kp == 0:
            raise ValueError('Os parametros selecionados invalidam o calculo CHR.')

        kp_imc = (2*tau_sel + theta_sel) / denominador_imc_kp
        ti_imc = tau_sel + theta_sel/2
        td_imc = (tau_sel * theta_sel) / denominador_imc_td

        kp_chr = 0.6*tau_sel / denominador_chr_kp
        ti_chr = tau_sel
        td_chr = theta_sel/2

        parametros_imc = [kp_imc, ti_imc, td_imc]
        parametros_chr = [kp_chr, ti_chr, td_chr]
        if not np.all(np.isfinite(parametros_imc)) or ti_imc <= 0:
            raise ValueError('Os parametros calculados para IMC sao invalidos.')
        if not np.all(np.isfinite(parametros_chr)) or ti_chr <= 0:
            raise ValueError('Os parametros calculados para CHR sao invalidos.')

        planta = montar_planta_interface(k_sel, tau_sel, theta_sel)
        controlador_imc = montar_controlador_interface(
            kp_imc,
            ti_imc,
            td_imc,
            planta
        )
        controlador_chr = montar_controlador_interface(
            kp_chr,
            ti_chr,
            td_chr,
            planta
        )

        tempo_imc, resposta_imc = ct.step_response(
            controlador_imc,
            tempo_pid_interface
        )
        tempo_chr, resposta_chr = ct.step_response(
            controlador_chr,
            tempo_pid_interface
        )
        resposta_imc *= setpoint_interface
        resposta_chr *= setpoint_interface

        metricas_imc = ct.step_info(controlador_imc)
        metricas_chr = ct.step_info(controlador_chr)

        resultado_imc = {
            'kp': kp_imc,
            'ti': ti_imc,
            'td': td_imc,
            'tr': float(metricas_imc['RiseTime']),
            'ts': float(metricas_imc['SettlingTime']),
            'mp': float(metricas_imc['Overshoot']),
        }
        resultado_chr = {
            'kp': kp_chr,
            'ti': ti_chr,
            'td': td_chr,
            'tr': float(metricas_chr['RiseTime']),
            'ts': float(metricas_chr['SettlingTime']),
            'mp': float(metricas_chr['Overshoot']),
        }

        if np.size(tempo_imc) == 0 or np.size(tempo_imc) != np.size(resposta_imc):
            raise ValueError('A simulacao IMC nao retornou uma resposta valida.')
        if np.size(tempo_chr) == 0 or np.size(tempo_chr) != np.size(resposta_chr):
            raise ValueError('A simulacao CHR nao retornou uma resposta valida.')
        if not np.all(np.isfinite(tempo_imc)) or not np.all(np.isfinite(resposta_imc)):
            raise ValueError('A simulacao IMC retornou valores invalidos.')
        if not np.all(np.isfinite(tempo_chr)) or not np.all(np.isfinite(resposta_chr)):
            raise ValueError('A simulacao CHR retornou valores invalidos.')
        if not np.all(np.isfinite(list(resultado_imc.values()))):
            raise ValueError('As metricas calculadas para IMC sao invalidas.')
        if not np.all(np.isfinite(list(resultado_chr.values()))):
            raise ValueError('As metricas calculadas para CHR sao invalidas.')

        ax_comparacao.clear()
        ax_comparacao.plot(
            tempo_chr,
            resposta_chr,
            label='CHR sem sobrevalor'
        )
        ax_comparacao.plot(
            tempo_imc,
            resposta_imc,
            label='IMC'
        )
        ax_comparacao.axhline(
            setpoint_interface,
            linestyle='--',
            label='SetPoint'
        )
        ax_comparacao.set_xlabel('Tempo (s)')
        ax_comparacao.set_ylabel('Press\u00e3o (bar)')
        ax_comparacao.set_title('Compara\u00e7\u00e3o dos m\u00e9todos de sintonia')
        ax_comparacao.grid()
        ax_comparacao.legend()
        fig_comparacao.tight_layout()
        canvas_comparacao.draw_idle()

        for chave in ('kp', 'ti', 'td', 'tr', 'ts', 'mp'):
            rotulo = tabela_comparacao.item(
                linhas_comparacao[chave],
                'values'
            )[0]
            tabela_comparacao.item(
                linhas_comparacao[chave],
                values=(
                    rotulo,
                    f"{float(resultado_imc[chave]):.6f}",
                    f"{float(resultado_chr[chave]):.6f}",
                )
            )

        var_status_comparacao.set(
            f"Compara\u00e7\u00e3o conclu\u00edda: {identificacao_ativa['metodo']}"
        )

    except ValueError as erro:
        messagebox.showerror(
            'Entrada inv\u00e1lida',
            str(erro)
        )
    except Exception as erro:
        messagebox.showerror('Erro', str(erro))


def sintonizar_interface():
    try:
        k_sel, tau_sel, theta_sel, _, _ = obter_identificacao_ativa()
        planta = montar_planta_interface(k_sel, tau_sel, theta_sel)

        if var_modo.get() == 'Metodo':
            kp, ti, td = parametros_metodo_interface()
            escrever_parametros(kp, ti, td)
        else:
            kp = float(var_kp.get())
            ti = float(var_ti.get())
            td = float(var_td.get())

        if ti == 0:
            messagebox.showerror('Parametros PID', 'Ti deve ser diferente de zero.')
            return

        Hcl_interface = montar_controlador_interface(kp, ti, td, planta)

        if var_modo.get() == 'Manual':
            polos = ct.poles(Hcl_interface)
            if np.any(np.real(polos) >= 0):
                messagebox.showerror('Controle PID', 'Sistema instavel para os parametros informados.')
                return

        setpoint_interface = float(var_setpoint.get())
        t_interface, y_interface = ct.step_response(Hcl_interface, tempo_pid_interface)
        y_interface *= setpoint_interface

        info_interface = ct.step_info(Hcl_interface)
        var_tr.set(f"{float(info_interface['RiseTime']):.6f}")
        var_ts.set(f"{float(info_interface['SettlingTime']):.6f}")
        var_mp.set(f"{float(info_interface['Overshoot']):.6f}")

        ax_pid.clear()
        ax_pid.plot(t_interface, y_interface, label='Resposta PID')
        ax_pid.axhline(setpoint_interface, linestyle='--', label='SetPoint')

        if var_marcar_tr.get():
            ax_pid.axvline(info_interface['RiseTime'], linestyle=':', label='tr')

        if var_marcar_ts.get():
            ax_pid.axvline(info_interface['SettlingTime'], linestyle=':', label='ts')

        if var_marcar_mp.get():
            indice_pico = int(np.argmax(y_interface))
            ax_pid.scatter(t_interface[indice_pico], y_interface[indice_pico], label='mp')

        ax_pid.set_xlabel('Tempo (s)')
        ax_pid.set_ylabel('Pressao (bar)')
        ax_pid.set_title('Controle PID')
        ax_pid.grid()
        ax_pid.legend()
        fig_pid.tight_layout()
        canvas_pid.draw_idle()

        figura_atual['fig'] = fig_pid
        var_status.set('Sintonia concluida.')

    except ValueError:
        messagebox.showerror('Entrada invalida', 'Preencha os campos numericos com valores validos.')
    except Exception as erro:
        messagebox.showerror('Erro', str(erro))


def exportar_interface():
    if figura_atual['fig'] is None:
        messagebox.showwarning('Exportar', 'Realize uma sintonia antes de exportar.')
        return

    caminho = filedialog.asksaveasfilename(
        title='Salvar grafico',
        defaultextension='.png',
        filetypes=[('Imagem PNG', '*.png')],
        initialfile='controle_pid.png'
    )

    if caminho:
        figura_atual['fig'].savefig(caminho, dpi=300, bbox_inches='tight')
        var_status.set(f'Grafico salvo em: {caminho}')


botao_usar_id.configure(command=selecionar_identificacao)
botao_limpar.configure(command=limpar_parametros)
botao_sintonizar.configure(command=sintonizar_interface)
botao_exportar.configure(command=exportar_interface)
botao_comparar.configure(command=comparar_metodos_interface)
radio_metodo.configure(command=atualizar_campos_sintonia)
radio_manual.configure(command=atualizar_campos_sintonia)
combo_metodo_pid.bind('<<ComboboxSelected>>', atualizar_campos_sintonia)
entries_pid['lambda'].bind('<FocusOut>', atualizar_campos_sintonia)
entries_pid['lambda'].bind('<Return>', atualizar_campos_sintonia)

atualizar_identificacao()
atualizar_campos_sintonia()

root.mainloop()

