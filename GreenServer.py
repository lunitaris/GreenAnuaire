#! /bin/python3
# -*- coding:utf-8 -*-

import sys
if(len(sys.argv) != 2):
    print("Usage: # python3 GreenServer.py port")
    print("Ex:    # python3 GreenServer.py 666")
    sys.exit()

import socket, threading, pickle
import uuid, hashlib
import signal, time

HOST = '127.0.0.1'
PORT = int(sys.argv[1])
global mySocket     ## variable globale qui servira a la fonction lance lors d'un SIGINT pour fermer le socket et quitter proprementself.


### Fonction qui retourne le hash du mot entré en paramètre.
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt



### Création du dictionnaire avec UN utilisateur par defaut (admin) pour pouvoir administrer l'annuaire
### Le mot de passe pourra ensuite être modifié, et enregistré dans le fichier annuaire.
global GreenAnuaire     ## Variable annuaire globale
ficAnnuaire = "Annuaire"    ## Nom du fichier annuaire à utiliser pour enregistrer / charger l'annuaire
adminDefaultPassword="green"    ## MOT DE PASSE PAR DEFAUT pour l'utilisateur admin


### Compte administrateur par défaut (Login : admin || Password : "green")
GreenAnuaire = {'admin': ['admin', 'local', 'IloveGreen@admin.com', 'Administrateur par defaut', '-', 'A', hash_password(adminDefaultPassword)]}

### Fonction qui sauvegarde l'annuaire courant dans le fichier pointé par la variable ficAnnuaire
def saveDico():
    with open(ficAnnuaire, 'wb') as f:
        pickle.dump(GreenAnuaire, f)


### Fonction qui verifie si le hash de la string 'user_password' correspond bien au hash passe en parametre (hashed_password) retourne TRUE si vrai, FALSE sinon.
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


### Retourne l'annuaire en string
def afficherA():
    return str(GreenAnuaire)

### Retourne la liste des cles de l'annuaire
def listU():
    return str(GreenAnuaire.keys())

# Ajout d'un user dans le dico. Chaque parametres correspond à une case du tableau.
def add(nom, prenom, mail, ville, poste, tel, droits, mdp):
    nomP = nom+'.'+prenom
    GreenAnuaire[nomP]= [nom, prenom, mail, poste, tel, droits, mdp]

### Retourne 1 si le nom d'utilisateur passé en paramètre enregistré dans l'annuaire est administrateur.
def isAdmin(login):
    if GreenAnuaire[login][5] == 'A':
        return 1
    else:
        return 0

### retourne 1 si l'utilisateur passé en paramètre  existe dans l'annuaire, sinon 0
def isPresent(user):
    if(user in GreenAnuaire):
        return 1
    else:
        return 0

### Retoure la taille de l'anuaire
def tailleA():
    return len(GreenAnuaire)

### Supprime l'utilisateur passé en paramètre de l'annuaire.
def delUser(user):
    if(isPresent(user) == 1):
        del GreenAnuaire[user]
        return 1
    else :
        return -1

class ThreadClient(threading.Thread):
    '''Héritage de la classe Thread pour gérer la connexion avec un client'''

    # Constructeur
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def authentifiction(self, nom, motDePasse):
         ### Si le login fournit est présent dans l'annuaire, le programme demande le mot de passe associé au login, sinon, la connection est coupé.
        ### En cas de mauvais mot de passe, la connection est coupé.
        if isPresent(nom) == 1:
            print("[Server] (",nom,") : Demande de connexion")

            ### Test du mot de passe fournit
            if check_password(GreenAnuaire[nom][6], motDePasse):
                welcome_message="Welcome "+nom+" 'FIN pour quitter'"
                self.connexion.send(str(welcome_message).encode())
                print("[Server] (",nom,") :Connecté!")
                return True
            else:
                print("[Server] (",nom,") : Mot de passe incorrect!")
                self.connexion.send("Error".encode())
                return False

        ### Si l'utilisateur n'a pas été trouvé dans l'annuaire
        else:
            print("[Server] (",nom,") : Utilisateur inconnu a tenté de se connecter!")
            self.connexion.send("Error".encode())
            return False

    ### Affiche le menu Administrateur
    def printCmdAdmin(self):
        heelp = """
        Commandes (Administrateur):
        \t* _add : ajouter un utilisateur
        \t* _print: print users
        \t* _list : lister users
        \t* _search : chercher un element
        \t* _del : supprimer un user
        \t* _save : sauvegarde l'annuaire
        \t* FIN: termine la connexion
        """
        self.connexion.send(heelp.encode())

    ### Affiche le menu utilisateur
    def printCmdUser(self):
        heelp = """
        Commandes (Utilisateur):
        \t* _search : chercher un element
        \t* _list : lister users
        \t* FIN: termine la connexion
        """
        self.connexion.send(heelp.encode())   

    ### Enregistre un nouvel utilisateur dans l'annuaire.
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
        
        
    ### Recherche le mot clé 'truc' passé en paramètre dans l'annuaire.
    ### Si plus de 5  éléments ont été trouvés, la fonction propose à l'utilisateur d'affiner la recherche (fonction récursive)
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

        loginCli=self.connexion.recv(512)   # reçoit le login utilisateur.
        nom=loginCli.decode()

        mdpCli=self.connexion.recv(512)   # reçoit le login utilisateur.
        passCli = mdpCli.decode()

        continuer= self.authentifiction(nom, passCli)
       

###############################################################################################
        ### Boucle principale du programme
        while (continuer == True):
            
            msgCliEncoded = self.connexion.recv(1024)   ## Reception du message
            msgClient = msgCliEncoded.decode()          ## Decode le message

            if (msgClient.upper() =="FIN" or msgClient == ''):               ## Condition d'arrêt.
                break

            # ///////////// ADMIN COMMANDES //////////////////////////
            if (msgClient =="_add" and isAdmin(nom)):   ### ajoute un utilisateur dans l'annuaire.
                self.insertIntoA()
            
            elif (msgClient =="_save" and isAdmin(nom)):  ### Sauvegarde l'annuaire courant
                saveDico()
                
            elif (msgClient =="_print" and isAdmin(nom)): ### Affiche le contenu de l'annuaire.
                self.connexion.send(afficherA().encode())
            #////////////////////////////////////////////////////////


            elif msgClient =="_list":
                self.connexion.send(listU().encode())
            elif msgClient =="_taille":
                self.connexion.send(tailleA().encode()) 
            elif msgClient =="_search":
                self.connexion.send("Entrez un element à rechercher: ".encode())
                rech=self.connexion.recv(128).decode()
                self.searchA(rech, GreenAnuaire)


            # Affiche les commandes disponibles selon les droits de l'utilisateur
            elif (msgClient =="_help" and isAdmin(nom)):
                self.printCmdAdmin()
            elif (msgClient =="_help" and isAdmin(nom) == 0):
                self.printCmdUser()


            # Affiche les droits de l'utilisateur courant
            elif (msgClient =="_droit"):
                if isAdmin(nom):
                     self.connexion.send("Vous etes Administrateur".encode())
                else:
                    self.connexion.send("Vous etes Utilisateur".encode())
                
            message = "%s> %s" % (nom, msgClient)
            print(message)


###########################################################################################
        # Fermeture de la connexion :
        nomTh=self.getName()
        # self.connexion.shutdown(socket.SHUT_RDWR)
        self.connexion.close()      # couper la connexion côté serveur
        del conn_client[nomTh]        # supprimer son entrée dans le dictionnaire
        print ("Client %s déconnecté." % nom)
        # Le thread se termine ici    

#######################################################################################


# Decommenter pour insérer quelques utilisteurs dans l'annuaire
#add("Burtin", "Graig", "burtin.graig@gmail.com", "Fondumonde", "Ingenieur", "083684876", "U")
#add("lepicard", "mael", "mael.lepicard@gmail.com", "Montrouge", "Ingenieur", "0669123442", "A","azerty")
#add("Admin1", "Admin1", "admin@hotmail.com", "ESGI", "Ingenieur", "123456789", "A")





try:     ### charge le fichier annuaire déja existant. Si il n'existe pas, il sera créé
    with open(ficAnnuaire, 'rb') as f:
        GreenAnuaire = pickle.load(f)       ### Dump le contenu de l'annuaire dans le fichier 
        print("Chargement du fichier annuaire '",ficAnnuaire,"'")
except:
    print("Fichier annuaire non trouvé, création du fichier '",ficAnnuaire,"'")
    print("Pour se connecter à l'annuaire, connectez vous sur le compte Admin par défaut")
    print("==> Login: admin, Password: ",adminDefaultPassword,"\n")
    saveDico()


######################  Lancement socket  #################################################################
# Initialisation du serveur - Définition du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ### Permet de réutilser le port 
    mySocket.bind((HOST, PORT))
except socket.error:
    print ("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()

print( "Serveur prêt, en attente de requêtes ...")
print( "Appuyez sur CTRL+C  pour quitter\n")

### Intercepte le signal SIGINT (ctrl+c) et termine proprement le programme.
def sigint_handler(signum, frame):
    global mySocket
    print("\nExiting GreenAnnuaire...")
    mySocket.close()
    sys.exit()
 
signal.signal(signal.SIGINT, sigint_handler)    # handle le sigint, et lance la fonction sigint_handler

mySocket.listen(5)  # Attente et prise en charge des connexions demandées par les clients :
conn_client = {}                # dictionnaire des connexions clients

while 1:    
    connexion, adresse = mySocket.accept()
    ### Créer un nouvel objet thread pour gérer la connexion :
    th = ThreadClient(connexion)
    th.start()

    ### Mémoriser la connexion dans le dictionnaire : 
    it = th.getName()        # identifiant du thread
    conn_client[it] = connexion
