# -*- coding: utf-8 -*-
from transition import Transition
from state import State
import os
import copy
import sp
from sp import *
from itertools import product
from automateBase import AutomateBase



class Automate(AutomateBase):
        
        def succElem(self, state, lettre):
                """State x str -> list[State]
                rend la liste des états accessibles à partir d'un état
                state par l'étiquette lettre
                """
                # successeurs : list[State]
                successeurs = []
                # t: Transitions
                for t in self.getListTransitionsFrom(state):
                        if t.etiquette == lettre and t.stateDest not in successeurs:
                                successeurs.append(t.stateDest)
                return successeurs

        def succ (self, listStates, lettre):
                """list[State] x str -> list[State]
                rend la liste des états accessibles à partir de la liste d'états
                listStates par l'étiquette lettre
                """
                #res : list[State]
                res = []
                #successeurs : list[State]
                successeurs = []

                for s in listStates:
                    successeurs = self.succElem(s,lettre)
                    for s1 in successeurs:
                        if(s1 not in res):
                            res = res + [s1]

			
		
                return res



        
        def acc(self):
                """ -> list[State]
                rend la liste des états accessibles
                """  
		         #res : list[State]
		         #res = []

		          
                return 



        """ Définition d'une fonction déterminant si un mot est accepté par un automate.
        Exemple :
                a=Automate.creationAutomate("monAutomate.txt")
                if Automate.accepte(a,"abc"):
                        print "L'automate accepte le mot abc"
                else:
                        print "L'automate n'accepte pas le mot abc"
        """
        @staticmethod
        def accepte(auto,mot) :
                """ Automate x str -> bool
                rend True si auto accepte mot, False sinon
                """
                #Ldep : list[State] , liste d'états de départ
                Ldep = auto.getListInitialStates()
                #Larr : list[State] , liste d'états d'arrivée
                Larr = []
                #Lm : list[Char], liste des lettres du mot
                Lm = [c for c in mot]
                
                #Lf : list[State] , liste d'états finaux
                Lf = auto.getListFinalStates()
                
                for i in range(0,len(mot)):
                    for s in Ldep: #s : etat courant
                        #succ : list[state] , liste des successeurs pour l'état courant
                        succ = auto.succElem(s,Lm[i])
                        Larr = Larr + succ
                        if(Larr == []):
                            return False
                        Ldep = Larr
                        Larr = []
                        
                for s in Ldep: #ici Ldep est en fait notre dernier Larr trouvée c'est à dire la liste finale des états successeurs. Il reste à vérifier si elle contient des états finaux.
                    if(s in Lf):
                        return True
                    else:
                        return False
                 



        @staticmethod
        def estComplet(auto,alphabet) :
                """ Automate x str -> bool
                rend True si auto est complet pour alphabet, False sinon
                """
                #Letats = list[State]
                Letats = auto.getListStates() #on récupère la liste de tout les états de l'automate
                for s in Letats: # s : State = etat courant. on parcourt tout les états
                    for c in alphabet:# c : char = lettre courante. on parcourt l'alphabet
                        if(auto.succElem(s,c) == []):
                            return False
                return True
        
        @staticmethod
        def estDeterministe(auto) :
                """ Automate  -> bool
                rend True si auto est déterministe, False sinon
                """
        		#Letats = list[State]
                Letats = auto.getListStates() #on récupère la liste de tout les états de l'automate
        
        		#alphabet : list[char]
                alphabet = auto.getAlphabetFromTransitions()
                
                if(len(alphabet)==0):
                    return True #cas trivial automate sans transition
                for s in Letats:
                    for c in alphabet:
                        if(len(auto.succElem(s,c))>1):
                            return False
                
                return True


       
        @staticmethod
        def completeAutomate(auto,alphabet) :
                """ Automate x str -> Automate
                rend l'automate complété d'auto, par rapport à alphabet
                """
                
                #autonew : Automate
                autonew = copy.deepcopy(auto) #on clone auto
                
                if(Automate.estComplet(auto,alphabet)):
                    return autonew #si l'automate est déjà complet, pas besoin de puit
                
                #Letats = list[State]
                Letats = auto.getListStates() #on récupère la liste de tout les états de l'automate
                #Lid = list[int]
                Lid = [s.id for s in Letats] #récupération de tout les id
                
                #puit = State
                
                puit = State(max(Lid)+1,False,False,"P") #on attribue bien un identifiant unique
                if(autonew.addState(puit)):
                    for s in Letats: 
                        for c in alphabet:
                            if(len(auto.succElem(s,c))==0):
                                autonew.addTransition(Transition(s,c,puit)) #création d'une transition vers le puit
                
                    for c in alphabet:
                        autonew.addTransition(Transition(puit,c,puit)) #rajout des boucles pour chaque lettre sur le puit
                
                return autonew


       
        @staticmethod
        def determinisation(auto) :
                """ Automate  -> Automate
                rend l'automate déterminisé d'auto
                """
                if(Automate.estDeterministe(auto)):
                    return auto
                
                #Lini = list[State]
                Lini = auto.getListInitialStates()
                
                #alphabet : list[String]
                alphabet = auto.getAlphabetFromTransitions()
                
                #cpt : int
                # servira d'id à nos nouveaux états, à incrémenter à chaque création d'état
                cpt = 0
                
                #Lt = list[Transition]
                Lt=[]
                
                #LS = list[State]
                LS = []
                
                #LSp : list[tuple(set[State],Bool,Bool,String]
                LSp = []
                
                #Eini : set[State]
                Eini = {s for s in Lini}
                
                #s0isFinal : boolean
                s0isFinal = False
                
                for s in Eini:
                    if(s.fin):
                        s0isFinal = True
                
                #labels0 : String
                labels0 = "{"
                cptbis = 0
                for s in Lini:
                    cptbis+=1
                    if(cptbis == len(Lini)):
                        labels0+= s.label + "}"
                    else:
                        labels0 += s.label +","
                #on a notre premier état, on l'ajoute à LS :
                LS.append(State(cpt,True,s0isFinal,labels0))
                cpt += 1
                
                #pseudo_s0 : tuple[set[State],Boolean,Boolean]
                pseudo_s0 = Eini
                
                LSp.append(pseudo_s0)
                
                # i : int, indice de l'état de départ courant
                i = 0
                
                # j'ai enlevé la partie "label" des pseudos états qui faisait foirer tout
                for E in LSp:
                    i += 1
                    d = 0
                    for c in alphabet:
                        #Lsucc = liste des successeurs
                        Ltemp = [e for e in E]
                        Lsucc = auto.succ(Ltemp,c) 
                        if(len(Lsucc)!= 0 ):
                            # label temporaire initialisé vide
                            labeltemp = "{"
                            # boolean temporaire à mettre à true si les successeurs contiennent un etat final
                            final = False
                            #boolean temp pour état initial
                            initial = False
                            #Pstemp : pseudo etat initialisé vide
                            Pstemp = ()
                            #Etemp = ensemble d'état temporaire
                            Etemp = set()
                            
                            #on créé les éléments de notre pseudo état
                            cptter = 0
                            for s in Lsucc:
                                cptter+= 1
                                if(cptter == len(Lsucc)):
                                    labeltemp += s.label + "}"
                                else:
                                    labeltemp += s.label +","
                                
                                Etemp.add(s)
                                if(s.fin):
                                    final = True
                                    
                                if(Lsucc == Lini):
                                    initial = True
                                    
                                Pstemp = Etemp
                            
                            if(Pstemp not in LSp):
                                LSp.append(Pstemp)
                                d += 1 
                                #on créé l'état correspondant
                                Stemp = State(cpt,initial,final,labeltemp)
                                cpt += cpt + 1
                                
                                LS.append(Stemp)
                                
                            Ttemp = Transition(LS[i-1],c,LS[i-1+d])
                            Lt.append(Ttemp)
                            
                return Automate(Lt)

                


        @staticmethod
        def complementaire(auto, alphabet):
                """ Automate x str -> Automate
                rend  l'automate acceptant pour langage le complémentaire du langage de auto
                """
                
                # il suffit de déterminiser puis compléter puis inverser les états finaux.
                #autonew : Automate
                autonew = copy.deepcopy(auto) #on clone auto
                
                #on le déterminise :
                if(not Automate.estDeterministe(auto)):
                    autonewdet = Automate.determinisation(autonew)
                else:
                    autonewdet = auto
                    
                #on le complete
                if(not Automate.estComplet(autonewdet,alphabet)):
                    autocomp = Automate.completeAutomate(autonewdet, alphabet)
                else:
                    autocomp = autonewdet
                    
                #on récupère la liste d'état
                Letat = autocomp.getListStates()
                
                
                #Liste d'état resultats
                Leres = []
                
                #liste de transition vide 
                Ltres = []
                
                #on construit la liste d'état en inversant le statut final
                for s in Letat:
                    stemp = State(s.id,s.init,not s.fin,s.label)
                    Leres.append(stemp)
                
                #on parcourt la liste d'état puis les transitions à chaque etat
                #a chaque transition on récupère l'état d'arrivée et son index
                #et on construit la transition correspondante de notre nouvel automate
                for i in range(0,len(Letat)):
                    Lt = auto.getListTransitionsFrom(Letat[i])
                    for t in Lt:
                        label = t.etiquette
                        j = Letat.index(t.stateDest)
                        Ltres.append(Transition(Letat[i],label,Letat[j]))
                     
                return Automate(Ltres)


     
        @staticmethod
        def intersection (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage l'intersection des langages des deux automates
                """
                
                #on va travailler sur des automates finis, déterministe et complets.
                auto1det = Automate.determinisation(auto1)
                auto2det = Automate.determinisation(auto2)
                
                
                alphabet1 = auto1.getAlphabetFromTransitions()
                alphabet2 = auto2.getAlphabetFromTransitions()
                
                alphabet = list(set(alphabet1 + alphabet2))
                
                auto1final = Automate.completeAutomate(auto1, alphabet)
                auto2final = Automate.completeAutomate(auto2, alphabet)
                
                
                #liste d'état vide :
                Leres = []
                
                #liste de transition vide :
                Lt = []
                
                
                #on initialise le process :
                Lini1 = auto1final.getListInitialStates()
                Lini2 = auto2final.getListInitialStates()
                
                #compteur pour attribution d'id
                cpt = 0
                
                L1 = auto1final.getListStates()
                L2 = auto2final.getListStates()
                #print("L1 = ",L1)
                #print("L2 = ",L2)

                #liste de label
                Llab = []
                
                for s1 in L1:
                    for s2 in L2:
                        for c in alphabet:
                            #Initialisation de Sdep et SuccTemp:
                            Sdep = None
                            SuccTemp = None

                            #ajout de l'état courrant
                            labelcourrant = "("+s1.label+","+s2.label+")"
                            if(labelcourrant not in Llab):
                                #on peut créé l'état de départ courrant:
                                Sdep = State(cpt,(s1.init and s2.init),(s1.fin and s2.fin),labelcourrant)
                                #ajout à Leres:
                                Leres.append(Sdep)
                                #ajout du label:
                                Llab.append(labelcourrant)
                                
                           

                            else :
                                for s in Leres:
                                    if(s.label == labelcourrant):
                                        Sdep = s

                            #print("Sdep :",Sdep)


                            #liste des successeurs. contient exactement 1 état car auto1 deterministe et complet
                            Lsucc1 = auto1final.succElem(s1,c) 
                            # l'état successeur
                            s1succ = Lsucc1[0]
                            #idem que pour auto1
                            Lsucc2 = auto2final.succElem(s2,c)
                            s2succ = Lsucc2[0]
                            labeltemp = "("+s1succ.label+","+s2succ.label+")"
                            #print("s1 succ =", s1succ,"s2 succ = ",s2succ)
                            if(labeltemp not in Llab):
                                # on créé notre état d'arrivé basé sur le couple s1,s2
                                SuccTemp = State(cpt,(s1succ.init and s2succ.init),(s1succ.fin and s2succ.fin),labeltemp)
                                cpt+= 1
                                #on ajoute notre état à la liste 
                                Leres.append(SuccTemp)
                                #on ajoute le label à la liste label
                                Llab.append(labeltemp)

                            else:
                                for s in Leres:
                                    if(s.label == labeltemp):
                                        SuccTemp = s
                            #print("SuccTemp : ",SuccTemp)
                            #on créé une transition avec nos etats basés sur les couples
                            TransitionTemp = Transition(Sdep,c,SuccTemp)
                            #print("TransitionTemp :",TransitionTemp)
                            
                            # on rajoute la transition à notre liste
                            if(TransitionTemp not in Lt):
                                Lt.append(TransitionTemp)
                            #print("Lt = ",Lt)
  
   
                #print("Leres = ", Leres)
                return Automate(Lt,Leres)


        @staticmethod
        def union (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage l'union des langages des deux automates
                """
                
                auto1b = copy.deepcopy(auto1)
                auto2b = copy.deepcopy(auto2)
                #on rajoute des préfixes
                auto2b.prefixStates(2)
                
                Lt = auto1b.listTransitions + auto2b.listTransitions
                
                
                return Automate(Lt)


        
       
        @staticmethod
        def concatenation (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage la concaténation des langages des deux automates
                """
                
                
                #on déterminise et complète
                auto1det = Automate.determinisation(auto1)
                auto2det = Automate.determinisation(auto2)
                #on change les IDs et labels du deuxième automate pour pas avoir d'états doublons
                auto2det.prefixStates(2)
                
                #on complete
                auto1final = Automate.completeAutomate(auto1det, auto1det.getAlphabetFromTransitions())
                auto2final = Automate.completeAutomate(auto2det, auto2det.getAlphabetFromTransitions())
                
                #on change l'ID du puit du deuxième pour éviter les doublons/ambiguité.
                for s in auto2final.listStates:
                    if s.label == "P":
                        s.insertPrefix(2)
                
                #On récupère les listes des états de chaque automate
                Ls1 = auto1final.getListStates()
                Ls2 = auto2final.getListStates()
                #et les listes spécifiques d'états initiaux et finaux:
                Linia1 = auto1final.getListInitialStates()
                Lfina1 = auto1final.getListFinalStates()
                Linia2 = auto2final.getListInitialStates()
                Lfina2 = auto2final.getListFinalStates()
                #booléen qui indique si l'état initial de a1 est aussi final
                b = Linia1[0].init and Linia1[0].fin
                if(b):
                    Linia2[0] = State(Linia2[0].id,False,Linia2[0].fin,Linia2[0].label)
                
                
                #Lt : liste de transition finale:
                Lt=[]
                #Liste d'état finale
                Leres = []
                #on récupère l'alphabet de A1
                alphabet1 = auto1final.getAlphabetFromTransitions()
                #on parcourt les états de A1.
                for s in auto1final.listStates:
                    for c in alphabet1:
                        #pour chaque lettre on récupère le successeur (déterministe = il y en a 1 seul)
                        Lsucc = auto1final.succElem(s, c)
                        
                        #on vire un cas inutile : notre état de départ est un état final de A1,
                        #et il n'est pas un état initial, et sa destination n'est pas finale 
                        if(s.fin and (not s.init) and (not Lsucc[0].fin)):
                            break
                            
                        #S'il n'est pas final on ajoute une transition copie conforme
                        if not Lsucc[0].fin:
                            Ttemp = Transition(s,c,Lsucc[0])
                            if(Ttemp not in Lt):
                                Lt.append(Ttemp)
                            Leres.append(s)
                            Leres.append(Lsucc[0])
                        #s'il est final on ajoute une transition vers l'initial de A2.
                        else:
                            Ttemp = Transition(s,c,Linia2[0])
                            Lt.append(Ttemp)
                            Leres.append(s)
                            Leres.append(Linia2[0])
                
                #alphabet de A2:
                alphabet2 = auto2final.getAlphabetFromTransitions()
                #on parcourt les états de A2:
                for s in auto2final.listStates:
                    for c in alphabet2:
                        sbis = s
                        #si on est sur l'état initial on prend notre état initial modifié
                        if s.init:
                            sbis = Linia2[0]
                            
                        Lsucc = auto2final.succElem(s,c)

                        Ttemp = Transition(sbis,c,Lsucc[0])
                        if Ttemp not in Lt:
                            Lt.append(Ttemp)
                        Leres.append(sbis)
                        Leres.append(Lsucc[0])
                        
                #Suppression des doublons de Leres:
                Leres = list(set(Leres))
                                
                return Automate(Lt)

       
        @staticmethod
        def etoile (auto):
                """ Automate  -> Automate
                rend l'automate acceptant pour langage l'étoile du langage de a
                """
                
                autodet = Automate.determinisation(auto)
                Lt = autodet.listTransitions
                
                Si = autodet.getListInitialStates()[0]
                
                for t in autodet.listTransitions:
                    if t.stateDest.fin:
                        tb = Transition(t.stateSrc,t.etiquette,Si)
                        Lt.append(tb)
                        
                        
                return Automate(Lt)
