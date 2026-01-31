# Visão Geral da API de IA do DMóvel (dmovel_ai_api)

Bem-vindo à documentação oficial da API de Inteligência Artificial do DMóvel. Este documento foi criado para desenvolvedores, estudantes e interessados que desejam entender como nossa aplicação funciona, quais tecnologias utilizamos e como você pode aprender a trabalhar com elas, mesmo sem experiência prévia.

## O que é este projeto?

O **dmovel_ai_api** é um serviço "backend" (a parte do sistema que roda no servidor) focado em fornecer funcionalidades de Inteligência Artificial para o aplicativo DMóvel. O objetivo principal é melhorar a acessibilidade, oferecendo recursos como resumos automáticos de comentários sobre locais e, futuramente, um assistente virtual para ajudar no uso do aplicativo.

## Tecnologias Utilizadas (O "Stack")

Abaixo explicamos cada peça do nosso quebra-cabeça e indicamos onde você pode aprender sobre elas.

### 1. Python (A Linguagem de Programação)
Toda a lógica da nossa API é escrita em Python. Escolhemos essa linguagem por ser a líder mundial em desenvolvimento de IA e por sua facilidade de leitura.
* **Para que serve:** Escrever as regras de negócio e conectar os serviços.
* **Onde aprender:**
    * [Curso de Python para Iniciantes (Curso em Vídeo - Gustavo Guanabara)](https://www.youtube.com/playlist?list=PLHz_AreHm4dlKP6QQCekuIPky1CiwmdI6)
    * [Documentação Oficial (Português)](https://docs.python.org/pt-br/3/tutorial/)

### 2. FastAPI (O Framework Web)
O FastAPI é a ferramenta que nos permite transformar nosso código Python em uma "API Web", ou seja, um endereço na internet que o aplicativo DMóvel pode chamar para pedir informações.
* **Para que serve:** Receber pedidos (Requests), validar dados e enviar respostas (Responses).
* **Onde aprender:**
    * [Site Oficial do FastAPI (Excelente e didático)](https://fastapi.tiangolo.com/)
    * [Tutorial de FastAPI em Português (YouTube)](https://www.youtube.com/results?search_query=fastapi+tutorial+portugues)

### 3. Docker (A Infraestrutura)
Para garantir que o código rode igual no seu computador e no servidor da nuvem, usamos "containers". Imagine o Docker como uma caixa que guarda o Python, as bibliotecas e o código, garantindo que nada quebre por diferenças de sistema operacional.
* **Para que serve:** Empacotar a aplicação para distribuição.
* **Onde aprender:**
    * [Descomplicando o Docker (LinuxTips)](https://www.youtube.com/watch?v=Kadwg15SSos)
    * [Docker para Iniciantes (Documentação)](https://docs.docker.com/get-started/)

### 4. Google Gemini & LangChain (A Inteligência Artificial)
Aqui está o cérebro do projeto. Usamos o modelo **Gemini** (do Google) para "pensar" e o **LangChain** para organizar esses pensamentos.
* **Google Gemini:** O modelo de linguagem que gera textos e entende contextos.
* **LangChain:** Uma biblioteca que nos ajuda a criar "cadeias" de raciocínio, ligando o modelo de IA a dados específicos (como nossos comentários).
* **Onde aprender:**
    * [Introdução ao LangChain (Documentação)](https://python.langchain.com/docs/get_started/introduction)
    * [Google AI Studio (Para testar o Gemini)](https://aistudio.google.com/)

## Como a API Funciona?

A arquitetura segue um fluxo simples:
1.  **Entrada:** O aplicativo envia dados (ex: uma lista de comentários) para uma rota (endpoint) do FastAPI.
2.  **Processamento:** O FastAPI valida se os dados estão corretos usando o Pydantic (validador).
3.  **Inteligência:** O sistema chama o `GeminiService` e executa uma "Chain" (corrente) do LangChain.
4.  **Saída:** A IA processa a informação e devolve uma resposta estruturada (ex: um resumo em texto).

## Próximos Passos e Guias Específicos

Para aprofundar seu conhecimento em áreas específicas deste projeto, acesse os guias abaixo:

* 📄 **[Guia de Resumos com LangChain](./GUIA_RESUMOS_LANGCHAIN.md):** Entenda como criamos a funcionalidade que lê comentários e gera resumos de acessibilidade.
* 🤖 **[Tutorial do Chatbot de Pesquisa](./TUTORIAL_CHATBOT_RAG.md):** Aprenda como planejar e implementar um assistente que tira dúvidas sobre o DMóvel lendo a documentação (Conceito de RAG).
