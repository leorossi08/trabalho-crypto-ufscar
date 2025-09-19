import socket

# Valores de exemplo (pode usar quaisquer primos e geradores)
g = 5
p = 23
x = 6  # O segredo que o cliente nao sabe
y = pow(g, x, p) # y = 8

HOST = '127.0.0.1'  # Endereco local (localhost)
PORT = 4354         # Mesma porta do desafio

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor falso ouvindo em {HOST}:{PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"Cliente conectado de {addr}")
        
        # Envia os valores iniciais
        conn.sendall(f"g: {g}\n".encode())
        conn.sendall(f"p: {p}\n".encode())
        conn.sendall(f"y: {y}\n".encode())

        for round_num in range(257):
            if round_num % 2 == 0: # Rodada Par (o truque)
                conn.sendall(b"Send g^r * y^-1 mod p.\n")
                C = int(conn.recv(1024).strip())
                conn.sendall(b"Send r.\n")
                r = int(conn.recv(1024).strip())

                # Verificacao do servidor
                if pow(g, r, p) != (C * y) % p:
                    conn.sendall(b"Verificacao falhou!\n")
                    break
            else: # Rodada Impar (a facil)
                conn.sendall(b"Send g^r mod p.\n")
                C = int(conn.recv(1024).strip())
                conn.sendall(b"Send r.\n")
                r = int(conn.recv(1024).strip())

                # Verificacao do servidor
                if C != pow(g, r, p):
                    conn.sendall(b"Verificacao falhou!\n")
                    break
            
            print(f"Rodada {round_num} verificada com sucesso!")

        else: # Se o loop terminar sem 'break'
            conn.sendall(b"utflag{questions_not_random}\n")
            print("Flag enviada!")