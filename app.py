from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/api/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.json

    if not dados:
        return jsonify({"error": "Dados inválidos"}), 400

    return jsonify({
        "message": "Dados salvos com sucesso!",
        "dados": dados
    }), 201


if __name__ == '__main__':
    app.run(debug=True)
