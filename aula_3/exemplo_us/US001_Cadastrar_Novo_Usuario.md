# User Story 1: Cadastrar Novo Usuário na Loja Virtual

**Prioridade:** High

## Critérios de Aceitação

### Cenário 1: Usuário cadastra com sucesso informações válidas
```gherkin
Given que estou na página de cadastro
When preencho nome, endereço, CPF válido e data de nascimento
And clico no botão "Cadastrar"
Then o usuário é salvo na base de dados
And recebo mensagem de confirmação "Cadastro realizado com sucesso"
And sou redirecionado para a página de login
```

### Cenário 2: Validação de CPF inválido
```gherkin
Given que estou preenchendo o formulário de cadastro
When insiro um CPF inválido
And clico em "Cadastrar"
Then recebo erro "CPF inválido"
And o formulário não é enviado
```

### Cenário 3: Campo obrigatório não preenchido
```gherkin
Given que estou no formulário de cadastro
When deixo um ou mais campos obrigatórios em branco
And clico em "Cadastrar"
Then aparecem mensagens de erro indicando quais campos são obrigatórios
And nenhum dado é salvo
```

## Descrição

Como usuário da loja virtual, desejo cadastrar minha conta com informações pessoais para poder fazer compras.

## Requisitos

- Validação de CPF com algoritmo de dígitos verificadores
- Armazenamento seguro de dados pessoais
- Confirmação de cadastro bem-sucedido
