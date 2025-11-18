# Implementação da US001 - Cadastrar Novo Usuário na Loja Virtual

## Estrutura do Projeto

### Arquivos Criados:

1. **models.py** - Modelo de dados
   - Classe `User`: Representa um usuário com todos seus atributos
   - Métodos de CRUD para gerenciar usuários em memória

2. **validators.py** - Validações
   - Função `format_cpf()`: Remove formatação do CPF
   - Função `is_valid_cpf()`: Valida CPF usando algoritmo de dígitos verificadores
   - Classe `UserRegistrationValidator`: Valida cada campo do cadastro

3. **service.py** - Lógica de negócio
   - Classe `UserRegistrationService`: Orquestra o registro de usuários
   - Método `register_user()`: Realiza todo o fluxo de cadastro
   - Métodos de consulta de usuários

4. **test_us001.py** - Testes automatizados
   - Testes para todos os 3 cenários do Gherkin
   - Testes adicionais para validações específicas

5. **main.py** - Aplicação interativa
   - Menu para interagir com o sistema
   - Opções de cadastro, listagem e busca

## Como Executar

### 1. Executar os Testes Automatizados

```bash
cd /home/lvn/IA_para_DEVs_CESAR_T2/aula_3/exemplo_Python_US001
python -m pytest test_us001.py -v
```

Ou:

```bash
python test_us001.py
```

### 2. Executar a Aplicação Interativa

```bash
python main.py
```

## Implementação dos Critérios de Aceitação

### Cenário 1: Usuário cadastra com sucesso informações válidas

**Gherkin:**
```gherkin
Given que estou na página de cadastro
When preencho nome, endereço, CPF válido e data de nascimento
And clico no botão "Cadastrar"
Then o usuário é salvo na base de dados
And recebo mensagem de confirmação "Cadastro realizado com sucesso"
And sou redirecionado para a página de login
```

**Implementação:**
- ✅ `UserRegistrationService.register_user()` valida todos os campos
- ✅ Se válidos, cria um novo `User` e o salva em memória
- ✅ Retorna mensagem "Cadastro realizado com sucesso"
- ✅ Retorna os dados do usuário criado

**Teste:** `test_scenario_1_successful_registration_with_valid_data()`

---

### Cenário 2: Validação de CPF inválido

**Gherkin:**
```gherkin
Given que estou preenchendo o formulário de cadastro
When insiro um CPF inválido
And clico em "Cadastrar"
Then recebo erro "CPF inválido"
And o formulário não é enviado
```

**Implementação:**
- ✅ `UserRegistrationValidator.validate_cpf()` valida o CPF usando algoritmo de dígitos verificadores
- ✅ Se CPF inválido, retorna erro "CPF inválido"
- ✅ `register_user()` não cria o usuário em caso de erro
- ✅ Não há redirecionamento (fluxo é bloqueado)

**Teste:** `test_scenario_2_invalid_cpf_validation()`

---

### Cenário 3: Campo obrigatório não preenchido

**Gherkin:**
```gherkin
Given que estou no formulário de cadastro
When deixo um ou mais campos obrigatórios em branco
And clico em "Cadastrar"
Then aparecem mensagens de erro indicando quais campos são obrigatórios
And nenhum dado é salvo
```

**Implementação:**
- ✅ `validate_all()` verifica todos os campos obrigatórios
- ✅ Cada validação específica retorna uma mensagem de erro clara
- ✅ Lista de erros é retornada ao usuário
- ✅ Usuário não é criado se houver erros

**Testes:**
- `test_scenario_3_missing_required_field_name()`
- `test_scenario_3_missing_required_field_address()`
- `test_scenario_3_missing_required_field_cpf()`
- `test_scenario_3_missing_required_field_birth_date()`

---

## Validações Implementadas

### Nome
- ✅ Obrigatório
- ✅ Mínimo 3 caracteres
- ✅ Máximo 150 caracteres
- ✅ Apenas letras, espaços e caracteres comuns (-, ', .)

### Endereço
- ✅ Obrigatório
- ✅ Mínimo 10 caracteres
- ✅ Máximo 300 caracteres

### CPF
- ✅ Obrigatório
- ✅ Deve conter 11 dígitos
- ✅ Validação de dígitos verificadores
- ✅ Não pode conter todos os dígitos iguais
- ✅ Não pode ser duplicado (CPF já cadastrado)
- ✅ Aceita formatação com ou sem pontos/hífen

### Data de Nascimento
- ✅ Obrigatório
- ✅ Formato YYYY-MM-DD
- ✅ Não pode ser data futura
- ✅ Pessoa deve ter pelo menos 18 anos

---

## Exemplos de Uso

### Cadastro Bem-sucedido

```python
from service import UserRegistrationService

success, response = UserRegistrationService.register_user(
    name="João Silva",
    address="Rua das Flores 123, São Paulo, SP",
    cpf="123.456.789-09",
    birth_date="1990-05-15"
)

if success:
    print(response['message'])
    print(response['user'])
```

### Verificação de CPF Inválido

```python
success, response = UserRegistrationService.register_user(
    name="João Silva",
    address="Rua das Flores 123, São Paulo, SP",
    cpf="123.456.789-00",  # CPF inválido
    birth_date="1990-05-15"
)

# Retorno:
# success = False
# response['errors'] = ['CPF inválido']
```

### Verificação de Duplicação de CPF

```python
# Primeiro cadastro
success1, _ = UserRegistrationService.register_user(
    name="João Silva",
    address="Rua das Flores 123, São Paulo, SP",
    cpf="123.456.789-09",
    birth_date="1990-05-15"
)

# Tentativa de cadastro com mesmo CPF
success2, response = UserRegistrationService.register_user(
    name="Maria Silva",
    address="Rua das Flores 456, Rio de Janeiro, RJ",
    cpf="123.456.789-09",
    birth_date="1992-03-20"
)

# Retorno:
# success2 = False
# response['errors'] = ['CPF já cadastrado']
```

---

## Padrões de Código

- ✅ Type hints em todas as funções
- ✅ Docstrings detalhadas
- ✅ Separação clara de responsabilidades (models, validators, service)
- ✅ Testes unitários completos
- ✅ Tratamento de erros apropriado
- ✅ Código limpo e reutilizável
