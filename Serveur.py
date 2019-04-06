import socket, select, threading, time

# la fonction start_server va ouvrir un socket sur l'ip "host" et le port "port"
# nb_waitlist est la file d'attente max des clients en attente de connexions
# la fonction renvoi la socket serveur
def start_server(host,port,nb_waitlist):
    
    connexion_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_main.bind((host, port))
    connexion_main.listen(nb_waitlist)
    print("server listenning on host: ", host, ", port :", port)

    return connexion_main

# la fonction accept_new_client va accepter une nouvelle connexion
# la fonction va renvoyer la nouvelle socket
def accept_new_client(connexion_main):
    connexion_with_client, client_infos = connexion_main.accept()
    print(client_infos)
    # Renvoi du socket du client accepté
    return connexion_with_client
  
# la fonction lit un message d'une socket "client" et le renvoi décodé.
def read_message_from_client(client):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = client.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data.decode()

def broadcast_message(message, sockets, socket, connexion_main):
    for c in sockets:
        if c != socket and c != connexion_main:
            msg_send=message.encode()
            c.send(msg_send)
            
def close_sockets(sockets, connexion_main):
     # Fermeture des connexions donc des sockets
    for client in sockets:
        if client is not connexion_main:
            client.close()
    connexion_main.close()  ## Fermeture du socket principal

def main():
    host = "127.0.0.1"
    port = 12807

    connexion_main = start_server(host, port, 5)

    server_up= True
    sockets = [connexion_main]

    while server_up:  ## while True:
       
        # On écoute la liste des sockets
        # Les clients renvoyés par select sont ceux devant être lus (recv)
        # On attend là jusqu'a qu'une y est une connexion ou un message (timeout a 0)
        # On encadre l'appel à select.select dans un bloc try
   
        ### Autre scénario 

        try:
            sockets_to_read, writable, errors = select.select(sockets,[], sockets, 0)
        except select.error:
            pass

    #on continue en séquence si pas d'erreurs
        else:  
            for client_error in errors:
                sockets.remove(client_error)
                client_error.close()
                print("Client déconnecté du à une error")
            # On parcourt la liste des clients à lire
            for socket in sockets_to_read:
                #Si la socket est la socket serveur, c'est une nouvelle connexion.
                if socket is connexion_main:
                    new_client = accept_new_client(socket)
                    # on l'ajoute au sockets à ecouter.
                    sockets.append(new_client)

                # Sinon on est un client
                else:
                    # On lit le message ecrit par le client.
                    try:
                        message = read_message_from_client(socket)
                    except ConnectionError:
                        socket.close()
                        sockets.remove(socket)
                        print("Client déconnecté")
                    else:
                        if not message:
                            socket.close()
                            sockets.remove(socket)
                            print("Client déconnecté")
                        else:
                            print("recieved msg :", message)
                            broadcast_message(message, sockets, socket, connexion_main)
                            if message.upper().endswith(":FIN"):
                                server_up = False
                                print("Fermeture des connexions par l'un des clients ")
    close_sockets(sockets, connexion_main)
   

main()
