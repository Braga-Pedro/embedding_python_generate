### **Desafio Técnico – Busca Inteligente de Empresas**

Duração: 7 dias corridos

**Formato de entrega**: repositório Git \+ README \+ script de execução (Docker Compose, Makefile ou [`run.sh`](http://run.sh)) \+ Link de vídeo explicativo da solução no Youtube mostrando ela em ação e também mostrando as partes que julga importante do código.

#### **1\. Objetivo**

Construir um microserviço de **busca conversacional** que interage com o usuário (CLI simples ou endpoint `/chat`) até entender se ele:

1. procura **uma empresa específica**; ou  
2. procura **qualquer empresa que exerça determinada atividade**.

Enquanto faltar informação, o serviço responde:

`{`  
  `"tipo_resposta": "mais_informacoes_necessarias",`  
  `"mensagem": "Texto explicando o que ainda precisa ser especificado"`  
`}`

Quando houver contexto suficiente, responde com **máx. 5 empresas**, dando **prioridade às empresas ativas** e só recorrendo às inativas se não houver ao menos cinco ativas pertinentes:

`{`  
  `"tipo_resposta": "lista_de_empresa",`  
  `"empresas": [`  
    `{`  
      `"nome": "...",`  
      `"telefone": "...",`  
      `"endereco": "...",`  
      `"atividades": ["...", "..."]`  
    `}`  
  `]`  
`}`

Lembre que a cada interação com o chat você precisa saber que se trata do mesmo usuário para poder manter o contexto da conversa.

O diálogo termina após o envio da lista.

#### **2\. Conjunto de dados**

Você receberá **duas planilhas CSV**:

1) **empresas\_ativas.csv** (Empresas em operação)  
2) **empresas\_inativas.csv** (Empresas encerradas/suspensas)

Ambos possuem o mesmo schema (colunas):

| Coluna | Exemplo / descrição |
| ----- | ----- |
| `id` | 197042 (inteiro) |
| `Codigo` | 625 (código interno) |
| `nome_empresa` | “ANA MARIA DE MELO DOS SANTOS.” |
| `Cidade` | “Natal” |
| `Bairro` | “Tirol” |
| `estado` | “RN” |
| `Texto` | Descrição rica em HTML / texto livre |
| `telefones` | “(84)32161980” ou lista separada por vírgulas |
| `atividades` | String com 1 ou mais atividades, separadas por vírgula |

**Importante**

* Pelo menos **3** colunas (`nome_empresa`, `Texto`, `atividades`) devem ser consideradas na vetorização/busca semântica, mas você pode adicionar mais colunas caso ache importante dado os requisitos da aplicação.

* “Ativas” devem sempre rankear primeiro; complete com “inativas” apenas se precisar de \<5 resultados.

Você **não** receberá dump SQL; fique livre para:

* Ler os CSVs direto;

* Importar para SQLite/PostgreSQL ou o que desejar;

* Indexar em um banco vetorial (pgvector, Chroma, Qdrant, etc.).

#### **3\. Requisitos funcionais**

| ID | Descrição |
| ----- | ----- |
| RF-1 | Detectar tipo de busca (empresa específica × atividade). |
| RF-2 | Gerar perguntas adicionais até haver contexto suficiente. |
| RF-3 | Retornar até 5 empresas, **preferindo ativas**. |
| RF-4 | Não enviar o dataset completo para a LLM; usar técnicas como **vetorização, RAG ou function/tool-calling**. |
| RF-5 | Registrar logs de cada sessão (JSON) contendo mensagens, tempo, qual tipo de busca a IA identificou (empresa específica ou busca por atividade). Se a busca identificada foi por “atividade”, então registrar qual foi a atividade identificada. Lembre-se que a atividade que a IA identifica por ser uma atividade não presente da base de dados, mas podemos ter alguma similar (de acordo com o embedding da vetorização). |

#### **4\. Tecnologias e modelos de IA**

Escolha livre – desde que o candidato **não precise gastar dinheiro**. Sugestões:

| Finalidade | Opções gratuitas ou open-source |
| ----- | ----- |
| **Embeddings** | *Google* **Text Embedding 004** por exemplo– veja docs: [https://ai.google.dev/gemini-api/docs/embeddings](https://ai.google.dev/gemini-api/docs/embeddings) |
|  | *Google* pricing & rate limits: [https://ai.google.dev/gemini-api/docs/pricing\#text-embedding-004](https://ai.google.dev/gemini-api/docs/pricing#text-embedding-004) |
| **LLM (razão/diálogo)** | Qualquer modelo/serviço desejado, Google também tem free tier para isso. |
| **Vetor-DB** | pgvector, Qdrant, etc. |

Explique no README:

* Por que escolheu o(s) modelo(s).  
* Como calculou o custo estimado para 1 000 diálogos (ex.: chamadas × preço, se aplicável), considerando o tier pago para produção.  
* Quais limites de taxa ou TOS se aplicam.  
* Mesmo com modelos gratuitos escolhidos para a avaliação, cite que modelos são na sua opinião melhores em um plano pago para um software em produção.

---

#### **5\. Requisitos não-funcionais**

* **Tempo médio de resposta** \< 5 segundos  
* **Custo mínimo** por diálogo (priorize modelos locais ou quotas gratuitas para os testes).  
* **Deploy em 1 comando** (`docker compose up`, `make run`, etc.).

#### **6\. Critérios de avaliação**

| Critério | Peso |
| ----- | ----- |
| Precisão / relevância | 40 % |
| Priorização correta (ativas \> inativas) | 5 % |
| Custo por atendimento (estimado) | 15 % |
| Qualidade de código | 20 % |
| UX do diálogo / clareza das perguntas | 10 % |
| Documentação e arquitetura | 10 % |

#### **7\. Entregáveis**

1. **Repositório Git** com código, testes e Docker/Makefile.  
2. **README.md** com:  
   * setup & running;  
   * explicação dos modelos, embedding, RAG, etc.;  
   * cálculo de custo e trade-offs.  
3. **Relatório curto** (≤ 2 pág.) com métricas coletadas e melhorias futuras.  
4. Scripts de ingestão: leitura dos CSVs, geração de embeddings, criação de índices.

#### **8\. Passos sugeridos para começar**

1. **Ingestão**: carregar ambos CSVs, marcar cada registro com `status = ativo/inativo`.  
2. **Embeddings**:  
   * Gere embedding de `nome_empresa + " " + Texto` **e** embedding separado de cada `atividade`.  
3. **Chat loop**:  
   * Mantenha contexto em memória ou store (Redis, SQLite…).  
   * Use function-calling para:  
     * `classificar_requisicao(pergunta)` → {tipo, possíveis\_atividades, empresa\_alvo?}.  
     * `buscar_empresas(filtros, limite=5)` → lista priorizando ativas.

4. **Fallback**: se \<5 ativas, complemente com inativas mantendo ordenação por relevância.  
5. **Log**: guarde JSON com mensagens, embeddings hits e tempo por etapa.

Boa sorte — qualquer dúvida, registre no README\!

