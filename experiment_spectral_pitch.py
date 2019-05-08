import random
import numpy as np
import expyriment
from  expyriment.stimuli import BlankScreen
from  expyriment import misc
import scipy.io.wavfile  # for scipy.io.wavfile.read
import simpleaudio as sa# to play sound
import os


## Useful functions for sounds reading
def load_sound_as_array(filename):
    [sample_rate, audio_data] = scipy.io.wavfile.read(filename)
    return [sample_rate, audio_data]

def play_mono(nparray, sample_rate=44100):
    audio = nparray[:]
    #normalise
    audio_norm = audio*(32767 / np.max(np.abs(audio)))
    # convert to 16-bit data
    audio_norm = audio_norm.astype(np.int16)
    play_obj = sa.play_buffer(audio_norm, 1, 2, sample_rate)
    # wait for playback to finish before exiting
    play_obj.wait_done()


path_stim = os.path.join(os.getcwd(),'stimuli')

## Initialisation
exp = expyriment.design.Experiment(name="Spectral pitch experiment")  # create an Experiment object
exp.add_data_variable_names(['clock', 'trial', 'Stimulus', 'Response', 'RT_reponse', 'Felt_chance', 'RT_chance'])
exp.add_experiment_info("duree de chaque son:{s}, duree entre les sons de chaque paire:{p}, duree entre chauqe paire:{i}".format(s = duree_son, p = nb_index_intra_stim, i = nb_index_inter_stim))

## Develop mode, à commenter pour faire passer l'exp !
expyriment.control.set_develop_mode(on=True)

expyriment.control.initialize(exp)

## Stimuli parameters
# si changement, modifier aussi le script matlab de generation des stimuli
nb_decalages = 5    # regarder le code matlab de generation des stimuli
nb_fc = 3           # regarder le code matlab de generation des stimuli
nb_rep = 2          # regarder le code matlab de generation des stimuli
nb_ordre = 2        # regarder le code matlab de generation des stimuli

Fe, son_courant = load_sound_as_array(r"{p}\1_1_1_1_son.wav".format(p = path_stim))

duree_son = .5
duree_intra_stim = 0.1
duree_inter_stim = 0.5

nb_index_duree = np.int(duree_son*Fe)
nb_index_intra_stim = np.int(duree_intra_stim*Fe)
nb_index_inter_stim = np.int(duree_inter_stim*Fe)


# Génération des labels des stimuli

liste_stim = []
for rep in range(nb_rep):
    for ordre in range(nb_ordre):
        for fc in range(nb_fc):
            for decalage in range(nb_decalages):
                label = "{d}_{f}_{o}_{r}".format(d = decalage+1, f = fc+1, o = ordre+1, r = rep+1)

                Fe, son_courant = load_sound_as_array(r"{p}\{d}_{f}_{o}_{r}_son.wav".format(p = path_stim, d = decalage+1, f = fc+1, o = ordre+1, r = rep+1))
                Fe, sin1_courant = load_sound_as_array(r"{p}\{d}_{f}_{o}_{r}_sin1.wav".format(p = path_stim, d = decalage+1, f = fc+1, o = ordre+1, r = rep+1))
                Fe, sin2_courant = load_sound_as_array(r"{p}\{d}_{f}_{o}_{r}_sin2.wav".format(p = path_stim, d = decalage+1, f = fc+1, o = ordre+1, r = rep+1))
                liste_stim.append((son_courant,sin1_courant,sin2_courant,label))

# Randomise stimuli
# separately for each repetition
liste_stim_rep1 = liste_stim[:int(len(liste_stim)/nb_rep)]
liste_stim_rep2 = liste_stim[int(len(liste_stim)/nb_rep):]
np.random.shuffle(liste_stim_rep1)
np.random.shuffle(liste_stim_rep2)
liste_stim = liste_stim_rep1+liste_stim_rep2

nb_trials = len(liste_stim)
#duree_paire = (duree_son*2 + duree_intra_stim) *1000 # ms

iti = 1000 # inter trial interval

# Préparation des stimuli visuels
square_paire_1 = expyriment.stimuli.Rectangle((50, 50), position=(-150, 0), colour = misc.constants.C_RED)
square_paire_1.preload()
square_paire_2 = expyriment.stimuli.Rectangle((50, 50), position=(150, 0), colour = misc.constants.C_RED)#+expyriment.stimuli.Rectangle((50, 50), position=(-150, 0), colour = misc.constants.C_RED)
square_paire_2.preload()

blankscreen = BlankScreen()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Starting experiment @@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Phase d'introduction
expyriment.control.start(skip_ready_screen = True)

expyriment.stimuli.TextScreen(
    "At each trial you are going to listen to pairs of sounds",
    "Press the left or the right arrow to choose which of the two pairs is the best match\n\nhint: you should focus on high frequencies !").present()
exp.keyboard.wait()

expyriment.stimuli.TextScreen("",
    "For example this pair is a good match because we can hear the first sound in the second ...").present()
exp.clock.wait(1000)
Fe, son_example = load_sound_as_array(r"{p}\son_example.wav".format(p = path_stim))
Fe, sin_good_example = load_sound_as_array(r"{p}\sin_good_example.wav".format(p = path_stim))

play_mono(sin_good_example[:nb_index_duree], Fe)
exp.clock.wait(duree_intra_stim*1000)
play_mono(son_example[:nb_index_duree], Fe)
exp.keyboard.wait()

expyriment.stimuli.TextScreen("",
    "... and this pair is a 'bad' match because the two sounds are very different one of each other").present()
exp.clock.wait(1000)
Fe, sin_bad_example = load_sound_as_array(r"{p}\sin_bad_example.wav".format(p = path_stim))

play_mono(sin_bad_example[:nb_index_duree], Fe)
exp.clock.wait(duree_intra_stim*1000)
play_mono(son_example[:nb_index_duree], Fe)
exp.keyboard.wait()

expyriment.stimuli.TextScreen("",
    """
    Sometimes it is not easy to tell the difference\n between the pairs !\n\n
    At the end of every trial you are going to be asked \nis you feel you answered by hasard ([key y]) or not ([key n])\n\n
    """).present()
exp.keyboard.wait()

blankscreen.present()

clock = expyriment.misc.Clock()

#Phase d'entrainement



#Phase de test
for nb_s in range(nb_trials):
    #clock = expyriment.misc.Clock()

    #exp.keyboard.wait()
    #blankscreen.present()

    expyriment.stimuli.TextLine("Trial {s} on {t}".format(s = nb_s+1, t = nb_trials)).present()
    exp.clock.wait(1000)

    time = clock.time

    son,sin1,sin2,label = liste_stim[nb_s]

    # Paire 1
    square_paire_1.present()
    play_mono(sin1[:nb_index_duree], Fe)
    exp.clock.wait(duree_intra_stim*1000)
    play_mono(son[:nb_index_duree], Fe)

    blankscreen.present()
    exp.clock.wait(duree_inter_stim*1000)

    # Paire 2
    square_paire_2.present()
    play_mono(sin2[:nb_index_duree], Fe)
    exp.clock.wait(duree_intra_stim*1000)
    play_mono(son[:nb_index_duree], Fe)
    blankscreen.present()

    # Reponse
    expyriment.stimuli.TextScreen("",
        """
        Which pair was the best match ?\n\n\n
        press [left arrow] if it is the first\n\n
        press [right arrow] if it is the second
        """).present()
    key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT, expyriment.misc.constants.K_RIGHT])
    if key == expyriment.misc.constants.K_LEFT:
        response = 'first_best'
    else:
        response = 'second_best'

    expyriment.stimuli.TextScreen("",
        """
        Do you feel like you answered by chance ?\n\n\n
        press [y] if yes\n\n
        press [n] if not
        """).present()
    key_c, rt_conf = exp.keyboard.wait([expyriment.misc.constants.K_y, expyriment.misc.constants.K_n])
    if key_c == expyriment.misc.constants.K_y:
        confidence = 'felt_chance'
    else:
        confidence = 'confident'
    blankscreen.present()

    # Save data
    exp.data.add([time, nb_s+1, label, response, rt, confidence, rt_conf])

    exp.clock.wait(iti)

expyriment.control.end()
