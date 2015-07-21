import socket,time
import sys
from tkinter import *
from tkinter.messagebox import * # boîte de dialogue

def closeWin():
    Mafenetre.destroy()

def Connet2serv(LOGIN, PASS, HOST, PORT):

    if(PORT == ''):
        PORT=666    # Port par défaut du GreenAnnuaire
        PORT = int(PORT)    # Conversion du PORT en int
    else:
        PORT = int(PORT)

    adresse_socket = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.settimeout(1)  # Timer: si rien n'arrive du serveur au bout de 1s

    try:
        sock.connect((HOST,PORT))
        sock.send(LOGIN.encode())
        time.sleep(1)
        sock.send(PASS.encode())

        data=''
        time.sleep(2)
        data = sock.recv(1024)

        print(data.decode())
        if(data.decode() != "Error"):

            ### Suppression de la fenetre si elle existe. Si elle n'existe pas, on continue
            try:        
                Mafenetre
                Mafenetre.destroy()
            except:
                pass
                
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
        else:
            print("Erreur d'authentification avec le serveur")
            print("login / password incorrect!")
    except socket.error:
        print ("La connexion a échoué...")
        showwarning('Résultat','Erreur de connection!')
        sock.close()
        sys.exit()

    sock.close()
    sys.exit()


if(len(sys.argv) != 1 and len(sys.argv) != 5):
    print("Usage: # python3 GreenClient.py  (lance le client en mode graphique (Tk))")
    print("Usage: # python3 GreenClient.py  login password serveurIP port (lance le client en ligne de commande)")
    print("Ex:    # python3 GreenServer.py user1 jaimelevert 192.168.1.66 666")
    sys.exit()
elif(len(sys.argv) == 5):
    Connet2serv(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    sys.exit()

Mafenetre = Tk()    # Creation de la fenetre
Mafenetre.title('Connexion Annuaire')
   
Label(Mafenetre, text="Login:").grid(row=0, sticky=W)       # Label login
Label(Mafenetre, text="Password:").grid(row=1, sticky=W)    # Label mot de passe
Label(Mafenetre, text="Serveur:").grid(row=2, sticky=W)     # Label adresse du serveur
Label(Mafenetre, text="Port:").grid(row=3, sticky=W)        # Label port du serveur

### Placement des inputbox sur la grid. On le fait en 2 fois pour ne pas perdre l'adresse des valeurs
addrServ= StringVar()
# portServ= IntVar()

Tlogin = Entry(Mafenetre)             # Inputbox login
mdp = Entry(Mafenetre)                # Inputbox mot de passe
addrServ = Entry(Mafenetre)           # Inputbox adresse du serveur
portServ = Entry(Mafenetre)           # Inputbox port du serveur
# portServ.insert(0,666)

Tlogin.grid(row=0, column=1)          # placement du inbox sur la grid
mdp.grid(row=1, column=1)             # placement de l'inputbox mdp sur la grid
addrServ.grid(row=2, column=1)        # placement de l'inputbox addServ sur la grid
portServ.grid(row=3, column=1)        # placement de l'inputbox portServ sur la grid


Button(Mafenetre, text='Connect', command= lambda: Connet2serv(Tlogin.get(), mdp.get(), addrServ.get(), portServ.get())).grid(row=4, columnspan =2)    # Bouton de connexion

mainloop()
