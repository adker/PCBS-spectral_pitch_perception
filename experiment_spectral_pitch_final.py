import random
import numpy as np
import expyriment
from  expyriment.stimuli import BlankScreen
from  expyriment import misc
import scipy.io.wavfile  # for scipy.io.wavfile.read
import simpleaudio as sa # to play sound
import os

###############################################################################################################################################################
# Useful functions for sounds reading
#####################################

def load_sound(filename):
    [sample_rate, audio_data] = scipy.io.wavfile.read(filename)
    # normalise
    audio_norm = audio_data*(32767 / np.max(np.abs(audio_data)))
    return [sample_rate, audio_norm]

def play_sound(nparray, sample_rate=44100):
    audio = nparray[:]
    # convert to 16-bit data
    audio = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

def present_visual_stimuli():
    # Paire 1
    square_paire_1.present()
    exp.clock.wait(duree_son*1000*2+duree_intra_stim*1000)
    blankscreen.present()
    exp.clock.wait(duree_inter_stim*1000)
    # Paire 2
    square_paire_2.present()
    exp.clock.wait(duree_son*1000*2+duree_intra_stim*1000)
    blankscreen.present()

def ask_for_response():
    expyriment.stimuli.TextScreen("",
        """
        Which pair was the best match ?\n\n\n
        press [left arrow] if it is the first\n\n
        press [right arrow] if it is the second
        """).present()
    key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])
    if key == expyriment.misc.constants.K_LEFT:
        reponse = 'first_best'
    else:
        reponse = 'second_best'
    return reponse, rt

def ask_for_confidence():
    expyriment.stimuli.TextScreen("",
        """
        How confident are you ?\n\n\n
        [1] confident\n\n
        [2] not really confident\n\n
        [3] answered by chance (no pair really matched)
        """).present()
    key_c, rt_conf = exp.keyboard.wait([expyriment.misc.constants.K_1, expyriment.misc.constants.K_2, expyriment.misc.constants.K_3])

    if key_c == expyriment.misc.constants.K_1:
        confidence = 1
    elif key_c == expyriment.misc.constants.K_2:
        confidence = 2
    else:
        confidence = 3
    blankscreen.present()
    return confidence, rt_conf

##############################################################################################################################################################
# Initialisation
#################

path_stim = os.path.join(os.getcwd(),'stimuli')
exp = expyriment.design.Experiment(name="Spectral pitch experiment")
exp.add_data_variable_names(['clock', 'trial', 'Stimulus_label', 'comparaison', 'zone_fc', 'ordre', 'f0', 'Occurence', 'Response_test', 'Response_entrainement', 'RT_reponse', 'Confidence', 'RT_conf', 'Entrainement_ou_test'])
exp.add_experiment_info("""
    clock = instant de reponse
    trial = numero du trial
    Stimulus_label = caracteristiques du stimulus
    comparaison = quel comparaison etait demandee, 4 niveaux:
        - entre (fc-1)*f0 et (fc-0.5f0) avec le centroide a (fc-0.5f0)
        - entre (fc)*f0 et (fc-0.5f0) avec le centroide a (fc-0.5f0)
        - entre (fc)*f0 et (fc-0.25f0) avec le centroide a (fc-0.25f0)
        - entre (fc)*f0 et (fc+0.25f0) avec le centroide a (fc+0.25f0)
    fc = zone du spectre ou ce trouve le centroide spectral, 3 niveaux:
        - autour de l'harmonique de rang 7 (partiels resolus)
        - autour de l'harmonique de rang 11 (patiels mal resolus)
        -autour de l'harmonique de rang 13 (partiels non resolus)
    ordre = ordre dans lequel sont presentees les paires de sons, 2 niveaux
        - 1 = pattern 'escalier' en premier
        - 2 = pattern 'lineaire' en premier
    f0 = frequence fondamentale (2 niveaux: 200 ou 220 Hz)
    Occurence = rang d occurence de ce stimulus
    Response_test = 0 ou 1 selon la paire choisie (premiere ou deuxième)
    Response_entrainement = True si la réponse du participant est correcte
    RT_reponse
    Confidence
    RT_conf
    Entrainement_ou_test = indique dans quelle phase on se trouve
    """)

## Develop mode, à commenter pour faire passer l'exp !
#expyriment.control.set_develop_mode(on=True)

expyriment.control.initialize(exp)

#############################################################################################################################################################
# Generation des stimuli
########################

# Parameters
# si changement, modifier aussi le script matlab de generation des stimuli
nb_comparaison = 4          # regarder le code matlab de generation des stimuli
nb_fc = 3           # regarder le code matlab de generation des stimuli
nb_rep = 3          # regarder le code matlab de generation des stimuli
nb_ordre = 2        # regarder le code matlab de generation des stimuli
nb_f0 = 2
nb_trials = nb_comparaison*nb_fc*nb_rep*nb_ordre*nb_f0
nb_trials_entrainement = nb_comparaison*nb_fc*2*nb_ordre*nb_f0 # one less block

# uncomment to go quickly through all phases of the experiement:
#nb_trials = 2
#nb_trials_entrainement = 2

iti = 500 # inter trial interval
duree_son = .5
duree_intra_stim = 0.1
duree_inter_stim = 0.5

# Construction des vecteurs "silence" à mettre entre les sons
Fe, son_courant = load_sound(r"{p}\comparaison_1_fc_1_ordre_1_f0_1_sin1.wav".format(p = path_stim)) # get Fe
nb_index_duree = np.int(duree_son*Fe)
nb_index_intra_stim = np.int(duree_intra_stim*Fe)
nb_index_inter_stim = np.int(duree_inter_stim*Fe)
silence_intra = np.zeros(nb_index_intra_stim)
silence_inter = np.zeros(nb_index_inter_stim)

exp.add_experiment_info("duree de chaque son: {s}, duree entre les sons de chaque paire: {p}, duree entre chaque paire: {i}".format(s = duree_son, p = duree_intra_stim, i = duree_inter_stim))

# Génération/construction/randomisation des stimuli
# Pour phase de test
liste_stim = []
for rep in range(nb_rep):
    liste_provisoire = []
    for f0 in range(nb_f0):
        for ordre in range(nb_ordre):
            for fc in range(nb_fc):
                for comparaison in range(nb_comparaison):
                    label = "comparaison_{c}_fc_{fc}_ordre_{o}_f0_{f}".format(c = comparaison+1, fc = fc+1, o = ordre+1, f = f0+1)
                    Fe, son_courant = load_sound(r"{p}\{l}_son.wav".format(p = path_stim, l = label))
                    Fe, sin1_courant = load_sound(r"{p}\{l}_sin1.wav".format(p = path_stim, l = label))
                    Fe, sin2_courant = load_sound(r"{p}\{l}_sin2.wav".format(p = path_stim, l = label))
                    # Construction du stimulus
                    # on interpole les silences et on ne prend que les longeurs de sons désirées
                    sin1_courant = sin1_courant[:nb_index_duree]
                    sin2_courant = sin2_courant[:nb_index_duree]
                    son_courant = son_courant[:nb_index_duree]
                    stimulus_1 = np.concatenate((sin1_courant,silence_intra,son_courant))
                    stimulus_2 = np.concatenate((sin2_courant,silence_intra,son_courant))
                    stimulus_courant = np.concatenate((stimulus_1,silence_inter,stimulus_2))
                    liste_provisoire.append((stimulus_courant,label, comparaison+1, fc+1, ordre+1, f0+1, rep+1))
    np.random.shuffle(liste_provisoire)
    liste_stim = liste_stim+liste_provisoire

# Pour deuxième phase d'entrainement
liste_entrainement2 = []
for f0 in range(nb_f0, 4):
    for ordre in range(nb_ordre):
        for fc in range(nb_fc):
            for comparaison in range(nb_comparaison):
                label = "comparaison_{d}_fc_{fc}_ordre_{o}_f0_{f}".format(d = comparaison+1, fc = fc+1, o = ordre+1, f = f0+1)
                Fe, son_courant = load_sound(r"{p}\{l}_son.wav".format(p = path_stim, l = label))
                Fe, sin1_courant = load_sound(r"{p}\{l}_sin1.wav".format(p = path_stim, l = label))
                Fe, sin2_courant = load_sound(r"{p}\{l}_sin2.wav".format(p = path_stim, l = label))
                sin1_courant = sin1_courant[:nb_index_duree]
                sin2_courant = sin2_courant[:nb_index_duree]
                son_courant = son_courant[:nb_index_duree]
                stimulus_1 = np.concatenate((sin1_courant,silence_intra,son_courant))
                stimulus_2 = np.concatenate((sin2_courant,silence_intra,son_courant))
                stimulus_courant = np.concatenate((stimulus_1,silence_inter,stimulus_2))
                liste_entrainement2.append((stimulus_courant,label, comparaison+1, fc+1, ordre+1, f0+1))
np.random.shuffle(liste_entrainement2)

# Pour première phase d'entrainement
liste_entrainement1 = []
for rep in range(2): # one less repetion than on the test phase to keep the experiment not too long
    liste_provisoire = []
    for f0 in range(nb_f0):
        for ordre in range(nb_ordre):
            for fc in range(nb_fc):
                for comparaison in range(nb_comparaison):
                    label = "comparaison_{d}_fc_{fc}_ordre_{o}_f0_{f}".format(d = comparaison+1, fc = fc+1, o = ordre+1, f = f0+1)
                    Fe, sin1_courant = load_sound(r"{p}\{l}_sin1.wav".format(p = path_stim, l = label))
                    Fe, sin2_courant = load_sound(r"{p}\{l}_sin2.wav".format(p = path_stim, l = label))
                    # Construction du stimulus
                    # on interpole les silences et on ne prend que les longeurs de sons désirées
                    sin1_courant = sin1_courant[:nb_index_duree]
                    sin2_courant = sin2_courant[:nb_index_duree]
                    if np.random.randint(2, size=1):
                        # la première paire est identique
                        stimulus_1 = np.concatenate((sin1_courant,silence_intra,sin1_courant))
                        stimulus_2 = np.concatenate((sin2_courant,silence_intra,sin1_courant))
                        stimulus_courant = np.concatenate((stimulus_1,silence_inter,stimulus_2))
                        bonne_rep = 1
                    else:
                        # la deuxième paire est identique
                        stimulus_1 = np.concatenate((sin1_courant,silence_intra,sin2_courant))
                        stimulus_2 = np.concatenate((sin2_courant,silence_intra,sin2_courant))
                        stimulus_courant = np.concatenate((stimulus_1,silence_inter,stimulus_2))
                        bonne_rep = 2
                    liste_provisoire.append((stimulus_courant,label, comparaison+1, fc+1, ordre+1, f0+1, rep+1, bonne_rep))
    np.random.shuffle(liste_provisoire)
    liste_entrainement1 = liste_entrainement1+liste_provisoire


# Préparation des stimuli visuels
square_paire_1 = expyriment.stimuli.Rectangle((50, 50), position=(-150, 0), colour = misc.constants.C_RED)
square_paire_1.preload()
square_paire_2 = expyriment.stimuli.Rectangle((50, 50), position=(150, 0), colour = misc.constants.C_RED)#+expyriment.stimuli.Rectangle((50, 50), position=(-150, 0), colour = misc.constants.C_RED)
square_paire_2.preload()

blankscreen = BlankScreen()

######################################################################################################################################################################""

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Starting experiment @@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#####################################################################################################################################################################
#@@@@@@@@@@@@@@@@@@@@@@@
# Phase d'introduction
#@@@@@@@@@@@@@@@@@@@@@@@

expyriment.control.start(skip_ready_screen = True)

expyriment.stimuli.TextScreen(
    "At each trial you are going to listen to pairs of sounds",
    "Press the left or the right arrow to choose which of the two pairs is the best match\n\nhint: you should focus on high frequencies !").present()
exp.keyboard.wait()

expyriment.stimuli.TextScreen("",
    "For example this pair is a good match because we can hear the first sound in the second ...").present()
exp.clock.wait(1000)
Fe, son_example = load_sound(r"{p}\son_example.wav".format(p = path_stim))
Fe, sin_good_example = load_sound(r"{p}\sin_good_example.wav".format(p = path_stim))

play_sound(sin_good_example[:nb_index_duree], Fe)
exp.clock.wait(duree_son*1000++duree_intra_stim*1000)
play_sound(son_example[:nb_index_duree], Fe)
exp.clock.wait(duree_son*1000)
exp.keyboard.wait()

expyriment.stimuli.TextScreen("",
    "... and this pair is a 'bad' match because the two sounds are very different one of each other").present()
exp.clock.wait(1000)
Fe, sin_bad_example = load_sound(r"{p}\sin_bad_example.wav".format(p = path_stim))

play_sound(sin_bad_example[:nb_index_duree], Fe)
exp.clock.wait(duree_son*1000+duree_intra_stim*1000)
play_sound(son_example[:nb_index_duree], Fe)
exp.clock.wait(duree_son*1000)
exp.keyboard.wait()

expyriment.stimuli.TextScreen("",
    """
    Sometimes it is not easy to tell the difference\n between the pairs ...\n\n
    and sometimes there is no perfect pair so you just have to\n choose the best one !\n\n
    At the end of every trial you are going to be asked \nhow confident you feel about your answer:\n [key 1] confident\n[key 2] not sure\n[key 3] answered by chance (no pair really matched)\n\n
    """).present()
exp.keyboard.wait()

blankscreen.present()

clock = expyriment.misc.Clock()

###########################################################################################################################################################################################################################
#@@@@@@@@@@@@@@@@@@@@@@@
#Phase d'entrainement 1
#@@@@@@@@@@@@@@@@@@@@@@@

expyriment.stimuli.TextScreen("First training phase",
    """
    You are going to compare pure tones\n
    Press the [space] key when you are ready !
    """).present()
exp.keyboard.wait(expyriment.misc.constants.K_SPACE)

for nb_s in range(nb_trials_entrainement):
#for nb_s in range(3):

    expyriment.stimuli.TextLine("Training {s} on {t}".format(s = nb_s+1, t = nb_trials_entrainement)).present()
    exp.clock.wait(1000)

    time = clock.time

    stimulus, label, comparaison, fc, ordre, f0, repetition, bonne_reponse = liste_entrainement1[nb_s]

    # Play audio stimulus
    play_sound(stimulus, Fe)

    # Present visual stimuli
    present_visual_stimuli()

    # Reponse
    reponse, rt = ask_for_response()

    # Give feadback
    if ((reponse == 'first_best') & (bonne_reponse == 1)) or ((reponse == 'second_best') & (bonne_reponse == 2)):
         expyriment.stimuli.TextLine("Ok !").present()
    else:
        expyriment.stimuli.TextLine("No ...").present()
    exp.keyboard.wait()
    blankscreen.present()

    # Save data
    exp.data.add([time, nb_s+1, label, comparaison, fc, ordre, f0, repetition,'NA', (reponse == bonne_reponse), rt, 'NA', 'NA', 'entrainement'])

##############################################################################################################################################################################################""
#@@@@@@@@@@@@@@@@@@@@@@@
#Phase d'entrainement 2
#@@@@@@@@@@@@@@@@@@@@@@@

expyriment.stimuli.TextScreen("Second training phase (shorter)",
    """
    Press the [space] key when you are ready !
    """).present()
exp.keyboard.wait(expyriment.misc.constants.K_SPACE)

nb_trial_entrainement = 5 # à choisir

for nb_s in range(nb_trial_entrainement):
#for nb_s in range(3):

    expyriment.stimuli.TextLine("Trial {s} on {t}".format(s = nb_s+1, t = nb_trial_entrainement)).present()
    exp.clock.wait(1000)

    time = clock.time

    stimulus, label, comparaison, fc, ordre, f0 = liste_entrainement2[nb_s]

    # Play audio stimulus
    play_sound(stimulus, Fe)

    # Present visual stimuli
    present_visual_stimuli()

    # Reponse
    reponse, rt = ask_for_response()
    confidence, rt_conf = ask_for_confidence()

    exp.clock.wait(iti)

##############################################################################################################################################################################
#@@@@@@@@@@@@@@@@@@@@@@
#Phase de test @@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@

expyriment.stimuli.TextScreen("Now the real experiment begins !",
    """
    Press the [space] key when you are ready !
    """).present()
exp.keyboard.wait(expyriment.misc.constants.K_SPACE)

for nb_s in range(nb_trials):
#for nb_s in range(3):

    expyriment.stimuli.TextLine("Trial {s} on {t}".format(s = nb_s+1, t = nb_trials)).present()
    exp.clock.wait(1000)

    time = clock.time

    stimulus, label, comparaison, fc, ordre, f0, repetition= liste_stim[nb_s]

    # Play audio stimulus
    play_sound(stimulus, Fe)

    # Present visual stimuli
    present_visual_stimuli()

    # Reponse
    reponse, rt = ask_for_response()
    confidence, rt_conf = ask_for_confidence()

    # Save data
    exp.data.add([time, nb_s+1, label, comparaison, fc, ordre, f0, repetition, reponse, 'NA', rt, confidence, rt_conf, 'test'])
    exp.clock.wait(iti)

expyriment.control.end()
