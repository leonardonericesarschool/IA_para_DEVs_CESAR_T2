"""Main application for user registration."""

from service import UserRegistrationService
from models import User
import json


def print_separator(title: str = ""):
    """Print a formatted separator."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'-'*60}\n")


def display_user(user_dict: dict):
    """Display user information formatted."""
    print(f"  ID: {user_dict['id']}")
    print(f"  Nome: {user_dict['name']}")
    print(f"  Endereço: {user_dict['address']}")
    print(f"  CPF: {user_dict['cpf']}")
    print(f"  Data de Nascimento: {user_dict['birth_date']}")
    print(f"  Cadastrado em: {user_dict['created_at']}")


def main():
    """Main application flow."""
    
    print_separator("SISTEMA DE CADASTRO DE USUÁRIOS")
    print("Bem-vindo ao sistema de cadastro da loja virtual!")
    
    while True:
        print("\nOpções:")
        print("  1. Cadastrar novo usuário")
        print("  2. Listar todos os usuários")
        print("  3. Buscar usuário por ID")
        print("  4. Sair")
        
        choice = input("\nEscolha uma opção (1-4): ").strip()
        
        if choice == '1':
            print_separator("CADASTRO DE NOVO USUÁRIO")
            
            name = input("Nome completo: ").strip()
            address = input("Endereço: ").strip()
            cpf = input("CPF (com ou sem formatação): ").strip()
            birth_date = input("Data de nascimento (YYYY-MM-DD): ").strip()
            
            print("\nProcessando cadastro...")
            success, response = UserRegistrationService.register_user(name, address, cpf, birth_date)
            
            if success:
                print_separator("✓ CADASTRO REALIZADO COM SUCESSO")
                print(response['message'])
                print()
                display_user(response['user'])
            else:
                print_separator("✗ ERRO NO CADASTRO")
                print(f"Mensagem: {response['message']}")
                print("\nErros encontrados:")
                for i, error in enumerate(response['errors'], 1):
                    print(f"  {i}. {error}")
        
        elif choice == '2':
            print_separator("LISTA DE USUÁRIOS")
            success, response = UserRegistrationService.get_all_users()
            
            if response['total'] == 0:
                print("Nenhum usuário cadastrado.")
            else:
                print(f"Total de usuários: {response['total']}\n")
                for i, user in enumerate(response['users'], 1):
                    print(f"Usuário {i}:")
                    display_user(user)
                    print()
        
        elif choice == '3':
            print_separator("BUSCAR USUÁRIO POR ID")
            user_id = input("ID do usuário: ").strip()
            
            try:
                user_id = int(user_id)
                success, response = UserRegistrationService.get_user(user_id)
                
                if success:
                    print()
                    display_user(response['user'])
                else:
                    print(f"\n✗ {response['message']}")
            except ValueError:
                print("\n✗ ID deve ser um número inteiro.")
        
        elif choice == '4':
            print_separator("ENCERRANDO")
            print("Obrigado por usar o sistema de cadastro!")
            break
        
        else:
            print("\n✗ Opção inválida. Tente novamente.")


if __name__ == '__main__':
    main()
