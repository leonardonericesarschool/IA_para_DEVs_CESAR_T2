"""Validators for user registration."""

import re
from datetime import datetime
from typing import Tuple, List


def format_cpf(cpf: str) -> str:
    """Remove formatting from CPF string.
    
    Args:
        cpf (str): CPF string with or without formatting
        
    Returns:
        str: CPF string without formatting
    """
    return re.sub(r'\D', '', cpf)


def is_valid_cpf(cpf: str) -> bool:
    """
    Validate a CPF number.
    
    A valid CPF has:
    - 11 digits
    - Not all digits the same
    - Correct check digits
    
    Args:
        cpf (str): CPF string with or without formatting
        
    Returns:
        bool: True if CPF is valid, False otherwise
    """
    # Remove formatting
    cpf = format_cpf(cpf)
    
    # Check length
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    
    # Check if all digits are the same
    if cpf == cpf[0] * 11:
        return False
    
    # Validate first check digit
    sum_first = sum(int(cpf[i]) * (10 - i) for i in range(9))
    first_digit = 11 - (sum_first % 11)
    first_digit = 0 if first_digit > 9 else first_digit
    
    if int(cpf[9]) != first_digit:
        return False
    
    # Validate second check digit
    sum_second = sum(int(cpf[i]) * (11 - i) for i in range(10))
    second_digit = 11 - (sum_second % 11)
    second_digit = 0 if second_digit > 9 else second_digit
    
    if int(cpf[10]) != second_digit:
        return False
    
    return True


class UserRegistrationValidator:
    """Validator for user registration data."""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """
        Validate user name.
        
        Args:
            name (str): User's name
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not name:
            return False, "Nome é obrigatório"
        
        if not isinstance(name, str):
            return False, "Nome deve ser texto"
        
        name = name.strip()
        if len(name) < 3:
            return False, "Nome deve ter pelo menos 3 caracteres"
        
        if len(name) > 150:
            return False, "Nome não pode ter mais de 150 caracteres"
        
        # Check if name contains only letters, spaces, and common characters
        if not all(c.isalpha() or c.isspace() or c in "'-." for c in name):
            return False, "Nome contém caracteres inválidos"
        
        return True, ""
    
    @staticmethod
    def validate_address(address: str) -> Tuple[bool, str]:
        """
        Validate user address.
        
        Args:
            address (str): User's address
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not address:
            return False, "Endereço é obrigatório"
        
        if not isinstance(address, str):
            return False, "Endereço deve ser texto"
        
        address = address.strip()
        if len(address) < 10:
            return False, "Endereço muito curto (mínimo 10 caracteres)"
        
        if len(address) > 300:
            return False, "Endereço não pode ter mais de 300 caracteres"
        
        return True, ""
    
    @staticmethod
    def validate_cpf(cpf: str, existing_users: List = None) -> Tuple[bool, str]:
        """
        Validate CPF.
        
        Args:
            cpf (str): CPF to validate
            existing_users (List, optional): List of existing users to check for duplicates
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not cpf:
            return False, "CPF é obrigatório"
        
        if not isinstance(cpf, str):
            return False, "CPF deve ser texto"
        
        formatted = format_cpf(cpf)
        
        if len(formatted) != 11:
            return False, "CPF deve conter 11 dígitos"
        
        if not is_valid_cpf(cpf):
            return False, "CPF inválido"
        
        # Check for duplicate CPF
        if existing_users:
            for user in existing_users:
                if user.cpf == formatted:
                    return False, "CPF já cadastrado"
        
        return True, ""
    
    @staticmethod
    def validate_birth_date(birth_date: str) -> Tuple[bool, str]:
        """
        Validate birth date.
        
        Args:
            birth_date (str): Birth date in YYYY-MM-DD format
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not birth_date:
            return False, "Data de nascimento é obrigatória"
        
        if not isinstance(birth_date, str):
            return False, "Data de nascimento deve ser texto"
        
        # Check format
        try:
            birth_datetime = datetime.strptime(birth_date, "%Y-%m-%d")
        except ValueError:
            return False, "Data de nascimento deve estar no formato YYYY-MM-DD"
        
        # Check if date is not in the future
        today = datetime.now()
        if birth_datetime > today:
            return False, "Data de nascimento não pode ser no futuro"
        
        # Check if person is at least 18 years old
        age_difference = today.year - birth_datetime.year
        if (today.month, today.day) < (birth_datetime.month, birth_datetime.day):
            age_difference -= 1
        
        if age_difference < 18:
            return False, "Usuário deve ter pelo menos 18 anos"
        
        return True, ""
    
    @staticmethod
    def validate_all(name: str, address: str, cpf: str, birth_date: str, existing_users: List = None) -> Tuple[bool, List[str]]:
        """
        Validate all user registration data.
        
        Args:
            name (str): User's name
            address (str): User's address
            cpf (str): User's CPF
            birth_date (str): User's birth date
            existing_users (List, optional): List of existing users to check for duplicates
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        name_valid, name_error = UserRegistrationValidator.validate_name(name)
        if not name_valid:
            errors.append(name_error)
        
        address_valid, address_error = UserRegistrationValidator.validate_address(address)
        if not address_valid:
            errors.append(address_error)
        
        cpf_valid, cpf_error = UserRegistrationValidator.validate_cpf(cpf, existing_users)
        if not cpf_valid:
            errors.append(cpf_error)
        
        birth_date_valid, birth_date_error = UserRegistrationValidator.validate_birth_date(birth_date)
        if not birth_date_valid:
            errors.append(birth_date_error)
        
        return len(errors) == 0, errors
