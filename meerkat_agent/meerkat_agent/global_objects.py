'''
Created on 2014. 6. 27.

@author: lsh
'''

'''
global objects for meerkat agents
'''
import sqlalchemy

#meerkat_modules
from config import Config


CONFIG = Config()

DB_ENGINE = sqlalchemy.create_engine(
      CONFIG.DBMS_NAME+'://'+
      CONFIG.DB_USER+':'+
      CONFIG.DB_PASSWORD+'@'+
      CONFIG.DB_HOST+':'+
      CONFIG.DB_PORT+'/'+
      CONFIG.DB_NAME,
      )
