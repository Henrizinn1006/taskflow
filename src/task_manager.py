# -*- coding: utf-8 -*-
"""
task_manager.py
Módulo central de regras de negócio do TaskFlow.

Contém a classe GerenciadorDeTarefas, responsável pelas operações
CRUD (Create, Read, Update, Delete) sobre as tarefas, com
persistência em arquivo JSON.

Mantido separado da camada web (app.py) para facilitar a
testabilidade com Pytest, seguindo o princípio de separação
de responsabilidades da Engenharia de Software.
"""

import json
import os

# Status permitidos para uma tarefa (espelham as colunas do Kanban)
STATUS_VALIDOS = ("A Fazer", "Em Progresso", "Concluído")

# Prioridades permitidas — adicionadas na MUDANÇA DE ESCOPO,
# a pedido do cliente (startup de logística) para destacar tarefas críticas
PRIORIDADES_VALIDAS = ("Alta", "Média", "Baixa")


class GerenciadorDeTarefas:
    """Gerencia o ciclo de vida das tarefas (CRUD + persistência)."""

    def __init__(self, caminho_arquivo="data/tarefas.json"):
        # Caminho do arquivo JSON usado como banco de dados simples
        self.caminho_arquivo = caminho_arquivo
        self.tarefas = []
        self._proximo_id = 1
        self._carregar()

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------
    def _carregar(self):
        """Carrega as tarefas do arquivo JSON, se ele existir."""
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                self.tarefas = json.load(f)
            # Garante que novos IDs não colidam com os já existentes
            if self.tarefas:
                self._proximo_id = max(t["id"] for t in self.tarefas) + 1

    def _salvar(self):
        """Grava a lista de tarefas no arquivo JSON."""
        pasta = os.path.dirname(self.caminho_arquivo)
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(self.tarefas, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def criar_tarefa(self, titulo, descricao="", prioridade="Média"):
        """Cria uma nova tarefa após validar as entradas."""
        # Validação de entrada: título é obrigatório
        if not titulo or not titulo.strip():
            raise ValueError("O título da tarefa é obrigatório.")
        # Validação de entrada: prioridade deve ser válida
        if prioridade not in PRIORIDADES_VALIDAS:
            raise ValueError(
                f"Prioridade inválida: {prioridade}. "
                f"Use uma de: {PRIORIDADES_VALIDAS}"
            )

        tarefa = {
            "id": self._proximo_id,
            "titulo": titulo.strip(),
            "descricao": descricao.strip(),
            "status": "A Fazer",          # toda tarefa nasce na coluna A Fazer
            "prioridade": prioridade,     # campo da mudança de escopo
        }
        self.tarefas.append(tarefa)
        self._proximo_id += 1
        self._salvar()
        return tarefa

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def listar_tarefas(self):
        """Retorna todas as tarefas ordenadas por prioridade (Alta primeiro)."""
        ordem = {"Alta": 0, "Média": 1, "Baixa": 2}
        return sorted(self.tarefas, key=lambda t: ordem.get(t.get("prioridade", "Média"), 1))

    def buscar_tarefa(self, id_tarefa):
        """Busca uma tarefa pelo ID. Retorna None se não existir."""
        for tarefa in self.tarefas:
            if tarefa["id"] == id_tarefa:
                return tarefa
        return None

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def atualizar_tarefa(self, id_tarefa, titulo=None, descricao=None,
                         status=None, prioridade=None):
        """Atualiza os campos informados de uma tarefa existente."""
        tarefa = self.buscar_tarefa(id_tarefa)
        if tarefa is None:
            raise ValueError(f"Tarefa com id {id_tarefa} não encontrada.")

        if titulo is not None:
            if not titulo.strip():
                raise ValueError("O título da tarefa não pode ficar vazio.")
            tarefa["titulo"] = titulo.strip()

        if descricao is not None:
            tarefa["descricao"] = descricao.strip()

        if status is not None:
            if status not in STATUS_VALIDOS:
                raise ValueError(
                    f"Status inválido: {status}. Use um de: {STATUS_VALIDOS}"
                )
            tarefa["status"] = status

        if prioridade is not None:
            if prioridade not in PRIORIDADES_VALIDAS:
                raise ValueError(
                    f"Prioridade inválida: {prioridade}. "
                    f"Use uma de: {PRIORIDADES_VALIDAS}"
                )
            tarefa["prioridade"] = prioridade

        self._salvar()
        return tarefa

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def excluir_tarefa(self, id_tarefa):
        """Remove uma tarefa pelo ID."""
        tarefa = self.buscar_tarefa(id_tarefa)
        if tarefa is None:
            raise ValueError(f"Tarefa com id {id_tarefa} não encontrada.")
        self.tarefas.remove(tarefa)
        self._salvar()
        return True
