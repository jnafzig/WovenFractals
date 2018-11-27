import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as patches
import matplotlib
import time
import argparse
from PIL import Image

from swatches import PaletteSelector, Palette
from menu import Menu, MenuItem, ItemProperties

font = {'size'   : 22}
matplotlib.rc('font', **font)



class ColorChoosePlot:
    def __init__(self, grid, palette):
        self.grid = grid
        self.selection = [-1, -1]
        self.palette = palette
        self.selected_palette = Palette(palette.colors[:4], palette.names[:4])

        self.fig, (self.img_ax, self.ax1, self.ax2) = plt.subplots(1, 3, 
                   figsize=(30,40), gridspec_kw = {'width_ratios':[4, 1, 1]})
        
        self.color_bins = np.array(range(0,len(self.selected_palette.names)+1)) - 1/2
        self.palette_bins = np.array(range(0,len(self.palette.names)+1)) - 1/2

        self.img = self.img_ax.imshow(grid, cmap=self.selected_palette.colormap)
        
        self.cm1 = self.selected_palette.plot(self.ax1, vert=True, show_names=True)

        self.cm2 = self.palette.plot(self.ax2, vert=True, show_names=True)

        self.rect1 = patches.Rectangle((-1/2, -5), 2, 1,
                                linewidth=4,
                                edgecolor='black',
                                facecolor=[0.5,0.5,0.5,0.25])
        self.ax1.add_patch(self.rect1)

        self.rect2 = patches.Rectangle((-1/2, -5),2,1,
                                linewidth=4,
                                edgecolor='black',
                                facecolor=[0.5,0.5,0.5,0.25])
        self.ax2.add_patch(self.rect2)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.menu = self.draw_menu()

        
    def onclick(self, event):
        if self.ax1 == event.inaxes:
            binid = np.digitize(event.ydata, self.color_bins)-1
            self.rect1.set_y(self.color_bins[binid])
            self.ax1.draw_artist(self.cm1)
            self.ax1.draw_artist(self.rect1)
            self.fig.canvas.blit(self.ax1.bbox)
            self.selection[0] = binid
        elif self.ax2 == event.inaxes:
            binid = np.digitize(event.ydata, self.palette_bins)-1
            self.rect2.set_y(self.palette_bins[binid])
            self.ax2.draw_artist(self.cm2)
            self.ax2.draw_artist(self.rect2)
            self.fig.canvas.blit(self.ax2.bbox)
            self.selection[1] = binid

        if self.selection[0] >= 0 and self.selection[1] >= 0: 
            self.rect1.set_y(-5)
            self.rect2.set_y(-5)
            new_color = self.palette.colors[self.selection[1]]
            new_name = self.palette.names[self.selection[1]]
            self.selected_palette.names[self.selection[0]] = new_name
            self.selected_palette.colors[self.selection[0]] = new_color
            self.img.set_cmap(self.selected_palette.colormap)

            self.cm1 = self.selected_palette.plot(self.ax1, vert=True, show_names=True)

            self.ax1.draw_artist(self.rect1)
            self.ax2.draw_artist(self.cm2)
            self.ax2.draw_artist(self.rect2)
            self.fig.canvas.draw()
            self.selection = [-1, -1]

    def get_new_palette(self, item):
        plt.close(fig=self.fig)
        ps = PaletteSelector()
        self.palette = ps.get_palette()
        self.selected_palette = Palette(self.palette.colors[:4], 
                                          self.palette.names[:4])
        

        self.fig, (self.img_ax, self.ax1, self.ax2) = plt.subplots(1, 3, 
                   figsize=(30,40), gridspec_kw = {'width_ratios':[4, 1, 1]})
        
        self.color_bins = np.array(range(0,len(self.selected_palette.names)+1)) - 1/2
        self.palette_bins = np.array(range(0,len(self.palette.names)+1)) - 1/2

        self.img = self.img_ax.imshow(grid, cmap=self.selected_palette.colormap)
        
        self.cm1 = self.selected_palette.plot(self.ax1, vert=True, show_names=True)

        self.cm2 = self.palette.plot(self.ax2, vert=True, show_names=True)

        self.rect1 = patches.Rectangle((-1/2, -5), 2, 1,
                                linewidth=4,
                                edgecolor='black',
                                facecolor=[0.5,0.5,0.5,0.25])
        self.ax1.add_patch(self.rect1)

        self.rect2 = patches.Rectangle((-1/2, -5),2,1,
                                linewidth=4,
                                edgecolor='black',
                                facecolor=[0.5,0.5,0.5,0.25])
        self.ax2.add_patch(self.rect2)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.menu = self.draw_menu()
        plt.show()

    def draw_menu(self):
        props = ItemProperties(labelcolor='black', bgcolor='yellow',
                               fontsize=22, alpha=0.2)
        hoverprops = ItemProperties(labelcolor='white', bgcolor='blue',
                                    fontsize=22, alpha=0.2)

        menuitems = []
        item = MenuItem(self.fig, "save", props=props, hoverprops=hoverprops,
                        on_select=self.save)

        menuitems.append(item)
        item = MenuItem(self.fig, "new palette", props=props, hoverprops=hoverprops,
                        on_select=self.get_new_palette)
        menuitems.append(item)

        return Menu(self.fig, menuitems)
        


    def save(self, item):
        # convert indices to corresponding rgb value and create PIL image
        image = Image.fromarray((256*np.array(self.selected_palette.colors)[grid]) \
                                .astype(np.uint8), 'RGB') 
        image.save('out.png')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Plot numpy array file.')
    parser.add_argument('infile', help='a file storing a numpy array')

    args = parser.parse_args()
    infile = args.infile 

    print('loading')
    start = time.time()
    grid = np.load(infile)
    end = time.time()
    print('time elapse', end-start)
    print(grid.shape)

    ps = PaletteSelector()
    sel = ColorChoosePlot(grid, ps.get_palette())

    plt.show()

