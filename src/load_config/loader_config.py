import json
import os
class ConfigLoader:
    
  
    '''
    def load_config(path=r"C:/Users/banas/OneDrive/เอกสาร/3. Work/Hospital-Inventory/src/config/config.json"):
        with open(path, "r", encoding="utf-8") as config:
            data = json.load(config)
        return data
    '''
    
    def load_config():
        # Path relative to the project root
        path = os.path.join("src","config", "config_streamlit.json")
        path = os.path.abspath(path)  # optional, ensures absolute path
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    
class GetSetting:
    @staticmethod
    def get_sap_csv():
        return ConfigLoader.load_config().get("SAP","")
    
    @staticmethod
    def get_max_level_stock():
        return ConfigLoader.load_config().get("MAX_STOCK_LEVEL","")
    
    @staticmethod
    def get_robot_log():
        return ConfigLoader.load_config().get("Robot_Log","")