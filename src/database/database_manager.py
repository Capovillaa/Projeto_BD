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

    def verificar_usuario_existe(self, nickname):        
        try:
            users_collection = self.db['users']
            
            usuario_doc = users_collection.find_one({"nickname": nickname})
            return usuario_doc is not None
            
        except Exception as e:
            print(f"Erro ao buscar usuário '{nickname}': {e}")
            return False 

    def listar_mensagens_nao_lidas(self, user_logado):
        try:
            mensagens_collection = self.db['mensagens']
            
            query = {
                "to": user_logado,
                "status": "nao lida"
            }
            
            mensagens_nao_lidas = list(mensagens_collection.find(query))
            
            return mensagens_nao_lidas
            
        except Exception as e:
            print(f"Erro ao listar mensagens não lidas: {e}")
            return []
        

    def marcar_como_lida(self, message_id): 
        try:
            mensagens_collection = self.db['mensagens']
            
            query = {"_id": message_id}
            
            update = {"$set": {"status": "lida"}}
            
            result = mensagens_collection.update_one(query, update)
            
            if result.matched_count == 1:
                return True
            else:
                print(f"Aviso: Não foi possível encontrar a mensagem com ID {message_id}.")
                return False
                
        except Exception as e:
            print(f"Erro ao marcar mensagem como lida: {e}")
            return False