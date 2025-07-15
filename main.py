import random

tabuleiro = {
    0: {"nome": "Início", "tipo": "inicio"},

    1: {"nome": "Avenida Paulista", "custo_compra": 300, "aluguel": 150, "hipoteca": 210},
    2: {"nome": "Rua Oscar Freire", "custo_compra": 280, "aluguel": 140, "hipoteca": 196},
    3: {"nome": "Rua 25 de Março", "custo_compra": 260, "aluguel": 130, "hipoteca": 182},
    4: {"nome": "Avenida Brigadeiro Faria Lima", "custo_compra": 240, "aluguel": 120, "hipoteca": 168},
    5: {"nome": "Rua Augusta", "custo_compra": 220, "aluguel": 110, "hipoteca": 154},
    6: {"nome": "Avenida Ibirapuera", "custo_compra": 200, "aluguel": 100, "hipoteca": 140},
    7: {"nome": "Rua da Consolação", "custo_compra": 180, "aluguel": 90, "hipoteca": 126},
    8: {"nome": "Avenida Rebouças", "custo_compra": 160, "aluguel": 80, "hipoteca": 112},
    9: {"nome": "Rua Teodoro Sampaio", "custo_compra": 140, "aluguel": 70, "hipoteca": 98},
    10: {"nome": "Rua Frei Caneca", "custo_compra": 120, "aluguel": 60, "hipoteca": 84},
    11: {"nome": "Avenida São João", "custo_compra": 100, "aluguel": 50, "hipoteca": 70},

    12: {"nome": "Estação do Brás", "tipo": "pausa"},

    13: {"nome": "Rua dos Pinheiros", "custo_compra": 100, "aluguel": 50, "hipoteca": 70},
    14: {"nome": "Avenida Angélica", "custo_compra": 120, "aluguel": 60, "hipoteca": 84},
    15: {"nome": "Rua Bela Cintra", "custo_compra": 140, "aluguel": 70, "hipoteca": 98},
    16: {"nome": "Avenida Pacaembu", "custo_compra": 160, "aluguel": 80, "hipoteca": 112},
    17: {"nome": "Rua Haddock Lobo", "custo_compra": 180, "aluguel": 90, "hipoteca": 126},
    18: {"nome": "Avenida Eusébio Matoso", "custo_compra": 200, "aluguel": 100, "hipoteca": 140},
    19: {"nome": "Rua Pamplona", "custo_compra": 220, "aluguel": 110, "hipoteca": 154},

    "status_rodada": {
            "rodada_atual": 1,
            "jogador_da_vez": 0
    }
}

jogadores = [
    {
        #jogador_1_impulsivo
        "personalidade": "Impulsivo",
        "jogador": 1,
        "local": 0,
        "dinheiro": 100,
        "propriedades": [],
        "dias_preso": 0,
        "perdeu": False
    },

    {
        #jogador_2_novato
        "personalidade": "Novato",
        "jogador": 2,
        "local": 0,
        "dinheiro": 100,
        "propriedades": [],
        "dias_preso": 0,
        "perdeu": False
    },

    {
        #jogador_3_exigente
        "personalidade": "Exigente",
        "jogador": 3,
        "local": 0,
        "dinheiro": 100,
        "propriedades": [],
        "dias_preso": 0,
        "perdeu": False
    },

    {
        #jogador_4_cauteloso
        "personalidade": "Cauteloso",
        "jogador": 4,
        "local": 0,
        "dinheiro": 100,
        "propriedades": [],
        "dias_preso": 0,
        "perdeu": False
    },
]

def montar_podio():
    dinheiro_lista = []
    for jogador in jogadores:
        dinheiro_lista.append([jogador['personalidade'], jogador['dinheiro']])

    classificacao = sorted(jogadores, key=lambda x: x['dinheiro'], reverse=True)
    print("\nPódio:")
    for i, jogador in enumerate(classificacao, start=1):
        print(f"{i}º lugar: {jogador['personalidade']} com ${jogador['dinheiro']}")


def acabou_o_jogo():
    perderam = 0

    for jogador in jogadores:
        if jogador['perdeu'] == True:
            perderam += 1

    if tabuleiro['status_rodada']['rodada_atual'] > 1000:
        montar_podio()
        return True

    elif perderam >= 3:
        montar_podio()
        return True


def jogador_da_vez():
    jogador_da_vez = tabuleiro['status_rodada']['jogador_da_vez']
    if jogador_da_vez > 3:
        tabuleiro['status_rodada']['jogador_da_vez'] = 0
        jogador_da_vez = 0

    return jogador_da_vez


def estou_preso(indice_jogador):
    if jogadores[indice_jogador]['dias_preso'] > 0:
        jogadores[indice_jogador]['dias_preso'] -= 1

        if jogadores[indice_jogador]['dias_preso'] > 0:
            pass
        else:
            # remove do brás e reposiciona
            jogadores[indice_jogador]['local'] = 12  # permanece no Brás, mas pode jogar na próxima rodada
        return True
    return False


def liquidar_jogador(indice_jogador):
    jogador = jogadores[indice_jogador]

    if not jogador['propriedades']:
        return  # Não tem propriedades para vender

    total_hipoteca = 0
    print(f"\n[Jogador {jogador['jogador']} está liquidando propriedades...]")

    # Vende cada propriedade e soma o valor da hipoteca
    for propriedade in jogador['propriedades'][:]:  # [:] cria uma cópia para evitar problemas ao remover
        valor_hipoteca = tabuleiro[propriedade]['hipoteca']
        total_hipoteca += valor_hipoteca
        print(f"- Vendeu {tabuleiro[propriedade]['nome']} por ${valor_hipoteca} (hipoteca)")
        jogador['propriedades'].remove(propriedade)

    jogador['dinheiro'] += total_hipoteca
    print(f"Total recebido: ${total_hipoteca} | Saldo final: ${jogador['dinheiro']}\n")


def perdeu(indice_jogador):
    jogador = jogadores[indice_jogador]

    if jogador['perdeu']:  # Se já está marcado como perdedor
        return True

    # Se não tem dinheiro e não tem propriedades → PERDEU
    elif jogador['dinheiro'] <= 0 and not jogador['propriedades']:
        print(f"Jogador {jogador['jogador']} entrou para a lista do Serasa, e faliu!")
        jogador['perdeu'] = True
        liquidar_jogador(indice_jogador)  # Garante que todas as propriedades são vendidas
        return True

    # Se não tem dinheiro, mas tem propriedades → TENTA VENDER TUDO
    elif jogador['dinheiro'] <= 0:
        print(f"Jogador {jogador['jogador']} está falido. E deverá vender suas ruas")
        liquidar_jogador(indice_jogador)  # Vende tudo e recebe o dinheiro

        # Se mesmo vendendo tudo, ainda está falido → PERDEU
        if jogador['dinheiro'] <= 0:
            print(f"Jogador {jogador['jogador']} não conseguiu pagar o Serasa e faliu definitivamente!")
            jogador['perdeu'] = True
            return True
        else:
            print(f"Jogador {jogador['jogador']} conseguiu pagar o Serasa, e continua no jogo!")
            return False

    else:
        return False  # Não perdeu


def pagar_aluguel(indice_jogador, indice_rua):
    jogador_atual = jogadores[indice_jogador]

    # Verifica todos os jogadores primeiro
    for jogador in jogadores:

        if jogador_atual['jogador'] == jogador['jogador']:
            continue # a rua é dele, nada acontece

        if indice_rua in jogador['propriedades']:  # Propriedade tem dono
            dinheiro_a_ser_transferido = 0

            # Lógica de pagamento
            while True:
                if perdeu(indice_jogador):
                    jogador_atual['perdeu'] = True
                    jogador['dinheiro'] += dinheiro_a_ser_transferido
                    break

                # Caso tenha dinheiro
                elif jogador_atual['dinheiro'] >= tabuleiro[indice_rua]['aluguel']:
                    jogador_atual['dinheiro'] -= tabuleiro[indice_rua]['aluguel']
                    jogador['dinheiro'] += tabuleiro[indice_rua]['aluguel']
                    print(f"Jogador {jogador_atual['jogador']} pagou aluguel de ${tabuleiro[indice_rua]['aluguel']} para {jogador['jogador']}")
                    break

                # Caso não tenha dinheiro, vender propriedades
                elif jogador_atual['dinheiro'] < tabuleiro[indice_rua]['aluguel'] and jogador_atual['propriedades']:
                    indice_rua_a_ser_vendida = jogador_atual['propriedades'][0]
                    jogador_atual['propriedades'].remove(indice_rua_a_ser_vendida)
                    jogador_atual['dinheiro'] += tabuleiro[indice_rua_a_ser_vendida]['hipoteca']
                    dinheiro_a_ser_transferido += tabuleiro[indice_rua_a_ser_vendida]['hipoteca']

                # Caso não consiga pagar mesmo vendendo propriedades
                else:
                    dinheiro_a_ser_transferido += jogador_atual['dinheiro']
                    jogador_atual['dinheiro'] = 0
                    break

            return True  # Aluguel foi pago ou jogador perdeu

    return False  # Ninguém é dono da propriedade

def comprar_rua(indice_jogador, indice_rua):
    jogador_atual = jogadores[indice_jogador]

    # logica - estou em rua impossivel de comprar?
    if jogador_atual['local'] == 12 or jogador_atual['local'] == 0:
        return False # para de executar a funcao

    # logica - paguei aluguel?
    if pagar_aluguel(indice_jogador, indice_rua):
        return False # para de executar a funcao

    
     # logica - comprar rua, baseado na personalidade
    if jogador_atual['personalidade'] == 'Impulsivo':
        if jogador_atual['dinheiro'] >= tabuleiro[indice_rua]['custo_compra']:
            jogador_atual['dinheiro'] -= tabuleiro[indice_rua]['custo_compra'] # pagando o valor da rua
            jogador_atual['propriedades'].append(indice_rua) # atribuindo rua, ao jogador
            print(f"Jogador {jogador_atual['jogador']} comprou {tabuleiro[indice_rua]['nome']}")

    elif jogador_atual['personalidade'] == 'Novato':
        n = random.randint(1,2) # 50% de chance de comprar
        if n == 2:
            if jogador_atual['dinheiro'] >= tabuleiro[indice_rua]['custo_compra']:
                jogador_atual['dinheiro'] -= tabuleiro[indice_rua]['custo_compra']  # pagando o valor da rua
                jogador_atual['propriedades'].append(indice_rua)  # atribuindo rua, ao jogador
                print(f"Jogador {jogador_atual['jogador']} comprou {tabuleiro[indice_rua]['nome']}")
    
    elif jogador_atual['personalidade'] == 'Exigente':
        if jogador_atual['dinheiro'] >= tabuleiro[indice_rua]['custo_compra']:
            if tabuleiro[indice_rua]['aluguel'] >= 90:
                jogador_atual['dinheiro'] -= tabuleiro[indice_rua]['custo_compra']  # pagando o valor da rua
                jogador_atual['propriedades'].append(indice_rua)  # atribuindo rua, ao jogador
                print(f"Jogador {jogador_atual['jogador']} comprou {tabuleiro[indice_rua]['nome']}")
    
    elif jogador_atual['personalidade'] == 'Cauteloso':
        if jogador_atual['dinheiro'] >= tabuleiro[indice_rua]['custo_compra']:
            if jogador_atual['dinheiro'] >= 170:
                jogador_atual['dinheiro'] -= tabuleiro[indice_rua]['custo_compra']  # pagando o valor da rua
                jogador_atual['propriedades'].append(indice_rua)  # atribuindo rua, ao jogador
                print(f"Jogador {jogador_atual['jogador']} comprou {tabuleiro[indice_rua]['nome']}")
    

def jogar(indice_jogador):
    global dado, passou_inicio

    # resetar flag de status
    passou_inicio = False

    # logica - eu perdi?
    if perdeu(indice_jogador) == True:
        return False

    # se estiver no brás, nao joga
    if jogadores[indice_jogador]['dias_preso'] > 0:
        return False

    dado = random.randint(1, 6)
    posicao_atual = jogadores[indice_jogador]['local']
    nova_posicao = (posicao_atual + dado) % 20

    # logica - passei no inicio?
    if posicao_atual + dado >= 20:
        jogadores[indice_jogador]['dinheiro'] += 100
        passou_inicio = True

    jogadores[indice_jogador]['local'] = nova_posicao

    # logica - estou no brás?
    if nova_posicao == 12 and posicao_atual != 12: # fica preso caso chegue no brás, caso esteja lá, nada acontece
        jogadores[indice_jogador]['dias_preso'] = 2
        return False
    
    # logica - irei comprar a rua? (baseado na personalidade)
    comprar_rua(indice_jogador, jogadores[indice_jogador]['local'])


def imprimir_status_rodada(indice_jogador):
    jogador = jogadores[indice_jogador]
    status_prisao = ""

    if perdeu(indice_jogador) == True:
        return False

    if jogador['dias_preso'] > 0:
        status_prisao = f" (PRESO)"

    print(f"\n[RODADA {tabuleiro['status_rodada']['rodada_atual']}]")
    print(f"Jogador {jogador['jogador']}{status_prisao}")
    print(f"Dinheiro ${jogador['dinheiro']}")
    print(f"Ruas {jogador['propriedades']}")

    # mostra quando for preso, e quando está livre
    if jogador['dias_preso'] <= 0 or jogador['dias_preso'] == 2:
        print(f"Tirou {dado} no dado")
        if jogador['local'] == 12:
            print(f"Pisou no Brás no horário de pico, vai ficar por lá 2 rodadas!")
        else:
            print(f"Está na casa {jogador['local']} {tabuleiro[jogador['local']]['nome']}")

    if passou_inicio:
        print(f"Passou pelo início e recebeu $100!")



    print('-' * 30)


while not acabou_o_jogo():
    indice_jogador_atual = tabuleiro['status_rodada']['jogador_da_vez']

    if not estou_preso(indice_jogador_atual):
        jogar(indice_jogador_atual)
        imprimir_status_rodada(indice_jogador_atual)

    # atualização do próximo jogador
    tabuleiro['status_rodada']['jogador_da_vez'] = (indice_jogador_atual + 1) % 4 #vez do proximo jogador
    tabuleiro['status_rodada']['rodada_atual'] += 1 #vai para a proxima rodada
