Feature: Login com Autenticação Multifator (MFA)

  # ── Happy Path ──
  Scenario: Login bem-sucedido com MFA válido
    Given que o usuário 'ana@email.com' está cadastrado
    And   a conta está ativa e desbloqueada
    When  ele informa e-mail e senha corretos
    And   insere o código MFA recebido por SMS
    Then  o sistema concede acesso à conta
    And   redireciona para a página inicial

  # ── Sad Path ──
  Scenario: Conta bloqueada após 3 tentativas incorretas
    Given que o usuário está no passo de inserção do MFA
    When  ele insere um código incorreto 3 vezes
    Then  a conta é bloqueada
    And   o usuário recebe notificação de bloqueio

  # ── Edge Case ──
  Scenario: Código MFA com espaços é rejeitado
    Given que o usuário está no passo de inserção do MFA
    When  ele insere '1 2 3 4 5 6' (com espaços)
    Then  o sistema exibe 'Formato inválido'
    And   a tentativa não é contabilizada