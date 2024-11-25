from flask import Flask, request, jsonify
import whisper
import os

# Inicialize o modelo Whisper
model = whisper.load_model("small")

app = Flask(__name__)

@app.route("/transcrever", methods=["POST"])
def transcrever():
    if "file" not in request.files:
        return jsonify({"Erro": "Nenhum arquivo enviado"}), 400

    # Cria a pasta para salvar nela o áudio recebido
    os.makedirs("../tmp", exist_ok=True)

    # Salva o arquivo recebido
    file = request.files["file"]
    file_path = os.path.join("../tmp", file.filename)
    file.save(file_path)

    # Transcreve o áudio
    result = model.transcribe(file_path, language="pt")
    os.remove(file_path)  # Remove o arquivo temporário

    return result["text"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)