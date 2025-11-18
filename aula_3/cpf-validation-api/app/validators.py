"""CPF validation module."""

import re


def format_cpf(cpf):
    """Remove formatting from CPF string.
    
    Args:
        cpf (str): CPF string with or without formatting
        
    Returns:
        str: CPF string without formatting
    """
    return re.sub(r'\D', '', cpf)


def is_valid_cpf(cpf):
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


def get_cpf_info(cpf: str) -> dict:
    """
    Get information about a CPF.
    
    Args:
        cpf (str): CPF string with or without formatting
        
    Returns:
        dict: Dictionary with CPF information
    """
    formatted = format_cpf(cpf)
    is_valid = is_valid_cpf(cpf)
    
    return {
        'original': cpf,
        'formatted': f'{formatted[0:3]}.{formatted[3:6]}.{formatted[6:9]}-{formatted[9:11]}' if len(formatted) == 11 else formatted,
        'is_valid': is_valid,
        'length': len(formatted)
    }
