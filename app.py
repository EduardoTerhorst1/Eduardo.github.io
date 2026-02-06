from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random
import io

app = Flask(__name__)

def gerar_pdf(total_exercicios, qtd_numeros, tipo):
    # Configuração por tipo
    if tipo == "dezena":
        minimo, maximo, largura = 10, 99, 2
    elif tipo == "centena":
        minimo, maximo, largura = 100, 999, 3
    else:
        minimo, maximo, largura = 1000, 9999, 4

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Courier", 11)

    # Layout
    margem_x = 40
    margem_y = 50
    coluna_largura = (width - margem_x * 2) / 2
    linha_altura = 16

    altura_exercicio = (qtd_numeros + 4) * linha_altura

    col = 0
    y = height - margem_y

    for i in range(1, total_exercicios + 1):
        # Troca de coluna
        if y - altura_exercicio < margem_y:
            col += 1
            y = height - margem_y

        # Nova página
        if col > 1:
            c.showPage()
            c.setFont("Courier", 11)
            col = 0
            y = height - margem_y

        x = margem_x + col * coluna_largura

        # Título
        c.drawString(x, y, f"Exercício {i:02d}")
        y -= linha_altura

        num_x = x + 20

        # Gera números
        numeros = [random.randint(minimo, maximo) for _ in range(qtd_numeros)]

        for idx, num in enumerate(numeros):
            # Só o último número recebe o "+"
            if idx == len(numeros) - 1:
                texto = f"+ {num}"
            else:
                texto = f"  {num}"

            c.drawString(num_x, y, texto)
            y -= linha_altura

        # Linha da soma
        c.drawString(num_x, y, "-" * (largura + 3))
        y -= linha_altura * 2

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
