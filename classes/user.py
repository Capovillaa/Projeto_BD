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
