import snowflake.connector
from settings import user, password, account, role

class SnowflakeConnector:
    
    def __init__(self, user=user, password=password, account=account, role=role):
    
        self.ctx = snowflake.connector.connect(
            user= user,
            password = password,
            account= account,
            role = role
            )
        
    def get_data_from_db(self):
        self.cs = self.ctx.cursor()
        try:
            self.cs.execute("SELECT NAME, CITY, STATE FROM TG_DW_DB.PUBLIC.BUILDING")
            self.data = self.cs.fetchall()
        finally:
            self.cs.close()
        self.ctx.close()
        
        return [x[0] + ' ' + x[1] + ', ' + x[-1] for x in self.data]
        