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
            print(f"MongoDB connection established successfully in database '{self.db_name}'.")
            return True
            
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            self.client = None
            self.db = None
            return False
    
    def getDatabase(self):
        
        if(self.db == None):
            print("No active database connection.")
            
        return self.db
    
    def close(self):
        if(self.client):
            self.client.close()
            print("MongoDB connection closed.")

    def send_message(self,message_obj: Message):
   
        message_data = message_obj.to_dict()
        
        self.db['mensagens'].insert_one(message_data)

    def check_user_exists(self, nickname):        
        try:
            users_collection = self.db['users']       
            user_doc = users_collection.find_one({"nickname": nickname})
            return user_doc is not None
            
        except Exception as e:
            print(f"Error searching for user '{nickname}': {e}")
            return False 

    def list_unread_messages(self, logged_user):
        try:
            messages_collection = self.db['mensagens']
            
            query = {
                "to": logged_user,
                "status": "nao lida"
            }
            
            unread_messages = list(messages_collection.find(query))
            
            return unread_messages
            
        except Exception as e:
            print(f"Error listing unread messages: {e}")
            return []
        

    def mark_as_read(self, message_id): 
        try:
            messages_collection = self.db['mensagens']
            
            query = {"_id": message_id}
            
            update = {"$set": {"status": "lida"}}
            
            result = messages_collection.update_one(query, update)
            
            if result.matched_count == 1:
                return True
            
            print(f"Warning: Could not find message with ID {message_id}.")
            return False   
         
        except Exception as e:
            print(f"Error marking message as read: {e}")
            return False