from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random
import io

app = Flask(__name__)

def gerar_pdf(total_exercicios, qtd_numeros, tipo):

    minimo, maximo = 100000, 999999

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Courier", 12)

    margem_x = 40
    margem_y = 50
    coluna_largura = (width - margem_x * 2) / 2
    linha_altura = 18  # 🔥 aumentei a altura das linhas

    altura_util = height - (margem_y * 2)
    exercicios_por_coluna = 3
    altura_exercicio = altura_util / exercicios_por_coluna

    exercicio_na_coluna = 0
    col = 0
    y_base = height - margem_y

    gabarito = []

    for i in range(1, total_exercicios + 1):

        if exercicio_na_coluna >= exercicios_por_coluna:
            exercicio_na_coluna = 0
            col += 1

        if col > 1:
            c.showPage()
            c.setFont("Courier", 12)
            col = 0

        x = margem_x + col * coluna_largura
        y = y_base - (exercicio_na_coluna * altura_exercicio)

        # Título
        c.drawString(x, y, f"Exercício {i:02d}")
        y -= linha_altura * 1.5  # 🔥 mais espaço após título

        alinhamento_x = x + coluna_largura - 20

        numeros = [random.randint(minimo, maximo) for _ in range(qtd_numeros)]
        soma = sum(numeros)

        for idx, num in enumerate(numeros):
            numero_formatado = f"{num:,}".replace(",", ".")

            if idx == len(numeros) - 1:
                texto = f"+ {numero_formatado}"
            else:
                texto = f"  {numero_formatado}"

            c.drawRightString(alinhamento_x, y, texto)
            y -= linha_altura

        # Linha da soma
        c.drawRightString(alinhamento_x, y, "-" * 12)
        y -= linha_altura

        # 🔥🔥🔥 GRANDE ESPAÇO PARA RESOLVER
        y -= linha_altura * 4

        gabarito.append((i, soma))

        exercicio_na_coluna += 1

    # ======= GABARITO =======
    c.showPage()
    c.setFont("Courier", 12)

    c.drawString(40, height - 50, "GABARITO")
    y = height - 80

    for numero_exercicio, resultado in gabarito:
        resultado_formatado = f"{resultado:,}".replace(",", ".")
        c.drawString(60, y, f"Exercício {numero_exercicio:02d} = {resultado_formatado}")
        y -= 22

        if y < 50:
            c.showPage()
            c.setFont("Courier", 12)
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        total_exercicios = int(request.form["exercicios"])
        qtd_numeros = int(request.form["numeros"])
        tipo = request.form["tipo"]

        pdf = gerar_pdf(total_exercicios, qtd_numeros, tipo)

        return send_file(
            pdf,
            as_attachment=True,
            download_name="exercicios_soma.pdf",
            mimetype="application/pdf"
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run()

