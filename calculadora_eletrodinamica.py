"""
Eletrodinâmica, Trabalho, Energia e Potência Elétrica
Calculadora de grandezas elétricas

Este programa funciona como uma calculadora de grandezas elétricas,
permitindo calcular corrente, tensão, resistência, potência, energia,
trabalho elétrico, consumo em kWh e custo da energia.
"""

import os


def calcular_corrente():
    """
    Funcionalidade 1 - Corrente Elétrica
    Fórmula: I = Q / t
    Entrada: carga (Q) e tempo (t)
    Saída: corrente elétrica (I) em ampères (A)
    """
    print("\n--- Cálculo de Corrente Elétrica ---")
    print("Fórmula: I = Q / t")
    try:
        Q = float(input("Digite a carga elétrica (C): "))
        t = float(input("Digite o tempo (s): "))

        if t == 0:
            print("Erro: o tempo não pode ser zero (divisão por zero).")
            return

        if Q < 0 or t < 0:
            print("Aviso: valores negativos foram informados.")

        I = Q / t
        print(f"\nCorrente elétrica = {I} A")
    except ValueError:
        print("Erro: digite um valor numérico válido.")


def calcular_tensao():
    """
    Funcionalidade 2 - Tensão Elétrica
    Fórmula: U = R * I  (Lei de Ohm)
    Entrada: resistência (R) e corrente (I)
    Saída: tensão elétrica (U) em volts (V)
    """
    print("\n--- Cálculo de Tensão Elétrica ---")
    print("Fórmula: U = R * I")
    try:
        R = float(input("Digite a resistência (Ω): "))
        I = float(input("Digite a corrente (A): "))

        U = R * I
        print(f"\nTensão elétrica = {U} V")
    except ValueError:
        print("Erro: digite um valor numérico válido.")


def calcular_resistencia():
    """
    Funcionalidade 3 - Resistência Elétrica
    Fórmula: R = U / I
    Entrada: tensão (U) e corrente (I)
    Saída: resistência (R) em ohms (Ω)
    Verificação: I != 0
    """
    print("\n--- Cálculo de Resistência Elétrica ---")
    print("Fórmula: R = U / I")
    try:
        U = float(input("Digite a tensão (V): "))
        I = float(input("Digite a corrente (A): "))

        if I == 0:
            print("Erro: a corrente não pode ser zero (divisão por zero).")
            return

        R = U / I
        print(f"\nResistência elétrica = {R} Ω")
    except ValueError:
        print("Erro: digite um valor numérico válido.")


def calcular_potencia():
    """
    Funcionalidade 4 - Potência Elétrica
    Oferece três possibilidades:
    A: P = U * I       (tensão e corrente)
    B: P = R * I²      (resistência e corrente)
    C: P = U² / R      (tensão e resistência)
    """
    print("\n--- Cálculo de Potência Elétrica ---")
    print("Escolha a opção conforme os dados que você possui:")
    print("  A - Tensão e Corrente       (P = U * I)")
    print("  B - Resistência e Corrente   (P = R * I²)")
    print("  C - Tensão e Resistência     (P = U² / R)")
    opcao = input("Digite a opção (A/B/C): ").strip().upper()

    try:
        if opcao == "A":
            U = float(input("Digite a tensão (V): "))
            I = float(input("Digite a corrente (A): "))
            P = U * I
            print(f"\nPotência = {P} W")

        elif opcao == "B":
            R = float(input("Digite a resistência (Ω): "))
            I = float(input("Digite a corrente (A): "))
            P = R * (I ** 2)
            print(f"\nPotência = {P} W")

        elif opcao == "C":
            U = float(input("Digite a tensão (V): "))
            R = float(input("Digite a resistência (Ω): "))

            if R == 0:
                print("Erro: a resistência não pode ser zero (divisão por zero).")
                return

            P = (U ** 2) / R
            print(f"\nPotência = {P} W")

        else:
            print("Opção inválida. Escolha A, B ou C.")
    except ValueError:
        print("Erro: digite um valor numérico válido.")


def calcular_energia():
    """
    Funcionalidade 5 - Energia Elétrica
    Fórmula: E = P * t
    Entrada: potência (P) e tempo (t)
    Saída: energia (E) em joules (J)
    Também converte para kWh quando aplicável.
    """
    print("\n--- Cálculo de Energia Elétrica ---")
    print("Fórmula: E = P * t")
    try:
        P = float(input("Digite a potência (W): "))
        t = float(input("Digite o tempo (s): "))

        if t < 0 or P < 0:
            print("Aviso: valores negativos foram informados.")

        E = P * t 
        print(f"\nEnergia = {E} J")

        E_kwh = E / 3_600_000
        print(f"Energia = {E_kwh} kWh")
    except ValueError:
        print("Erro: digite um valor numérico válido.")


def calcular_trabalho():
    """
    Funcionalidade 6 - Trabalho Elétrico
    Fórmula: W = U * Q
    Entrada: tensão (U) e carga (Q)
    Saída: trabalho (W) em joules (J)
    """
    print("\n--- Cálculo de Trabalho Elétrico ---")
    print("Fórmula: W = U * Q")
    try:
        U = float(input("Digite a tensão (V): "))
        Q = float(input("Digite a carga (C): "))

        W = U * Q
        print(f"\nTrabalho = {W} J")
    except ValueError:
        print("Erro: digite um valor numérico válido.")


def calcular_consumo():
    """
    Funcionalidade 7 - Consumo de Energia em kWh
    Fórmula: E = P_kW * t * dias
    Entrada: potência (W), tempo por dia (h), quantidade de dias
    Saída: consumo (E) em kWh
    """
    print("\n--- Cálculo de Consumo em kWh ---")
    print("Fórmula: E = P(kW) * t(h) * dias")
    try:
        P_w = float(input("Digite a potência do equipamento (W): "))
        t = float(input("Digite o tempo de uso por dia (h): "))
        dias = float(input("Digite a quantidade de dias: "))

        if t < 0 or dias < 0 or P_w < 0:
            print("Aviso: valores negativos foram informados.")

        P_kw = P_w / 1000

        E = P_kw * t * dias

        print(f"\nPotência = {P_kw} kW")
        print(f"Consumo = {E} kWh")
    except ValueError:
        print("Erro: digite um valor numérico válido.")


def calcular_custo():
    """
    Funcionalidade 8 - Custo da Energia Elétrica
    Fórmula: C = E * tarifa
    Entrada: energia consumida (kWh) e tarifa (R$/kWh)
    Saída: custo (C) em reais (R$)
    """
    print("\n--- Cálculo de Custo da Energia ---")
    print("Fórmula: C = E * tarifa")
    try:
        E = float(input("Digite a energia consumida (kWh): "))
        tarifa = float(input("Digite a tarifa (R$/kWh): "))

        if E < 0 or tarifa < 0:
            print("Aviso: valores negativos foram informados.")

        C = E * tarifa
        print(f"\nCusto = R$ {C:.2f}")
    except ValueError:
        print("Erro: digite um valor numérico válido.")


def limpar_tela():
    """Limpa a tela do terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def exibir_menu():
    """Exibe o menu principal da calculadora."""
    print("=" * 37)
    print("  CALCULADORA DE ELETRODINÂMICA")
    print("=" * 37)
    print("1 - Calcular corrente elétrica")
    print("2 - Calcular tensão elétrica")
    print("3 - Calcular resistência")
    print("4 - Calcular potência")
    print("5 - Calcular energia")
    print("6 - Calcular trabalho elétrico")
    print("7 - Calcular consumo em kWh")
    print("8 - Calcular custo da energia")
    print("9 - Sair")
    print("=" * 37)


def main():
    """Função principal que controla o fluxo do programa."""
    opcoes = {
        "1": calcular_corrente,
        "2": calcular_tensao,
        "3": calcular_resistencia,
        "4": calcular_potencia,
        "5": calcular_energia,
        "6": calcular_trabalho,
        "7": calcular_consumo,
        "8": calcular_custo,
    }

    while True:
        exibir_menu()
        opcao = input("Digite a opção: ").strip()

        if opcao == "9":
            print("\nEncerrando o programa. Até logo!")
            break

        if opcao in opcoes:
            opcoes[opcao]()
        else:
            print("Opção inválida. Digite um número de 1 a 9.")

        # Pausa para o usuário ler o resultado antes de limpar a tela
        input("\nPressione ENTER para continuar...")
        limpar_tela()


if __name__ == "__main__":
    main()
