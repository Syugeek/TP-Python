import socket, select, threading, time

host = '127.0.0.1'
port = 12807

connexion_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_main.bind((host, port))
connexion_main.listen(5)

print("server listenning on port :", port)

server_up= True

connected_clients = []

while server_up:  ## while True:
    # On va vérifier les nouveaux clients qui se connectent
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms
    rlist, wlist, xlist = select.select([connexion_main],[], [], 0.06)  # 60 ms de time out
     
    for connexion in rlist:  #les clients  de rlist
        connexion_with_client, connexion_infos = connexion.accept()

        # Renvoi du socket du client accepté
        # On ajoute le socket connecté à la liste des clients
        connected_clients.append(connexion_with_client)

        #print(connected_clients)
     
    # On écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là  50ms maximum
    # On encadre l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée

    ### Autre scénario 

    client_to_read = []
    try:
        rlist, wlist, xlist = select.select(connected_clients,[], [], 0.05)
    except select.error:
        pass

#on continue en séquence si pas d'erreurs
    else:  
        # On parcourt la liste des clients à lire
        for rclient in rlist:
            # Client est de type socket
            msg_rcvd = rclient.recv(1024)
            msg_rcvd = msg_rcvd.decode()
            print("recieved msg :", msg_rcvd)
            rclient.send(b"5 / 5")
            #print(rclient)
            for c in connected_clients:
            	if c != rclient:
            		msg_send=msg_rcvd.encode()
            		c.send(msg_send)


            if msg_rcvd.upper() == "FIN":
                server_up = False

print("Fermeture des connexions par l'un des clients ")

# Fermeture des connexions donc des sockets
for client in connected_clients:
    client.close()
 
connexion_principale.close()  ## Fermeture du socket principal
