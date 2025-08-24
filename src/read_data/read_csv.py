import csv
import sys
import os
import pandas as pd 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from load_config.loader_config import GetSetting

class ReadCSV:
    
    @staticmethod
    def read_sap_csv_convert_to_df():
        csv_path = GetSetting.get_sap_csv()
        print(csv_path)
        dataframe = pd.read_csv(csv_path)
        #print(dataframe)
        return dataframe 

if __name__ == "__main__":
    ReadCSV.read_sap_csv_convert_to_df()