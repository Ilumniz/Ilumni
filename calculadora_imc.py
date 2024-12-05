import tkinter as tk
from tkinter import ttk, messagebox
import os

# Função para calcular o IMC
def calcular_imc():
    try:
        idade = entry_idade_imc.get()
        altura = float(entry_altura.get().replace(",", "."))
        peso = float(entry_peso.get().replace(",", "."))
        sexo = sexo_var.get()

        # Calculando o IMC
        imc = peso / (altura ** 2)
        resultado = f"{imc:.2f}"

        if imc < 18.5:
            classificacao = "Abaixo do peso"
        elif 18.5 <= imc < 24.9:
            classificacao = "Peso normal"
        elif 25 <= imc < 29.9:
            classificacao = "Sobrepeso"
        else:
            classificacao = "Obesidade"

        # Exibindo resultado no label
        label_resultado.config(text=f"Seu IMC é: {resultado}\nClassificação: {classificacao}")

        # Adicionando resultado à tabela
        tabela.insert("", "end", values=(idade, f"{altura:.2f}", f"{peso:.2f}", sexo, resultado, classificacao))
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para altura e peso.")

# Função para finalizar o cadastro do aluno
def finalizar_cadastro():
    nome = entry_nome.get().strip()
    idade = entry_idade.get().strip()
    peso_inicial_str = entry_peso_inicial.get().strip().replace(",", ".")  # Convertendo vírgula para ponto
    imc_inicial_str = entry_imc_inicial.get().strip().replace(",", ".")  # Convertendo vírgula para ponto
    peso_desejado_str = entry_peso_desejado.get().strip().replace(",", ".")  # Convertendo vírgula para ponto
    imc_atual_str = entry_imc_atual.get().strip().replace(",", ".")  # Convertendo vírgula para ponto

    # Validação dos campos
    if not nome or not idade or not peso_inicial_str or not imc_inicial_str or not peso_desejado_str or not imc_atual_str:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
        return

    try:
        peso_inicial = float(peso_inicial_str)
        imc_inicial = float(imc_inicial_str)
        peso_desejado = float(peso_desejado_str)
        imc_atual = float(imc_atual_str)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        return

    # Salvar os dados em um arquivo de texto
    aluno_data = f"{nome};{idade};{peso_inicial};{imc_inicial};{peso_desejado};{imc_atual}\n"
    
    # Criar diretório para salvar os dados
    if not os.path.exists("cadastros"):
        os.makedirs("cadastros")
    
    # Salvar os dados no arquivo
    with open("cadastros/alunos.txt", "a") as file:
        file.write(aluno_data)

    # Exibir mensagem de sucesso
    messagebox.showinfo("Cadastro", "Aluno cadastrado com sucesso!")

    # Limpar os campos após o cadastro
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_peso_inicial.delete(0, tk.END)
    entry_imc_inicial.delete(0, tk.END)
    entry_peso_desejado.delete(0, tk.END)
    entry_imc_atual.delete(0, tk.END)

# Função para buscar aluno por nome
def buscar_aluno():
    nome_pesquisa = entry_pesquisa_nome.get().strip()
    
    if not nome_pesquisa:
        messagebox.showwarning("Atenção", "Por favor, insira o nome do aluno para pesquisa.")
        return

    # Buscar dados do aluno no arquivo
    try:
        with open("cadastros/alunos.txt", "r") as file:
            alunos = file.readlines()
            encontrado = False
            for aluno in alunos:
                dados = aluno.strip().split(";")
                if dados[0].lower() == nome_pesquisa.lower():
                    encontrado = True
                    # Exibir os dados do aluno
                    label_resultado_pesquisa.config(
                        text=f"Nome: {dados[0]}\nIdade: {dados[1]}\nPeso Inicial: {dados[2]}\nIMC Inicial: {dados[3]}\nPeso Desejado: {dados[4]}\nIMC Atual: {dados[5]}"
                    )
                    break
            if not encontrado:
                messagebox.showinfo("Resultado", "Aluno não encontrado.")
    except FileNotFoundError:
        messagebox.showwarning("Erro", "Arquivo de cadastros não encontrado.")

# Criação da janela principal
root = tk.Tk()
root.title("☺ Calculadora e Cadastro de IMC ☺")
root.geometry("800x600")

# Estilo personalizado
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#1a1a2e", borderwidth=0)
style.configure("TNotebook.Tab", background="#1a1a2e", foreground="white", padding=(10, 5))
style.map("TNotebook.Tab", background=[("selected", "#162447")])

# Definindo fontes
fonte_profissional = ("Segoe UI", 10)

# Abas
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill="both", expand=True)

# Aba de IMC
aba_imc = ttk.Frame(notebook)
notebook.add(aba_imc, text="☺ Calculadora de IMC ☺")

# Campos de entrada da calculadora
label_idade_imc = ttk.Label(aba_imc, text="Idade:")
label_idade_imc.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_idade_imc = ttk.Entry(aba_imc, font=fonte_profissional)
entry_idade_imc.grid(row=0, column=1, padx=5, pady=5)

label_altura = ttk.Label(aba_imc, text="Altura (m):")
label_altura.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_altura = ttk.Entry(aba_imc, font=fonte_profissional)
entry_altura.grid(row=1, column=1, padx=5, pady=5)

label_peso = ttk.Label(aba_imc, text="Peso (kg):")
label_peso.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_peso = ttk.Entry(aba_imc, font=fonte_profissional)
entry_peso.grid(row=2, column=1, padx=5, pady=5)

label_sexo = ttk.Label(aba_imc, text="Sexo:")
label_sexo.grid(row=3, column=0, padx=5, pady=5, sticky="e")

sexo_var = tk.StringVar(value="Masculino")
radio_masculino = ttk.Radiobutton(aba_imc, text="Masculino", variable=sexo_var, value="Masculino")
radio_masculino.grid(row=3, column=1, sticky="w")
radio_feminino = ttk.Radiobutton(aba_imc, text="Feminino", variable=sexo_var, value="Feminino")
radio_feminino.grid(row=3, column=2, sticky="w")

# Botão de cálculo
btn_calcular = ttk.Button(aba_imc, text="Calcular IMC", command=calcular_imc)
btn_calcular.grid(row=4, column=0, columnspan=3, pady=10)

# Resultado
label_resultado = ttk.Label(aba_imc, text="", font=("Arial", 12), foreground="blue")
label_resultado.grid(row=5, column=0, columnspan=3, pady=10)

# Tabela de resultados
tabela = ttk.Treeview(aba_imc, columns=("Idade", "Altura", "Peso", "Sexo", "IMC", "Classificação"), show="headings", height=8)
tabela.grid(row=6, column=0, columnspan=3, pady=10)

# Configuração das colunas
tabela.heading("Idade", text="Idade")
tabela.heading("Altura", text="Altura (m)")
tabela.heading("Peso", text="Peso (kg)")
tabela.heading("Sexo", text="Sexo")
tabela.heading("IMC", text="IMC")
tabela.heading("Classificação", text="Classificação")

# Aba de Cadastro de Alunos
aba_cadastro = ttk.Frame(notebook)
notebook.add(aba_cadastro, text="▲Cadastro de Alunos▲")

# Campos de entrada para cadastro de alunos
label_nome = ttk.Label(aba_cadastro, text="Nome:")
label_nome.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nome = ttk.Entry(aba_cadastro, font=fonte_profissional)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

label_idade = ttk.Label(aba_cadastro, text="Idade:")
label_idade.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_idade = ttk.Entry(aba_cadastro, font=fonte_profissional)
entry_idade.grid(row=1, column=1, padx=5, pady=5)

label_peso_inicial = ttk.Label(aba_cadastro, text="Peso Inicial (kg):")
label_peso_inicial.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_peso_inicial = ttk.Entry(aba_cadastro, font=fonte_profissional)
entry_peso_inicial.grid(row=2, column=1, padx=5, pady=5)

label_imc_inicial = ttk.Label(aba_cadastro, text="IMC Inicial:")
label_imc_inicial.grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_imc_inicial = ttk.Entry(aba_cadastro, font=fonte_profissional)
entry_imc_inicial.grid(row=3, column=1, padx=5, pady=5)

label_peso_desejado = ttk.Label(aba_cadastro, text="Peso Desejado (kg):")
label_peso_desejado.grid(row=4, column=0, padx=5, pady=5, sticky="e")
entry_peso_desejado = ttk.Entry(aba_cadastro, font=fonte_profissional)
entry_peso_desejado.grid(row=4, column=1, padx=5, pady=5)

label_imc_atual = ttk.Label(aba_cadastro, text="IMC Atual:")
label_imc_atual.grid(row=5, column=0, padx=5, pady=5, sticky="e")
entry_imc_atual = ttk.Entry(aba_cadastro, font=fonte_profissional)
entry_imc_atual.grid(row=5, column=1, padx=5, pady=5)

# Botão para finalizar o cadastro
btn_finalizar_cadastro = ttk.Button(aba_cadastro, text="Finalizar Cadastro", command=finalizar_cadastro)
btn_finalizar_cadastro.grid(row=6, column=0, columnspan=2, pady=10)

# Label para mostrar mensagem de sucesso
label_resultado_pesquisa = ttk.Label(aba_cadastro, text="", font=("Arial", 12), foreground="blue")
label_resultado_pesquisa.grid(row=7, column=0, columnspan=2, pady=10)

# Aba de Pesquisa de Alunos
aba_pesquisa = ttk.Frame(notebook)
notebook.add(aba_pesquisa, text="◊Pesquisa de Alunos◊")

# Campo de pesquisa por nome
label_pesquisa_nome = ttk.Label(aba_pesquisa, text="Nome do Aluno:")
label_pesquisa_nome.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_pesquisa_nome = ttk.Entry(aba_pesquisa, font=fonte_profissional)
entry_pesquisa_nome.grid(row=0, column=1, padx=5, pady=5)

# Botão para buscar aluno
btn_buscar_aluno = ttk.Button(aba_pesquisa, text="Buscar", command=buscar_aluno)
btn_buscar_aluno.grid(row=1, column=0, columnspan=2, pady=10)

# Label para mostrar os resultados da pesquisa
label_resultado_pesquisa = ttk.Label(aba_pesquisa, text="", font=("Arial", 12), foreground="blue")
label_resultado_pesquisa.grid(row=2, column=0, columnspan=2, pady=10)

# Função para buscar aluno
def buscar_aluno():
    nome_pesquisa = entry_pesquisa_nome.get().strip()
    
    if not nome_pesquisa:
        messagebox.showwarning("Atenção", "Por favor, insira o nome do aluno para pesquisa.")
        return

    # Buscar dados do aluno no arquivo
    try:
        with open("cadastros/alunos.txt", "r") as file:
            alunos = file.readlines()
            encontrado = False
            for aluno in alunos:
                dados = aluno.strip().split(";")
                if dados[0].lower() == nome_pesquisa.lower():
                    encontrado = True
                    # Exibir os dados do aluno
                    label_resultado_pesquisa.config(
                        text=f"Nome: {dados[0]}\nIdade: {dados[1]}\nPeso Inicial: {dados[2]}\nIMC Inicial: {dados[3]}\nPeso Desejado: {dados[4]}\nIMC Atual: {dados[5]}"
                    )
                    break
            if not encontrado:
                messagebox.showinfo("Resultado", "Aluno não encontrado.")
    except FileNotFoundError:
        messagebox.showwarning("Erro", "Arquivo de cadastros não encontrado.")


        # Aba de Cadastro de Treinos
aba_treino = ttk.Frame(notebook)
notebook.add(aba_treino, text="Ω Cadastro de Treinos Ω")

# Labels e campos para nome do aluno
label_nome_treino = ttk.Label(aba_treino, text="Nome do Aluno:")
label_nome_treino.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nome_treino = ttk.Entry(aba_treino, font=fonte_profissional)
entry_nome_treino.grid(row=0, column=1, padx=5, pady=5)

# Listas para armazenar os widgets dinamicamente
entry_exercicios = []
entry_repeticoes = []

# Criando campos para 10 exercícios e repetições
for i in range(10):
    label_exercicio = ttk.Label(aba_treino, text=f"Exercício {i+1}:")
    label_exercicio.grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
    entry_exercicio = ttk.Entry(aba_treino, font=fonte_profissional)
    entry_exercicio.grid(row=i+1, column=1, padx=5, pady=5)
    entry_exercicios.append(entry_exercicio)

    label_repeticao = ttk.Label(aba_treino, text=f"Repetições {i+1}:")
    label_repeticao.grid(row=i+1, column=2, padx=5, pady=5, sticky="e")
    entry_repeticao = ttk.Entry(aba_treino, font=fonte_profissional)
    entry_repeticao.grid(row=i+1, column=3, padx=5, pady=5)
    entry_repeticoes.append(entry_repeticao)

# Botão para arquivar treino
btn_arquivar_treino = ttk.Button(aba_treino, text="Arquivar Treino", command=lambda: arquivar_treino())
btn_arquivar_treino.grid(row=12, column=0, columnspan=4, pady=10)

# Função para arquivar treino
def arquivar_treino():
    nome = entry_nome_treino.get().strip()
    if not nome:
        messagebox.showwarning("Atenção", "Por favor, insira o nome do aluno.")
        return

    # Coletando os exercícios e repetições
    treinos = []
    for i in range(10):
        exercicio = entry_exercicios[i].get().strip()
        repeticao = entry_repeticoes[i].get().strip()
        if exercicio and repeticao:  # Ignora campos vazios
            treinos.append((exercicio, repeticao))

    if not treinos:
        messagebox.showwarning("Atenção", "Por favor, insira ao menos um exercício e repetição.")
        return

    # Criando diretório se necessário
    if not os.path.exists("cadastros"):
        os.makedirs("cadastros")

    # Salvando os dados no arquivo
    with open("cadastros/treinos.txt", "a") as file:
        file.write(f"Aluno: {nome}\n")
        for exercicio, repeticao in treinos:
            file.write(f"Exercício: {exercicio}; Repetições: {repeticao}\n")
        file.write("\n")  # Linha em branco para separar os treinos

    # Exibindo mensagem de sucesso
    messagebox.showinfo("Cadastro", "Treino arquivado com sucesso!")

    # Limpando os campos
    entry_nome_treino.delete(0, tk.END)
    for entry_exercicio in entry_exercicios:
        entry_exercicio.delete(0, tk.END)
    for entry_repeticao in entry_repeticoes:
        entry_repeticao.delete(0, tk.END)

# Aba de Pesquisa de Treinos
aba_pesquisa_treino = ttk.Frame(notebook)
notebook.add(aba_pesquisa_treino, text="↔ Pesquisa de Treinos ↔")

# Campo de pesquisa por nome do aluno
label_pesquisa_treino = ttk.Label(aba_pesquisa_treino, text="Nome do Aluno:")
label_pesquisa_treino.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_pesquisa_treino = ttk.Entry(aba_pesquisa_treino, font=fonte_profissional)
entry_pesquisa_treino.grid(row=0, column=1, padx=5, pady=5)

# Botão para buscar treino
btn_buscar_treino = ttk.Button(aba_pesquisa_treino, text="Buscar", command=lambda: buscar_treino())
btn_buscar_treino.grid(row=1, column=0, columnspan=2, pady=10)

# Label para mostrar os resultados da pesquisa
label_resultado_treino = ttk.Label(aba_pesquisa_treino, text="", font=("Arial", 12), foreground="blue", justify="left")
label_resultado_treino.grid(row=2, column=0, columnspan=2, pady=10)

# Função para buscar treino
def buscar_treino():
    nome_pesquisa = entry_pesquisa_treino.get().strip()
    if not nome_pesquisa:
        messagebox.showwarning("Atenção", "Por favor, insira o nome do aluno para pesquisa.")
        return

    # Buscar dados no arquivo
    try:
        with open("cadastros/treinos.txt", "r") as file:
            treinos = file.read()
            # Filtrar os treinos pelo nome
            aluno_treinos = []
            treino_secoes = treinos.split("\n\n")  # Separando os treinos em blocos
            for secao in treino_secoes:
                if secao.startswith(f"Aluno: {nome_pesquisa}"):
                    aluno_treinos.append(secao)

            if aluno_treinos:
                resultado = "\n\n".join(aluno_treinos)
                label_resultado_treino.config(text=resultado)
            else:
                messagebox.showinfo("Resultado", "Nenhum treino encontrado para este aluno.")
    except FileNotFoundError:
        messagebox.showwarning("Erro", "Arquivo de treinos não encontrado.")

        # Adicionar esta importação no início do arquivo
from datetime import datetime

# Lista de dicas diárias
dicas_diarias = [
    "Beba pelo menos 2 litros de água por dia para manter-se hidratado.",
    "Inclua frutas e verduras em todas as suas refeições.",
    "Faça exercícios físicos regularmente, pelo menos 30 minutos por dia.",
    "Evite alimentos ultraprocessados e prefira opções naturais.",
    "Durma de 7 a 9 horas por noite para garantir um bom descanso.",
    "Pratique técnicas de relaxamento, como meditação ou ioga, para reduzir o estresse.",
    "Reduza o consumo de açúcar e priorize carboidratos complexos.",
    "Não pule refeições, especialmente o café da manhã.",
    "Inclua fontes de proteína magra, como frango ou peixe, em suas refeições.",
    "Consuma oleaginosas, como nozes e castanhas, para uma boa saúde cerebral."
]

# Função para obter dica do dia
def obter_dica_diaria():
    # Usa o dia do ano para selecionar uma dica
    dia_do_ano = datetime.now().timetuple().tm_yday
    indice_dica = dia_do_ano % len(dicas_diarias)  # Cicla as dicas ao longo do ano
    return dicas_diarias[indice_dica]

# Aba de Dicas de Saúde
aba_dicas = ttk.Frame(notebook)
notebook.add(aba_dicas, text="Dicas de Saúde")

# Exibir dica do dia
dica_do_dia = obter_dica_diaria()
label_dica_titulo = ttk.Label(aba_dicas, text="☼ Dica de Saúde do Dia ♫", font=("Segoe UI", 14, "bold"))
label_dica_titulo.pack(pady=10)

label_dica_conteudo = ttk.Label(aba_dicas, text=dica_do_dia, font=("Segoe UI", 12), wraplength=700, justify="center")
label_dica_conteudo.pack(pady=20)

# Botão para atualizar a dica (se desejar trocar manualmente)
def atualizar_dica():
    nova_dica = obter_dica_diaria()
    label_dica_conteudo.config(text=nova_dica)

btn_atualizar_dica = ttk.Button(aba_dicas, text="Atualizar Dica", command=atualizar_dica)
btn_atualizar_dica.pack(pady=10)



        



