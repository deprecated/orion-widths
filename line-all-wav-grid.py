import os
import sys
from misc_utils import sanitize_string
from astropy.table import Table
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import MultipleLocator, MaxNLocator

sns.set(style='white')

linetab = Table.read('basic-line-list.tab', format='ascii.tab')

figfile = 'line-all-wav-grid.pdf'

fig, axes = plt.subplots(33, 8, figsize=(20, 50))
flaxes = axes.flat
for row in linetab:
    wav0 = row['wav0']
    wavid = str(int(wav0+0.5))
    species = sanitize_string(row['Ion'])
    sname = 'spec-data/spec1d-{}-{}.tab'.format(species, wavid)
    try:
        tab = Table.read(sname, format='ascii.tab')
    except FileNotFoundError:
        print(sname, 'not found', file=sys.stderr)
        continue
    label = '{} {:.2f}'.format(row['Ion'], wav0)
    netflux = (tab['flux'] - tab['cont'])/tab['cont']
    mask4 = np.abs(tab['wav'] - wav0) < 4.0
    mask2 = np.abs(tab['wav'] - wav0) < 2.0
    mask_blue = np.abs(tab['wav'] - (wav0 - 6.0)) < 2.0
    mask_red = np.abs(tab['wav'] - (wav0 + 6.0)) < 2.0
    margin = 0.2*max(netflux[mask2].max(), -netflux.min())
    ymin = netflux.min() - margin
    ymax = max(0.0, netflux[mask2].max()) + 4*margin
    ax = next(flaxes)
    ax.plot(tab['wav'], netflux, label=label, c='r')
    ax.axhline(0.0,  ls='--', c='b')
    if netflux[mask2].sum() > 0.0:
        # Emission line
        fillcolor = 'r'
    else:
        # Absorption line
        fillcolor = 'b'
    ax.fill_between(tab['wav'], netflux, where=mask4,
                    color=fillcolor, alpha=0.3)
    if row['blue cont']:
        ax.fill_between(tab['wav'], netflux, ymin,
                        where=mask_blue, color='k', alpha=0.1)
    if row['red cont']:
        ax.fill_between(tab['wav'], netflux, ymin,
                        where=mask_red, color='k', alpha=0.1)
    ax.axvline(wav0, ls='--', color='k')
    ax.legend(loc='best', frameon=True, framealpha=0.8)
    ax.set(
        xlim=[tab['wav'].min(), tab['wav'].max()],
        ylim=[ymin, ymax],
    )
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(7))

axes[-1, 0].set(
    xlabel='Wavelength, Angstrom', ylabel='Flux',
)

fig.tight_layout()
fig.savefig(figfile)
print(figfile, end='')
