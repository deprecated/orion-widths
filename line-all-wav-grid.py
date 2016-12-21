import os
from misc_utils import sanitize_string
from astropy.table import Table
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import MultipleLocator, MaxNLocator

sns.set(style='white')

linetab = Table.read('basic-line-list.tab', format='ascii.tab')

figfile = 'line-all-wav-grid.pdf'

fig, axes = plt.subplots(19, 8, figsize=(20, 30))
flaxes = axes.flat
for row in linetab:
    wav0 = row['wav0']
    wavid = str(int(wav0+0.5))
    species = sanitize_string(row['Ion'])
    sname = 'spec-data/spec1d-{}-{}.tab'.format(species, wavid)
    try:
        tab = Table.read(sname, format='ascii.tab')
    except FileNotFoundError:
        print(sname, 'not found')
        continue
    label = '{} {:.2f}'.format(row['Ion'], wav0)
    netflux = (tab['flux'] - tab['cont'])/tab['cont']
    mask4 = np.abs(tab['wav'] - wav0) < 4.0
    mask1 = np.abs(tab['wav'] - wav0) < 1.0
    ax = next(flaxes)
    ax.plot(tab['wav'], netflux, label=label, c='r')
    ax.axhline(0.0,  ls='--', c='b')
    if netflux[mask1].sum() > 0.0:
        # Emission line
        fillcolor = 'r'
    else:
        # Absorption line
        fillcolor = 'b'
    ax.fill_between(tab['wav'], netflux, where=mask4,
                    color=fillcolor, alpha=0.3)
    ax.axvline(wav0, ls='--', color='k')
    ax.legend(loc='best')
    margin = 0.2*max(netflux[mask1].max(), -netflux.min())
    ax.set(
        xlim=[tab['wav'].min(), tab['wav'].max()],
        ylim=[netflux.min() - margin,
	      max(0.0, netflux[mask1].max()) + 3*margin],
    )
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(7))

axes[-1, 0].set(
    xlabel='Wavelength, Angstrom', ylabel='Flux',
)

fig.tight_layout()
fig.savefig(figfile)
print(figfile)
