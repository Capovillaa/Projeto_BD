from database.mongo_connection import MongoConnector

class User:

    def __init__(self,email,senha,nickname):
        self.email = email
        self.senha = senha
        self.nickname = nickname

    def cadastro(self,db):
        if db is None:
            print("Erro: A instância do banco de dados é inválida.")
            return False

        try:
            users_collection = db['users']

            users_collection.insert_one({
                "email":self.email,
                "senha":self.senha,
                "nickname":self.nickname
            })

            print(f"Usuário {self.nickname} cadastrado com sucesso!")
            return True
        except Exception as e:
            print(f"Ocorreu um erro ao cadastrar o usuário: {e}")
            return False
        
    def login(cls, db, email, senha):
        if db is None:
            print("Erro: A instância do banco de dados é inválida para login.")
            return None
        
        try:
            users_collection = db['users']
        
            usuario_doc = users_collection.find_one({"email": email})
            
            if usuario_doc:
                if usuario_doc['senha'] == senha:
                    print(f"Login bem-sucedido!")
                    
                    return cls(
                        email=usuario_doc['email'], 
                        senha=usuario_doc['senha'], 
                        nickname=usuario_doc['nickname']
                    )
                else:
                    print("Erro: Senha incorreta.")
                    return None
            else:
                print(f"Erro: Usuário com o email '{email}' não encontrado.")
                return None
                
        except Exception as e:
            print(f"Ocorreu um erro durante o login: {e}")
            return None
