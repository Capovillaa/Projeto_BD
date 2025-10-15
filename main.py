from database.mongo_connection import MongoConnector
from connection_string import URI
from classes.user import User

def main():
    
    DB_NAME = "Mensageria"
    connection = MongoConnector(URI,DB_NAME)

    if(connection.connect() == False):
        print("Não foi possivel estabelecer a conexao com o banco de dados")
        return    
    
    db = connection.getDataBase()
    
    usuario_logado = None 

    while True:
        print("\n--- Sistema de Mensagem ---")
        
        if usuario_logado:
            print(f"Bem-vindo, {usuario_logado.nickname}!")
            print("1. Enviar Mensagem")
            print("2. Deslogar")
            print("3. Sair")
        else:
            print("1. Login")
            print("2. Criar Conta")
            print("3. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if not usuario_logado: 
            if escolha == '1':
                print("\n--- Login de Usuário ---")
                email = input("Digite seu e-mail: ")
                senha = input("Digite sua senha: ")

                if not email or not senha:
                    print("E-mail e senha são obrigatórios.")
                    continue
                
                usuario_logado = User.login(db, email, senha) 
                
                if usuario_logado:
                    print(f"Você está agora logado como {usuario_logado.nickname}.")
                    
            elif escolha == '2':
                print("\n--- Criação de Conta ---")
    
                while True:
                    email = input("Digite seu endereço de e-mail: ")

                    if not email:
                        print("Erro: O e-mail não pode ser vazio.")
                        continue

                    valid_email, msg_email = User.validar_email(email)
        
                    if valid_email:
                        break  
                    else:
                        print(msg_email) 
            
                while True:
                    nickname = input("Digite o seu nome de usuário: ")
        
                    if not nickname:
                        print("Erro: O nome de usuário não pode ser vazio.")
                        continue
            
                    valid_nickname, msg_nickname = User.validar_nickname(nickname)
        
                    if valid_nickname:
                        break  
                    else:
                       print(msg_nickname)

                while True:
                    senha = input("Digite sua senha: ")
        
                    if not senha:
                        print("Erro: A senha não pode ser vazia.")
                        continue
        
                    valid_senha, msg_senha = User.validar_senha(senha)
        
                    if valid_senha:
                        currentUser = User(email, senha, nickname)
                        if currentUser.cadastro(db):
                            break
                    else:
                        print(msg_senha)

                
            elif escolha == '3':
                print("Saindo do programa. Até mais!")
                break
            
            else:
                print("Opção inválida. Por favor, tente novamente.")
                
        else: 
            if escolha == '1':
                print("")
                
            elif escolha == '2':
                print(f"Deslogando de {usuario_logado.nickname}.")
                usuario_logado = None 
                
            elif escolha == '3':
                print("Saindo do programa. Até mais!")
                break
            
            else:
                print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
