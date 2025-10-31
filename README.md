# Automação Serverless na AWS: Processamento Orientado a Eventos (Lambda e S3)

Este repositório documenta o desafio prático de laboratório focado na **automação de tarefas** na nuvem AWS, consolidando o conhecimento em tarefas automatizadas com Lambda Function e S3. O objetivo principal é documentar a implementação de uma arquitetura *serverless* na qual um evento de armazenamento no Amazon S3 serve como gatilho para a execução de uma função AWS Lambda.

A documentação visa demonstrar o processo técnico de forma clara e estruturada, servindo como material de apoio para futuras implementações.

---

## Objetivos do Projeto e Serverless

O projeto foi construído sobre o pilar da **Arquitetura Orientada a Eventos (Event-Driven Architecture - EDA)**.

* **Problema Resolvido:** Automatizar o processamento de novos arquivos (Objetos) logo após serem carregados em um ambiente de armazenamento.
* **Solução:** Utilizar um evento de criação de objeto no **Amazon S3** para invocar uma função **AWS Lambda** de forma totalmente *serverless*.
* **Conceito Base:** A automação na AWS permite executar ações baseadas em eventos, como um arquivo no S3 iniciar um processo no Lambda.

---

## Diagrama de Arquitetura Conceitual

O fluxo de trabalho completo da automação está visualmente representado no diagrama a seguir, que detalha a relação e a comunicação assíncrona entre os serviços.

**Link Direto para o Diagrama:** [Visualizar Arquitetura Detalhada](./images/arquitetura.png)


---

## Passo a Passo da Configuração do Pipeline (Serverless)

Abaixo está o passo a passo lógico para a implementação da automação S3 $\rightarrow$ Lambda.

### 1. Provisionamento do Bucket S3 (O Produtor)

1.  **Criação:** Cria-se um Bucket S3 na região AWS desejada, configurado para uso geral.
2.  **Configuração de Notificação:** O Bucket S3 é configurado para emitir eventos. É crucial definir o tipo de evento que servirá como gatilho:
    * **Tipo de Evento Selecionado:** `s3:ObjectCreated:Put` (para novos uploads).
    * **Filtros (Opcional):** É possível adicionar prefixos (ex: `uploads/`) ou sufixos (ex: `.csv`) para restringir a execução da Lambda apenas a arquivos específicos.

### 2. Implementação da Função AWS Lambda (O Consumidor)

1.  **Criação da Função:** Cria-se uma função Lambda, escolhendo um *runtime* (ex: Python ou Node.js).
2.  **Definição da IAM Role:** Uma Role de Execução (Role IAM) é criada. Essa Role é vital para segurança:
    * **Permissões Essenciais:** `AWSLambdaBasicExecutionRole` (para escrever logs no CloudWatch).
    * **Permissão S3:** A Role deve receber permissão explícita para ler o Bucket S3 (`s3:GetObject`) se a função precisar processar o arquivo.
3.  **Código da Função:** O código, cujo rascunho está em `src/lambda_function.py`, é implementado para:
    * Receber e **desempacotar (parsear)** o *payload* JSON enviado pelo S3.
    * Extrair o nome do Bucket e a chave do Objeto (`objectKey`) para saber qual arquivo processar.
    * Executar a lógica de negócio (ex: processamento de dados, redimensionamento de imagens, etc.).

### 3. Conexão do Gatilho e Teste

1.  **Adição do Trigger:** O Bucket S3 é configurado como o *Trigger* na seção de configuração da função Lambda. Essa ação estabelece a permissão para que o S3 invoque a Lambda.
2.  **Teste Final:** Um arquivo de teste é carregado no Bucket S3. A verificação do sucesso da automação é feita no **Amazon CloudWatch Logs**, onde a função Lambda registra a mensagem de que o evento foi recebido e processado.

---

## Insights Adquiridos e O que Eu Aprendi

O desafio consolidou o entendimento sobre os aspectos conceituais e operacionais de arquiteturas *serverless* e *event-driven*:

| Conceito-Chave | Aprendizado e Insight |
| :--- | :--- |
| **Invocação Assíncrona** | Entendi que o S3 invoca o Lambda de forma **assíncrona**. Isso significa que o S3 apenas envia a notificação (*push*) e não espera pela resposta. Esse modelo é fundamental para garantir a **escalabilidade** e o **desacoplamento**, permitindo que o sistema absorva picos de upload sem falhar. |
| **Parsing do Payload** | A lógica da função Lambda depende integralmente de saber **extrair a informação correta** do objeto `event['Records'][0]['s3']`. Isso confirmou que o código deve ser adaptado à estrutura de dados do serviço que o invoca. |
| **Serverless e Eficiência** | O modelo **AWS Lambda** reforça o princípio *serverless*: não há custo quando a função está ociosa, e a capacidade de processamento escala automaticamente (até 1000 invocações por segundo por padrão), tornando a solução **altamente custo-eficiente** para cargas de trabalho variáveis. |
| **Segurança por Padrão (IAM)** | A Role IAM deve seguir o **Princípio do Privilégio Mínimo**. Aprendi que, além das permissões de log, a função Lambda precisa da permissão explícita de `s3:GetObject` no *bucket* específico para **ler** o arquivo, garantindo que ela não tenha acesso a recursos desnecessários. |

---

## Código de Referência

O rascunho da lógica que seria implementada na Função AWS Lambda, com foco na extração dos metadados do evento S3, pode ser encontrado no arquivo:

[src/lambda_function.py](src/lambda_function.py)
