from flask import Flask, render_template, request, redirect, url_for, flash
from task_manager import GerenciadorDeTarefas, STATUS_VALIDOS, PRIORIDADES_VALIDAS

app = Flask(__name__)
app.secret_key = "taskflow-dev"
gerenciador = GerenciadorDeTarefas()

@app.route("/")
def index():
    tarefas = gerenciador.listar_tarefas()
    return render_template(
        "index.html",
        tarefas=tarefas,
        status_validos=STATUS_VALIDOS,
        prioridades=PRIORIDADES_VALIDAS,
    )

@app.route("/criar", methods=["POST"])
def criar():
    try:
        gerenciador.criar_tarefa(
            titulo=request.form.get("titulo", ""),
            descricao=request.form.get("descricao", ""),
            prioridade=request.form.get("prioridade", "Média"),
        )
        flash("Tarefa criada com sucesso!", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("index"))

@app.route("/atualizar/<int:id_tarefa>", methods=["POST"])
def atualizar(id_tarefa):
    try:
        gerenciador.atualizar_tarefa(
            id_tarefa,
            status=request.form.get("status") or None,
            prioridade=request.form.get("prioridade") or None,
        )
        flash("Tarefa atualizada!", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("index"))

@app.route("/excluir/<int:id_tarefa>", methods=["POST"])
def excluir(id_tarefa):
    try:
        gerenciador.excluir_tarefa(id_tarefa)
        flash("Tarefa excluída.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
