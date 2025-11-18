"""User registration service."""

from models import User
from validators import UserRegistrationValidator, format_cpf
from typing import Tuple, List, Dict


class UserRegistrationService:
    """Service for managing user registration."""
    
    @staticmethod
    def register_user(name: str, address: str, cpf: str, birth_date: str) -> Tuple[bool, Dict]:
        """
        Register a new user with validation.
        
        Args:
            name (str): User's full name
            address (str): User's address
            cpf (str): User's CPF
            birth_date (str): User's birth date (YYYY-MM-DD format)
            
        Returns:
            Tuple[bool, Dict]: (success, response_dict)
                - If success: {
                    'message': 'Cadastro realizado com sucesso',
                    'user': {...user data...}
                  }
                - If error: {
                    'message': 'Dados inválidos',
                    'errors': [...list of errors...]
                  }
        """
        # Get existing users for duplicate check
        existing_users = User.get_all()
        
        # Validate all data
        is_valid, errors = UserRegistrationValidator.validate_all(
            name, address, cpf, birth_date, existing_users
        )
        
        if not is_valid:
            return False, {
                'message': 'Dados inválidos',
                'errors': errors
            }
        
        try:
            # Format CPF
            formatted_cpf = format_cpf(cpf)
            
            # Create user
            user = User.create(name, address, formatted_cpf, birth_date)
            
            # Format CPF for display
            formatted_cpf_display = f"{formatted_cpf[0:3]}.{formatted_cpf[3:6]}.{formatted_cpf[6:9]}-{formatted_cpf[9:11]}"
            
            return True, {
                'message': 'Cadastro realizado com sucesso',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'address': user.address,
                    'cpf': formatted_cpf_display,
                    'birth_date': user.birth_date,
                    'created_at': user.created_at
                }
            }
        
        except Exception as e:
            return False, {
                'message': 'Erro ao realizar cadastro',
                'error': str(e)
            }
    
    @staticmethod
    def get_user(user_id: int) -> Tuple[bool, Dict]:
        """
        Get user by ID.
        
        Args:
            user_id (int): User ID
            
        Returns:
            Tuple[bool, Dict]: (success, response_dict)
        """
        user = User.get_by_id(user_id)
        
        if not user:
            return False, {
                'message': 'Usuário não encontrado'
            }
        
        # Format CPF for display
        formatted_cpf = f"{user.cpf[0:3]}.{user.cpf[3:6]}.{user.cpf[6:9]}-{user.cpf[9:11]}"
        
        return True, {
            'user': {
                'id': user.id,
                'name': user.name,
                'address': user.address,
                'cpf': formatted_cpf,
                'birth_date': user.birth_date,
                'created_at': user.created_at
            }
        }
    
    @staticmethod
    def get_all_users() -> Tuple[bool, Dict]:
        """
        Get all registered users.
        
        Returns:
            Tuple[bool, Dict]: (success, response_dict)
        """
        users = User.get_all()
        users_list = []
        
        for user in users:
            formatted_cpf = f"{user.cpf[0:3]}.{user.cpf[3:6]}.{user.cpf[6:9]}-{user.cpf[9:11]}"
            users_list.append({
                'id': user.id,
                'name': user.name,
                'address': user.address,
                'cpf': formatted_cpf,
                'birth_date': user.birth_date,
                'created_at': user.created_at
            })
        
        return True, {
            'total': len(users_list),
            'users': users_list
        }
