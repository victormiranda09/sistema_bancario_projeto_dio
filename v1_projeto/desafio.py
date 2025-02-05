print("\nBem vindo ao Sistema Bancario em Python")

saldo = 0
limite = 500
extrato = ""
numeros_saques = 0
LIMITE_SAQUES = 3

while True:

    print("""
Opções de ações que você pode fazer em nosso sistema:

        [1] depositar    
        [2] saque
        [3] extrato
        [4] sair
""")
    opção = int(input("O que você deseja fazer? "))

    if opção == 1:
        valor_deposito = float(input("Valor do Depósito: R$ "))
        if valor_deposito <= 0:
            print("Desculpa, mas só é possivel depósitar valores positivos")
        else:
            saldo += valor_deposito
            extrato += f"\nValor depósitado: R$ {valor_deposito:.2f}"
            print("Valor depósitado com sucesso!")

        #só pode depositar uma valor positivo
        #armazenar os valores no extrato

    elif opção == 2:
        valor_saque = float(input("Valor Saque: R$ "))
        if numeros_saques == LIMITE_SAQUES:
            print("Operação Falhou! Limite de saques diarios atingido")
        elif valor_saque > 500:
            print("Operação Falhou! Não é possivel fazer saque superior a R$ 500.00")
        elif saldo < valor_saque:
            print("Operação Falhou! Saldo Insuficiente")
        
        else:
            saldo -= valor_saque
            numeros_saques += 1
            extrato += f"\nValor sacado: R$ {valor_saque:.2f}"
            print("Valor sacado com sucesso!")

        #só pode ser 3 saques diarios
        #limite maximo de 500 reais por saque
        #caso não tenha saldo, deve mostra uma mensagem dizendo que não tem saldo
        #armazenar os saques no extrato

    elif opção == 3:
        print("-"*35)
        print("EXTRATO DA CONTA".center(35, " "))
        print("-"*35)
        print("Não foram realizadas movimentações" if not extrato else extrato)
        print(f"\nSaldo disponivel: R$ {saldo:.2f}")
        print("-"*35)

        #mostrar na tela os valores de deposito e saques feito na conta de forma formatada ex: R$ 150,00

    elif opção == 4:
        print("Obrigador por escolher nosso banco, volte sempre!")
        break
        

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada. ")