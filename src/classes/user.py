from database.database_manager import DatabaseManager

class User:

    def __init__(self, email, password, nickname):
        self.email = email
        self.password = password
        self.nickname = nickname

    @staticmethod
    def validate_email(email):
        if email.count('@') != 1:
            return False, "Error: The email must contain one '@' symbol." 
        
        parts = email.split('@')
        domain = parts[1]
        
        if '.' not in domain:
            return False, "Error: The email domain (part after '@') must contain a dot (.)."
        
        if len(email) < 8: 
            return False, "Error: Email is too short." 

        return True, ""
    
    @staticmethod
    # Renomeado validar_senha para validate_password
    def validate_password(password): # Renomeado senha para password
        # Renomeado CARACTERES_ESPECIAIS para SPECIAL_CHARACTERS
        SPECIAL_CHARACTERS = '!@#$%^&*()-_+=[]{}|;:,.<>?' 

        if len(password) < 8:
            return False, "Error: The password must be at least 8 characters long." # Traduzido
            
        if ' ' in password:
            return False, "Error: The password cannot contain spaces." # Traduzido
            
        # Variáveis booleanas traduzidas
        has_uppercase = False
        has_lowercase = False
        has_number = False
        has_special = False
        
        for char in password: # Renomeado senha para password
            if char.isupper():
                has_uppercase = True # Renomeado
            elif char.islower():
                has_lowercase = True # Renomeado
            elif char.isdigit():
                has_number = True # Renomeado
            elif char in SPECIAL_CHARACTERS:
                has_special = True # Renomeado
            
        if not has_uppercase: # Renomeado
            return False, "Error: The password must contain at least one uppercase letter." # Traduzido
        if not has_lowercase: # Renomeado
            return False, "Error: The password must contain at least one lowercase letter." # Traduzido
        if not has_number: # Renomeado
            return False, "Error: The password must contain at least one number." # Traduzido
        if not has_special: # Renomeado
            return False, "Error: The password must contain at least one special character (!@#$%...). " # Traduzido
            
        return True, ""
    
    @staticmethod 
    # Renomeado validar_nickname para validate_nickname
    def validate_nickname(nickname):
        if len(nickname) < 3:
            return False, "Error: Nickname must contain more than 3 characters." # Traduzido
        if ' ' in nickname:
            return False, "Error: Nickname cannot have spaces." # Traduzido
        
        return True, ""
    
    # Renomeado verificar_duplicidade para check_duplicity
    def check_duplicity(self, db):
        users_collection = db['users']

        if users_collection.find_one({"email": self.email}):
            return False, "Error: This email is already registered." # Traduzido
        
        if users_collection.find_one({"nickname": self.nickname}):
            return False, "Error: This username is already in use." # Traduzido
        return True, ""

    # Renomeado cadastro para register
    def register(self, db):
        if db is None:
            print("Error: The database instance is invalid.") # Traduzido
            return False

        try:
            users_collection = db['users']

            users_collection.insert_one({
                "email": self.email,
                "senha": self.password, # MANTER "senha" (Campo do MongoDB)
                "nickname": self.nickname
            })

            print(f"User {self.nickname} registered successfully!") # Traduzido
            return True
        except Exception as e:
            print(f"An error occurred while registering the user: {e}") # Traduzido
            return False
        
    @classmethod 
    def login(cls, db, email, password): # Renomeado senha para password
        if db is None:
            print("Error: The database instance is invalid for login.") # Traduzido
            return None
        
        try:
            users_collection = db['users']
        
            user_doc = users_collection.find_one({"email": email}) # Renomeado usuario_doc
            
            if user_doc:
                # MANTER "senha" (Campo do MongoDB)
                if user_doc['senha'] == password: 
                    print(f"Login successful!") # Traduzido
                    
                    return cls(
                        email=user_doc['email'], 
                        password=user_doc['senha'], # Usando user_doc['senha'] do BD
                        nickname=user_doc['nickname']
                    )
                else:
                    print("Error: Incorrect password.") # Traduzido
                    return None
            else:
                print(f"Error: User with email '{email}' not found.") # Traduzido
                return None
                
        except Exception as e:
            print(f"An error occurred during login: {e}") # Traduzido
            return None