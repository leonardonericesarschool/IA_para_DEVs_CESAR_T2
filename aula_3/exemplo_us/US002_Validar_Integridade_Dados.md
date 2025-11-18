# User Story 2: Validar Integridade dos Dados Cadastrados

**Prioridade:** High

## Critérios de Aceitação

### Cenário 1: Validar formato de endereço
```gherkin
Given que estou preenchendo o endereço
When insiro um endereço com menos de 10 caracteres
And clico em "Cadastrar"
Then recebo aviso "Endereço muito curto"
And o formulário não é enviado
```

### Cenário 2: Verificar data de nascimento válida
```gherkin
Given que estou preenchendo a data de nascimento
When insiro uma data futura
And clico em "Cadastrar"
Then recebo erro "Data de nascimento não pode ser futura"
And o cadastro não é realizado
```

### Cenário 3: Validar CPF duplicado
```gherkin
Given que existe um CPF já cadastrado na base
When tento cadastrar um novo usuário com o mesmo CPF
And clico em "Cadastrar"
Then recebo erro "CPF já cadastrado"
And o novo cadastro é bloqueado
```

## Descrição

Como administrador da loja, desejo garantir que todos os dados cadastrados sejam válidos e íntegros para manter a qualidade da base de dados.

## Requisitos

- Validação de endereço (mínimo de caracteres)
- Validação de data de nascimento (não futura)
- Verificação de CPF duplicado no banco de dados
- Mensagens de erro claras e específicas
