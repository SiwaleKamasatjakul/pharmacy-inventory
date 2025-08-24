import csv
import sys
import os
import pandas as pd 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from load_config.loader_config import GetSetting

class ReadExcel:
    
    @staticmethod
    def read_robot_log_excel_convert_to_df():
        excel_path = GetSetting.get_robot_log()
        print(excel_path)
        dataframe = pd.read_excel(excel_path)
        #print(dataframe)
        return dataframe 

if __name__ == "__main__":
    ReadExcel.read_robot_log_excel_convert_to_df()