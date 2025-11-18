# CPF Validation API

Uma API REST desenvolvida com Flask para validação de CPF (Cadastro de Pessoa Física).

## Descrição

Esta aplicação fornece endpoints para validar números de CPF brasileiros. O CPF é validado através de algoritmos matemáticos que verificam os dígitos verificadores.

## Funcionalidades

- ✅ Validação de CPF individual
- ✅ Validação em lote de múltiplos CPFs
- ✅ Formatação automática de CPF (XXX.XXX.XXX-XX)
- ✅ Verificação de integridade através de dígitos verificadores
- ✅ Endpoints GET e POST
- ✅ Tratamento de erros robusto

## Estrutura do Projeto

```
cpf-validation-api/
├── app/
│   ├── __init__.py          # Inicialização da aplicação Flask
│   ├── routes.py            # Definição dos endpoints da API
│   └── validators.py        # Lógica de validação de CPF
├── tests/                   # Testes unitários
├── run.py                   # Entry point da aplicação
├── requirements.txt         # Dependências do projeto
├── README.md               # Este arquivo
└── LICENSE                 # Licença MIT
```

## Instalação

### Pré-requisitos

- Python 3.8+
- pip

### Passos

1. Clone o repositório:
```bash
cd cpf-validation-api
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

Para iniciar o servidor:

```bash
python run.py
```

O servidor estará disponível em `http://localhost:5000`

## Endpoints da API

### 1. Health Check
```
GET /api/health
```

Verifica se a API está funcionando.

**Resposta:**
```json
{
  "status": "ok",
  "message": "CPF Validation API is running"
}
```

### 2. Validar CPF (POST)
```
POST /api/validate
```

Valida um CPF através de POST.

**Request Body:**
```json
{
  "cpf": "12345678901"
}
```

**Resposta:**
```json
{
  "cpf": "123.456.789-01",
  "is_valid": true,
  "original": "12345678901",
  "length": 11
}
```

### 3. Validar CPF (GET)
```
GET /api/validate/:cpf
```

Valida um CPF através de GET.

**Exemplo:**
```
GET /api/validate/12345678901
```

**Resposta:**
```json
{
  "cpf": "123.456.789-01",
  "is_valid": true,
  "original": "12345678901",
  "length": 11
}
```

### 4. Validar Múltiplos CPFs
```
POST /api/validate-batch
```

Valida múltiplos CPFs em uma única requisição.

**Request Body:**
```json
{
  "cpfs": ["12345678901", "98765432100", "111.111.111-11"]
}
```

**Resposta:**
```json
{
  "results": [
    {
      "cpf": "123.456.789-01",
      "is_valid": true,
      "original": "12345678901"
    },
    {
      "cpf": "987.654.321-00",
      "is_valid": false,
      "original": "98765432100"
    },
    {
      "cpf": "111.111.111-11",
      "is_valid": false,
      "original": "111.111.111-11"
    }
  ],
  "total": 3,
  "valid_count": 1
}
```

## Regras de Validação

Um CPF é considerado válido quando:

1. Possui exatamente 11 dígitos
2. Não possui todos os dígitos iguais
3. Os dígitos verificadores estão corretos

Os dígitos verificadores são calculados usando o algoritmo específico de CPF.

## Exemplos de CPFs para Teste

- Válido: `123.456.789-09`
- Inválido: `111.111.111-11` (todos dígitos iguais)
- Inválido: `12345678901` (dígitos verificadores incorretos)

## Teste com cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Validar um CPF
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"cpf": "12345678909"}'

# Validar CPF via GET
curl http://localhost:5000/api/validate/12345678909

# Validar múltiplos CPFs
curl -X POST http://localhost:5000/api/validate-batch \
  -H "Content-Type: application/json" \
  -d '{"cpfs": ["12345678909", "98765432100"]}'
```

## Dependências

- **Flask**: Framework web para criar a API REST
- **Werkzeug**: Utilitários para WSGI

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

Desenvolvido como projeto educacional para demonstração de API REST com Flask e validação de CPF.

## Melhorias Futuras

- [ ] Adicionar testes unitários
- [ ] Validar origem do CPF (estado)
- [ ] Cache de resultados
- [ ] Rate limiting
- [ ] Autenticação de API key
- [ ] Documentação com Swagger/OpenAPI
