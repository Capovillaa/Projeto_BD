from database.database_manager import DatabaseManager

class User:

    def __init__(self,email,senha,nickname):
        self.email = email
        self.senha = senha
        self.nickname = nickname

    @staticmethod
    def validar_email(email):
        if email.count('@') != 1:
            return False, "Erro: O e-mail deve conter um símbolo '@'."
        
        partes = email.split('@')
        dominio = partes[1]
        
        if '.' not in dominio:
            return False, "Erro: O domínio do e-mail (parte após o '@') deve conter um ponto (.)."
        
        if len(email) < 8: 
             return False, "Erro: E-mail muito curto."

        return True, ""
    
    @staticmethod
    def validar_senha(senha):
        CARACTERES_ESPECIAIS = '!@#$%^&*()-_+=[]{}|;:,.<>?'

        if len(senha) < 8:
            return False, "Erro: A senha deve ter pelo menos 8 caracteres."
            
        if ' ' in senha:
            return False, "Erro: A senha não pode conter espaços."
            
        tem_maiuscula = False
        tem_minuscula = False
        tem_numero = False
        tem_especial = False
        
        for char in senha:
            if char.isupper():
                tem_maiuscula = True
            elif char.islower():
                tem_minuscula = True
            elif char.isdigit():
                tem_numero = True
            elif char in CARACTERES_ESPECIAIS:
                tem_especial = True
            
        if not tem_maiuscula:
            return False, "Erro: A senha deve conter pelo menos uma letra maiúscula."
        if not tem_minuscula:
            return False, "Erro: A senha deve conter pelo menos uma letra minúscula."
        if not tem_numero:
            return False, "Erro: A senha deve conter pelo menos um número."
        if not tem_especial:
            return False, "Erro: A senha deve conter pelo menos um caractere especial (!@#$%...). "
            
        return True, ""
    
    @staticmethod    
    def validar_nickname(nickname):
        if len(nickname) < 3:
            return False, "Erro: Nickname deve conter mais de 3 caracteres "
        if ' ' in nickname:
            return False, "Erro: Nickname não deve ter espaços"
        
        return True, ""
    
    def verificar_duplicidade(self, db):
        users_collection = db['users']

        if users_collection.find_one({"email": self.email}):
            return False, "Erro: Este e-mail já está cadastrado."
        
        if users_collection.find_one({"nickname": self.nickname}):
            return False, "Erro: Este nome de usuário já está em uso."
        return True, ""

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
        
    @classmethod    
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
