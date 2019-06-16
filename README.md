# PCBS-spectral_pitch_perception


#### Final project for PCBS class
#### (on the same topic as an internship at the LSP, ENS)
##### [web page version here](https://adker.github.io/PCBS-spectral_pitch_perception/)
#### *Adrien Kerebel*
##### *experiment designed with the help of A. de Cheveigné and J. Graves*

## Subject: auditory perception (pitch perception)

The aim of the project is to decide between two potential predictive models of spectral pitch perception (like in overtone singing).

**Table of Contents**

- [Background information](#background-information)
    - [Overtone singing](#overtone-singing)
    - [Research question](#Research question)
- [Description of the experiment](#description-of-the-experiment)
    - [Hypothesis](#hypothesis)


## Background information
#### Overtone singing

Overtone singing (aka throat singing or Khoomei) is a set of traditional singing styles and techniques that originated from central Asia.
![map](figures/fig_map_asia.png)
In these styles, a single singer produces two pitches at the same time: typically, one low steady note and a high whistle made of the harmonics of the low tone.

A commonly accepted explanation of the technique is that the singer produces a spectrally rich sound from which specific harmonics are amplified by resonating in his nasal and vocal cavities (like in a Helmholtz resonator).

An example of overtone singing in the Sygyt style can be found [here](https://www.youtube.com/watch?v=vo34v7QQ254) or [on this wave file](supplementary/throat_singing_example.wav)
We can follow the overtone melody from 00:54 to 01:04 of the video on this spectrogram (see below, you should focus on the 1000Hz-3000Hz frequency range).
![spectrogram](figures/fig_spectrogram.png)

We can notice that there are two kinds of pitches here: a **virtual pitch** corresponding to the fundamental frequency of the sound and **spectral pitches** elicited by maxima of energy in the spectrum.  

#### Research question

I am interested here in how to predict the perceived spectral pitch from the physical properties of the sound.

For doing that, I imagined two very simple models of spectral pitch perception.

According to the first model, the spectral pitch corresponds to the center of the **spectral envelope** of the sound (an imaginary line that determines the height of each harmonic partial in the spectrum).
For example, for this sound it would be 3000Hz:
![env](figures/fig_spectrum_envelop.png)

According to the second model, the spectral pitch corresponds to the frequency of the harmonic partial that has the most energy (the higher bar in the spectrum).
For example, for this sound it would be 1400Hz:
![env](figures/fig_spectrum_partial.png)

It is worth noting that these two models predict the same pitch when the spectral envelope is centered on a harmonic of the sound (like in overtone singing). To decide between them we have to use sounds for which it is not the case.

The predictions of the two models are summed up in the following figure:
![two models](figures/fig_two_models.png "courbe des modeles")


## Description of the experiment

The experiment is designed to decide between the two curves on the figure above in three "*harmonic zones*": around the 7th harmonic (where partials are resolved), around the 11th harmonic (where partials are less resolved), and around the 13th harmonic (where partials are not resolved).

#### Hypothesis

Our hypothesis is that the perceived spectral pitch will follow the strongest harmonic partial model for low spectral pitches (where partials are resolved) and that it will follow the position of the spectral envelope for higher spectral pitches (unresolved partials).

#### Task

In every trial, we try to see which of the two models best fits the spectral pitch elicited by a given complex sound.

Participants are presented with two pairs of sound consisting of one sine wave and a complex tone (with the same complex tone on each pair). They are asked to choose which of the two pairs consist of sounds that "match the best together". Every time, the two sine waves correspond to the prediction of the two models.

```python
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
```

We assume that the sine wave whose frequency is the closest to the perceived spectral pitch of the complex sound will be perceived to "match the best" with this sound.

At the end of every trial, the subject is asked to rate how confident he is about he answer on a three-degree scale.

```python
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
```

Four types of comparisons are made, corresponding to four positions of the spectral envelope on a "harmonic zone". For a harmonic zone centered on f_z, the comparisons made are as follows:
![comp](figures/fig_comparisons.png)

#### Procedure

To make sure that participants can discriminate frequencies, I included a **test phase** at the beginning of the experiment, where the subject has to compare pairs of pure tones.
All the potential spectral pitches that are proposed in the "real" task are tested for discrimination in the test phase.

Then there is a brief **familiarisation phase** on the format of the real task (but with different f0s).

Then the **task** begins (4 comparisons X 3 harmonic zones X 3 repetitions X 2 possible orders of a pair X 2 f0s = 144 trials).

The full experiment code is available [here](experiment_spectral_pitch_final.py). Note that the stimuli have to be generated before running the experiment, see procedure below.

#### Stimuli

Complex sounds stimuli are synthetic sounds produced as follows:
- we generate an impulsions series (with chosen fundamental frequency f0)
![impulsion series](figures/fig_impulsions.png)

        function serie_imp = clics(f0, Fe, duree)

        taille = Fe*duree;
        nb_imp = f0*duree;
        pas = floor(taille/nb_imp);
        serie_imp = zeros(1,taille);

        for i = 0:(nb_imp-2)
        serie_imp((i*pas)+1) = 1;
        end

        end

- we filter it in a resonating filter (with chosen resonance frequency fr and quality factor Q)
![filter](figures/fig_filter.png)

        function son_filtre = filtre(son, Fe, bump, Q)

        Wo = bump/(Fe/2);
        [B,A] = nt_filter_peak(Wo,Q);
        clics_filtre = filter(B,A,son);
        son_filtre = clics_filtre*(max(son)/max(clics_filtre));

        end

- we obtain a sound with two pitches
![env](figures/fig_spectrum_envelop.png)

This was done with a [Matlab script](generation_of_stimuli_final.m) using [this filter](nt_filter_peak.m) (I haven't coded the filter).

Every single complex sound and sine wave are then stored as wave files in a folder, waiting to be called in the experiment python script as follows:

The two pairs of sounds of every trial are built as vector and stored in a list before the beginning of the task. They are also randomised within each repetition block.

```python
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
                    # on interpole les silences et on ne prend que les longueurs de sons désirées
                    sin1_courant = sin1_courant[:nb_index_duree]
                    sin2_courant = sin2_courant[:nb_index_duree]
                    son_courant = son_courant[:nb_index_duree]
                    stimulus_1 = np.concatenate((sin1_courant,silence_intra,son_courant))
                    stimulus_2 = np.concatenate((sin2_courant,silence_intra,son_courant))
                    stimulus_courant = np.concatenate((stimulus_1,silence_inter,stimulus_2))
                    liste_provisoire.append((stimulus_courant,label, comparaison+1, fc+1, ordre+1, f0+1, rep+1))
    np.random.shuffle(liste_provisoire)
    liste_stim = liste_stim+liste_provisoire
```

## Results

A detailed analysis of the results of the experiment is available on the attached R markdown document.

Briefly, the second model (strongest partial in the spectrum) seems to be preferred on the *resolved partials zones* (as expected).

Interestingly, none of the models is strongly preferred on the non-resolved partials zone.    

![res](figures/fig_res.png)

## Supplementary material

The scripts used to make the figures of this document are available in the "supplementary" folder of the repository (![spectrum](supplementary/spectre_plot.m), ![filter frequency response](supplementary/plot_reponse_en_frequence.m), ![sonagramme](supplementary/plot_sonagramme.m)).
