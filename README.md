# 🚀 Finance-IA Revisor de Tom & LGPD

[![CI/CD Pipeline](https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd/actions/workflows/ci-cd.yml)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd/pkgs/container/finance-ia-revisor-tom-lgpd)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Sistema HTTP automatizado para revisão inteligente de ideias de conteúdo** com integração OpenAI, garantindo conformidade com tom de voz, consistência de canais/formatos e compliance LGPD.

## ✨ Características Principais

- 🤖 **Integração OpenAI**: Revisões inteligentes com ChatGPT
- 🔒 **Segurança Avançada**: Gerenciamento seguro de chaves API
- 🌐 **API HTTP**: Endpoints RESTful para integração
- 📊 **Múltiplos Revisores**: Local, OpenAI Client, OpenAI Agent, Híbrido
- 🐳 **Docker Ready**: Containerização completa
- 🔄 **CI/CD**: Pipeline automático com GitHub Actions
- 📈 **Monitoramento**: Logs estruturados e healthcheck
- 🛡️ **LGPD Compliance**: Validação automática de conformidade

## 📋 Funcionalidades

### 🔍 Revisores Disponíveis

| Revisor | Descrição | Uso Recomendado |
|---------|-----------|----------------|
| **Local** | Regras pré-definidas | Validação rápida básica |
| **OpenAI Client** | API direta OpenAI | Revisões simples |
| **OpenAI Agent** | Sistema de agentes | Análises complexas |
| **Híbrido** | Local + IA | Melhor custo-benefício |

### 📊 Tipos de Revisão

- 🎯 **Tom de Voz**: Consistência com identidade Finance-IA
- 📱 **Canal/Formato**: Adequação ao meio de distribuição
- 🛡️ **LGPD**: Conformidade com proteção de dados
- 🔄 **Comparação**: Análise entre diferentes abordagens

## 🚀 Instalação e Configuração

### Método 1: Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd.git
cd finance-ia-revisor-tom-lgpd

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Execute com Docker Compose
docker-compose up -d

# Verifique se está funcionando
curl http://localhost:5000/healthz
```

### Método 2: Instalação Local

```bash
# Clone o repositório
git clone https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd.git
cd finance-ia-revisor-tom-lgpd

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
export OPENAI_API_KEY="sua-chave-openai"
export AUTH_TOKEN="seu-token-de-autenticacao"

# Execute a aplicação
python app.py
```

### Método 3: Produção com Gunicorn

```bash
# Instale o Gunicorn
pip install gunicorn

# Execute em produção
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
```

## 🔧 Configuração de Variáveis de Ambiente

### Variáveis Obrigatórias

```bash
# Chave da API OpenAI (obrigatória)
OPENAI_API_KEY=sk-proj-...

# Token de autenticação para a API (obrigatório)
AUTH_TOKEN=seu-token-seguro-aqui
```

### Variáveis Opcionais

```bash
# Configurações da aplicação
FLASK_ENV=production
PORT=5000
DEBUG=false
LOG_LEVEL=INFO

# Configurações do Gunicorn (produção)
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
GUNICORN_BIND=0.0.0.0:5000
```

## 🌐 API HTTP - Endpoints

### 🔐 Autenticação

Todos os endpoints (exceto `/healthz`) requerem autenticação via Bearer Token:

```bash
Authorization: Bearer seu-token-aqui
```

### 📍 Endpoints Disponíveis

#### 1. Health Check
```bash
GET /healthz
# Resposta: {"status": "healthy", "timestamp": "..."}
```

#### 2. Revisar Ideia
```bash
POST /revisar
Content-Type: application/json
Authorization: Bearer seu-token
OpenAI-API-Key: sk-proj-...  # Opcional, pode usar variável de ambiente

{
  "ideia": "Criar post sobre investimentos em renda fixa",
  "tipo_revisor": "openai_agent",
  "incluir_comparacao": true
}
```

#### 3. Testar Todos os Revisores
```bash
POST /testar
Content-Type: application/json
Authorization: Bearer seu-token
OpenAI-API-Key: sk-proj-...

{
  "ideia": "Vamos falar sobre criptomoedas para iniciantes"
}
```

#### 4. Obter Estatísticas
```bash
GET /estatisticas
Authorization: Bearer seu-token
OpenAI-API-Key: sk-proj-...

# Resposta: estatísticas de uso dos revisores
```

#### 5. Gerar Template
```bash
GET /template
Authorization: Bearer seu-token

# Resposta: template de ideia para preenchimento
```

#### 6. Obter Listas Válidas
```bash
GET /listas
Authorization: Bearer seu-token

# Resposta: listas de canais, formatos, KPIs, etc.
```

## 💡 Exemplos Práticos

### Exemplo 1: Revisão Simples via cURL

```bash
curl -X POST http://localhost:5000/revisar \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer seu-token" \
  -H "OpenAI-API-Key: sk-proj-..." \
  -d '{
    "ideia": "Post sobre como investir na bolsa de valores",
    "tipo_revisor": "local",
    "incluir_comparacao": false
  }'
```

### Exemplo 2: Teste Completo via Python

```python
import requests

url = "http://localhost:5000/testar"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer seu-token",
    "OpenAI-API-Key": "sk-proj-..."
}
data = {
    "ideia": "Vamos criar um webinar sobre planejamento financeiro"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### Exemplo 3: Uso Programático

```python
from interface_revisor import InterfaceRevisor

# Inicialize o revisor
revisor = InterfaceRevisor(openai_api_key="sua-chave")

# Revise uma ideia
ideia = "Criar série de posts sobre criptomoedas"
resultado = revisor.revisar(
    ideia=ideia,
    tipo_revisor="hibrido",
    incluir_comparacao=True
)

print(f"Resultado: {resultado}")
```

## 🔗 Integração com n8n

### Configuração do Webhook

1. **Crie um nó HTTP Request** no n8n
2. **Configure os parâmetros**:
   ```json
   {
     "method": "POST",
     "url": "http://seu-servidor:5000/revisar",
     "headers": {
       "Content-Type": "application/json",
       "Authorization": "Bearer {{ $env.AUTH_TOKEN }}",
       "OpenAI-API-Key": "{{ $env.OPENAI_API_KEY }}"
     },
     "body": {
       "ideia": "{{ $json.ideia }}",
       "tipo_revisor": "openai_agent",
       "incluir_comparacao": true
     }
   }
   ```

### Exemplo de Workflow n8n

```json
{
  "name": "Finance-IA Content Review",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "finance-ia-review"
      }
    },
    {
      "name": "Review Content",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://finance-ia-reviewer:5000/revisar",
        "method": "POST",
        "headers": {
          "Authorization": "Bearer {{ $env.AUTH_TOKEN }}"
        }
      }
    }
  ]
}
```

## 🚀 Deploy em Produção

### Deploy com Docker Compose

```bash
# 1. Clone e configure
git clone https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd.git
cd finance-ia-revisor-tom-lgpd
cp .env.example .env

# 2. Configure as variáveis no .env
OPENAI_API_KEY=sk-proj-sua-chave-real
AUTH_TOKEN=token-super-seguro-producao
FLASK_ENV=production

# 3. Execute em produção
docker-compose up -d

# 4. Verifique os logs
docker-compose logs -f finance-ia-reviewer
```

### Deploy com Kubernetes

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: finance-ia-reviewer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: finance-ia-reviewer
  template:
    metadata:
      labels:
        app: finance-ia-reviewer
    spec:
      containers:
      - name: finance-ia-reviewer
        image: ghcr.io/marvin-ds/finance-ia-revisor-tom-lgpd:latest
        ports:
        - containerPort: 5000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: finance-ia-secrets
              key: openai-api-key
        - name: AUTH_TOKEN
          valueFrom:
            secretKeyRef:
              name: finance-ia-secrets
              key: auth-token
```

### Deploy em Cloud Providers

#### AWS ECS
```bash
# 1. Build e push da imagem
docker build -t finance-ia-reviewer .
docker tag finance-ia-reviewer:latest your-account.dkr.ecr.region.amazonaws.com/finance-ia-reviewer:latest
docker push your-account.dkr.ecr.region.amazonaws.com/finance-ia-reviewer:latest

# 2. Crie o serviço ECS usando a imagem
```

#### Google Cloud Run
```bash
# Deploy direto do repositório
gcloud run deploy finance-ia-reviewer \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📊 Monitoramento e Logs

### Estrutura de Logs

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "message": "Request processed successfully",
  "trace_id": "abc123",
  "endpoint": "/revisar",
  "method": "POST",
  "status_code": 200,
  "response_time_ms": 1250,
  "openai_key_source": "header",
  "revisor_type": "openai_agent"
}
```

### Métricas Importantes

- **Taxa de Sucesso**: Porcentagem de requests bem-sucedidos
- **Tempo de Resposta**: Latência média por endpoint
- **Uso de API OpenAI**: Tokens consumidos e custos
- **Erros por Tipo**: Distribuição de códigos de erro
- **Throughput**: Requests por segundo

### Health Checks

```bash
# Verificação básica
curl http://localhost:5000/healthz

# Verificação com autenticação
curl -H "Authorization: Bearer seu-token" http://localhost:5000/estatisticas
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Erro 401 - Unauthorized
```bash
# Verifique se o token está correto
echo $AUTH_TOKEN

# Teste com curl
curl -H "Authorization: Bearer $AUTH_TOKEN" http://localhost:5000/healthz
```

#### 2. Erro 400 - OpenAI API Key
```bash
# Verifique se a chave está configurada
echo $OPENAI_API_KEY

# Teste a chave diretamente
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

#### 3. Timeout nos Requests
```bash
# Aumente o timeout do Gunicorn
export GUNICORN_TIMEOUT=300

# Ou configure no docker-compose.yml
GUNICORN_TIMEOUT: 300
```

#### 4. Alto Uso de Memória
```bash
# Reduza o número de workers
export GUNICORN_WORKERS=2

# Monitore o uso
docker stats finance-ia-reviewer
```

### Logs de Debug

```bash
# Ative logs detalhados
export LOG_LEVEL=DEBUG
export DEBUG=true

# Visualize logs em tempo real
docker-compose logs -f finance-ia-reviewer
```

## 🚀 Como Usar

### Uso Básico (Interface Simplificada)

```python
from interface_revisor import InterfaceRevisor

# Criar instância do revisor local
interface = InterfaceRevisor()

# Revisar uma ideia (dicionário)
ideia = {
    "data_da_semana": "2024-01-15",
    "tema": "Como fazer alocação de ativos",
    "persona": "Pessoa física iniciante",
    # ... outros campos
}

resultado = interface.revisar_ideia_dict(ideia)
print(resultado)
```

### Interface com IA 🤖

```python
from interface_revisor import InterfaceRevisor

# Inicializar com IA
revisor = InterfaceRevisor(
    usar_ia=True, 
    api_key="sua-chave-openai"
)

# Revisar com diferentes métodos
resultado_local = revisor.revisar_ideia_dict(ideia, "local")
resultado_ia = revisor.revisar_ideia_dict(ideia, "openai_client")
resultado_hibrido = revisor.revisar_ideia_dict(ideia, "hibrido")

# Comparar métodos
resultado_comparacao = revisor.revisar_ideia_dict(
    ideia, 
    "auto", 
    incluir_comparacao=True
)
```

### Uso via JSON String

```python
# Revisar uma ideia (JSON string)
json_ideia = '{"data_da_semana": "2024-01-15", "tema": "...", ...}'
resultado = interface.revisar_ideia_json(json_ideia)
```

### Linha de Comando

```bash
# Revisar com método local
python interface_revisor.py revisar exemplo.json local

# Revisar com IA
python interface_revisor.py revisar exemplo.json openai_client --ia

# Revisar com método híbrido
python interface_revisor.py revisar exemplo.json hibrido --ia

# Revisar com comparação
python interface_revisor.py revisar exemplo.json auto --ia --comparacao

# Testar todos os revisores
python interface_revisor.py testar exemplo.json --ia

# Ver estatísticas de uso
python interface_revisor.py stats --ia

# Gerar template de ideia
python interface_revisor.py template

# Ver listas válidas
python interface_revisor.py listas
```

## 📁 Estrutura do Projeto

```
├── revisor_tom_lgpd.py      # Classe principal do revisor (local)
├── listas_validas.py        # Listas de valores válidos e mapeamentos
├── interface_revisor.py     # Interface principal
├── openai_client.py         # Cliente OpenAI
├── openai_agent.py          # Agente OpenAI
├── revisor_hibrido.py       # Revisor híbrido (local + IA)
├── exemplos_teste.py        # Exemplos e testes do sistema
├── exemplo_uso_ia.py        # Exemplos com IA
├── exemplo_demo.json        # Arquivo de exemplo
└── README.md               # Esta documentação
```

## 🧪 Executar Testes

```bash
# Executar todos os testes (local)
python exemplos_teste.py

# Exemplos com IA
python exemplo_uso_ia.py

# Teste específico com IA
python interface_revisor.py testar exemplo_demo.json --ia

# Apenas validação (sem modificar)
python exemplos_teste.py --validacao

# Salvar exemplos em arquivos JSON
python exemplos_teste.py --salvar
```

## 📝 Formato de Entrada/Saída

### Entrada (Ideia Original)
```json
{
  "data_da_semana": "YYYY-MM-DD",
  "tema": "string curta (deixe a dor/desejo explícito)",
  "persona": "valor de listas_validas.personas",
  "pilar": "valor de listas_validas.pilares",
  "formato": "valor de listas_validas.formatos",
  "canal": "valor de listas_validas.canais",
  "cta": "valor de listas_validas.ctas",
  "kpi_principal": "valor de listas_validas.kpis",
  "status": "Ideia",
  "roteirizado_em": "",
  "publicado_em": "",
  "lgpd_ok": "Sim",
  "prioridade": "valor de listas_validas.prioridade",
  "links_assets": "",
  "observacoes": "ex.: dor: ... | desejo: ..."
}
```

### Saída (Resultado da Revisão)
```json
{
  "ideia_corrigida": {
    // Mesma estrutura da entrada, com correções aplicadas
  },
  "ajustes": [
    "Lista de frases explicando o que foi alterado e por quê",
    "Máximo de 6 itens, objetivos e concisos"
  ]
}
```

## 🎯 Regras de Revisão

### Tom de Voz (6 Pilares)
1. **Didático**: Simplifica jargões, explica termos técnicos
2. **Empático**: Reconhece dores/desejos, linguagem acolhedora
3. **Prático**: Foca em 3 passos ou 1 ação concreta
4. **Confiável**: Remove promessas irreais, números plausíveis
5. **Moderno**: Linguagem atual e clara
6. **Inspirador**: Mostra benefícios finais sem exageros

### Consistência Canal/Formato
- **Reel/Short** → Instagram, TikTok ou YouTube (Shorts)
- **Carrossel** → Instagram
- **YouTube Longo** → YouTube
- **Post Telegram** → Telegram
- **Stories/Status** → Instagram (Stories) ou WhatsApp (Status)

### KPI por Canal
- **Instagram/TikTok/Shorts** → Salvamentos ou CTR WhatsApp/Comunidade
- **YouTube Longo** → Retenção (50%) ou Cliques LP
- **Telegram** → Engajamento ou CTR WhatsApp/LP

### LGPD Compliance
- ❌ **Proibido**: Nome completo, telefone, CPF, e-mail, renda específica
- ✅ **Permitido**: Casos genéricos, primeiros nomes, faixas de valores
- 🔧 **CTAs Seguros**: "Entrar na Comunidade Gratuita do Telegram", "WhatsApp: Diagnóstico 5'"

## 🤖 Configuração da IA

### Requisitos
```bash
pip install openai
```

### Configuração da API
```python
# Definir chave da API (recomendado: variável de ambiente)
import os
os.environ['OPENAI_API_KEY'] = 'sua-chave-aqui'

# Ou passar diretamente
revisor = InterfaceRevisor(usar_ia=True, api_key='sua-chave-aqui')
```

### Tipos de Revisor
- **`local`**: Apenas validações programáticas (rápido, sem custo)
- **`openai_client`**: ChatGPT via API (inteligente, custo por token)
- **`openai_agent`**: Assistente OpenAI (mais contexto, maior custo)
- **`hibrido`**: Combina local + IA (equilibrado)
- **`auto`**: Seleção automática baseada na complexidade

## 🔧 Personalização

### Adicionar Novos Valores às Listas
Edite o arquivo `listas_validas.py` para incluir novos:
- Personas
- Pilares
- Formatos
- Canais
- CTAs
- KPIs
- Prioridades

### Modificar Regras de Tom
Ajuste os métodos na classe `RevisorTomLGPD` em `revisor_tom_lgpd.py`:
- `_simplificar_linguagem()`
- `_explicitar_dor_desejo()`
- `_tornar_pratico()`
- `_remover_promessas_irreais()`
- `openai_client.py`: Ajustar prompts da IA
- `openai_agent.py`: Configurar instruções do assistente

## ⚠️ Campos Imutáveis

Estes campos **NUNCA** são alterados pelo revisor:
- `status` (sempre "Ideia")
- `roteirizado_em` (sempre vazio)
- `publicado_em` (sempre vazio)
- `lgpd_ok` (sempre "Sim")

## 📊 Monitoramento

O sistema inclui estatísticas de uso:
- Número de revisões por método
- Tempo médio de processamento
- Tokens utilizados (OpenAI)
- Taxa de sucesso por tipo

## 🤝 Integração com n8n

O sistema foi projetado para integração com n8n:
1. n8n envia ideia para revisão
2. Revisor retorna `ideia_corrigida` + `ajustes`
3. n8n atualiza planilha com `status = "Revisado"`

## 🤝 Contribuição

### Como Contribuir

1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

### Padrões de Desenvolvimento

```bash
# Instale as dependências de desenvolvimento
pip install -r requirements.txt
pip install pytest black flake8 bandit safety

# Execute os testes
pytest

# Formate o código
black .

# Verifique a qualidade do código
flake8 .
bandit -r .
safety check
```

### Estrutura do Projeto

```
finance-ia-revisor-tom-lgpd/
├── app.py                 # Aplicação Flask principal
├── interface_revisor.py   # Interface principal do sistema
├── revisor_local.py       # Revisor com regras locais
├── revisor_openai.py      # Revisores com integração OpenAI
├── exemplo_http_service.py # Exemplos de uso da API
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
├── docker-compose.yml    # Orquestração de containers
├── .env.example          # Exemplo de variáveis de ambiente
├── .github/workflows/    # Pipelines CI/CD
└── README.md            # Documentação
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

### Reportar Problemas

Se você encontrar algum problema, por favor:

1. **Verifique** se o problema já foi reportado nas [Issues](https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd/issues)
2. **Crie** uma nova issue com:
   - Descrição detalhada do problema
   - Passos para reproduzir
   - Logs relevantes
   - Informações do ambiente (OS, Python, Docker, etc.)

### FAQ

**Q: Como obter uma chave da API OpenAI?**
A: Acesse [platform.openai.com](https://platform.openai.com), crie uma conta e gere uma API key.

**Q: O sistema funciona sem internet?**
A: Parcialmente. O revisor local funciona offline, mas os revisores OpenAI requerem conexão.

**Q: Posso usar outros modelos de IA?**
A: Atualmente suportamos apenas OpenAI, mas contribuições para outros provedores são bem-vindas.

**Q: Como configurar rate limiting?**
A: Use um reverse proxy como Nginx ou configure middleware Flask personalizado.

## 🏷️ Versioning

Usamos [SemVer](http://semver.org/) para versionamento. Para as versões disponíveis, veja as [tags neste repositório](https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd/tags).

## 👥 Autores

- **Finance-IA Team** - *Desenvolvimento inicial* - [Finance-IA](https://github.com/marvin-ds)

Veja também a lista de [contribuidores](https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd/contributors) que participaram deste projeto.

## 🙏 Agradecimentos

- OpenAI pela API de inteligência artificial
- Comunidade Flask pelo framework web
- Contribuidores do projeto
- Equipe Finance-IA pelo feedback e testes

---

<div align="center">
  <strong>🚀 Finance-IA Revisor de Tom & LGPD</strong><br>
  <em>Revisão inteligente de conteúdo com IA</em><br><br>
  
  [![GitHub](https://img.shields.io/badge/GitHub-finance--ia--revisor--tom--lgpd-blue?logo=github)](https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd)
  [![Docker Hub](https://img.shields.io/badge/Docker-finance--ia--reviewer-blue?logo=docker)](https://github.com/marvin-ds/finance-ia-revisor-tom-lgpd/pkgs/container/finance-ia-revisor-tom-lgpd)
  
  **Feito com ❤️ pela equipe Finance-IA**
</div>