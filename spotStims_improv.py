from pandastim.stimuli import stimulus, stimulus_details, textures
from pandastim.buddies import stimulus_buddies
from pathlib import Path
import sys
import os
from datetime import datetime as dt
import random
import time

#### SET THE EXPERIMENT CONDITIONS ####
experiment = False
experiment_num = '3'


if experiment:
    experiment_num = experiment_num #experiment number and fish id are interchangeable
else:
    experiment_num = 'test'

genotype = 'eval3h2bgcamp6s' #huch2bgcamp8m
age = 9 #dpf
feeding = 'unfed_28hrs' #unfed, fed_gav, fed_adlib
stimulus_type = 'mono_R' #mono_L, mono_R, bino
direction = 'PA' #AP front to back
notes = ""

#### SETTING UP FOLDERS TO STORE DATA ####

data_folder = r'R:\data\karina\gut_tectum'
exp_name = f'{experiment_num}_{genotype}_{age}dpf_{feeding}_{stimulus_type}_{dt.today().strftime("%Y%m%d")}'
exp_folder = os.path.join(data_folder, exp_name)
if not os.path.exists(exp_folder):
    os.mkdir(exp_folder)

mySavePath =  f"{data_folder}\{exp_name}\stim_output.txt"

paramspath = (
    Path(sys.executable)
    .parents[0]
    .joinpath(r"Lib\site-packages\pandastim\resources\params\improv_params_kmf.json")
            )

stimBuddy = stimulus_buddies.StimulusBuddy(
    reporting="onMotion",
    savePath=mySavePath,
            )

##texture##
bg_intensity = 0
fg_intensity = 255

# moving stimulus
angle=270 #91 goes from L->R, 270 R->L
velocity=0.14
stationary_time=0 #a time here just changes the size, but it doesnt move
duration=10

#### STIMULUS DETAILS ####
circ_sizes = [10, 20,30] #[2, 3, 5, 8, 9, 6]
circle_center = (-80,-20)
#circle_centers = [(-80,-30), (-80,0), (-80,-20)] #up-down, left^-right
distance_from_fish = '[(-80,0) = dh:1.0cm, dv:0.5], [(-80,-30) = dh:1.5cm, dv:0.5], [(-80,-20) = dh:1.25cm, dv:0.5]'
used_distance_mm = 10

# create a texture
fin_stims = []

circ_sizes = circ_sizes*5

#circle_centers = circle_centers*5
for c in circ_sizes: #{circle_centers}
    circ_textures = [textures.CircleGrayTex(
        circle_center=circle_center, circle_radius=c,
        bg_intensity=bg_intensity, fg_intensity=fg_intensity,
        texture_size=1024)]

    for tex in circ_textures:

        static_circ = stimulus_details.MonocularStimulusDetails(
            stim_name="static_circle",
            angle=angle,
            velocity=0.0,
            stationary_time=2,
            duration=1,
            hold_after=0.0,
            texture=tex
        )

        moving_circ = stimulus_details.MonocularStimulusDetails(
            stim_name=f"{tex.circle_radius}",
            angle=angle,
            velocity=velocity,
            stationary_time=stationary_time,
            duration=duration,
            hold_after=10.0,
            texture=tex
        )

        fin_stims.append(static_circ)
        fin_stims.append(moving_circ)

#### SAVES TXT FILE WITH STIM DETAILS ####
if experiment == True:
    stim_details_folder = os.path.join(exp_folder)
    if not os.path.exists(stim_details_folder):
        os.mkdir(stim_details_folder)

    file = open(os.path.join(stim_details_folder, 'stim_details.txt'), 'w')
    new_line = '\n'

    to_write = f'### STIM DETAILS ### \
               {new_line}circle_sizes={circ_sizes} \
               {new_line}circle_center={circle_center} \
               {new_line} \
               {new_line}distance_from_fish={distance_from_fish} \
               {new_line}used_distance_mm={used_distance_mm} \
               {new_line}direction={direction} \
               {new_line}{new_line}### MOVING CIRCLE ### \
               {new_line}angle={angle} \
               {new_line}velocity={velocity} \
               {new_line}stationary_time={stationary_time} \
               {new_line}duration={duration} \
               {new_line}### TEXTURE ### \
               {new_line}bg_intensity={bg_intensity} \
               {new_line}fg_intensity={fg_intensity} \
               {new_line}params_file={paramspath} \
               {new_line}notes={notes}'


    file.write(to_write)
    file.close()

    exp_start = input('Press Enter to continue: ')

pstim = stimulus.OpenLoopStimulus(fin_stims, buddy=stimBuddy, params_path=paramspath)
pstim.run()



