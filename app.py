from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from pathlib import Path
import tempfile

from src.extractor import extract_from_pdf
from src.xml_generator import generate_xml
from src.validators import validate_data

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
app.secret_key = "troque-esta-chave-em-producao"

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/gerar-xml", methods=["POST"])
def gerar_xml():
    pdf_file = request.files.get("pdf_file")
    template_type = request.form.get("template_type", "compra_financiamento")
    local = request.form.get("local", "RECIFE/PE").strip()
    numero_contrato = request.form.get("numero_contrato", "").strip()
    data_instrumento = request.form.get("data_instrumento", "").strip()

    if not pdf_file or not pdf_file.filename.lower().endswith(".pdf"):
        flash("Envie um arquivo PDF válido.")
        return redirect(url_for("index"))

    temp_pdf = UPLOAD_DIR / pdf_file.filename
    pdf_file.save(temp_pdf)

    try:
        extracted = extract_from_pdf(temp_pdf)

        if local:
            extracted["local"] = local
        if numero_contrato:
            extracted["numero_contrato"] = numero_contrato
        if data_instrumento:
            extracted["data_instrumento"] = data_instrumento

        validate_data(extracted, template_type)
        xml_content = generate_xml(extracted, template_type)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
            tmp.write(xml_content.encode("utf-8"))
            tmp_path = tmp.name

        return send_file(
            tmp_path,
            as_attachment=True,
            download_name="asgard_gerado.xml",
            mimetype="application/xml",
        )
    except Exception as exc:
        flash(f"Erro ao processar PDF: {exc}")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
