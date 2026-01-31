# Guia de Implementação: Resumos Inteligentes e Integração de Dados com LangChain

Este guia detalha como utilizamos o **LangChain** para criar funcionalidades de Inteligência Artificial no projeto DMóvel. Focaremos em dois pilares:
1.  **Estado Atual:** Como sumarizamos comentários recebidos (Funcionalidade existente em `summarize_comments_chain.py`).
2.  **Objetivo Final:** Como o LangChain será usado para conectar diretamente ao Banco de Dados, automatizando a busca de informações.

---

## Parte 1: O Que Já Temos (Sumarização de Comentários)

Atualmente, nossa API recebe uma lista de comentários pronta e pede para a IA resumir. A lógica está no arquivo `api/chain/summarize_comments_chain.py`.

### O Conceito: Chains (Correntes)
O LangChain funciona conectando passos lógicos, chamados de "Chains". No nosso código, o fluxo é:
> **Template de Prompt** → **Modelo Gemini** → **Formatador de Saída (Parser)**

#### Como Funciona o Código Atual:
1.  **Schema (Pydantic):** Definimos em `api/models/schemas.py` que queremos receber um objeto com `summary` (texto) e `accessibility_aspects` (lista). Isso "força" a IA a ser organizada.
2.  **Prompt Template:** Em `summarize_comments_chain.py`, criamos uma "persona" (especialista em acessibilidade) e damos instruções claras: "Foque em rampas, piso tátil, atitude da equipe".
3.  **Execução:** O método `summarize_comments` junta tudo e envia para o Google Gemini processar.

---

## Parte 2: O Próximo Passo (Integração com Banco de Dados)

O objetivo final deste projeto não é apenas processar textos soltos, mas permitir que a IA **consulte o banco de dados do DMóvel diretamente**. Para isso, expandiremos o uso do LangChain.

### Por que usar LangChain com Banco de Dados?
Em vez de escrevermos consultas manuais para cada nova pergunta, usamos o LangChain para traduzir perguntas naturais em comandos de banco de dados. Outro caminho é criar um conjunto de consultas e fornecer como tools para a LLM decidir qual(is) vão utilizar.

### Ferramentas Necessárias
Para atingir esse objetivo, estudaremos as seguintes ferramentas do LangChain:

#### 1. SQLDatabase Wrapper
O LangChain possui uma ferramenta que conecta ao seu banco (PostgreSQL, MySQL, etc.) e entende a estrutura das tabelas automaticamente.
* **Onde aprender:** [LangChain SQL Utilities](https://python.langchain.com/docs/integrations/tools/sql_database)

#### 2. Chains SQL (Text-to-SQL)
Podemos criar uma Chain que recebe: *"Como estão os comentários sobre acessibilidade do Parque Ibirapuera?"* e a IA executa:
1.  Gera o SQL: `SELECT comment FROM reviews WHERE place_name = 'Parque Ibirapuera';`
2.  Roda no Banco.
3.  Pega os resultados e passa para a nossa Chain de Sumarização (da Parte 1).

### Fluxo Integrado (A Visão do Futuro)
O "Super Bot" do DMóvel funcionará assim:

1.  **Usuário pergunta:** "O cinema do shopping é acessível?"
2.  **LangChain SQL:** Entende que precisa buscar comentários do "cinema" no banco de dados.
3.  **Recuperação:** A IA executa o SQL e traz 50 comentários recentes.
4.  **LangChain Summarization:** Pega esses 50 comentários e gera o resumo de acessibilidade (usando o código que já temos).
5.  **Resposta:** "Baseado em 50 comentários, o cinema possui rampas, mas o atendimento..."

---

## Roteiro de Estudos para Implementação

Para quem vai implementar essa conexão com o banco, siga esta trilha de aprendizado:

1.  **Entenda o SQLAlchemy:** O LangChain usa essa biblioteca do Python para conectar nos bancos.
    * [Tutorial de SQLAlchemy](https://www.youtube.com/results?search_query=sqlalchemy+python+tutorial)
2.  **LangChain SQL Chains:** Aprenda a criar bots que consultam tabelas.
    * [Tutorial: Chat with your SQL Data](https://python.langchain.com/docs/use_cases/sql/quickstart)
3.  **Output Parsers:** Aprenda como fazer a IA devolver dados limpos (JSON) mesmo quando consulta o banco, para que o frontend do aplicativo não quebre.

## Resumo
A arquitetura do DMóvel está sendo preparada para que o **LangChain** seja o cérebro central: ele não apenas escreve o texto final (resumo), mas também é o "braço" que vai até o banco de dados buscar a matéria-prima (os dados) para trabalhar.
