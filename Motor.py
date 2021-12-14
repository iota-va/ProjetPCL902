# -*- coding: utf-8 -*-
"""
Created on Fri Sep  10 09:00:00 2021

@author: KESTEL Samuel
"""

import time

#%% pour voir le port de connection
# print([comport.device for comport in serial.tools.list_ports.comports()])


#%% ouverture communication avec le port
#board = pyf.Arduino('COM3')

class Motor :

    def __init__(self, instrument):
        self.instrument = instrument

#%%déplacement horaire de 7.2 degrés pour réglage
    def h (self):
        ts = 0.1
        for i in range(4,8):
            self.instrument.digital[i].write(1)  # chaque etape fait tourner de 1.8° donc la boucle fait
            time.sleep(ts)  # tourner de 7,2°
            self.instrument.digital[i].write(0)


#%%déplacement antihoraire de 7.2 degrés pour réglage
    def a (self):
        ts = 0.1
        for i in range(4,8):
            self.instrument.digital[11-i].write(1)  # chaque etape fait tourner de 1.8° donc la boucle fait
            time.sleep(ts)  # tourner de 7,2°
            self.instrument.digital[11-i].write(0)


#%% placement pour démarrer au bon endroit (il faut déjà se placer à presque 0° mais du coté moins si cela n'est pas bien obtenu, utiliser les fonction a() et h()
    def zero (self) :
        self.a()
        time.sleep(0.0001)
        self.h()
        time.sleep(0.0001)


#%% fonction de balayage par pas(fct de mesure a placer)
    def sens_horaire2(self, angle, pas, ti, step):  #pas variable et multiple de 0.9° -> il faut definir des angles multiples de 0.9°
        an = 0                                #ti=temps d'intégration (dépend de la constante de temps de la détection
        PAS = int(pas / 0.9)                  #step est la borne de départ
        ts = 0.01
        TS = 0
        step = float(step)
        while angle > an:                       #tant que l'angle parcourru n'a pas atteint la valeur souhaité

            time.sleep(ti)

            for i in range(0, PAS):             #tant que le pas voulu n'est pas obtenue on fait tourner le moteur (par demi-pas de moteur d'où le float

                if step - int(step) == 0:       # si le code allumage (~borne à allumer) prend une valeur complète

                    self.instrument.digital[int(step)].write(1)   #allumage de la borne
                    time.sleep(ts)
                    an = an + 0.9
                    step = step + 0.5

                    self.instrument.digital[int(step)].write(0)   #extinction de la borne
                    time.sleep(TS)

                else:                           # si le code allumage (~borne à allumer) n'est pas un entier->allumage de deux bornes successives
                    if step != 7.5:
                        self.instrument.digital[int(step)].write(1)
                        self.instrument.digital[int(step) + 1].write(1)
                        time.sleep(ts)

                        an = an + 0.9
                        step = step + 0.5
                        self.instrument.digital[int(step)].write(0)
                        self.instrument.digital[int(step)-1].write(0)
                        time.sleep(TS)

                    else:                               #modification pour la valeur 7.5 afin dallumer la 7 et la 4 puis retourner à step=4
                        self.instrument.digital[int(step)].write(1)
                        self.instrument.digital[4].write(1)
                        time.sleep(ts)

                        an = an + 0.9
                        step = 4.0
                        self.instrument.digital[int(step)].write(0)
                        self.instrument.digital[int(7.0)].write(0)
                        time.sleep(TS)

        #fonction de mesure à placer


#%% fonction placement angle de départ de mesure
    def initialisation(self, ai):       #reprise de la fonction initialisation avec modif pour tourner dans le sens inverse
        self.isInitialize = False
        an = 0
        step = float(4)
        while ai > an:
            if step - int(step) == 0.5:

                self.instrument.digital[int(step)].write(1)
                time.sleep(0.01)
                self.instrument.digital[int(step)].write(0)
                time.sleep(0)
                an = an + 0.9
                step = step - 0.5


            else:
                if step != 4 :
                    self.instrument.digital[int(step)].write(1)
                    self.instrument.digital[int(step) - 1].write(1)
                    time.sleep(0.01)
                    self.instrument.digital[int(step)].write(0)
                    self.instrument.digital[int(step) - 1].write(0)
                    time.sleep(0)

                    an = an + 0.9
                    step = step - 0.5


                else:
                    self.instrument.digital[int(step)].write(1)
                    self.instrument.digital[7].write(1)
                    time.sleep(0.01)
                    self.instrument.digital[int(step)].write(0)
                    self.instrument.digital[7].write(0)
                    time.sleep(0)
                    an = an + 0.9
                    step = 7.5
        return self.isInitialize == True



#%%fonction de mesure complète (initialisation+sens_horaire2)
    def mesure_auto(self,angle,pas, ti, step):

        self.initialisation(angle)
        time.sleep(0.1)
        self.sens_horaire2(2*angle, pas, ti, step)

#board.exit()  pour couper la liaison avec l'arduino -> une fois l'expérience finie