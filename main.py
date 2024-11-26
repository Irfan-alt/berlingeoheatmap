
# currentWorkingDirectory = "C:\\Users\\DELL\\VsCodeProjects\\berlingeoheatmap_project1"
# currentWorkingDirectory = "/mnt/c/Users/DELL/VsCodeProjects/Berlingeoheatmap"

# -----------------------------------------------------------------------------
import os
# os.chdir(currentWorkingDirectory)
print("Current working directory\n" + os.getcwd())

import pandas                        as pd
from core import methods             as m1
from core import HelperTools         as ht

from config                          import pdict

# -----------------------------------------------------------------------------
@ht.timer
def main():
    """Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""

    # Load datasets
    try:
        dfr_lstat = pd.read_csv("datasets/Ladesaeulenregister.csv",
                                 delimiter=';',
                                 skiprows= 10,
                                #  on_bad_lines= "skip",
                                 low_memory=False,
                                 encoding='utf-8')
        dfr_resid = pd.read_csv("datasets/plz_einwohner.csv",
                                delimiter = ',',
                                encoding='utf-8')
        dfg_geo = pd.read_csv("datasets/geodata_berlin_plz.csv",
                              delimiter=';',
                              encoding='utf-8')
        print("succesfull")
    except Exception as e:
        print(f"Error loading datasets: {e}")
        return
        
    # Preprocess the datasets
    try:
        # Preprocess electric charging station data
        gdf_lstat = m1.preprop_lstat(dfr_lstat, dfg_geo, pdict)

        # Count charging stations by postal code
        gdf_lstat_counted = m1.count_plz_occurrences(gdf_lstat)

        # Preprocess population data
        gdf_residents = m1.preprop_resid(dfr_resid, dfg_geo, pdict)
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return

    # Create and display Streamlit app with the heatmaps
    try:
        m1.make_streamlit_electric_Charging_resid(gdf_lstat_counted, gdf_residents)
    except Exception as e:
        print(f"Error in visualization: {e}")



if __name__ == "__main__": 
    main()

