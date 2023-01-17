from os import listdir

from astropy.io.votable import parse
import matplotlib.pyplot as plt
import pandas as pd
#votable = parse("lte008-4.0-0.0.BT-Cond.7.dat.xml")
#votable = parse("lte056-4.0-0.5a+0.2.BT-NextGen.7.dat.xml")
from astropy.modeling.models import BlackBody
from astropy import units as u
from astropy.visualization import quantity_support
import numpy as np

path = f'https://vizier.cds.unistra.fr/viz-bin/votable?-ref=VIZ63c11688144c3&-out.add=_r&-out.add=_RAJ%2C_DEJ&-sort=_r&-order=I&-oc.form=sexa&-c.r=%20%202&-c.geom=r&-out.src=IV%2F39%2Ftic82&-source=IV%2F39%2Ftic82&-out.orig=standard&-out=TIC&-out=Teff&-out=s_Teff&-out=Mass&-out=s_Mass&-out=LClass&-out=Lum&Lum=0&-out=s_Lum&s_Lum=0&-meta.ucd=2&-meta=1&-meta.foot=1&-out.max=200&=CDS%2C%20France&-c.eq=J2000&-c.u=arcmin'
path2 = f'https://vizier.cds.unistra.fr/viz-bin/votable?-ref=VIZ63c13de3225e34&-out.add=_r&-out.add=_RAJ%2C_DEJ&-sort=_r&-order=I&-oc.form=sexa&-out.src=J%2FMNRAS%2F382%2F1073%2Ftableb1%2CJ%2FMNRAS%2F382%2F1073%2Ftableb2&-c.r=%20%202&-c.geom=r&-source=J%2FMNRAS%2F382%2F1073%2Ftableb1%20J%2FMNRAS%2F382%2F1073%2Ftableb2&-out=recno&-out=Mass&-out=e_Mass&-out=logTeff&-out=e_logTeff&-out=logL&-out=e_logL&-meta.ucd=2&-meta=1&-meta.foot=1&-out.max=1000&=CDS%2C%20France&-c.eq=J2000&-c.u=arcmin'
path3 = f'https://vizier.cds.unistra.fr/viz-bin/votable?-ref=VIZ63c4ef3c2e9127&-out.add=_r&-out.add=_RAJ%2C_DEJ&-sort=_r&-order=I&-oc.form=sexa&-c.r=%20%202&-c.geom=r&-out.src=J%2FApJ%2F903%2F43%2Ftable1&-source=J%2FApJ%2F903%2F43%2Ftable1&-out=Mass&-out=Teff&-out=logL&-meta.ucd=2&-meta=1&-meta.foot=1&-out.max=200&=CDS%2C%20France&-c.eq=J2000&-c.u=arcmin'

votable = parse(path)
votable2 = parse(path2)
votable3 = parse(path3)

print(votable)

def eddinton_luminosity(msun):
    return 1.25*10e38*msun/(3.828*10e33)

table = votable.get_first_table()
array = table.array


table2 = votable2.get_table_by_index(1)
array2 = table2.array

table3 = votable3.get_table_by_index(0)
array3 = table3.array

catalog =[]

msun_list = []
luminosity_list = []
el_list = []

fig, ax = plt.subplots(2,1,figsize=(8,6))

for row in array:
    msun = row[5]
    luminosity = row[8]
    el = eddinton_luminosity(msun)
    msun_list.append(msun)
    luminosity_list.append(luminosity)
    el_list.append(el)
    new_row = np.ma.filled(row, fill_value=0)
    catalog.append(new_row)
    
for row in array2:
    msun = row[1]
    luminosity = 10**(row[5])
    el = eddinton_luminosity(msun)
    msun_list.append(msun)
    luminosity_list.append(luminosity)
    el_list.append(el)
    
for row in array3:
    msun = row[2]
    luminosity = 10**row[4]
    el = eddinton_luminosity(msun)
    msun_list.append(msun)
    luminosity_list.append(luminosity)
    el_list.append(el)
def eddinton_luminosity_theoretical(mass):
    return mass

def low_mass_theoretical(mass):
    return 0.23*mass**2.3

def solar_mass_luminosity_theoretical(mass):
    return mass**4

def regular_mass_luminosity_theoretical(mass):
    return 1.4*mass**3.5

def high_mass_luminosity_theoretical(mass):
    return 32000*mass
fig, ax = plt.subplots(1,1,figsize=(30,30))

msun_list = np.array(msun_list)

marker = 'o'
size = 500
alpha=0.1

ax[0].scatter(msun_list[msun_list<0.43], low_mass_theoretical(msun_list[msun_list<0.43]), marker=marker,s=size,alpha=alpha,c="gray")
ax[0].scatter(msun_list[(0.43<=msun_list) & (msun_list<2)], solar_mass_luminosity_theoretical(msun_list[(0.43<=msun_list) & (msun_list<2)]), marker=marker,s=size,alpha=alpha,)
ax[0].scatter(msun_list[(2<=msun_list) & (msun_list<40)], regular_mass_luminosity_theoretical(msun_list[(2<=msun_list) & (msun_list<40)]), marker=marker,s=size,alpha=alpha,c="green")
ax[0].scatter(msun_list[msun_list>40], regular_mass_luminosity_theoretical(msun_list[msun_list>40]), marker=marker,s=size,alpha=alpha,c="red")

ax[0].scatter(msun_list[:len(array):], luminosity_list[:len(array)], c='red', marker='o',alpha=1, label="G0V-M5.5V stars (Paegert+, 2021)")

ax[0].scatter(msun_list[len(array):len(array)+len(array2)], luminosity_list[len(array):len(array)+len(array2)], c='orange', marker='o',alpha=1, label="B0V-G0V stars (Malkov+, 2007)")

ax[0].scatter(msun_list[len(array)+len(array2):], luminosity_list[len(array)+len(array2):], c='purple', marker='o',alpha=1, label="O0V-B0V stars (Dorigo Jones+, 2020)")

ax[0].scatter(msun_list, el_list, c='gray', alpha=1, marker="x",label="Eddington luminosity")

ax[0].set_xlabel("Mass (Msun)")
ax[0].set_ylabel("LogL(Lsun)")

plt.rcParams['font.size'] = 30

ax[0].legend()

ax[0].set_yscale('log')
ax[1].set_yscale('log')

plt.show()