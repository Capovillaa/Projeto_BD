from database.database_manager import DatabaseManager
from database.connection_string import URI
from classes.user import User
from utils.interface import input_list_messages,input_send_message,get_valid_input

DB_NAME = "Mensageria"
connection = DatabaseManager(URI,DB_NAME)
connection.connect()

def main():
    
    db = connection.getDatabase() 
    logged_user = None 

    while True:
        print("\n--- Messaging System ---")
        
        if logged_user:
            print(f"Welcome, {logged_user.nickname}!") 
            print("1. Send Message") 
            print("2. List Messages") 
            print("3. Logout and Exit")
        else:
            print("1. Login")
            print("2. Create Account") 
            print("3. Exit") 
            
        choice = input("Choose an option: ") 
        
        if not logged_user: 
            if choice == '1':
                print("\n--- User Login ---") 
                email = input("Enter your email: ") 
                password = input("Enter your password: ") 
                print("------------------------\n")

                if not email or not password:
                    print("Email and password are required.")
                    continue
                
                logged_user = User.login(db, email, password) 
                
                if logged_user:
                    print(f"You are logged in as {logged_user.nickname}.")
                    
            elif choice == '2':
                print("\n--- Account Creation ---") 
    
                email = get_valid_input("Enter your email: ", User.validate_email)
                password = get_valid_input("Enter your password: ", User.validate_password)
                nickname = get_valid_input("Enter your nickname: ", User.validate_nickname)

                logged_user = User(email, password, nickname)
                logged_user.register(db) 
                
            elif choice == '3':
                print("Exiting program. Goodbye!") 
                connection.close()
                break
                
            else:
                print("Invalid option. Please try again.") 
                
        else:
            if choice == '1':
                input_send_message(logged_user.nickname, connection)
                
            elif choice == '2':
                input_list_messages(logged_user, connection)
                
            elif choice == '3':
                print("Logging out and Exiting program. Goodbye!") 
                connection.close()
                break
                
            else:
                print("Invalid option. Please try again.") 

if __name__ == "__main__":
    main()