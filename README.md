# 👤 Microsserviço Accounts - Ateliê Digital

## 📖 Sobre o Projeto
O **Ateliê Digital** é um sistema web que funciona como um marketplace exclusivo para produtos artesanais. O objetivo da plataforma é conectar diretamente os artesãos independentes aos consumidores, oferecendo ferramentas para que os vendedores gerenciem seus negócios e os clientes encontrem produtos com facilidade e segurança.

Neste repositório encontra-se o microsserviço de **Accounts (Contas e Identidade)**. Dentro da arquitetura do sistema, ele é a API responsável pela gestão de usuários, cadastros, autenticação tradicional e social (login via Google), verificação de e-mails, recuperação de senhas e gerenciamento completo de perfis. Além disso, o serviço administra as **carteiras financeiras (Wallets)** e o histórico de transações dos artesãos vendedores na plataforma.

Apesar de rodar de forma independente, este microsserviço se comunica ativamente com os demais serviços da arquitetura — consumindo e processando dados provenientes de *Catalog* e *Orders* via mensageria assíncrona com FastStream e RabbitMQ, além de publicar eventos e registros detalhados de todas as transações e alterações críticas de contas para o microsserviço de *Auditoria de Logs*.

## 🚀 Tecnologias e Recursos
Este microsserviço foi construído utilizando as seguintes tecnologias e bibliotecas:

* **Django & Django Rest Framework (DRF):** Framework web principal e toolkit poderoso para a construção da API RESTful robusta e segura.
* **Autenticação e Social Login:** Autenticação via tokens JWT com `djangorestframework-simplejwt`, gerenciamento de fluxo de autenticação com `dj-rest-auth` e suporte nativo a login social via Google através do `django-allauth`.
* **FastStream com RabbitMQ:** Framework moderno e ultrarrápido para mensageria assíncrona, responsável pelo consumo de dados dos serviços Catalog e Orders e pela publicação de dados de auditoria nas filas do RabbitMQ sem bloquear as requisições HTTP.
* **PostgreSQL:** Banco de dados relacional oficial do ecossistema, utilizando o driver moderno e de altíssimo desempenho `psycopg[binary]>=3.3.4`.
* **Documentação de API:** Geração automática de schemas OpenAPI e interfaces interativas Swagger UI utilizando `drf-spectacular` e `drf-yasg`.
* **Validação e Processamento de Mídia:**
    * **validate-docbr:** Validação rigorosa de documentos de identidade brasileiros (CPF e CNPJ para o cadastro e verificação de artesãos).
    * **Pillow:** Processamento e manipulação de imagens para fotos de perfil dos usuários.
* **Integrações HTTP & Assincronismo:** Uso do `httpx` para requisições externas assíncronas e `asgiref` para interoperabilidade assíncrona no ecossistema Django.
* **Segurança e Ambiente:** Gestão de configurações e variáveis de ambiente isoladas e seguras através do `django-environ`.
* **Ferramentas de Suporte:**
    * **uv:** Gerenciador de pacotes e ambientes virtuais ultrarrápido.

---

## ⚙️ Configuração do Ambiente

Para rodar este projeto, utilizaremos o **uv** para gerenciar o ambiente e as bibliotecas.

### 1. Instalação do uv
Se você ainda não tem o `uv` instalado, abra o seu terminal e execute o comando correspondente ao seu sistema operacional:

**No Linux (ou macOS):**
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```
**No Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Criando o Ambiente Virtual
Na pasta raiz do projeto, crie um ambiente virtual limpo executando:
```bash
uv venv
```

Após a criação, **ative o ambiente virtual**:
* **Linux / macOS:**
    ```bash
    source .venv/bin/activate
    ```
* **Windows:**
    ```cmd
    .venv\Scripts\activate
    ```
### 3. Instalando as Bibliotecas
Com o ambiente ativado, instale as dependências listadas nas tecnologias utilizando o `uv`. Você pode instalar todas de uma vez através do seu arquivo de dependências (como o `pyproject.toml` ou `requirements.txt`):

```bash
uv pip install -r requirements.txt
```

*Caso precise instalar as bibliotecas manualmente para testar o ambiente, o comando base seria:*
```bash
uv pip install "django>=6.0.2" "djangorestframework>=3.17.1" "djangorestframework-simplejwt>=5.5.1" "dj-rest-auth[with-social]>=7.2.0" "django-allauth[socialaccount]>=65.15.1" "faststream[cli,rabbit]>=0.7.1" "psycopg[binary]>=3.3.4" "validate-docbr>=2.0.0" "pillow>=12.1.0" "django-environ>=0.13.0" "drf-spectacular>=0.29.0" "drf-yasg>=1.21.15" "httpx>=0.28.1" pytest ruff taskipy
```
---

## ▶️ Como Executar a API

Você pode rodar o serviço em modo local de desenvolvimento diretamente via terminal ou de forma conteinerizada utilizando o Docker Compose para emular o ecossistema completo do Ateliê Digital.

### Opção 1: Execução Local 

Para iniciar o servidor local de desenvolvimento, basta rodar:

```bash
uv run manage.py migrate

uv run manage.py runserver

```

### Opção 2: Execução via Docker Compose (Recomendado)
Para integrar o serviço de orders aos demais microsserviços do **Ateliê Digital** (como o RabbitMQ e o banco de dados PostgreSQL), a execução via Docker Compose garante que todos os containers compartilhem a mesma rede de comunicação interna.

1. **Crie a rede de comunicação global do projeto** (caso ainda não tenha sido criada no seu ambiente docker):
   ```bash
   docker network create atelie-network
   ```

2. **Inicie o serviço construindo a imagem do container**:
   Na raiz do repositório, execute o comando abaixo para realizar o build da imagem Docker e subir o serviço em background ou anexado ao terminal:
   ```bash
   docker compose up --build
   ```

Com o container em execução, o serviço começará automaticamente a escutar os eventos do RabbitMQ na rede `atelie-network` e o painel administrativo estará acessível no navegador através de `http://localhost:8000/` (ou na porta configurada em seu `docker-compose.yml`).
