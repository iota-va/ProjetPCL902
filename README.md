# ProjetPCL902

Partie code pour le projet tutoré de PCL902

Auteurs : ALFONSO Vincent, DEPELSEMACKER Karl, KESTEL Samuel

Professeur : HORNY Nicolas

Ce dossier comporte quatre fichiers python et un dossier venv pour l'environnement virtuel.

## Motor.py

`Motor.py` est la librairie servant à contrôler le moteur pas-à-pas connecté à un Arduino.

On peut faire tourner le moteur dans un sens ou dans l'autre grâce aux méthodes `h()` (horaire) et `a()` (antihoraire).

Le mouvement pour les mesures est effectué à l'aide de la méthode `mesure_auto()` qui prend en compte l'initialisation et le déplacement horaire et antihoraire du moteur.

## Detection_synchrone.py

Cette librairie permet la communication avec la détection synchrone.

La méthode `lockin_set_freq()` permet de sélectionner la fréquence cible.

`lockin_time_const()` est utilisée pour choisir le temps d'intégration.

Pour sélectionner la sensibilité voulue, ce sera la méthode `lockin_sensitivity()`.

La dernière méthode `initialize_lockin()` permet de changer l'harmonique, le courant, la tension, le mode du courant, l'offset (mV), l'amplitude (mV) et la source utilisée. 

## Interface.py

C'est avec ce fichier que l'expérience est contrôlée. L'interface est divisée en quatre parties :

**Motor** : connecter et entrer les paramètres utiles au moteur.

**Lock-In** : connecter et entrer les paramètres utiles à la détection synchrone.

**Graphic** : faire les mesures et tracer le fit des résultats

**Measure** : affichage des données des mesures et du fit dans un tableau 

## setup.py

`setup.py` est le fichier qui sert à rendre notre interface graphique exécutable sur Windows. Pour cela il faut lancer le programme.

Un problème a été aperçu. Le fichier `pyvisa.resources.resource.pyc` est manquant dans le dossier `dist`. 

Pour régler cela, chercher `pyvisa.resources.resource.py` dans la librairie pyvisa et faire la commande suivante dans une console python :

`import py_compile`

`py_compile.compile("NOM_DU_FICHIER.py")`

Après cela, mettre le fichier obtenu dans `library.zip`.

**ATTENTION** : Vérifier le nom du port utilisé pour l'arduino et le changer si besoin à la ligne 205 du code `Interface.py`