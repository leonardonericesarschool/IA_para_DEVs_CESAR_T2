"""Test cases for US001 - Cadastrar Novo Usuário."""

import unittest
from models import User
from validators import UserRegistrationValidator, format_cpf, is_valid_cpf
from service import UserRegistrationService


class TestUserRegistration(unittest.TestCase):
    """Test cases for user registration."""
    
    def setUp(self):
        """Reset users before each test."""
        User.reset()
    
    # ============================================================================
    # Cenário 1: Usuário cadastra com sucesso informações válidas
    # ============================================================================
    
    def test_scenario_1_successful_registration_with_valid_data(self):
        """
        Scenario: Usuário cadastra com sucesso informações válidas
        Given que estou na página de cadastro
        When preencho nome, endereço, CPF válido e data de nascimento
        And clico no botão "Cadastrar"
        Then o usuário é salvo na base de dados
        And recebo mensagem de confirmação "Cadastro realizado com sucesso"
        """
        # Given
        User.reset()
        
        # When
        success, response = UserRegistrationService.register_user(
            name="João Silva",
            address="Rua das Flores 123, São Paulo, SP",
            cpf="123.456.789-09",
            birth_date="1990-05-15"
        )
        
        # Then
        self.assertTrue(success)
        self.assertIn('message', response)
        self.assertEqual(response['message'], 'Cadastro realizado com sucesso')
        self.assertIn('user', response)
        
        user = response['user']
        self.assertEqual(user['name'], 'João Silva')
        self.assertEqual(user['address'], 'Rua das Flores 123, São Paulo, SP')
        self.assertEqual(user['cpf'], '123.456.789-09')
        self.assertEqual(user['birth_date'], '1990-05-15')
        
        # Verify user is saved in database
        saved_user = User.get_by_id(user['id'])
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.name, 'João Silva')
    
    # ============================================================================
    # Cenário 2: Validação de CPF inválido
    # ============================================================================
    
    def test_scenario_2_invalid_cpf_validation(self):
        """
        Scenario: Validação de CPF inválido
        Given que estou preenchendo o formulário de cadastro
        When insiro um CPF inválido
        And clico em "Cadastrar"
        Then recebo erro "CPF inválido"
        And o formulário não é enviado (usuário não é criado)
        """
        # When
        success, response = UserRegistrationService.register_user(
            name="João Silva",
            address="Rua das Flores 123, São Paulo, SP",
            cpf="123.456.789-00",  # Invalid CPF
            birth_date="1990-05-15"
        )
        
        # Then
        self.assertFalse(success)
        self.assertIn('errors', response)
        self.assertIn('CPF inválido', response['errors'])
        
        # Verify no user was created
        users = User.get_all()
        self.assertEqual(len(users), 0)
    
    # ============================================================================
    # Cenário 3: Campo obrigatório não preenchido
    # ============================================================================
    
    def test_scenario_3_missing_required_field_name(self):
        """
        Scenario: Campo obrigatório não preenchido (Nome)
        Given que estou no formulário de cadastro
        When deixo o campo nome em branco
        And clico em "Cadastrar"
        Then aparecem mensagens de erro indicando que o campo é obrigatório
        And nenhum dado é salvo
        """
        # When
        success, response = UserRegistrationService.register_user(
            name="",
            address="Rua das Flores 123, São Paulo, SP",
            cpf="123.456.789-09",
            birth_date="1990-05-15"
        )
        
        # Then
        self.assertFalse(success)
        self.assertIn('errors', response)
        self.assertTrue(any('Nome é obrigatório' in error for error in response['errors']))
        
        # Verify no user was created
        users = User.get_all()
        self.assertEqual(len(users), 0)
    
    def test_scenario_3_missing_required_field_address(self):
        """
        Scenario: Campo obrigatório não preenchido (Endereço)
        """
        # When
        success, response = UserRegistrationService.register_user(
            name="João Silva",
            address="",
            cpf="123.456.789-09",
            birth_date="1990-05-15"
        )
        
        # Then
        self.assertFalse(success)
        self.assertIn('errors', response)
        self.assertTrue(any('Endereço é obrigatório' in error for error in response['errors']))
        
        # Verify no user was created
        users = User.get_all()
        self.assertEqual(len(users), 0)
    
    def test_scenario_3_missing_required_field_cpf(self):
        """
        Scenario: Campo obrigatório não preenchido (CPF)
        """
        # When
        success, response = UserRegistrationService.register_user(
            name="João Silva",
            address="Rua das Flores 123, São Paulo, SP",
            cpf="",
            birth_date="1990-05-15"
        )
        
        # Then
        self.assertFalse(success)
        self.assertIn('errors', response)
        self.assertTrue(any('CPF é obrigatório' in error for error in response['errors']))
        
        # Verify no user was created
        users = User.get_all()
        self.assertEqual(len(users), 0)
    
    def test_scenario_3_missing_required_field_birth_date(self):
        """
        Scenario: Campo obrigatório não preenchido (Data de nascimento)
        """
        # When
        success, response = UserRegistrationService.register_user(
            name="João Silva",
            address="Rua das Flores 123, São Paulo, SP",
            cpf="123.456.789-09",
            birth_date=""
        )
        
        # Then
        self.assertFalse(success)
        self.assertIn('errors', response)
        self.assertTrue(any('Data de nascimento é obrigatória' in error for error in response['errors']))
        
        # Verify no user was created
        users = User.get_all()
        self.assertEqual(len(users), 0)
    
    # ============================================================================
    # Additional validation tests
    # ============================================================================
    
    def test_cpf_format_with_and_without_formatting(self):
        """Test CPF validation with and without formatting."""
        # Valid CPF with formatting
        self.assertTrue(is_valid_cpf("123.456.789-09"))
        
        # Valid CPF without formatting
        self.assertTrue(is_valid_cpf("12345678909"))
        
        # Invalid CPF
        self.assertFalse(is_valid_cpf("123.456.789-00"))
    
    def test_cpf_duplicate_detection(self):
        """Test that duplicate CPF is detected."""
        # Create first user
        success1, response1 = UserRegistrationService.register_user(
            name="João Silva",
            address="Rua das Flores 123, São Paulo, SP",
            cpf="123.456.789-09",
            birth_date="1990-05-15"
        )
        self.assertTrue(success1)
        
        # Try to create second user with same CPF
        success2, response2 = UserRegistrationService.register_user(
            name="Maria Silva",
            address="Rua das Flores 456, Rio de Janeiro, RJ",
            cpf="123.456.789-09",
            birth_date="1992-03-20"
        )
        
        # Should fail due to duplicate CPF
        self.assertFalse(success2)
        self.assertIn('CPF já cadastrado', response2['errors'])
        
        # Only one user should be in database
        users = User.get_all()
        self.assertEqual(len(users), 1)
    
    def test_future_birth_date_validation(self):
        """Test that future birth date is rejected."""
        success, response = UserRegistrationService.register_user(
            name="João Silva",
            address="Rua das Flores 123, São Paulo, SP",
            cpf="123.456.789-09",
            birth_date="2030-05-15"  # Future date
        )
        
        self.assertFalse(success)
        self.assertIn('Data de nascimento não pode ser no futuro', response['errors'])
    
    def test_address_minimum_length(self):
        """Test that address must have minimum length."""
        success, response = UserRegistrationService.register_user(
            name="João Silva",
            address="Rua",  # Too short
            cpf="123.456.789-09",
            birth_date="1990-05-15"
        )
        
        self.assertFalse(success)
        self.assertIn('Endereço muito curto', response['errors'])
    
    def test_name_minimum_length(self):
        """Test that name must have minimum length."""
        success, response = UserRegistrationService.register_user(
            name="Jo",  # Too short
            address="Rua das Flores 123, São Paulo, SP",
            cpf="123.456.789-09",
            birth_date="1990-05-15"
        )
        
        self.assertFalse(success)
        self.assertIn('Nome deve ter pelo menos 3 caracteres', response['errors'])


if __name__ == '__main__':
    unittest.main()
