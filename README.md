# desafio_inoa
Desafio da INOA em Python com Django

## Guia para uso

# Monitoramento de Ativos

Este é um projeto de aplicação web desenvolvido com Django para monitorar os preços de ativos da bolsa de valores (B3). A aplicação permite que os usuários cadastrem ativos, definam um "túnel de preço" (mínimo e máximo) e um intervalo de checagem. Se o preço do ativo sair desse túnel, o usuário é notificado por e-mail.

## Funcionalidades

-   **Autenticação de Usuário**: Cadastro, Login e Logout.
-   **Dashboard Personalizado**: Cada usuário visualiza e gerencia apenas os seus próprios ativos.
-   **Gerenciamento de Ativos**: Adicionar, editar e remover ativos para monitoramento.
-   **Túnel de Preço**: Definir um preço mínimo e máximo para cada ativo.
-   **Intervalo de Checagem**: Configurar a frequência com que o preço de cada ativo é verificado.
-   **Monitoramento em Background**: Utiliza `django-q` para executar as checagens de preço de forma assíncrona, sem travar a aplicação.
-   **Notificações por E-mail**: Envio de alertas quando o preço de um ativo ultrapassa os limites definidos.
-   **Histórico de Preços**: Página de detalhes para cada ativo, exibindo a cotação atual e o histórico de preços verificados.

## Tecnologias Utilizadas

-   **Backend**: Python, Django
-   **Busca de Cotações**: `yfinance`
-   **Tarefas em Background**: `django-q`
-   **Banco de Dados**: SQLite (padrão do Django)
-   **Frontend**: HTML, CSS

---

## Guia de Instalação e Uso

### Pré-requisitos

-   Python 3.8 ou superior
-   Git

### 1. Clonar o Repositório

```bash
git clone https://github.com/thiagomout/desafio_inoa.git
cd desafio_inoa
```

### 2. Configurar o Ambiente Virtual

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente (Linux/macOS)
source venv/bin/activate
```

### 3. Instalar as Dependências

Com o ambiente ativado, instale todas as bibliotecas necessárias a partir do arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

As credenciais e chaves secretas são gerenciadas através de um arquivo `.env`.

-   Crie um arquivo chamado `.env` na raiz do projeto.
-   Adicione as seguintes variáveis, substituindo pelos seus valores:

```env
# Use uma chave forte e única para produção. Pode gerar uma nova.
SECRET_KEY='django-insecure-!%$apgvd5vuk0p101t!75e-epvyh%1j6&!bcwziufe2-%wp1_3'

# Configurações de E-mail (usando as credenciais do Desafio Alerta como exemplo.)
EMAIL_HOST_USER='desafioalerta@gmail.com'
EMAIL_HOST_PASSWORD='yhqe lxly gesq xfsh'
```

### 5. Aplicar as Migrações do Banco de Dados

Este comando cria as tabelas necessárias no banco de dados.

```bash
python manage.py migrate
```

### 6. Criar um Superusuário (Opcional)

Para acessar a área administrativa do Django (`/admin`).

```bash
python manage.py createsuperuser
```

---

## Rodando a Aplicação

Para que o sistema funcione completamente (servidor web e monitoramento em background), você precisará rodar **dois comandos em dois terminais separados**.

### Terminal 1: Iniciar o Servidor Django

Este comando inicia o servidor de desenvolvimento web.

```bash
python manage.py runserver
```

Acesse a aplicação no seu navegador em: `http://127.0.0.1:8000/`

### Terminal 2: Iniciar o Cluster do Django-Q

Este comando inicia o processo que executa as tarefas em background, como a checagem de preços. **Este processo deve permanecer rodando**.

```bash
python manage.py qcluster
```

Com os dois processos rodando, a aplicação está totalmente funcional. Você pode se cadastrar, adicionar ativos e o sistema de monitoramento irá funcionar conforme o intervalo


