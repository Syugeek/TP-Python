###############################################
# Mise en place d'un client simple
# simulation d'une connexion client/serveur
#"""""""""""""""""  version basique """""""""""#

import socket,sys
  
# création d'un socket pour la connexion avec le serveur en local
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
# connexion au serveur, bloc surveillé, et gestion de l'exception
    sock.connect(('127.0.0.1',12807))

except socket.error:
   print("la connexion a échoué.......")
   sys.exit()

print(">>> Connexion établie avec le serveur...")
# Envoi et réception de messages
sock.send(b"hello serveur, je suis le client2 ")
msgServer=sock.recv(1024) # taille par défaut
print(">>> S :", msgServer.decode())
 
msgClient=b"" 
while msgClient.upper()!=b"FIN":
          
         if msgServer.upper()=='FIN':
              break   
         print(">>> Envoi vers le serveur")      
         msgClient=input(">>> ")
         msgClient=msgClient.encode()
         
         sock.send(msgClient)
         print("Confirmation du serveur :")
         msgServer=sock.recv(1024)
          
         print(msgServer.decode())

print (" Fermeture de ma connexion ")
sock.close()
