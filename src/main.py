from database.database_manager import DatabaseManager
from database.connection_string import URI
from classes.user import User
from classes.security import Security
from classes.message import Message

DB_NAME = "Mensageria"
connection = DatabaseManager(URI,DB_NAME)
connection.connect()

def obter_input_valido(prompt: str, funcao_validacao):

    while(True):
        
        valor_input = input(prompt)

        if not valor_input:
            print("Este campo não pode ser vazio")
            continue
        
        if "nickname" in prompt.lower():
            valor_input = "@" + valor_input

        is_valid, mensagem = funcao_validacao(valor_input)

        if is_valid:
            return valor_input
        else:
            print(mensagem)

def input_enviar_mensagem(from_user):
    while (True):
        to_user = input("Digite o @ do destinatário: ")

        if not to_user.startswith('@'):
            to_user = '@' + to_user 
            
        if not to_user or to_user == '@':
            print("Erro: O nome de usuário não pode ser vazio.")
            continue 

        if connection.verificar_usuario_existe(to_user):
            title = input("Digite o título da mensagem: ")
            while(True):
                text = input("Digite o texto da mensagem (mínimo 50 caracteres): ")
                if len(text) >= 50:
                    text_bytes = bytes(text,'utf-8')
                    senha_bytes = bytes(input("Digite a chave para criptografar: "),'utf-8')

                    mensagem_cifrada = Security.encrypt(senha_bytes,text_bytes)

                    new_message = Message(
                        from_user,
                        to_user,
                        title,
                        mensagem_cifrada,
                        status="nao lida"
                    )
                    connection.enviar_mensagem(new_message) 
                    
                    return print("\nMensagem enviada com sucesso\n")
                    
                else:
                    print(f"A mensagem possui apenas {len(text)} caracteres, minimo é 50!!")
        else:
            print(f" Erro: O usuário '{to_user}' não existe. Tente novamente.")
            
def input_listar_mensagens(usuario_logado, connection):
    print("\n--- CAIXA DE ENTRADA: MENSAGENS NÃO LIDAS ---")
    
    mensagens = connection.listar_mensagens_nao_lidas(usuario_logado.nickname)
    
    if not mensagens:
        print("Você não tem mensagens não lidas.")
        return

    print(f"Você tem {len(mensagens)} mensagem(ns) não lida(s):")
    print("-" * 40)

    mapa_mensagens = {} 
    
    for i, msg in enumerate(mensagens):
        numero = i + 1
        mapa_mensagens[numero] = msg 
        
        print(f"[{numero}] De: {msg['from']} | Título: {msg['title']}")
        print("-" * 40)
        
    while True:
        try:
            escolha = input("Digite o [número] da mensagem que deseja ler (ou [S] para sair): ").upper()
            
            if escolha == 'S':
                return
            
            numero_escolhido = int(escolha)
            
            if numero_escolhido in mapa_mensagens:
                msg_escolhida = mapa_mensagens[numero_escolhido]
                
                print(f"\nDetalhes da Mensagem #{numero_escolhido}")
                print(f"Título: {msg_escolhida['title']}")
                print(f"Remetente: {msg_escolhida['from']}")

                try:
                    senha_bytes = bytes(input(" Digite a chave para descriptografar: "),'utf-8')
                    
                    mensagem_cifrada = msg_escolhida['message']
                    
                    mensagem_descriptografada_bytes = Security.decrypt(senha_bytes, mensagem_cifrada)
                    
                    texto_original = mensagem_descriptografada_bytes.decode('utf-8')
                    
                    print("\n=============================================")
                    print(f"** MENSAGEM ORIGINAL **\n{texto_original}")
                    print("=============================================\n")
                    
                    if connection.marcar_como_lida(msg_escolhida['_id']):
                        print("\n")
                    else:
                        print(" Aviso: Falha ao atualizar o status da mensagem no banco de dados.")
                    return 
                        
                except Exception as e:
                    print(f" ERRO na Descriptografia: A chave pode estar incorreta ou a mensagem corrompida. ({e})")
                    
            else:
                print(" Número de mensagem inválido. Tente novamente.")           
        except ValueError:
            print(" Entrada inválida. Digite um número ou 'S' para sair.")

def main():
    
    db = connection.getDataBase()
    
    usuario_logado = None 

    while True:
        print("\n--- Sistema de Mensagem ---")
        
        if usuario_logado:
            print(f"Bem-vindo, {usuario_logado.nickname}!")
            print("1. Enviar Mensagem")
            print("2. listar mensagens")
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
                print("------------------------\n")
                if not email or not senha:
                    print("E-mail e senha são obrigatórios.")
                    continue
                
                usuario_logado = User.login(db, email, senha) 
                
                if usuario_logado:
                    print(f"Você está logado como {usuario_logado.nickname}.")
                    
            elif escolha == '2':
                print("\n--- Criação de Conta ---")
    
                email = obter_input_valido("Digite seu e-mail: ", User.validar_email)
                senha = obter_input_valido("Digite sua senha: ", User.validar_senha)
                nickname = obter_input_valido("Digite o seu nickname: ", User.validar_nickname)

                usuario_logado = User(email,senha,nickname)
                usuario_logado.cadastro(db)
                

            elif escolha == '3':
                print("Saindo do programa. Até mais!")
                break
            
            else:
                print("Opção inválida. Por favor, tente novamente.")
                
        else: 
            if escolha == '1':
                input_enviar_mensagem(usuario_logado.nickname)
                
            elif escolha == '2':
                input_listar_mensagens(usuario_logado, connection)
                
            elif escolha == '3':
                print("Saindo do programa. Até mais!")
                break
            
            else:
                print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
