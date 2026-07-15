# -*- coding: utf-8 -*-
"""
test_app.py
Testes de integração das rotas web do TaskFlow (Pytest + Flask test client).

Validam o comportamento das rotas HTTP de ponta a ponta,
simulando requisições reais de um usuário.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import app as modulo_app  # noqa: E402
from task_manager import GerenciadorDeTarefas  # noqa: E402


@pytest.fixture
def cliente(tmp_path):
    """Cliente de teste do Flask com armazenamento isolado."""
    modulo_app.gerenciador = GerenciadorDeTarefas(
        caminho_arquivo=str(tmp_path / "tarefas.json")
    )
    modulo_app.app.config["TESTING"] = True
    with modulo_app.app.test_client() as cliente:
        yield cliente


def test_pagina_inicial_carrega(cliente):
    """A página inicial deve responder com status 200."""
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert "TaskFlow".encode() in resposta.data


def test_criar_tarefa_via_formulario(cliente):
    """POST /criar deve adicionar a tarefa e redirecionar para a lista."""
    resposta = cliente.post(
        "/criar",
        data={"titulo": "Entrega urgente", "descricao": "Rota SP-RJ", "prioridade": "Alta"},
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    assert "Entrega urgente".encode() in resposta.data


def test_criar_tarefa_sem_titulo_mostra_erro(cliente):
    """Título vazio deve exibir mensagem de erro, sem quebrar a aplicação."""
    resposta = cliente.post(
        "/criar", data={"titulo": ""}, follow_redirects=True
    )
    assert resposta.status_code == 200
    assert "obrigatório".encode() in resposta.data


def test_atualizar_status_da_tarefa(cliente):
    """POST /atualizar deve mudar o status exibido."""
    cliente.post("/criar", data={"titulo": "Testar CI", "prioridade": "Média"})
    resposta = cliente.post(
        "/atualizar/1", data={"status": "Concluído"}, follow_redirects=True
    )
    assert resposta.status_code == 200
    assert "atualizada".encode() in resposta.data


def test_excluir_tarefa(cliente):
    """POST /excluir deve remover a tarefa da lista."""
    cliente.post("/criar", data={"titulo": "Tarefa descartável", "prioridade": "Baixa"})
    resposta = cliente.post("/excluir/1", follow_redirects=True)
    assert resposta.status_code == 200
    assert "Tarefa descartável".encode() not in resposta.data
