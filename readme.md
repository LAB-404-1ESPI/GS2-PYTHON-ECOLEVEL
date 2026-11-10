# EcoLevel — Protótipo em Python

## GRUPO - LAB-404
### INTEGRANTES:
      Arthur Caram Fiorese Herrada - RM569578
	  Matheus Medeiros da Cunha - RM572780
	  Matheus Sequeira Franco da Silva - RM571127
	  Gustavo Ferreira Silva - RM571675
	  Felipe Ricardo Moreira Aguiar - RM573410

## 1. Descrição
EcoLevel é uma plataforma de incentivo à reciclagem. O protótipo simula o fluxo descrito na documentação: o usuário cria uma conta e recebe um ID único, escolhe um ponto de descarte, registra o peso bruto de um saco e recebe uma identificação de sessão. Depois, a equipe de triagem informa o peso efetivamente reciclável. O sistema credita moedas e XP somente sobre o peso aprovado.

## 2. Funcionalidades
- Cadastro de usuários com ID único e entrada por ID.
- Menu de pontos de descarte demonstrativos e status operacional.
- Registro de sessão de descarte e emissão de etiqueta textual demonstrativa.
- Painel da equipe para consultar a fila e validar a triagem.
- Separação entre peso bruto, peso reciclável aprovado e peso rejeitado.
- Crédito de 10 Moedas EcoLevel por quilograma aprovado.
- Progressão de níveis por XP e bônus de moedas ao avançar.
- Carteira, histórico de descartes e catálogo/resgate de recompensas.
- Persistência automática de dados em `data.json`.

## 3. Requisitos
- Python 3.10 ou superior.
- Não utiliza bibliotecas externas; somente módulos da biblioteca padrão do Python.

## 4. Como executar
1. Extraia o arquivo ZIP.
2. Abra a pasta `EcoLevel_Projeto`.
3. Execute no terminal:

   ```bash
   python main.py
   ```

   Em alguns computadores, o comando pode ser `python3 main.py`.

4. O arquivo `data.json` será criado automaticamente na primeira execução e atualizado durante o uso.

## 5. Como testar o fluxo principal
1. No menu inicial, escolha `1 - Criar conta`.
2. Informe nome e e-mail. Guarde o ID apresentado (ex.: `EC0001`).
3. No menu do usuário, escolha `2 - Registrar descarte / pesar saco`.
4. Selecione um ponto disponível (por exemplo, `M001`) e informe o peso bruto.
5. Volte ao menu inicial e escolha `3 - Painel da equipe de triagem`.
6. Use a senha demonstrativa `TRIAGEM2026`.
7. Escolha `2 - Analisar uma sessão`, informe o código da sessão e o peso reciclável aprovado. O peso aprovado não pode superar o peso bruto.
8. Entre novamente com o ID do usuário e consulte a carteira e o histórico.

## 6. Regras de negócio implementadas
- O crédito de moedas considera somente o peso reciclável aprovado pela triagem humana.
- Cada quilograma aprovado gera 10 moedas.
- Para demonstrar a progressão, o protótipo também atribui 10 XP por quilograma aprovado. **Essa taxa de XP é uma regra de implementação proposta para o protótipo**, pois a documentação do projeto define a progressão por marcos, mas não fixa uma taxa de XP por quilograma.
- Marcos acumulados de XP: nível 2 em 100 XP, nível 3 em 250 XP, nível 4 em 500 XP e nível 5 em 850 XP.
- Bônus por evolução: 10, 10, 10 e 15 moedas, respectivamente.
- Recompensas e seus custos são exemplos demonstrativos e podem ser alterados pela equipe.
- Uma sessão já analisada não pode receber novo crédito.

## 7. Requisitos da atividade atendidos
| Requisito | Onde aparece |
|---|---|
| Menu de opções | `main()`, `user_menu()` e `admin_menu()` |
| Validação de entradas | `read_non_empty()`, `read_positive_float()` e validações das operações |
| Tratamento de exceções | `try/except` na leitura JSON, entrada numérica e execução principal |
| `if/elif/else` | Validações de cadastro, peso, saldo e triagem |
| `match/case` | Menus principal, usuário e triagem |
| `while` e `for` | Menus, validações, listagens e cálculo de níveis |
| Funções com parâmetros e retorno | Funções de cadastro, login, consulta, triagem e persistência |
| Listas, tuplas e dicionários | Sessões, máquinas, recompensas, níveis e usuários |
| Arquivos JSON | `load_data()` e `save_data()` |
| Boas práticas | Funções separadas, nomes descritivos e comentários |

## 8. Acesso demonstrativo da equipe
- Senha: `TRIAGEM2026`
- Essa senha existe apenas para permitir a demonstração do painel. Não é uma solução de segurança para uso real.

## 9. Limitações e evoluções futuras
Este trabalho é uma simulação acadêmica. Não há conexão real com balanças, impressoras térmicas, máquinas, GPS, mapas, cooperativas ou empresas parceiras. Os pontos exibidos são demonstrativos. Em uma versão futura, essas integrações exigiriam hardware, serviços externos, autenticação adequada e acordos operacionais.

## 10. Arquivos
- `main.py`: código-fonte da aplicação.
- `data.json`: arquivo inicial de persistência (criado/atualizado pelo programa).
- `prompt.md`: descrição transparente do uso de IA.
- `readme.md`: documentação de instalação, execução, testes e requisitos.
