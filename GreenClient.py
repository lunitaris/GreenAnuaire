#! /bin/python3
# -*- coding:utf-8 -*-

import sys
if(len(sys.argv) != 2):
    print("Usage: # python3 GreenServer.py port")
    print("Ex:    # python3 GreenServer.py 666")
    sys.exit()


import pickle 
import socket, threading
import uuid
import hashlib

HOST = '127.0.0.1'
PORT = int(sys.argv[1])

# Variable annuaire globale
global GreenAnuaire
GreenAnuaire = {}



# Fonctions de verification de mot de passe.==================================================;

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

#============================================================================================;

def afficherA():
    return str(GreenAnuaire)

def listU():
    return str(GreenAnuaire.keys())

# Ajout d'un user dans le dico
def add(nom, prenom, mail, ville, poste, tel, droits, mdp):
    nomP = nom+'.'+prenom
    GreenAnuaire[nomP]= [nom, prenom, mail, poste, tel, droits, mdp]

def isAdmin(login):
    if GreenAnuaire[login][5] == 'A':
        return 1
    else:
        return 0

# retourne 1 si l'user existe dans l'annuaire, sinon 0
def isPresent(user):
    if(user in GreenAnuaire):
        return 1
    else:
        return 0


def tailleA():
    return len(GreenAnuaire)

def delUser(user):
    if(isPresent(user) == 1):
        del GreenAnuaire[user]
        return 1
    else :
        return -1

class ThreadClient(threading.Thread):
    '''Héritage de la classe Thread pour gérer la connexion avec un client'''

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn


    def printCmdAdmin(self):
        heelp = """
        Commandes (Administrateur):
        \t* _add : ajouter un utilisateur
        \t* _print: print users
        \t* _list : lister users
        \t* _del : supprimer un user
        \t* _save : sauvegarde l'annuaire
        """
        self.connexion.send(heelp.encode())


    def printCmdUser(self):
        heelp = """
        Commandes (Utilisateur):
        \t* _print: print users
        \t* _list : lister users
        """
        self.connexion.send(heelp.encode())   

    def insertIntoA(self):
        # nom = input("Nom : ")
        self.connexion.send("Nom: ".encode())
        Inom=self.connexion.recv(512).decode()

        # prenom = input("Prenom : ")
        self.connexion.send("Prenom: ".encode())
        Iprenom=self.connexion.recv(512).decode()

        # mail = input("Mail : ")
        self.connexion.send("Mail: ".encode())
        Imail=self.connexion.recv(512).decode()

        # ville = input("Ville : ")
        self.connexion.send("Ville: ".encode())
        Iville=self.connexion.recv(512).decode()

        # poste = input("Poste : ")
        self.connexion.send("Poste: ".encode())
        Iposte=self.connexion.recv(512).decode()

        # tel = input("Télephone : ")
        self.connexion.send("Telephone: ".encode())
        Itel=self.connexion.recv(512).decode()

        # droits = input("Admin (A) / User (U) : ")
        self.connexion.send("Admin (A) - User (U) : ".encode())
        Istatus=self.connexion.recv(512).decode()

        # mdp = input("Mot de passe: ")
        self.connexion.send("Mot de passe : ".encode())
        Imdp=self.connexion.recv(512).decode()
        hashed_password = hash_password(Imdp)

        nomP = Inom+'.'+Iprenom
        # Ajout des info saisies dans l'annuaire
        if(isPresent(nomP)):
            self.connexion.send("Erreur : utilisateur déja présent sur l'annuaire.".encode())
            print("Ajout  d'un user existant failed!")
        else:
            add(Inom, Iprenom, Imail, Iville, Iposte, Itel, Istatus, hashed_password)
            self.connexion.send("Ajout Effectué! ".encode())
            print("Ajout effectue a partir d un client! ")
        
        

    def searchA(self, truc, dico):
        tab={} # tableau contenant les resultats
        cpt=0
        for cle in dico.items():
            if(truc in str(cle)):
                cpt=cpt+1
                tab[cpt] = cle # On place la ligne dans le tableau de resultat

        for result in tab:
            ligne = str(tab[result])
            self.connexion.send(ligne.encode())

        infoRecherche="\n\n Recherche terminée. \n "+str(cpt)+" résultat(s) trouvé(s) \n"
        self.connexion.send(infoRecherche.encode())
        if(cpt > 5):
            self.connexion.send("Affiner la recherche? (oui/non) ".encode())
            rep=self.connexion.recv(128).decode()
            if(rep != "oui"):
                self.connexion.send("Donner un element à rechercher parmis les résultats: ".encode())
                affine=self.connexion.recv(128).decode()
                self.searchA(affine, tab)





    def run(self):
        # Dialogue avec le client :
        nom = self.getName()        # Chaque thread possède un nom

        # LoginMess="Bonjour, Please enter Login: "
        # self.connexion.send(LoginMess.encode())

        loginCli=self.connexion.recv(512)
        nom=loginCli.decode()


        if isPresent(nom) == 1:
            self.connexion.send("User trouvé! ".encode())
            print("[Server] Demande de connection de "+nom)
            self.connexion.send("Mot de passe? ".encode())
            motDePasse=self.connexion.recv(128).decode()

            if check_password(GreenAnuaire[nom][6], motDePasse):
                self.connexion.send("\n ====== Connecté!  ====== \n".encode())
            else:
                self.connexion.send("Mauvais mot de passe! ".encode())
                self.connexion.send("Echec.".encode())
                self.connexion.close()      # couper la connexion côté serveur
                return 666

            print("Utilisateur: ",nom," connecté!")

        else:
            self.connexion.send("User non trouvé!".encode())
            print("Utilisateur inconnu: ",nom," a tenté de se connecter. ")
            self.connexion.send("FIN".encode())
            self.connexion.close()      # couper la connexion côté serveur
            return 666
           
        while 1:
            
            msgCliEncoded = self.connexion.recv(1024)
            msgClient = msgCliEncoded.decode()
            if msgClient.upper() =="FIN":
                break

            # ///////////// ADMIN COMMANDES //////////////////////////
            if (msgClient =="_add" and isAdmin(nom)):   # Done
                self.insertIntoA()
            # Sauvegarde l'annuaire courant
            if (msgClient =="_save" and isAdmin(nom)):
                saveDico()
            #////////////////////////////////////////////////////////


            if msgClient =="_print": # Done
                self.connexion.send(afficherA().encode())
            if msgClient =="_list":
                self.connexion.send(listU().encode())
            if msgClient =="_taille":
                self.connexion.send(tailleA().encode()) 
            if msgClient =="_search":
                self.connexion.send("Entrez un element à rechercher: ".encode())
                rech=self.connexion.recv(128).decode()
                self.searchA(rech, GreenAnuaire)


            # Affiche les commandes disponibles selon les droits de l'utilisateur
            if (msgClient =="_help" and isAdmin(nom)):
                self.printCmdAdmin()
            if (msgClient =="_help" and isAdmin(nom) == 0):
                self.printCmdUser()
            # =================================================================


            # Affiche les droits de l'utilisateur courant
            if (msgClient =="_droit"):
                if isAdmin(nom):
                     self.connexion.send("Vous etes Administrateur".encode())
                else:
                    self.connexion.send("Vous etes Utilisateur".encode())

            if msgClient =="_exit":
                break
                
            message = "%s> %s" % (nom, msgClient)
            print(message)

            # Faire suivre le message à tous les autres clients :
            # for cle in conn_client:
              #   if cle != nom:      # ne pas le renvoyer à l'émetteur
                #    conn_client[cle].send(message.encode())
                    
        # Fermeture de la connexion :
        nomTh=self.getName()
        self.connexion.close()      # couper la connexion côté serveur
        del conn_client[nomTh]        # supprimer son entrée dans le dictionnaire
        print ("Client %s déconnecté." % nom)
        # Le thread se termine ici    

#######################################################################################

#add("Burtin", "Graig", "burtin.graig@gmail.com", "Fondumonde", "Ingenieur", "083684876", "U")
# add("lepicard", "mael", "mael.lepicard@gmail.com", "Montrouge", "Ingenieur", "0669123442", "A","azerty")
#add("Admin1", "Admin1", "admin@hotmail.com", "ESGI", "Ingenieur", "123456789", "A")


def saveDico():
    with open('GreenAnuaire.pickle', 'wb') as f:
        pickle.dump(GreenAnuaire, f)


with open('GreenAnuaire.pickle', 'rb') as f:
    GreenAnuaire = pickle.load(f)
    print("Chargement de l'annuaire : Done \n")


# Initialisation du serveur - Définition du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print ("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()

# On continue en séquence
print( "Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)

# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}                # dictionnaire des connexions clients

while 1:    
    connexion, adresse = mySocket.accept()

    # Créer un nouvel objet thread pour gérer la connexion :
    th = ThreadClient(connexion)
    th.start()

    # Mémoriser la connexion dans le dictionnaire : 
    it = th.getName()        # identifiant du thread
    conn_client[it] = connexion
    # print( "Client %s connecté, adresse IP %s, port %s." % (it, adresse[0], adresse[1]))
 

    
