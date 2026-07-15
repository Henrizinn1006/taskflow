import json
import os

STATUS_VALIDOS = ("A Fazer", "Em Progresso", "Concluído")
PRIORIDADES_VALIDAS = ("Alta", "Média", "Baixa")

class GerenciadorDeTarefas:
    def __init__(self, caminho_arquivo="data/tarefas.json"):
        self.caminho_arquivo = caminho_arquivo
        self.tarefas = []
        self._proximo_id = 1
        self._carregar()

    def _carregar(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                self.tarefas = json.load(f)
            if self.tarefas:
                self._proximo_id = max(t["id"] for t in self.tarefas) + 1

    def _salvar(self):
        pasta = os.path.dirname(self.caminho_arquivo)
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(self.tarefas, f, ensure_ascii=False, indent=2)

    def criar_tarefa(self, titulo, descricao="", prioridade="Média"):
        if not titulo or not titulo.strip():
            raise ValueError("O título da tarefa é obrigatório.")
        if prioridade not in PRIORIDADES_VALIDAS:
            raise ValueError(
                f"Prioridade inválida: {prioridade}. "
                f"Use uma de: {PRIORIDADES_VALIDAS}"
            )

        tarefa = {
            "id": self._proximo_id,
            "titulo": titulo.strip(),
            "descricao": descricao.strip(),
            "status": "A Fazer",
            "prioridade": prioridade,
        }
        self.tarefas.append(tarefa)
        self._proximo_id += 1
        self._salvar()
        return tarefa

    def listar_tarefas(self):
        ordem = {"Alta": 0, "Média": 1, "Baixa": 2}
        return sorted(self.tarefas, key=lambda t: ordem.get(t.get("prioridade", "Média"), 1))

    def buscar_tarefa(self, id_tarefa):
        for tarefa in self.tarefas:
            if tarefa["id"] == id_tarefa:
                return tarefa
        return None

    def atualizar_tarefa(self, id_tarefa, titulo=None, descricao=None, status=None, prioridade=None):
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

    def excluir_tarefa(self, id_tarefa):
        tarefa = self.buscar_tarefa(id_tarefa)
        if tarefa is None:
            raise ValueError(f"Tarefa com id {id_tarefa} não encontrada.")
        self.tarefas.remove(tarefa)
        self._salvar()
        return True
