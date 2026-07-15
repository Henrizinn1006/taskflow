# -*- coding: utf-8 -*-
"""
test_task_manager.py
Testes unitários das regras de negócio do TaskFlow (Pytest).

Cobrem as quatro operações CRUD e as validações de entrada,
garantindo que o sistema se comporte corretamente mesmo com
dados inválidos — requisito de controle de qualidade do projeto.
"""

import os
import sys

import pytest

# Permite importar o módulo da pasta src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from task_manager import GerenciadorDeTarefas  # noqa: E402


@pytest.fixture
def gerenciador(tmp_path):
    """Cria um gerenciador isolado com arquivo temporário para cada teste."""
    arquivo = tmp_path / "tarefas_teste.json"
    return GerenciadorDeTarefas(caminho_arquivo=str(arquivo))


# ----------------------------------------------------------------------
# CREATE
# ----------------------------------------------------------------------
def test_criar_tarefa_valida(gerenciador):
    """Deve criar uma tarefa com os dados informados."""
    tarefa = gerenciador.criar_tarefa("Configurar banco", "Criar schema inicial", "Alta")
    assert tarefa["id"] == 1
    assert tarefa["titulo"] == "Configurar banco"
    assert tarefa["status"] == "A Fazer"
    assert tarefa["prioridade"] == "Alta"


def test_criar_tarefa_sem_titulo_gera_erro(gerenciador):
    """Validação de entrada: título vazio deve gerar ValueError."""
    with pytest.raises(ValueError):
        gerenciador.criar_tarefa("")
    with pytest.raises(ValueError):
        gerenciador.criar_tarefa("   ")


def test_criar_tarefa_prioridade_invalida_gera_erro(gerenciador):
    """Validação de entrada: prioridade inexistente deve gerar ValueError."""
    with pytest.raises(ValueError):
        gerenciador.criar_tarefa("Tarefa", prioridade="Urgentíssima")


# ----------------------------------------------------------------------
# READ
# ----------------------------------------------------------------------
def test_listar_ordena_por_prioridade(gerenciador):
    """Tarefas de prioridade Alta devem aparecer primeiro (mudança de escopo)."""
    gerenciador.criar_tarefa("Baixa prioridade", prioridade="Baixa")
    gerenciador.criar_tarefa("Alta prioridade", prioridade="Alta")
    gerenciador.criar_tarefa("Média prioridade", prioridade="Média")

    lista = gerenciador.listar_tarefas()
    assert [t["prioridade"] for t in lista] == ["Alta", "Média", "Baixa"]


def test_buscar_tarefa_inexistente_retorna_none(gerenciador):
    """Buscar ID que não existe deve retornar None."""
    assert gerenciador.buscar_tarefa(999) is None


# ----------------------------------------------------------------------
# UPDATE
# ----------------------------------------------------------------------
def test_atualizar_status(gerenciador):
    """Deve mover a tarefa de 'A Fazer' para 'Em Progresso'."""
    tarefa = gerenciador.criar_tarefa("Implementar login")
    atualizada = gerenciador.atualizar_tarefa(tarefa["id"], status="Em Progresso")
    assert atualizada["status"] == "Em Progresso"


def test_atualizar_status_invalido_gera_erro(gerenciador):
    """Validação de entrada: status fora da lista deve gerar ValueError."""
    tarefa = gerenciador.criar_tarefa("Tarefa qualquer")
    with pytest.raises(ValueError):
        gerenciador.atualizar_tarefa(tarefa["id"], status="Pausado")


def test_atualizar_tarefa_inexistente_gera_erro(gerenciador):
    """Atualizar ID inexistente deve gerar ValueError."""
    with pytest.raises(ValueError):
        gerenciador.atualizar_tarefa(42, status="Concluído")


# ----------------------------------------------------------------------
# DELETE
# ----------------------------------------------------------------------
def test_excluir_tarefa(gerenciador):
    """Deve remover a tarefa da lista."""
    tarefa = gerenciador.criar_tarefa("Tarefa temporária")
    assert gerenciador.excluir_tarefa(tarefa["id"]) is True
    assert gerenciador.buscar_tarefa(tarefa["id"]) is None


def test_excluir_tarefa_inexistente_gera_erro(gerenciador):
    """Excluir ID inexistente deve gerar ValueError."""
    with pytest.raises(ValueError):
        gerenciador.excluir_tarefa(123)


# ----------------------------------------------------------------------
# PERSISTÊNCIA
# ----------------------------------------------------------------------
def test_persistencia_em_json(tmp_path):
    """As tarefas devem ser recarregadas do arquivo entre instâncias."""
    arquivo = str(tmp_path / "tarefas.json")

    g1 = GerenciadorDeTarefas(caminho_arquivo=arquivo)
    g1.criar_tarefa("Tarefa persistida", prioridade="Alta")

    g2 = GerenciadorDeTarefas(caminho_arquivo=arquivo)
    tarefas = g2.listar_tarefas()
    assert len(tarefas) == 1
    assert tarefas[0]["titulo"] == "Tarefa persistida"
