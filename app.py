from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random
import io
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        total_exercicios = int(request.form["exercicios"])
        qtd_numeros = int(request.form["numeros"])
        tipo = request.form["tipo"]

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

        x = 50
        y = height - 50
        line_height = 18

        c.setFont("Courier", 11)

        for i in range(1, total_exercicios + 1):
            c.drawString(x, y, f"Exercício {i:02d}")
            y -= line_height

            for _ in range(qtd_numeros):
                num = random.randint(minimo, maximo)
                c.drawRightString(x + 220, y, str(num))
                y -= line_height

            c.drawString(x + 160, y, "-" * largura)
            y -= line_height * 2

            if y < 80:
                c.showPage()
                c.setFont("Courier", 11)
                y = height - 50

        c.save()
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="exercicios_soma.pdf",
            mimetype="application/pdf"
        )

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

