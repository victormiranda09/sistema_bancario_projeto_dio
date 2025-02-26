from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereço):
        self.__endereço = endereço
        self.contas = []

    def realizar_transaçao(self, conta, transaçao):
        transaçao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereço):
        super().__init__(endereço)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero_conta, cliente):
        self.__saldo = 0
        self.__numero_conta = numero_conta
        self.__agencia = "0001"
        self.__cliente = cliente
        self.__historico = Historico()

    
    @classmethod
    def Nova_Conta(cls, cliente, numero_conta):
        return cls(numero_conta, cliente)
        
    @property
    def Saldo(self):
        return self.__saldo
    
    @property
    def numero_conta(self):
        return self.__numero_conta
    
    @property
    def agencia(self):
        return self.__agencia

    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def historico(self):
        return self.__historico
    
    def sacar(self, valor):
        saldo = self.__saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("Operação falhou!, Você não tem saldo suficiente")
        elif valor > 0:
            self.__saldo -= valor
            print("Saque feito com sucesso")
            return True
        else:
            print("Operação Falhou! Só é possivel Sacar valores Positivos")

        return False
        
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print("Depósito feito com sucesso")
        else:
            print("Operação Falhou! Só é possivel Depósitar valores Positivos")
            return False
        
        return True
           
class ContaCorrente(Conta):
    def __init__(self,numero_conta, cliente, limite_valor_saque = 500, limite_nro_saques= 3):
        super().__init__(numero_conta, cliente)
        self.__limite_valor_saque = limite_valor_saque
        self.__limite_nro_saque = limite_nro_saques

    def sacar(self, valor):
        numero_saques = len(
            [transaçao for transaçao in self.historico.transaçoes
             if transaçao["tipo"] == Saque.__name__])
        
        excedeu_limite = valor > self.__limite_valor_saque
        excedeu_saques = numero_saques >= self.__limite_nro_saque

        if excedeu_limite:
            print("Não pode fazer saques acima de R$500,00 ")

        elif excedeu_saques:
            print("Números de saques diarios atingidos")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
Titular:\t{self.cliente.nome}
Agência:\t{self.agencia}             
C\C:\t{self.numero_conta}
            """

class Historico: 
    def __init__(self):
        self.__transaçoes = []

    @property
    def transaçoes(self):
        return self.__transaçoes


    def adicionar_transaçao(self, transaçao):
        self.__transaçoes.append(
            {
                "tipo": transaçao.__class__.__name__,
                "valor": transaçao.valor,
                "data": datetime.now().strftime("%d-%m-%y  %H:%M:%S"),
            })
    
class Transaçao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transaçao):
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor
    
    def registrar(self, conta):
        sucesso_transaçao = conta.sacar(self.valor)

        if sucesso_transaçao:
            conta.historico.adicionar_transaçao(self)

class Deposito(Transaçao):
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor
    
    def registrar(self, conta):
        sucesso_transaçao = conta.depositar(self.valor)

        if sucesso_transaçao:
            conta.historico.adicionar_transaçao(self)

def menu(): 
    print(f" Menu ".center(40, "="), end=" ")
    print("""
Depósitar [ d ]    Nova Conta    [ nc ]
Saque\t  [ s ]    Listar Contas [ lc ]
Extrato\t  [ e ]    Novo Cliente  [ nu ]
Sair\t  [ q ] """) 
    print("="*40)

def filtrar_clientes(cpf, clientes): 
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente; ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do Depósito: "))
    transaçao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transaçao(conta, transaçao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente; ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do Saque: "))
    transaçao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transaçao(conta, transaçao)
    
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente; ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("EXTRATO DA CONTA".center(40, "="))
    transaçoes = conta.historico.transaçoes

    extrato = ""
    if not transaçoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transaçao in transaçoes:
            extrato += f"\n{transaçao['tipo']}: R${transaçao['valor']:.2f} {transaçao['data']}"

    print(extrato)
    print(f"\nSaldo disponivel: R$ {conta.Saldo:.2f}")
    print("="*40)
    
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/yy): ")
    endereço = input("Endereço:(rua, numero - bairro - cidade/sigla estado): \n")

    cliente = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereço=endereço)
    clientes.append(cliente)
    print("Usuário criado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado! Fluxo de criação de conta encerrado!")
        return 
    
    conta = ContaCorrente.Nova_Conta(cliente=cliente, numero_conta= numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("="*40)
        print(conta)

def main():
    print("\nBem vindo ao Sistema Bancario em Python")
    clientes = []
    contas = []
    

    while True:
        menu()
        opção = str(input("O que você deseja fazer? "))

        if opção == "d":
            depositar(clientes)

        elif opção == "s":
            sacar(clientes)
            
        elif opção == "e":
            exibir_extrato(clientes)

        elif opção == "nu":
            criar_cliente(clientes)

        elif opção == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opção == "lc":    
            listar_contas(contas)

        elif opção == "q":
            print("Obrigador por escolher nosso banco, volte sempre!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada. ")

main()
