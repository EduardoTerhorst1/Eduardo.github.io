from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random
import io
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    erro = None

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

        # Margens
        margin_x = 40
        margin_top = height - 50
        margin_bottom = 50

        # Colunas
        colunas = 2
        coluna_largura = (width - margin_x * 2) / colunas

        usable_height = margin_top - margin_bottom

        linhas_por_exercicio = 1 + qtd_numeros + 2
        total_linhas = total_exercicios * linhas_por_exercicio

        # Fonte mínima
        font_min = 7
        line_height = usable_height / (total_linhas / colunas)
        font_size = line_height * 0.9

        if font_size < font_min:
            erro = (
                "Quantidade de exercícios muito alta para caber "
                "em uma folha A4. Reduza o número de exercícios "
                "ou de números por exercício."
            )
            return render_template("index.html", erro=erro)

        c.setFont("Courier", font_size)

        x_base = margin_x
        y = margin_top
        coluna_atual = 0

        for i in range(1, total_exercicios + 1):
            x = x_base + coluna_atual * coluna_largura

            c.drawString(x, y, f"Exercício {i:02d}")
            y -= line_height

            for _ in range(qtd_numeros):
                num = random.randint(minimo, maximo)
                c.drawRightString(x + coluna_largura - 20, y, str(num))
                y -= line_height

            c.drawString(x + coluna_largura - 70, y, "-" * largura)
            y -= line_height * 2

            # Quebra de coluna
            if y < margin_bottom + line_height * linhas_por_exercicio:
                coluna_atual += 1
                if coluna_atual >= colunas:
                    erro = (
                        "Conteúdo excede o limite de uma folha A4. "
                        "Reduza a quantidade de exercícios."
                    )
                    return render_template("index.html", erro=erro)

                y = margin_top

        c.save()
        buffer.seek(0)
        
    if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="exercicios_soma.pdf",
            mimetype="application/pdf"
        )

    return render_template("index.html", erro=erro)


