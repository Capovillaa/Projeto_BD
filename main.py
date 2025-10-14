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
                
                usuario_logado = User.login(db, email, senha) 
                
                if usuario_logado:
                    print(f"Você está agora logado como {usuario_logado.nickname}.")
                    
            elif escolha == '2':
                print("\n--- Criação de Conta ---")
                email = input("Digite seu endereco de e-mail: ")
                nickname = "@"+ input("Digite o seu nome de usuário: ")
                senha = input("Digite sua senha: ")
                currentUser = User(email,senha,nickname)
                currentUser.cadastro(db)
                
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

if __name__ == "_main_":
    main()