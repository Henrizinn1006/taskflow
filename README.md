# 📋 TaskFlow — Sistema de Gerenciamento de Tarefas

![CI](https://github.com/Henrizinn1006/taskflow/actions/workflows/ci.yml/badge.svg)

Projeto desenvolvido pela **TechFlow Solutions** (empresa fictícia) para uma startup de
logística que precisa acompanhar o fluxo de trabalho em tempo real, **priorizar tarefas
críticas** e monitorar o desempenho da equipe.

> Trabalho da disciplina de **Engenharia de Software** — *Construindo um Projeto Ágil no
> GitHub: Da Gestão ao Controle de Qualidade*.

---

## 🎯 Objetivo

Aplicar na prática os conceitos de Engenharia de Software: metodologias ágeis (Kanban),
versionamento com Git/GitHub, testes automatizados e integração contínua (CI), simulando
o ciclo de vida real de um software — do planejamento à gestão de mudanças.

## 📦 Escopo

**Escopo inicial:**
- CRUD completo de tarefas (criar, listar, atualizar e excluir);
- Interface web simples para operar o sistema;
- Persistência de dados em arquivo JSON;
- Testes automatizados com Pytest;
- Pipeline de CI com GitHub Actions (lint + testes).

**Escopo após mudança (ver seção Gestão de Mudanças):**
- ➕ Campo de **prioridade** (Alta / Média / Baixa) nas tarefas, com ordenação
  automática e destaque visual das tarefas críticas.

## 🔄 Metodologia

O projeto foi gerenciado com **Kanban**, usando o **GitHub Projects**:

- Quadro com as colunas **A Fazer (To Do)**, **Em Progresso (In Progress)** e **Concluído (Done)**;
- Cada funcionalidade virou um card, movido entre as colunas conforme o andamento;
- Commits pequenos e frequentes, com mensagens semânticas (`feat:`, `test:`, `docs:`, `ci:`...);
- Qualidade garantida por testes automatizados executados a cada push pelo GitHub Actions.

## 🚀 Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/Henrizinn1006/taskflow.git
cd taskflow

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
python src/app.py
```

Acesse **http://localhost:5000** no navegador.

## 🧪 Como rodar os testes

```bash
pytest tests -v
```

Os testes cobrem as quatro operações CRUD, as validações de entrada
(título obrigatório, status e prioridade válidos) e a persistência em JSON.

## 📁 Estrutura do projeto

```
taskflow/
├── .github/workflows/ci.yml   # Pipeline de integração contínua
├── src/
│   ├── app.py                 # Camada web (Flask)
│   ├── task_manager.py        # Regras de negócio (CRUD)
│   ├── templates/index.html   # Interface do usuário
│   └── static/style.css       # Estilos
├── tests/
│   ├── test_task_manager.py   # Testes unitários
│   └── test_app.py            # Testes de integração (rotas)
├── docs/                      # Diagramas UML e documentação
├── requirements.txt
└── README.md
```

## 🔀 Gestão de Mudanças (mudança de escopo)

**O que mudou:** durante o desenvolvimento, o cliente (startup de logística) solicitou a
inclusão de um campo de **prioridade** nas tarefas, pois entregas críticas estavam se
perdendo no meio da lista.

**Justificativa:** em logística, atrasos em tarefas críticas (ex.: liberação de uma carga)
geram custo direto. A priorização visual permite que a equipe identifique imediatamente o
que não pode esperar — atendendo ao requisito original de "priorizar tarefas críticas".

**Como a mudança foi gerenciada (processo ágil):**
1. Novo card **"Adicionar campo de prioridade às tarefas"** criado na coluna *A Fazer* do Kanban;
2. Impacto avaliado: alteração no modelo de dados, na interface e novos testes;
3. Implementação em commit dedicado (`feat: adiciona campo de prioridade às tarefas`);
4. Novos testes unitários garantindo a validação e a ordenação por prioridade;
5. Pipeline de CI validou a mudança antes da integração;
6. Card movido para *Concluído* e README atualizado (este registro).

Essa simulação demonstra o valor das metodologias ágeis: **mudanças são bem-vindas**,
desde que controladas — com rastreabilidade (Kanban + commits) e segurança (testes + CI).

## 🛠️ Tecnologias

| Ferramenta | Uso |
|---|---|
| Python 3.11 + Flask | Aplicação web |
| Pytest | Testes automatizados |
| Flake8 | Qualidade de código (lint) |
| GitHub Actions | Integração contínua |
| GitHub Projects | Quadro Kanban |

## 👤 Autor

Henri Tavares — Engenharia de Software, UniFECAF.
