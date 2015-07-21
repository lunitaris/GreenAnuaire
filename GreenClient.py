import socket,time
import sys
from tkinter import *
from tkinter.messagebox import * # boîte de dialogue

def Connet2serv():

    HOST = addrServ.get()       ### récupération de l'adresse du serveur entré dans l'input box
    PORT = int(portServ.get())  ### récupération du port du serveur entré dans l'input box
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (HOST   ,PORT)
    sock.settimeout(1)
    print('connecting to %s port %s' % server_address)

    LOGIN = Tlogin.get()
    PASS = mdp.get()

    try:
        sock.connect(server_address)
        sock.send(LOGIN.encode())
        time.sleep(1)
        sock.send(PASS.encode())

        data=''
        time.sleep(2)
        data = sock.recv(1024)

        print(data.decode())
        if(data.decode() != "Error"):
            while True:

                rep = input("["+LOGIN+"]# ")
                if(len(rep)):
                    sock.send(rep.encode())
                if(rep == "FIN"):
                    print()
                    break

                try:
                    data = sock.recv(1024)
                    print('%s' % data.decode())
                except socket.timeout:              ### Si rien n'est envoyé par le serveur au bout de 1 seconde
                   pass

    except socket.error:
        print ("La connexion a échoué...")
        showwarning('Résultat','Erreur de connection.\n!')
        
        #sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        sys.exit()

    sock.close()
    sys.exit()


Mafenetre = Tk()
Mafenetre.title('Connexion Annuaire')


####################################    Login   #######################################
### Label pour afficher 'login'
Label1 = Label(Mafenetre, text = 'Login')
Label1.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un widget Entry (champ de saisie) pour le login
Tlogin= StringVar()
Champ = Entry(Mafenetre, textvariable= Tlogin, bg ='bisque', fg='maroon')
Champ.focus_set()
Champ.pack(side = LEFT, padx = 5, pady = 5)


####################################    MDP   #######################################
### Label pour afficher 'login'
Label2 = Label(Mafenetre, text = 'Password')
Label2.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un widget Entry (champ de saisie) pour le login
mdp= StringVar()
Champ = Entry(Mafenetre, textvariable= mdp, bg ='bisque', fg='maroon')
Champ.focus_set()
Champ.pack(side = LEFT, padx = 5, pady = 5)

#################################   Adresse du serveur  ###############################
### Label pour afficher 'Adresse du serveur'
Label3 = Label(Mafenetre, text = 'Adresse du serveur ')
Label3.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un widget Entry (champ de saisie) pour l'adresse du serveur
addrServ= StringVar()
Champ3 = Entry(Mafenetre, textvariable= addrServ, bg ='bisque', fg='maroon')
Champ3.pack(side = LEFT, padx = 5, pady = 5)


#################################   Port du serveur     ###############################
### Label pour afficher 'Adresse du serveur'
Label4 = Label(Mafenetre, text = 'Port du serveur ')
Label4.pack(side = LEFT, padx = 5, pady = 5)

# Création d'un widget Entry (champ de saisie) pour le port du serveur
portServ= StringVar()
Champ4 = Entry(Mafenetre, textvariable= portServ, bg ='bisque', fg='maroon')
Champ4.pack(side = LEFT, padx = 5, pady = 5)

#################################   Bouton valider  ###############################
# Création d'un widget Button (bouton Valider)
Bouton = Button(Mafenetre, text ='Valider', command = Connet2serv)
Bouton.pack(side = RIGHT, padx = 5, pady = 5)

Mafenetre.mainloop()
