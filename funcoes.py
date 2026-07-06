#Funções para os cálculo
import pycba as cba
import matplotlib.pyplot as plt

#Determinações de variaveis e listas utilizadas

carga_final = 0
carga_inicial = 0
momento_m = 0
x_fim = 0
x_ini = 0
carga_w = 0
vao_idx = 0
x_pos = 0
forca_p = 0
comprimento = 0
E = 0
G = 0
L = []
R = []
tabela_apoio = {
    "ROLETE": [-1, 0],
    "PINO": [-1, 0],
    "ENGASTE": [-1, -1],
    "LIVRE": [0, 0],
}


def fun_qtd_apoios():
    qtd_apoios = 0
    qtd_apoios = int(input("Você tem quantos apoios? "))
    if qtd_apoios <= 1:
        print("Uma viga precisa de no minimo 2 apoios")
    for i in range(qtd_apoios - 1):
        distancia = float(input(f"qual a distãncia do apoio {i} para o apoio {i+1}? (em metros)"))
        if distancia > 0:
            L.append(distancia)
            i += 1
        else:
            print("De uma distancia valida")
    print("\nAs distâncias entre seus pontos de apoio são (em metros):", L)

    print("Defina os tipo dos apoios: ROLETE PINO ENGASTE LIVRE")
    for i in range(qtd_apoios):
        tipo_apoio = input(f"qual o tipo do apoio {i}?").upper().strip()
        if tipo_apoio in tabela_apoio:
            R.extend(tabela_apoio[tipo_apoio])
        else:
            print("De um tipo valido de apoio")

def momento_inercia():
    b = 0
    h = 0
    Ix = 0
    Iy = 0
    bab = 0
    hab = 0
    bal = 0
    hal = 0
    perfil = input("Digite qual e o tipo de perfil da sua viga (ex: RETANGULAR ou I): ")
    perfil_digitado = perfil.upper().strip()
    if perfil_digitado == "RETANGULAR":
        b = float(input("Qual e a Base do seu retangulo (em metros)? "))
        h = float(input("Qual e a altura do seu retangulo (em metros)? "))
        Ix = (b * (h ** 3)) / 12
        Iy = (h * (b ** 3)) / 12
        print(f"Os momentos de inercia dessa viga sao: Ix = {Ix}, Iy = {Iy}")
        return Ix, Iy
    elif perfil_digitado == "I":
        bab = float(input("Qual e a Base da aba da viga (em metros)? "))
        hab = float(input("Qual e a altura da aba da viga (em metros)? "))
        bal = float(input("Qual e a Base da alma da viga (em metros)? "))
        hal = float(input("Qual e a altura da alma da viga (em metros)? "))
        Ix = ((bal * (hal**3)) / 12) + 2 * (((bab * (hab**3)) / 12) + (bab * hab * ((hal / 2 + hab / 2) ** 2)))
        Iy = ((hal*(bal**3))/12) + 2*((hab*(bab**3))/12)
        print(f"Os momentos de inercia dessa viga sao: Ix = {Ix},m^4 Iy = {Iy}m^4")
        return Ix, Iy

def caracteristica_material():
    E= 0
    G = 0
    material_input = input("Digite o material o qual a viga e feita: ")
    material = material_input.lower().strip()
    print("Esse programa ainda não possui banco de dados de matériais sinta-se livre para contribuir")
    E = float(input("Insira o modulo de Elasticidade E (em Gpa)="))
    G = float(input("Insira o modulo de Rigidez G (em GPa)="))
    print(f"Modulo de elasticiade E = {E} e seu modulo de rigidez G = {G}")
    return E, G

def analise_viga(Ix, E):
    global beam_analysis 
    print(R)
    EI = E * (10**6) * Ix
    beam_analysis = cba.BeamAnalysis(L, EI, R)
    print(f"analise_viga criou: {beam_analysis}") 
    print(f"id do objeto: {id(beam_analysis)}")

def Funcao_Concentrada(vao_idx, forca_p, x_pos):
    global beam_analysis
    beam_analysis.add_pl(i_member=vao_idx, p=forca_p, a=x_pos)

def Funcao_Uniforme(vao_idx, carga_w, x_ini, x_fim):   
    global beam_analysis
    comprimento = x_fim - x_ini
    beam_analysis.add_pudl(i_member=vao_idx, w=carga_w, a=x_ini, c=comprimento)

def Funcao_Momento(vao_idx, momento_m, x_pos):
    global beam_analysis 
    beam_analysis.add_ml(i_member=vao_idx, m=momento_m, a=x_pos)

def Funcao_Linear(vao_idx, carga_inicial, carga_final, x_ini, x_fim):
    global beam_analysis  
    comprimento = x_fim - x_ini
    beam_analysis.add_trap(i_member=vao_idx, w1=carga_inicial, w2=carga_final, a=x_ini, c=comprimento)

def qtd_forcas():
    quantidade_forcas = 0
    quantidade_forcas = int(input("Qual e a quantidade de forcas aplicadas nessa viga?:"))
    i = 0
    for i in range(quantidade_forcas):
        print(f"configure a forca {i}")
        vao_idx = int(input(f"Qual vao da viga a forca esta localizada?"))
        print("Escolha o tipo de item:")
        print("1 - Forca Concentrada (P)")
        print("2 - Carga Uniforme (w)")
        print("3 - Momento Fletor (M)")
        print("4 - Carga Linear Variavel / Trapezoidal (w1 a w2)")
        opcao = input("Digite o número da opcao desejada: ").strip()

        if opcao == "1":
            forca_p = float(input("Digite o valor da força P (em kN)(para baixo positivo): "))
            x_pos = float(input("Digite a posição x da força no vão (em metros): "))
            Funcao_Concentrada(vao_idx, forca_p, x_pos)
            print(f"Força Concentrada {i + 1} adicionada com sucesso!")

        elif opcao == "2":
            carga_w = float(input("Digite o valor da carga uniforme w (em kN/m)(para baixo positivo): "))
            x_ini = float(input("Digite a posição inicial x_ini (em metros): "))
            x_fim = float(input("Digite a posição final x_fim (em metros): "))
            Funcao_Uniforme(vao_idx, carga_w,x_ini, x_fim)
            print(f"Carga Uniforme {i + 1} adicionada com sucesso!")

        elif opcao == "3":
            momento_m = float(input("Digite o valor do momento M (em kNm)(sentido horario negativo): "))
            x_pos = float(input("Digite a posição x do momento no vão (em metros): "))
            Funcao_Momento(vao_idx, momento_m, x_pos)
            print(f"Momento {i + 1} adicionado com sucesso!")

        elif opcao == "4":
            carga_inicial = float(input("Digite a carga inicial w1 (em kN/m)(para baixo positivo): "))
            carga_final = float(input("Digite a carga final w2 (em kN/m)(para baixo positivo): "))
            x_ini = float(input("Digite a posição inicial x_ini (em metros): "))
            x_fim = float(input("Digite a posição final x_fim (em metros): "))
            Funcao_Linear(vao_idx, carga_inicial, carga_final, x_ini, x_fim)
            print(f"Carga Linear {i + 1} adicionada com sucesso!")

def geracao_graficos():
    global beam_analysis   
    beam_analysis.analyze()
    beam_analysis.plot_beam(dimensions=True, labels=True, load_values=True)
    beam_analysis.plot_results()
    plt.show()