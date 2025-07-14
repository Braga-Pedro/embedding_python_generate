# Gerador de Embeddings para Dados Empresariais

Este projeto tem como objetivo gerar embeddings dos dados de empresas, permitindo que modelos de linguagem (LLMs) possam realizar buscas inteligentes e análises contextuais baseadas nos dados internos da própria empresa.

## Por que gerar embeddings dos dados empresariais?

Embeddings são representações vetoriais dos dados que capturam o significado semântico e relacional das informações. Ao mapear e transformar dados empresariais em embeddings, é possível:

- **Facilitar buscas inteligentes:** Consultas por similaridade e contexto, indo além de simples buscas por palavras-chave.
- **Personalizar LLMs:** Permitir que modelos de linguagem entendam e respondam com base no conhecimento específico da empresa.
- **Aumentar a eficiência analítica:** Embeddings tornam análises, recomendações e automações mais precisas e relevantes.

## Estrutura de Diretórios

```
embedding_python_generate/
│
├── docker/
│   └── python/
│       └── Dockerfile           # Dockerfile para o serviço de setup
│
├── src/
│   ├── main.py                  # Script principal de geração de embeddings
│   ├── config.py                # Configurações e variáveis de ambiente
│   ├── database/
│   │   ├── migrations/          # Scripts de criação de tabelas
│   │   ├── utils/               # Utilitários de conexão e validação
│   │   ├── factories/           # Inserção de dados
│   │   └── embeddings/          # Geração dos embeddings
│   ├── formatters/              # Carregamento e formatação dos dados CSV
│   ├── data/                    # Arquivos CSV de empresas ativas/inativas
│   └── .env                     # Variáveis de ambiente do projeto
│
├── docker-compose.yml           # Orquestração dos containers
└── README.md                    # Documentação do projeto
```

## Lógica de Containização

O projeto utiliza Docker para garantir um ambiente isolado e replicável, com três containers principais:

- **pgsql_smart_search:** Banco de dados PostgreSQL com extensão pgvector para armazenar embeddings.
- **ollama_smart_search:** Serviço de LLM (Ollama) para geração dos embeddings via API.
- **setup_smart_search:** Serviço responsável por executar o pipeline de ingestão, mapeamento e geração dos embeddings dos dados empresariais.

O fluxo de execução é:

1. **Banco de dados e LLM sobem primeiro.**
2. **O container de setup aguarda ambos estarem prontos.**
3. **O script principal (main.py) conecta ao banco, verifica/cria tabelas, carrega dados CSV e gera embeddings usando o endpoint do Ollama.**
4. **Os embeddings são armazenados no banco, prontos para uso em buscas inteligentes e aplicações LLM.**

## Como executar

1. Configure os arquivos `.env` conforme necessário.
2. Execute os containers com:

   ```sh
   docker-compose up -d --build
   ```

3. O pipeline será executado automaticamente, gerando e armazenando os embeddings dos dados empresariais.

---