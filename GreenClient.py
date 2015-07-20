# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).
import sys

if(len(sys.argv) != 3):
    print("Usage: # python3 GreenClient.py login port")
    print("Ex:    # python3 GreenClient.py administrator 666")
    sys.exit()

import socket, threading, time


HOST = '127.0.0.1'
PORT = int(sys.argv[2])

# Variable globale d'arret de thread. Si celle-ci est à 1, tous les threads se coupent
global iKillYouBloodyThread
iKillYouBloodyThread = 0



#-----------------------------------------------------------------------
class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        global iKillYouBloodyThread     # variable d'arret du thread.
        while iKillYouBloodyThread == 0:
            msgServerEncoded = self.connexion.recv(1024)
            message_recu = msgServerEncoded.decode()

            message = "%s> %s" % ("Server: ", message_recu)
            print(message)

            if message_recu =='' or message_recu.upper() == "FIN":
                iKillYouBloodyThread=1
        
        print ("Adios!")
        iKillYouBloodyThread=1
        self.connexion.close()
    
#------------------------------------------------------------------------
class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        global iKillYouBloodyThread     # variable d'arret du thread
        login = str(sys.argv[1])
        self.connexion.send(login.encode())
        time.sleep(3)

        while iKillYouBloodyThread == 0:
            sys.stdout.flush()
            message_emis = input("["+login+"]# ")
            if message_emis.upper()=="FIN":
                iKillYouBloodyThread=1
                break
            if iKillYouBloodyThread == 0:
                self.connexion.send(message_emis.encode())
                sys.stdout.flush()
        
        
        iKillYouBloodyThread=1
        time.sleep(1)
        print("Amigos!")
        self.connexion.close()

# ----------------Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((HOST, PORT))
except socket.error:
    print ("La connexion a échoué...")
    sys.exit()    
print ("Connexion établie avec le serveur...")
            
# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :

th_E1 = ThreadEmission(connexion)
th_R1 = ThreadReception(connexion)
th_E1.start()
th_R1.start()
