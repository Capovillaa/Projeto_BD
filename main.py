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

    while True:
        print("\n--- Sistema de Mensagem ---")
        print("1. Login")
        print("2. Criar Conta")
        print("3. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            print("Funcionalidade de Login ainda não implementada.")
                
        elif escolha == '2':
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

if __name__ == "__main__":
    main()