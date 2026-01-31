# Tutorial de Implementação: Chatbot de Pesquisa para o DMóvel (RAG)

Este documento é um guia de planejamento e aprendizado para implementar um **Chatbot de Suporte** na nossa API. O objetivo desse bot é responder perguntas dos usuários sobre como usar o aplicativo DMóvel, baseando-se exclusivamente na nossa documentação oficial.

Para isso, utilizaremos uma técnica chamada **RAG (Retrieval-Augmented Generation)** ou Geração Aumentada por Recuperação.

## O Que é RAG?

Imagine que o Google Gemini é um estudante muito inteligente, mas que não leu o manual do DMóvel. O RAG é o processo de permitir que esse estudante consulte o manual (nossos documentos) antes de responder a uma pergunta.

**Vídeo Recomendado:** [O que é RAG? (Explicação em 5 minutos)](https://www.youtube.com/results?search_query=what+is+rag+langchain)

## Roteiro de Implementação

Como construiríamos isso usando LangChain e Gemini? Aqui está o fluxo lógico que você deve seguir:

### 1. Preparação dos Dados (Ingestão)
Primeiro, precisamos ensinar o conteúdo ao robô.
* **O que fazer:** Pegar os PDFs ou arquivos Markdown de ajuda do DMóvel.
* **Técnica:** Usar "Document Loaders" do LangChain para ler os arquivos.
* **Recurso:** [LangChain Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/)

### 2. Quebra de Texto (Chunking)
Não podemos enviar um livro inteiro para a IA de uma vez (é caro e lento).
* **O que fazer:** Dividir o texto em pedaços menores (chunks) de, por exemplo, 1000 caracteres.
* **Técnica:** Usar "Text Splitters".
* **Recurso:** [Como dividir textos para IA](https://python.langchain.com/docs/modules/data_connection/document_transformers/)

### 3. Vetorização (Embeddings)
Computadores não entendem texto, entendem números. Precisamos converter os pedaços de texto em listas de números (vetores) que representam o **significado** da frase.
* **O que fazer:** Usar um modelo de Embeddings (o Google tem o `GoogleGenerativeAIEmbeddings`).
* **Conceito:** Frases com significados parecidos terão números parecidos.

### 4. O Banco de Dados Vetorial (Vector Store)
Precisamos guardar esses números em um lugar onde seja rápido pesquisar.
* **O que fazer:** Usar um banco vetorial como FAISS ou ChromaDB (que funcionam localmente) ou Pinecone (na nuvem).
* **Ação:** Salvar os "chunks" convertidos em vetores neste banco.

### 5. A Recuperação (Retrieval) - A Mágica Acontece Aqui
Quando o usuário pergunta: *"Como mudo minha senha?"*:
1.  Convertemos a pergunta do usuário em números (vetor).
2.  O banco de dados procura os pedaços de texto (chunks) que matematicamente são mais "próximos" da pergunta.
3.  O sistema recupera os 3 ou 4 trechos mais relevantes do manual.

### 6. A Geração da Resposta
Finalmente, montamos o prompt para o Gemini:
> "Use as informações abaixo (os trechos recuperados) para responder à pergunta do usuário: 'Como mudo minha senha?'. Se a resposta não estiver no texto, diga que não sabe."

## Como Integrar na Nossa API (FastAPI)

Para trazer isso para o `dmovel_ai_api`, você precisará:
1.  Criar uma nova rota, ex: `/chat/support`.
2.  No início da aplicação, carregar o banco vetorial (passos 1 a 4 rodam apenas uma vez ou quando a doc muda).
3.  Na rota, executar os passos 5 e 6 a cada pergunta.

## Materiais de Estudo para este Projeto

* **Tutorial Completo de RAG com LangChain:** [Chat with your Data](https://python.langchain.com/docs/use_cases/question_answering/)
* **Embeddings do Google:** [Documentação Google GenAI](https://ai.google.dev/docs/embeddings_guide)
* **Vector Stores para Iniciantes:** [Entendendo Bancos Vetoriais](https://www.youtube.com/results?search_query=vector+databases+explained)
