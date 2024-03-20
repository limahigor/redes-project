import socket
import threading
import time
# Configurações do servidor
HOST = 'localhost'
PORT = 5001

# status do jogo
game_on = False
vez = 0

# Mapa do jogo
mapa = [
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0]
]

# Cria um socket para o servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liga o socket à porta e endereço
server_socket.bind((HOST, PORT))

# Coloca o socket em modo de escuta
server_socket.listen()

# Lista para armazenar os sockets dos clientes conectados
clients = [] 

# Função que verifica se algum jogador ganhou
def verify_winner():
    player1_pieces = 0
    player2_pieces = 0
    
    for row in mapa:
        for cell in row:
            if cell in [1, 3]:
                player1_pieces += 1
            elif cell in [2, 4]:
                player2_pieces += 1
    
    if player1_pieces == 0:
        return 2
    elif player2_pieces == 0:
        return 1
    else:
        return 0

# Função para lidar com as conexões dos clientes
def handle_client(client_socket):
    global vez, mapa
    # Adiciona o socket do cliente à lista
    clients.append(client_socket)

    if len(clients) == 2:
        for jogador, c in enumerate(clients):
            game_on = 'GameOn:True'
            c.send(game_on.encode('utf-8'))
            time.sleep(0.1)
            if(jogador == 0):
                vez = 'Vez:True:1'
                c.send(vez.encode('utf-8'))
            elif(jogador == 1):
                vez = 'Vez:False:2'
                c.send(vez.encode('utf-8'))
    elif len(clients) < 2:
        for c in clients:
            game_on = 'False'
            c.send(game_on.encode('utf-8'))
    vez = 0

    ativo = True
    while ativo:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            message = message.split(':')
            message[2] = message[2].replace(',', '').replace('[', '').replace(']', '').split(' ')

            for row in range(8):
                for col in range(8):
                    mapa[row][col] = int(message[2][row*8 + col])
                
            if message[0] == 'Vez':
                print(message)
                if len(message) <= 3:
                    vez = 0 if message[1] == '2' else 1

                for jogador, c in enumerate(clients):
                    if(jogador == vez):
                        c.send('Vez:True'.encode('utf-8'))
                        time.sleep(0.1)
                        c.send(f'Mapa:{mapa}'.encode('utf-8'))
                    else:
                        c.send('Vez:False'.encode('utf-8'))
                        time.sleep(0.1)
                        c.send(f'Mapa:{mapa}'.encode('utf-8'))

            winner = verify_winner()
            if winner != 0:
                for c in clients:
                    print(f"Win: {winner}")
                    c.send(f'Winner:{winner}'.encode('utf-8'))
                    time.sleep(0.1)
                ativo = False
        except:
            clients.remove(client_socket)
            break

    # Fecha a conexão do socket
    client_socket.close()

# Função para aceitar as conexões dos clientes
def accept_connections():
    while True:
        # Aceita a conexão do cliente
        client_socket, client_address = server_socket.accept()

        print(f'{client_address} conectou-se ao servidor.')

        # Cria uma thread para lidar com a conexão do cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Inicia a thread para aceitar as conexões dos clientes
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()