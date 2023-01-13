import json
import pandas as pd
import requests
from os import listdir
import io

def get_TIC(planet_name):
    url = f'https://exofop.ipac.caltech.edu/tess/gototicid.php?target={planet_name}&json'
    result = requests.get(url)
    data = json.loads(result.text)
    return data['TIC']

def TIC_df(planet_name):
    TIC = get_TIC(planet_name)
    url_planet  = f'https://exofop.ipac.caltech.edu/tess/download_planet.php?id={TIC}'
    url_stellar = f'https://exofop.ipac.caltech.edu/tess/download_stellar.php?id={TIC}'
    url_other   = f'https://exofop.ipac.caltech.edu/tess/download_nearbytarget.php?id={TIC}&output=pipe'
    TOI_df      = pd.read_csv(url_planet, delimiter='|', index_col=1)
    Star_df     = pd.read_csv(url_stellar, delimiter='|', index_col=1)
    Other_df    = pd.read_csv(url_other, delimiter='|', index_col=1)
    return TOI_df, Star_df, Other_df

print(TIC_df('KELT-9b')[1])