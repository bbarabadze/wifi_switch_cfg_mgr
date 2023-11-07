from os import getenv
from dotenv import load_dotenv
from scrapli.driver.core import AsyncIOSXEDriver, AsyncEOSDriver
import yaml

load_dotenv()

# Define a function to update the credentials from environment variables
def set_credentials(config):
    
    for model_details in config.values():      
        
        model_details[0] = globals()[model_details[0]]
        
        conn_details = model_details[1]
        conn_details['auth_username'] =getenv(conn_details['auth_username'])
        conn_details['auth_password'] = getenv(conn_details['auth_password'])
        
        if 'auth_secondary' in conn_details:
          conn_details['auth_secondary'] = getenv(conn_details['auth_secondary'])
    
    return config


def get_conn_details(model):
  
  with open('conn_params.yaml', 'r') as file:
    config = yaml.safe_load(file)

  config = set_credentials(config)

  return config[model][0], config[model][1]


if __name__ == '__main__':
   print(get_conn_details('aruba2022')) #სატესტო