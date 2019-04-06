###############################################
# Mise en place d'un client simple
# simulation d'une connexion client/serveur
#"""""""""""""""""  version basique """""""""""#

import socket, sys, select, threading, getopt

# la fonction lit un message d'une socket "socket" et le renvoi décodé.
def read_message_from_socket(socket):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = socket.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data.decode()

def read_and_send(sock, clientname):
    while True:        
        # On lit une ligne sur l'input, bloquant.
        msgClient=input("")
        
        # On recupere les messages et on les affiche.
        # Idéalement devrait etre dans un autre thread que l'input et le send plus bas. 
        read_and_write(sock)

        # On envoie le message au serveur.
        msgClient=msgClient.encode()
        sock.send(clientname.encode() + b" :" + msgClient)

        # Si on a ecris FIN sur l'input, on sort.
        if msgClient.upper()==b"FIN":
            break

def read_and_write(sock):
    # On ecoute sur la socket serveur pendant 50ms max.
    try:
        sockets_to_read, writable, errors = select.select([sock],[], [sock], 0.05)
    except select.error:
        pass
    else:  
        for client_error in errors:
            client_error.close()
            print("Client déconnecté du à une error")
            sys.exit()
        # On parcourt la liste des clients à lire
        for socket in sockets_to_read:
            try:
                message = read_message_from_socket(socket)
            except ConnectionError:
                socket.close()
                print("Client déconnecté")
                sys.exit()
            else:      
                print("recieved msg :", message)

def main(clientname):
    # création d'un socket pour la connexion avec le serveur en local
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
    # connexion au serveur, bloc surveillé, et gestion de l'exception
        sock.connect(('127.0.0.1',12807))

    except socket.error:
        print("la connexion a échoué.......")
        sys.exit()

    print(">>> Connexion établie avec le serveur...")
    read_and_send(sock, clientname)
    sock.close()

if len(sys.argv) >= 2:
    main(sys.argv[1])
else:
    print('Client.py [NameOfClient]')