"""User model for registration."""

from datetime import datetime
from typing import Optional


class User:
    """User model for storing registration data."""
    
    # In-memory storage (in production, use a real database)
    _users = {}
    _id_counter = 1
    
    def __init__(self, name: str, address: str, cpf: str, birth_date: str, user_id: Optional[int] = None):
        """
        Initialize a User.
        
        Args:
            name (str): User's full name
            address (str): User's address
            cpf (str): User's CPF (without formatting)
            birth_date (str): User's birth date (YYYY-MM-DD format)
            user_id (int, optional): User ID (auto-generated if not provided)
        """
        if user_id is None:
            user_id = User._id_counter
            User._id_counter += 1
        
        self.id = user_id
        self.name = name
        self.address = address
        self.cpf = cpf
        self.birth_date = birth_date
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """
        Convert user to dictionary.
        
        Returns:
            dict: User data as dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'cpf': self.cpf,
            'birth_date': self.birth_date,
            'created_at': self.created_at
        }
    
    @classmethod
    def create(cls, name: str, address: str, cpf: str, birth_date: str) -> 'User':
        """
        Create and save a new user.
        
        Args:
            name (str): User's full name
            address (str): User's address
            cpf (str): User's CPF
            birth_date (str): User's birth date (YYYY-MM-DD format)
            
        Returns:
            User: The created user instance
        """
        user = cls(name, address, cpf, birth_date)
        cls._users[user.id] = user
        return user
    
    @classmethod
    def get_by_cpf(cls, cpf: str) -> Optional['User']:
        """
        Get user by CPF.
        
        Args:
            cpf (str): CPF to search for
            
        Returns:
            User or None: User if found, None otherwise
        """
        for user in cls._users.values():
            if user.cpf == cpf:
                return user
        return None
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """
        Get user by ID.
        
        Args:
            user_id (int): User ID
            
        Returns:
            User or None: User if found, None otherwise
        """
        return cls._users.get(user_id)
    
    @classmethod
    def get_all(cls) -> list:
        """
        Get all users.
        
        Returns:
            list: List of all users
        """
        return list(cls._users.values())
    
    @classmethod
    def reset(cls):
        """Reset all users (for testing)."""
        cls._users = {}
        cls._id_counter = 1
