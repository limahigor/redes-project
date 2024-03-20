import socket
import threading
import pygame
from pgu import gui

MARROM = (84, 38, 6)
BEJE = (222, 184, 129)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL_CLARO = (0, 0, 155)
P_ESCURA = (0, 0, 0)
P_CLARA = (189, 148, 89)
OURO = (255, 215, 0)
clicked = False
game_on = False
vez = False
WIN = 0
jogador = 0
tela = None
jogo_ativo = False
obrigatorio = {
    'estado': False,
    'pos': [],
    'dama': False,
    'pos_dama': []
}
continuar_pulando = {
    'estado': False,
    'x': '',
    'y': '',
}
movimentos_possiveis = []
pos_dama = {
    'x': -2,
    'y': -2
}

cor = MARROM
circle_radius = 20

mapa_cor = [
    [BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM],
    [MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE],
    [BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM],
    [MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE],
    [BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM],
    [MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE],
    [BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM],
    [MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE],
]

mapa_cor_fixo = [
    [BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM],
    [MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE],
    [BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM],
    [MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE],
    [BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM],
    [MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE],
    [BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM],
    [MARROM, BEJE, MARROM, BEJE, MARROM, BEJE, MARROM, BEJE],
]

mapa = [
    [0, 1, 0, 1, 0, 1, 0, 1 ],
    [1, 0, 1, 0, 1, 0, 1, 0 ],
    [0, 1, 0, 1, 0, 1, 0, 1 ],
    [0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0 ],
    [2, 0, 2, 0, 2, 0, 2, 0 ],
    [0, 2, 0, 2, 0, 2, 0, 2 ],
    [2, 0, 2, 0, 2, 0, 2, 0]
]

# Class widget or pop-up window
class POPDialog(gui.Dialog):
    def __init__(self, value, **params):
        title = gui.Label("Vencedor")
        main = gui.Table(width=100, height=70)
        label = gui.Label(value)
        btn = gui.Button("Encerrar")
        btn.connect(gui.CLICK, self.encerrar_jogo, None)
        main.tr()
        main.td(label)
        main.tr()
        main.tr()
        main.td(btn)
        gui.Dialog.__init__(self, title, main)

    def encerrar_jogo(self):
        global jogo_ativo
        self.close()
        jogo_ativo = False

HOST = 'localhost'
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

def receive_data():
    global cor, game_on, vez, jogador
    while True:
        response = client_socket.recv(1024).decode('utf-8')
        response = response.split(':')

        if response[0] == 'GameOn':
            game_on = True if response[1] == 'True' else False
        elif response[0] == 'Vez':
            vez = True if response[1] == 'True' else False
            if len(response) > 2:
                jogador = int(response[2])
                print(f"Jogador: {response[2]}")
        elif response[0] == 'Mapa':
            response[1] = response[1].replace(',', '').replace('[', '').replace(']', '').split(' ')
            for row in range(8):
                for col in range(8):
                    mapa[row][col] = int(response[1][row*8 + col])
        elif response[0] == 'Winner':
            print(response[1])
            WIN = int(response[1])
            if WIN != 0:
                anunciar_ganhador()

def anunciar_ganhador():
    dialog = None
    print(f"Win: {WIN}")
    if WIN == jogador:
        dialog = POPDialog("Você venceu!")
        print("Você venceu!")
    else:
        dialog = POPDialog("Você perdeu!")
        print("Você perdeu!")
    dialog.open()

    # client_socket.close()

def render_text(text, color, x, y):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    tela.blit(text_surface, (x, y))

def send_data(continua):
    if continua:
        client_socket.send(f'Vez:{jogador}:{mapa}:{continua}'.encode('utf-8'))
    else:
        client_socket.send(f'Vez:{jogador}:{mapa}'.encode('utf-8'))

def reiniciar_base():
    global mapa_cor
    for row_aux in range(8):
        for col_aux in range(8):
            mapa_cor[row_aux][col_aux] = mapa_cor_fixo[row_aux][col_aux]

def pos_validas_jogador_1(row, col):
    global mapa_cor

    if (((row + 1) < 8) and ((col + 1) < 8)) and mapa[row + 1][col + 1] == 0:
        mapa_cor[row+1][col+1] = VERDE
    if (((row + 1) < 8) and ((col - 1) >= 0)) and mapa[row + 1][col - 1] == 0:
        mapa_cor[row+1][col-1] = VERDE

def pos_validas_jogador_2(row, col):
    global mapa_cor

    if (((row - 1) >= 0) and ((col + 1) < 8)) and mapa[row - 1][col + 1] == 0:
        mapa_cor[row-1][col+1] = VERDE
    if (((row - 1) >= 0) and ((col - 1) >= 0)) and mapa[row - 1][col - 1] == 0:
        mapa_cor[row-1][col-1] = VERDE

def pos_validas_dama(row, col, rival):
    global mapa_cor

    i, j = row, col
    while (i+1 < 8 and j+1 < 8) and (mapa[i+1][j+1] == 0):
        if mapa[i+1][j+1] == 0:
            mapa_cor[i+1][j+1] = VERDE
        i+=1
        j+=1

    i, j = row, col
    while (i+1 < 8 and j-1 >= 0) and (mapa[i+1][j-1] == 0):
        if mapa[i+1][j-1] == 0:
            mapa_cor[i+1][j-1] = VERDE
        i+=1
        j-=1

    i, j = row, col
    while (i-1 >= 0 and j+1 < 8) and (mapa[i-1][j+1] == 0 or mapa[i-1][j+1] == rival or mapa[i-1][j+1] == rival+2):
        if mapa[i-1][j+1] == 0:
            mapa_cor[i-1][j+1] = VERDE
        i-=1
        j+=1

    i, j = row, col
    while (i-1 >= 0 and j-1 >= 0) and (mapa[i-1][j-1] == 0 or mapa[i-1][j-1] == rival or mapa[i-1][j-1] == rival+2):
        if mapa[i-1][j-1] == 0:
            mapa_cor[i-1][j-1] = VERDE
        i-=1
        j-=13

def transformar_em_dama(row, col):
    if(jogador == 1 and row == 7):
        mapa[row][col] = 3
    elif(jogador == 2 and row == 0):
        mapa[row][col] = 4

def att_jogador(row, col, eat, type, dama):
    global mapa, continuar_pulando
    if not eat:
        if not dama:
            if mapa_cor[row][col] == VERDE:
                mapa[row][col] = jogador
                mapa[pos_dama['x']][pos_dama['y']] = 0
        else:
            if mapa_cor[row][col] == VERDE:
                mapa[row][col] = jogador+2
                mapa[pos_dama['x']][pos_dama['y']] = 0
        transformar_em_dama(row, col)
        send_data(False)
        reiniciar_base()
    if eat and type == 1:
        if mapa_cor[row][col] == VERDE:
            mapa[pos_dama['x']+1][pos_dama['y']+1] = 0
            mapa[pos_dama['x']][pos_dama['y']] = 0
            mapa[row][col] = jogador
    elif eat and type == 2:
        if mapa_cor[row][col] == VERDE:
            mapa[pos_dama['x']+1][pos_dama['y']-1] = 0
            mapa[pos_dama['x']][pos_dama['y']] = 0
            mapa[row][col] = jogador
    elif eat and type == 3:
        if mapa_cor[row][col] == VERDE:
            mapa[pos_dama['x']-1][pos_dama['y']+1] = 0
            mapa[pos_dama['x']][pos_dama['y']] = 0
            mapa[row][col] = jogador
    elif eat and type == 4:
        if mapa_cor[row][col] == VERDE:
            mapa[pos_dama['x']-1][pos_dama['y']-1] = 0
            mapa[pos_dama['x']][pos_dama['y']] = 0
            mapa[row][col] = jogador
    
    if eat:
        if mapa_cor[row][col] == VERDE:
            continuar_pulando['estado']	= True
            continuar_pulando['x'] = row
            continuar_pulando['y'] = col
            if not pos_validas_obrigatorio(row, col, jogador%2+1):
                transformar_em_dama(row, col)
                send_data(False)
                continuar_pulando['estado'] = False
                continuar_pulando['x'] = ''
                continuar_pulando['y'] = ''
            else:
                send_data(True)
            
        reiniciar_base()

def add_obrigatorio(i, j, obrigatorio):
    obrigatorio['estado'] = True
    if (i, j) not in obrigatorio['pos']:
        obrigatorio['pos'].append((i, j))

def analise_jogada_obrigatoria(i, j, rival):
    global obrigatorio

    rival_dama = rival + 2

    if (i+2 < 8 and j+2 < 8) and ((mapa[i+1][j+1] == rival) or (mapa[i+1][j+1] == rival_dama)) and mapa[i+2][j+2] == 0:
        add_obrigatorio(i, j, obrigatorio)
    elif (i+2 < 8 and j-2 >= 0) and ((mapa[i+1][j-1] == rival) or (mapa[i+1][j-1] == rival_dama)) and mapa[i+2][j-2] == 0:
        add_obrigatorio(i, j, obrigatorio)
    elif (i-2 >= 0 and j+2 < 8) and ((mapa[i-1][j+1] == rival) or (mapa[i-1][j+1] == rival_dama)) and mapa[i-2][j+2] == 0:
        add_obrigatorio(i, j, obrigatorio)
    elif (i-2 >= 0 and j-2 >= 0) and ((mapa[i-1][j-1] == rival) or (mapa[i-1][j-1] == rival_dama)) and mapa[i-2][j-2] == 0:
        add_obrigatorio(i, j, obrigatorio)
                
def analise_jogada_obrigatoria_dama(row, col, rival):
    global obrigatorio
    i, j = row, col
    while i+1 < 8 and j+1 < 8 and (mapa[i+1][j+1] == 0 or mapa[i+1][j+1] == rival or mapa[i+1][j+1] == rival+2):
        if mapa[i+1][j+1] == rival or mapa[i+1][j+1] == rival+2:
            if i+2 < 8 and j+2 < 8 and mapa[i+2][j+2] == 0:
                obrigatorio['dama'] = True
                if (row, col) not in obrigatorio['pos_dama']:
                    obrigatorio['pos_dama'].append((row, col))
                break
        i+=1
        j+=1
    
    i, j = row, col
    while i+1 < 8 and j-1 >= 0 and (mapa[i+1][j-1] == 0 or mapa[i+1][j-1] == rival or mapa[i+1][j-1] == rival+2):
        if mapa[i+1][j-1] == rival or mapa[i+1][j-1] == rival+2:
            if i+2 < 8 and j-2 >= 0 and mapa[i+2][j-2] == 0:
                obrigatorio['dama'] = True
                if not (row, col) in obrigatorio['pos_dama']:
                    obrigatorio['pos_dama'].append((row, col))
                break
        i+=1
        j-=1
    
    i, j = row, col
    while i-1 >= 0 and j+1 < 8 and (mapa[i-1][j+1] == 0 or mapa[i-1][j+1] == rival or mapa[i-1][j+1] == rival+2):
        if mapa[i-1][j+1] == rival or mapa[i-1][j+1] == rival+2:
            if i-2 >= 0 and j+2 < 8 and mapa[i-2][j+2] == 0:
                obrigatorio['dama'] = True    
                if not (row, col) in obrigatorio['pos_dama']:
                    obrigatorio['pos_dama'].append((row, col))
                break
        i-=1
        j+=1
    
    i, j = row, col
    while i-1 >= 0 and j-1 >= 0 and (mapa[i-1][j-1] == 0 or mapa[i-1][j-1] == rival or mapa[i-1][j-1] == rival+2):
        if mapa[i-1][j-1] == rival or mapa[i-1][j-1] == rival+2:
            if i-2 >= 0 and j-2 >= 0 and mapa[i-2][j-2] == 0:
                obrigatorio['dama'] = True
                if not (row, col) in obrigatorio['pos_dama']:
                    obrigatorio['pos_dama'].append((row, col))
                break
        i-=1
        j-=1
        

def verificar_estado_obrigatorio():
    global mapa, jogador, obrigatorio
    for i in range(8):
        for j in range(8):
            if mapa[i][j] == jogador:
                analise_jogada_obrigatoria(i, j, (jogador % 2) + 1)
            elif mapa[i][j] == (jogador + 2):
                analise_jogada_obrigatoria_dama(i, j, (jogador % 2) + 1)

def pos_validas_obrigatorio(row, col, rival):
    global mapa, mapa_cor, obrigatorio
    qtd = 0

    rival_dama = rival + 2

    if row+2 < 8 and col+2 < 8 and ((mapa[row + 1][col+1] == rival) or (mapa[row + 1][col+1] == rival_dama)) and mapa[row+2][col+2] == 0:
        mapa_cor[row+2][col+2] = VERDE
        qtd+=1
    if row+2 < 8 and col-2 >= 0 and ((mapa[row+1][col-1] == rival) or (mapa[row+1][col-1] == rival_dama)) and mapa[row+2][col-2] == 0:
        mapa_cor[row+2][col-2] = VERDE
        qtd+=1
    if row-2 >= 0 and col+2 < 8 and ((mapa[row-1][col+1] == rival) or (mapa[row-1][col+1] == rival_dama)) and mapa[row-2][col+2] == 0:
        mapa_cor[row-2][col+2] = VERDE
        qtd+=1
    if row-2 >= 0 and col-2 >= 0 and ((mapa[row-1][col-1] == rival) or (mapa[row-1][col-1] == rival_dama)) and mapa[row-2][col-2] == 0:
        mapa_cor[row-2][col-2] = VERDE
        qtd+=1
    
    return False if qtd == 0 else True

def pos_validas_obrigatorio_dama(row, col, rival):
    global mapa, mapa_cor, obrigatorio
    qtd_geral = 0
    qtd = 0
    i,j = row,col
    while i+1 < 8 and j+1 < 8 and qtd < 2:
        if qtd == 1 and mapa[i+1][j+1] == 0:
            mapa_cor[i+1][j+1] = VERDE
        elif (i+2 < 8 and j+2 < 8 and (mapa[i+1][j+1] == rival or mapa[i+1][j+1] == rival+2) and mapa[i+2][j+2] == 0):
            qtd+=1
        i+=1
        j+=1
    qtd_geral+=qtd
    qtd = 0
    i,j = row,col
    while i+1 < 8 and j-1 >= 0 and qtd < 2:
        if qtd == 1 and mapa[i+1][j-1] == 0:
            mapa_cor[i+1][j-1] = VERDE
        elif (i+2 < 8 and j-2 >= 0 and (mapa[i+1][j-1] == rival or mapa[i+1][j-1] == rival+2) and mapa[i+2][j-2] == 0):
            qtd+=1
        i+=1
        j-=1
    qtd_geral+=qtd
    qtd = 0
    i,j = row,col
    while i-1 >= 0 and j+1 < 8 and qtd < 2:
        if qtd == 1 and mapa[i-1][j+1] == 0:
            mapa_cor[i-1][j+1] = VERDE
        elif (i-2 >= 0 and j+2 < 8 and (mapa[i-1][j+1] == rival or mapa[i-1][j+1] == rival+2) and mapa[i-2][j+2] == 0):
            qtd+=1
        i-=1
        j+=1
    qtd_geral+=qtd
    qtd = 0
    i,j = row,col
    while i-1 >= 0 and j-1 >= 0 and qtd < 2:
        if qtd == 1 and mapa[i-1][j-1] == 0:
            mapa_cor[i-1][j-1] = VERDE
        elif (i-2 >= 0 and j-2 >= 0 and (mapa[i-1][j-1] == rival or mapa[i-1][j-1] == rival+2) and mapa[i-2][j-2] == 0):
            qtd+=1
        i-=1
        j-=1
    qtd_geral+=qtd

    return False if qtd_geral == 0 else True

def apagar_inimigo(row, col, rival):
    global mapa, mapa_cor, obrigatorio

    if pos_dama['x'] + pos_dama['y'] == row + col:
        if col > pos_dama['y']:
            i,j = pos_dama['x'], pos_dama['y']
            while i > row and j < col:
                mapa[i][j] = 0
                i-=1
                j+=1
            mapa[i][j] = jogador+2
        else:
            i,j = pos_dama['x'], pos_dama['y']
            while i < row and j > col:
                mapa[i][j] = 0
                i+=1
                j-=1
            mapa[i][j] = jogador + 2
    elif pos_dama['x'] - pos_dama['y'] == row - col:
        if pos_dama['x'] > row and pos_dama['y'] > col:
            i, j = pos_dama['x'], pos_dama['y']
            while i > row and j > col:
                mapa[i][j] = 0
                i-=1
                j-=1
            mapa[i][j] = jogador + 2
        else:
            i, j = pos_dama['x'], pos_dama['y']
            while i < row and j < col:
                mapa[i][j] = 0
                i+=1
                j+=1
            mapa[i][j] = jogador + 2

def remove_element_list():
    obrigatorio['pos'].clear()
    obrigatorio['pos_dama'].clear()
    pos_dama['x'] = -2
    pos_dama['y'] = -2
                
def movimento(tela):
    global obrigatorio
    
    if len(obrigatorio['pos']) == 0:
        obrigatorio['estado'] = False
    if len(obrigatorio['pos_dama']) == 0:
        obrigatorio['dama'] = False
    
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // 75
    row = mouse_pos[1] // 75

    verificar_estado_obrigatorio()

    if obrigatorio['estado'] or obrigatorio['dama']:
        if (row, col) in obrigatorio['pos'] or (row, col) in obrigatorio['pos_dama']:
            pos_dama['x'] = row
            pos_dama['y'] = col
            reiniciar_base()
            if continuar_pulando['estado'] and (row, col) != (continuar_pulando['x'], continuar_pulando['y']):
                mapa_cor[row][col] = VERMELHO
            else:
                if mapa[row][col] == jogador and (row, col) in obrigatorio['pos']:
                    pos_validas_obrigatorio(row, col, (jogador % 2) + 1)
                elif mapa[row][col] == jogador+2 and (row, col) in obrigatorio['pos_dama']:
                    pos_validas_obrigatorio_dama(row, col, (jogador % 2) + 1)
        elif mapa[row][col] == jogador or mapa[row][col] == jogador+2:
            reiniciar_base()
            mapa_cor[row][col] = VERMELHO
        elif pos_dama['x']+2 < 8 and pos_dama['y']+2 < 8 and (row == pos_dama['x']+2 and col == pos_dama['y']+2) and obrigatorio['estado'] and mapa[pos_dama['x']][pos_dama['y']] == jogador:
            if mapa[row][col] == 0 and continuar_pulando['estado'] and continuar_pulando['x']+2 == row and continuar_pulando['y']+2 == col and pos_dama['x'] == continuar_pulando['x'] and pos_dama['y'] == continuar_pulando['y']:
                att_jogador(row, col, True, 1, False)
                remove_element_list()
                reiniciar_base()
            elif mapa[row][col] == 0 and not continuar_pulando['estado']:
                att_jogador(row, col, True, 1, False)
                remove_element_list()
                reiniciar_base()
        elif pos_dama['x']+2 < 8 and pos_dama['y']-2 >= 0 and (row == pos_dama['x']+2 and col == pos_dama['y']-2) and obrigatorio['estado'] and mapa[pos_dama['x']][pos_dama['y']] == jogador:
            if mapa[row][col] == 0 and continuar_pulando['estado'] and continuar_pulando['x']+2 == row and continuar_pulando['y']-2 == col and pos_dama['x'] == continuar_pulando['x'] and pos_dama['y'] == continuar_pulando['y']:
                att_jogador(row, col, True, 2, False)
                remove_element_list()
                reiniciar_base()
            elif mapa[row][col] == 0 and not continuar_pulando['estado']:
                att_jogador(row, col, True, 2, False)
                remove_element_list()
                reiniciar_base()
        elif pos_dama['x']-2 >= 0 and pos_dama['y']+2 < 8 and (row == pos_dama['x']-2 and col == pos_dama['y']+2) and obrigatorio['estado'] and mapa[pos_dama['x']][pos_dama['y']] == jogador:
            if mapa[row][col] == 0 and continuar_pulando['estado'] and continuar_pulando['x']-2 == row and continuar_pulando['y']+2 == col and pos_dama['x'] == continuar_pulando['x'] and pos_dama['y'] == continuar_pulando['y']:
                att_jogador(row, col, True, 3, False)
                remove_element_list()
                reiniciar_base()
            elif mapa[row][col] == 0 and not continuar_pulando['estado']:
                att_jogador(row, col, True, 3, False)
                remove_element_list()
                reiniciar_base()
        elif pos_dama['x']-2 >= 0 and pos_dama['y']-2 >= 0 and (row == pos_dama['x']-2 and col == pos_dama['y']-2) and obrigatorio['estado'] and mapa[pos_dama['x']][pos_dama['y']] == jogador:
            if mapa[row][col] == 0 and continuar_pulando['estado'] and continuar_pulando['x']-2 == row and continuar_pulando['y']-2 == col and pos_dama['x'] == continuar_pulando['x'] and pos_dama['y'] == continuar_pulando['y']:
                att_jogador(row, col, True, 4, False)
                remove_element_list()
                reiniciar_base()
            elif mapa[row][col] == 0 and not continuar_pulando['estado']:
                att_jogador(row, col, True, 4, False)
                remove_element_list()
                reiniciar_base()
        elif obrigatorio['dama'] and mapa_cor[row][col] == VERDE and ((pos_dama['x'], pos_dama['y']) in obrigatorio['pos_dama'] or (continuar_pulando['x'], continuar_pulando['y']) in obrigatorio['pos_dama']):
            apagar_inimigo(row, col, (jogador%2)+1)
            if pos_validas_obrigatorio_dama(row, col, jogador%2+1):
                continuar_pulando['estado'] = True
                continuar_pulando['x'] = row
                continuar_pulando['y'] = col
                send_data(True)
            else:
                continuar_pulando['estado'] = False
                continuar_pulando['x'] = ''
                continuar_pulando['y'] = ''
                send_data(False)
            remove_element_list()
            reiniciar_base()
            
    else:
        if mapa[row][col] == jogador:
            pos_dama['x'] = row
            pos_dama['y'] = col
            
            reiniciar_base()
            if jogador == 1:
                pos_validas_jogador_1(row, col)
            elif jogador == 2:
                pos_validas_jogador_2(row, col)
        elif mapa[row][col] == jogador + 2:
            pos_dama['x'] = row
            pos_dama['y'] = col

            reiniciar_base()
            pos_validas_dama(row, col, (jogador%2)+1)
        elif((row == pos_dama['x'] + 1 and col == pos_dama['y']+1) or (row == pos_dama['x']+1 and col == pos_dama['y']-1)) and jogador == 1 and mapa[pos_dama['x']][pos_dama['y']] == 1:
            if mapa[row][col] == 0:
                att_jogador(row, col, False, 0, False)
        elif ((row == pos_dama['x']-1 and col == pos_dama['y']+1) or (row == pos_dama['x']-1 and col == pos_dama['y']-1)) and jogador == 2 and mapa[pos_dama['x']][pos_dama['y']] == 2:
            if mapa[row][col] == 0:
                att_jogador(row, col, False, 0, False)
        elif mapa[pos_dama['x']][pos_dama['y']] > 2:
            if (pos_dama['x'] + pos_dama['y'] == row + col or pos_dama['x'] - pos_dama['y'] == row-col) and mapa[row][col] == 0:
                att_jogador(row, col, False, 0, True)

def jogo():
    global vez, clicked, pos_dama, game_on, tela, jogo_ativo
    #init pygame
    pygame.init()

    # Cria a tela
    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Jogo de Damas")

    font = pygame.font.Font(None, 30)
    
    jogo_ativo = True
    while jogo_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False
            if game_on and vez:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    movimento(tela)

        tela.fill(AZUL_CLARO)

        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(tela, mapa_cor[row][col], [col*75, row*75, 75, 75])
                else:
                    pygame.draw.rect(tela, mapa_cor[row][col], [col*75, row*75, 75, 75])
                if mapa[row][col] == 1:
                    pygame.draw.circle(tela, P_CLARA, (col*75+37, row*75+37), circle_radius)
                elif mapa[row][col] == 2:
                    pygame.draw.circle(tela, P_ESCURA, (col*75+37, row*75+37), circle_radius)
                elif mapa[row][col] == 3:
                    pygame.draw.circle(tela, P_CLARA, (col*75+37, row*75+37), circle_radius)
                    pygame.draw.arc(tela, OURO, ((col*75+37)-10-7, (row*75+37)-(10)-(7), (10+7)*2, (10+7)*2), 0, 6.28318, 7)
                elif mapa[row][col] == 4:
                    pygame.draw.circle(tela, P_ESCURA, (col*75+37, row*75+37), circle_radius)
                    pygame.draw.arc(tela, OURO, ((col*75+37)-10-7, (row*75+37)-(10)-(7), (10+7)*2, (10+7)*2), 0, 6.28318, 7)

        player_surface = font.render(f"Jogador {jogador}", True, (255, 255, 255))
        text_surface = font.render(f"Vez do jogador {jogador if vez else jogador%2+1 }", True, (255, 255, 255))

        tela.blit(player_surface, (655, 10))
        tela.blit(text_surface, (622, 270))
        
        pygame.display.update()
    pygame.quit()

# Cria as threads para receber e enviar dados
receive_thread = threading.Thread(target = receive_data)
game_thread = threading.Thread(target = jogo)

# Inicia as threads
receive_thread.start()
game_thread.start()
