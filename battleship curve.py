"""
Kyler Natividad
License: MIT

This is a simple script for creating battleship curves
that I created for an archaeology class project.
"""

from matplotlib.pyplot import *
from numpy import *

#################### Data ######################
#Plug your values into here

start_year = 1910
year_increment = 20

data = ["flowers",       [0, 2, 5, 7, 5],
        "crosses",       [3, 4, 2, 1, 0],
        "angel",         [0, 2, 7, 5, 2],
        "star of david", [0, 0, 2, 2, 1]]

filename = 'example.png'
################## Formating ###################
percentage_markers = True
border_color = 'black'
fill_color = 'black'
height = 0.9
show_y_ticks = False

preview_only = False
################################################

labels = [data[i] for i in range(len(data)) if i%2 == 0]
numbers = [data[i] for i in range(len(data)) if i%2 == 1]

n_sets = len(numbers)
set_length  = len(numbers[0])

years = arange(start_year, start_year+year_increment*set_length, year_increment)
year_labels = ["{}-{}".format(y, y+year_increment) for y in years]

#check for errors in the data
bad_sets = ""
for i in range(n_sets):
    if set_length != len(numbers[i]):
        bad_sets += "data set #{}: {}\n".format(i+1, labels[i])

assert not bad_sets, "\nwrong number of elements for the following data sets:\n{}".format(bad_sets)

def tot(n, i):
    sum = 0
    for j in n:
        sum += j[i]
    return sum

total = [tot(numbers, i) for i in range(set_length)]
percentages = [[ns[i]*1.0/total[i] for i in range(set_length)] for ns in numbers]

f, axs = subplots(1, n_sets, sharex=True, sharey=True)

for i in range(n_sets):
    ax = axs[i]

    axs[i].set_title(labels[i])
    rects = ax.barh(arange(set_length), percentages[i],
                        height, [-x/2.0 for x in percentages[i]],
                        tick_label=year_labels, align='center', color=fill_color, edgecolor=border_color)
    if percentage_markers:
        for j in range(len(rects)):
            rect = rects[j]
            
            percent_string = "{:.0f}%".format(100.0*percentages[i][j])
            
            t = ax.text(0, 0, percent_string,
                        verticalalignment='center', weight='bold',
                        clip_on=True)
            
            bb = t.get_window_extent(renderer=f.canvas.get_renderer())
            bb_coords = bb.transformed(axs[i].transData.inverted())
        
            if (rect.get_width() > bb_coords.width+0.025):
                x = rect.get_x() + rect.get_width()/2.0
                clr = 'white'
                align = 'center'
            else:
                x = rect.get_x()+rect.get_width()+0.025
                clr = 'black'
                align = 'left'
            y = rect.get_y() + rect.get_height()/2.0
            
            t.set_color(clr)
            t._x = x
            t._y = y
            t._horizontalalignment = align

axs[0].tick_params(
    axis='y',
    which='both',
    right='off')

f.subplots_adjust(wspace=0)
setp([a.get_xticklabels() for a in f.axes], visible=False)

for ax in axs:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(
        axis='x',
        which='both',
        top='off',
        bottom='off')
    ax.spines['left'].set_visible(False)

for ax in axs[1 if show_y_ticks else 0:]:
    ax.tick_params(
        axis='y',
        which='both',
        left='off',
        right='off',
        labelbottom='off')

if preview_only:
    show()
else:
    savefig(filename)
