import sys
import os
import pandas as pd 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from read_data.read_csv import ReadCSV
from datetime import datetime
import numpy as np
from dateutil import parser


from load_config.loader_config import GetSetting

class ExpireDateCalculation:
    
    @staticmethod
    def expiredateCalculation():
        date_format = "%m/%d/%Y"
        today_datetime = datetime.today().strftime('%m/%d/%Y')
        today_date = parser.parse(today_datetime)
        
        #print(type(today_date))
        
        sap_csv_df = ReadCSV.read_sap_csv_convert_to_df()
        
        sap_csv_df["ExpirationDate"] = pd.to_datetime(sap_csv_df["ExpirationDate"])
        #print(sap_csv_df.info())
        
        sap_csv_df["DateBeforeExpire"] = (sap_csv_df["ExpirationDate"] -today_date).dt.days
        #print(sap_csv_df)
        
        filter_expire_date_less_than_30_days = sap_csv_df[sap_csv_df["DateBeforeExpire"] <= 30]
        #print(filter_expire_date_less_than_30_days)
        return filter_expire_date_less_than_30_days
    
class ReservePharmacyButNoStock:
    @staticmethod
    def reserved_pharmacy_but_no_stock():
        sap_csv_df = ReadCSV.read_sap_csv_convert_to_df()
        #print(sap_csv_df)
        filter_df_reserve_pharmacy_but_no_stock = sap_csv_df[sap_csv_df['ReservedQty'] > sap_csv_df["UnrestrictedQty"]]
        print(filter_df_reserve_pharmacy_but_no_stock)
        return filter_df_reserve_pharmacy_but_no_stock


class MinStockLevel:
    
    @staticmethod
    def minstock_level():
        sap_csv_df = ReadCSV.read_sap_csv_convert_to_df()
        max_level_info = GetSetting.get_max_level_stock()
        
        
        
        for material_id, max_level in max_level_info.items():
            
            threadhold = MinStockLevel.percentage_calculate(max_level)
            print(f"{material_id}: {max_level} - {threadhold}")
            
            check_max_level = sap_csv_df[(sap_csv_df["MaterialID"] == material_id) & (sap_csv_df["UnrestrictedQty"] <= threadhold)]
            print(check_max_level)
            return check_max_level
        
            '''
                if sap_csv_df[sap_csv_df["UnrestrictedQty"]] < threadhold:
                    sap_csv_df[sap_csv_df["MinStockLevel"]] == "True"
                else:
                    sap_csv_df[sap_csv_df["MinStockLevel"]] == "False"
            '''    
        #print(sap_csv_df)
                

        
    @staticmethod
    def percentage_calculate(max_level):
        
        return  (int(20) *int(max_level))/100    

    
    
if __name__ == "__main__":
    #ExpireDateCalculation.expiredateCalculation()
    #ReservePharmacyButNoStock.reserved_pharmacy_but_no_stock()
    MinStockLevel.minstock_level()