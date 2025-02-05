def menu():
    print("""
Opções de ações que você pode fazer em nosso Banco:
[d]         depositar  
[s]         saque 
[e]         extrato
[nc]        Nova Conta
[lc]        Listar Contas
[nu]        Novo Usuário
[q]         sair
""")
    
def função_valor_deposito(valor_deposito, saldo, extrato,/):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f"\nValor depósitado: R$ {valor_deposito:.2f}"
        print("Depósito realizado com sucesso!")
    else:
        print("Desculpa, mas só é possivel depósitar valores positivos")

    return saldo, extrato 

def função_valor_saque(*,valor, saldo, extrato, numeros_saques, limite,LIMITE_SAQUES):
    excedeu_saldo = saldo < valor
    excedeu_limite = valor > limite
    excedeu_saque = numeros_saques >= LIMITE_SAQUES

    if excedeu_saque:
        print("Operação Falhou! Limite de saques diarios atingido."), saldo, extrato, numeros_saques
    elif excedeu_limite:
        print("Operação Falhou! Não é possivel fazer saque superior a R$ 500.00."), saldo, extrato, numeros_saques
    elif excedeu_saldo:
        print("Operação Falhou! Saldo Insuficiente."), saldo, extrato, numeros_saques
    elif valor > 0:
        saldo -= valor
        numeros_saques += 1
        extrato += f"\nValor sacado: R$ {valor:.2f}"
        print("Saque realizado com sucesso!")
    else:
        print("Operação Falhou! O valor informado é inválido.")

    return saldo, extrato
    
def exibir_extrato(saldo,/,*, novo_extrato):

    print("-"*35)
    print("EXTRATO DA CONTA".center(35, " "))
    print("-"*35)
    print("Não foram realizadas movimentações" if not novo_extrato else novo_extrato)
    print(f"\nSaldo disponivel: R$ {saldo:.2f}")
    print("-"*35)
    return str("")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF!")


    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/yy): ")
    endereço = input("Endereço:(rua, numero - bairro - cidade/sigla estado): \n")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereço})
    print("Usuário criado com sucesso!")

def filtar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

def listar_contas(contas):
    for conta in contas:
        linha = f"""
Agência: {conta["agencia"]}
C/C:     {conta["numero_conta"]}
Titular: {conta["usuario"]["nome"]}
        """
    print("="*50)
    print(linha)
    return str("")

def main():
    print("\nBem vindo ao Sistema Bancario em Python")

    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numeros_saques = 0
    usuarios = []
    contas = []
    

    while True:
        menu()
        opção = str(input("O que você deseja fazer? "))

        if opção == "d":
            valor_deposito = float(input("Valor do Depósito: R$ "))
            saldo, extrato = função_valor_deposito(valor_deposito, saldo, extrato)

        elif opção == "s":
            valor_saque = float(input("Valor Saque: R$ "))
            saldo, extrato = função_valor_saque(
                valor = valor_saque, 
                saldo = saldo, 
                extrato=extrato, 
                numeros_saques =numeros_saques, 
                limite = limite, 
                LIMITE_SAQUES=LIMITE_SAQUES)

        elif opção == "e":
            exibir_extrato(saldo, novo_extrato= extrato)

        elif opção == "nu":
            criar_usuario(usuarios)

        elif opção == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        
        elif opção == "lc":    
            print(listar_contas(contas))

        elif opção == "q":
            print("Obrigador por escolher nosso banco, volte sempre!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada. ")

main()
