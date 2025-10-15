#classe para gerenciar conexao com o banco de dados
from pymongo import MongoClient
from classes.message import Message

class DatabaseManager:
    
    def __init__(self, URI: str, db_name: str):
        self.URI = URI
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.URI)

            self.db = self.client[self.db_name]
            print(f"Conexão com o MongoDB estabelecida com sucesso no banco '{self.db_name}'.")
            return True
            
        except Exception as e:
            print(f"Erro de conexão com o MongoDB: {e}")
            self.client = None
            self.db = None
            return False
    
    def getDataBase(self):
        
        if(self.db == None):
            print("Não há uma conexão ativa com o banco de dados.")
            
        return self.db
    
    def close(self):
        if(self.client):
            self.client.close()
            print("Conexão com o MongoDB fechada.")

    def enviar_mensagem(self,message_obj: Message):
   
        message_data = message_obj.to_dict()
        
        self.db['mensagens'].insert_one(message_data)
       