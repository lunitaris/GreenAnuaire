# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).
import sys

# if(len(sys.argv) != 3):
#    print("Usage: # python3 GreenClient.py login port")
 #   print("Ex:    # python3 GreenClient.py administrator 666")
#    sys.exit()

import socket, threading, time

from tkinter import *
from tkinter.messagebox import * # boîte de dialogue




def Connet2serv():

    HOST = int(addrServ.get())
    PORT = int(portServ.get())
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((HOST, PORT))
    except socket.error:
        print ("La connexion a échoué...")
        sys.exit()    
    print ("Connexion établie avec le serveur...")



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





    def Verification():
        self.connexion.send(login.get().encode())

    # if login.get() == 'admin':
    #     # le mot de passe est bon : on affiche une boîte de dialogue puis on ferme la fenêtre
    #     showinfo('Résultat','\n Connecté au serveur')
    #     Mafenetre.destroy()
    # else:
    #     # le mot de passe est incorrect : on affiche une boîte de dialogue
    #     showwarning('Résultat','Mot de passe incorrect.\nVeuillez recommencer !')
    #     Motdepasse.set('')

        
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


        # Création de la fenêtre principale (main window)
Mafenetre = Tk()
Mafenetre.title('Connexion Annuaire')


####################################    Login   #######################################
### Label pour afficher 'login'
Label1 = Label(Mafenetre, text = 'Login')
Label1.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un widget Entry (champ de saisie) pour le login
login= StringVar()
Champ = Entry(Mafenetre, textvariable= login, bg ='bisque', fg='maroon')
Champ.focus_set()
Champ.pack(side = LEFT, padx = 5, pady = 5)



#################################   Adresse du serveur  ###############################
### Label pour afficher 'Adresse du serveur'
Label2 = Label(Mafenetre, text = 'Adresse du serveur ')
Label2.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un widget Entry (champ de saisie) pour l'adresse du serveur
addrServ= StringVar()
Champ2 = Entry(Mafenetre, textvariable= addrServ, bg ='bisque', fg='maroon')
Champ2.pack(side = LEFT, padx = 5, pady = 5)


#################################   Port du serveur     ###############################
### Label pour afficher 'Adresse du serveur'
Label3 = Label(Mafenetre, text = 'Port du serveur ')
Label3.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un widget Entry (champ de saisie) pour le port du serveur
portServ= StringVar()
Champ3 = Entry(Mafenetre, textvariable= portServ, bg ='bisque', fg='maroon')
Champ3.pack(side = LEFT, padx = 5, pady = 5)

#################################   Bouton valider  ###############################
# Création d'un widget Button (bouton Valider)
Bouton = Button(Mafenetre, text ='Valider', command = Connet2serv)
Bouton.pack(side = RIGHT, padx = 5, pady = 5)

Mafenetre.mainloop()



# ----------------Programme principal - Établissement de la connexion :
   
# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :



th_E1 = ThreadEmission(connexion)
th_R1 = ThreadReception(connexion)
th_E1.start()
th_R1.start()
