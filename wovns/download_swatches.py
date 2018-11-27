from urllib.request import urlretrieve
from urllib.parse import unquote
from os.path import isfile

def download_swatches(url, filename, nums):
    for num in nums:
        outfile = unquote(filename.format(num))
        if isfile(outfile):
            print(outfile, 'already downloaded')
        else:
            print('Downloading', outfile, 'from')
            print(url.format(num) + filename.format(num))
            urlretrieve(url.format(num) + filename.format(num), outfile)
            print()

landscape_url = 'https://www.wovns.com/palette_files/Talma/Landscape/{0}/'
landscape_filename = 'WOVNS%20Talma%20Landscape%20{0}.ase'
landscape_nums = [1,2,3,4,5,6,7,8,9,10,11,18,19,20]

download_swatches(landscape_url, landscape_filename, landscape_nums)

eden_url = 'https://www.wovns.com/palette_files/Talma/Eden/{0}/'
eden_filename = 'WOVNS%20Talma%20Eden%20{0}.ase'
eden_nums = range(1,21)

download_swatches(eden_url, eden_filename, eden_nums)

pastel_url = 'https://www.wovns.com/palette_files/Talma/Pastel/{}/'
pastel_filename = 'WOVNS%20Talma%20Pastel%20{}.ase'
pastel_nums = range(1,21)

download_swatches(pastel_url, pastel_filename, pastel_nums)

spectrum_url = 'https://www.wovns.com/palette_files/Talma/Spectrum/{}/'
spectrum_filename = 'WOVNS%20Talma%20Spectrum%20{}.ase'
spectrum_nums = range(1,21)

download_swatches(spectrum_url, spectrum_filename, spectrum_nums)
