from database.database_manager import *
from classes.user import User
from classes.security import Security
from classes.message import Message

def get_valid_input(prompt: str, validation_function): 
    while(True):
        
        input_value = input(prompt)

        if not input_value:
            print("This field cannot be empty.") 
            continue

        if "nickname" in prompt.lower():
            if not input_value.startswith('@'):
                 input_value = "@" + input_value
        
        is_valid, message = validation_function(input_value)

        if is_valid:
            return input_value
        else:
            print(message)

def input_send_message(from_user, connection):
    while (True):
        to_user = input("Enter the recipient's @ nickname: ") 

        if not to_user.startswith('@'):
            to_user = '@' + to_user 
            
        if not to_user or to_user == '@':
            print("Error: The nickname cannot be empty.") 
            continue 

        if connection.check_user_exists(to_user):
            title = input("Enter the message title: ") 
            while(True):
                text = input("Enter the message text (minimum 50 characters): ") 
                if len(text) >= 50:
                    text_bytes = bytes(text,'utf-8')
                    password_bytes = bytes(input("Enter the encryption key: "),'utf-8') 

                    encrypted_message = Security.encrypt(password_bytes, text_bytes) 

                    new_message = Message(
                        from_user,
                        to_user, 
                        title,
                        encrypted_message,
                        status="nao lida"
                    )

                    connection.send_message(new_message) 
                    
                    return print("\nMessage sent successfully\n") 
                    
                else:
                    print(f"The message has only {len(text)} characters. Minimum is 50!") 
        else:
            print(f" Error: The user '{to_user}' does not exist. Please try again.") 

def input_list_messages(logged_user, connection): 
    print("\n--- INBOX: UNREAD MESSAGES ---") 
    
    messages = connection.list_unread_messages(logged_user.nickname)
    
    if not messages:
        print("You have no unread messages.") 
        return

    print(f"You have {len(messages)} unread message(s):") 
    print("-" * 40)

    message_map = {} 
    
    for i, msg in enumerate(messages):
        number = i + 1 
        message_map[number] = msg 
        
        print(f"[{number}] From: {msg['from']} | Title: {msg['title']}") 
        print("-" * 40)
        
    while True:
        try:
            choice = input("Enter the [number] of the message to read (or [S] to exit): ").upper() 
            
            if choice == 'S':
                return
            
            chosen_number = int(choice) 
            
            if chosen_number in message_map:
                chosen_message = message_map[chosen_number] 
                
                print(f"\nMessage Details #{chosen_number}") 
                print(f"Title: {chosen_message['title']}")
                print(f"Sender: {chosen_message['from']}") 

                try:
                    password_bytes = bytes(input(" Enter the key to decrypt: "),'utf-8')
                    
                    encrypted_message = chosen_message['message'] 
                    
                    decrypted_message_bytes = Security.decrypt(password_bytes, encrypted_message) 
                    
                    original_text = decrypted_message_bytes.decode('utf-8') 
                    
                    print("\n=============================================")
                    print(f"** ORIGINAL MESSAGE **\n{original_text}") 
                    print("=============================================\n")
                    
                    if connection.mark_as_read(chosen_message['_id']):
                        print("Message marked as read.\n") 
                    else:
                        print(" Warning: Failed to update message status in the database.") 
                    return 
                        
                except Exception as e:
                    print(f" DECRYPTION ERROR: The key might be incorrect or the message corrupted. ({e})") 
                    
            else:
                print(" Invalid message number. Please try again.") 
        except ValueError:
            print(" Invalid input. Enter a number or 'S' to exit.") 