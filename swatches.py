import swatch
from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib
from glob import glob
import os

font = {'size'   : 22}
matplotlib.rc('font', **font)

class Palette():
    def __init__(self, colors, names, name=None):
       self.colors = colors
       self.names = names
       self.name = name

    @property
    def colormap(self):
        return ListedColormap(self.colors)

    def plot(self, ax, vert=False, show_names=False):
        if vert:
            artist = ax.imshow([[i, i] for i in range(len(self.colors))], 
                      cmap=self.colormap, aspect=2)
            ax.yaxis.tick_right()
            ax.set_xticks([])
            if show_names:
                ax.set_yticks(range(len(self.names)))
                ax.set_yticklabels(self.names)
            else:
                ax.set_yticks([])
        else:
            artist = ax.imshow([[i for i in range(len(self.colors))]]*2, 
                        cmap=self.colormap, aspect=0.5)
            ax.set_yticks([])
            if show_names:
                ax.set_xticks(range(len(self.names)))
                ax.set_xticklabels(self.names)
                ax.set_title(self.name)
                for tick in ax.get_xticklabels():
                    tick.set_rotation(45)
        return artist
        
        

def get_colors(swatch_name, choices = None):
    colors = swatch.parse('wovns/WOVNS Talma ' + swatch_name + '.ase')

    if not choices:
        for i, color in enumerate(colors):
            print(i, color['name'], color['data']['values'])

        choices = [int(choice) for choice in input('Enter numbers: ').split()]

    return ListedColormap([colors[choice]['data']['values'] for choice in choices]) ,\
        [colors[choice]['name'] for choice in choices]

def get_palette(swatch_file):
    colors = swatch.parse(swatch_file)
    name = os.path.basename(swatch_file)[:-4].replace('WOVNS ', '') 
    return Palette([color['data']['values'] for color in colors], \
                    [color['name'] for color in colors], name=name)


class PaletteSelector():
    def __init__(self, data_dir='wovns'):
    
        self.swatch_files = sorted(glob(os.path.join(data_dir, '*.ase')))
        
        num_swatches = len(self.swatch_files)
        self.palettes = []
        for swatch_file in self.swatch_files:
            self.palettes.append(get_palette(swatch_file))
        
        self.fig = plt.figure(figsize=(30,15))
        self.fig.subplots_adjust(left=0.01,right=.99,top=.99,bottom=.1)
        gs = GridSpec(2, num_swatches, figure=self.fig, height_ratios=(3,1))
        self.axes = [self.fig.add_subplot(gs[0,i]) for i in range(num_swatches)]
        self.bottom_ax = self.fig.add_subplot(gs[1,:])

        for ax, palette in zip(self.axes, self.palettes):
            palette.plot(ax, vert=True)

        self.selected_swatch_id = 10
        
        self.palettes[self.selected_swatch_id].plot(self.bottom_ax, show_names=True)

        self.cid1 = self.fig.canvas.mpl_connect('axes_enter_event', self.onenter)
        self.cid2 = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.show()
    

    def onenter(self, event):
        for i, ax in enumerate(self.axes):
            if event.inaxes==ax:
                self.selected_swatch_id = i
                break
        self.palettes[self.selected_swatch_id].plot(self.bottom_ax, show_names=True)
        self.fig.canvas.draw()
    
    def onclick(self, event):
        if event.inaxes and event.button==1:
            plt.close(fig=self.fig)

    def get_palette(self):
        return self.palettes[self.selected_swatch_id]


if __name__ == '__main__':
    sel = PaletteSelector()
    print(sel.get_palette())
