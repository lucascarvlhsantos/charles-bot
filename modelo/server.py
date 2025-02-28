from flask import Flask, request, jsonify
from chat import enviar_mensagem
from flask_cors import CORS
import ollama
import html
import json

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Initialize the client once
client = ollama.Client()

def decode_and_fix_encoding(text):
    """
    Corrige problemas de codificação UTF-8 que aparecem como 'Ã©', 'Ã£', etc.
    """
    try:
        # Tenta decodificar o texto como se fosse Latin-1 e reinterpreta como UTF-8
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Retorna o texto original se falhar
        return text

@app.route('/enviar-prompt', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        print(data)
        
        if not isinstance(data, dict):
            return jsonify({'status': "error", 'message': 'Invalid JSON format'}), 400

        prompt = data.get('prompt', '')
        print(prompt)
        if not prompt:
            return jsonify({'status': "error", 'message': 'Prompt is required'}), 400
        
        # Processa a resposta do chat
        repostaChat = enviar_mensagem(prompt)
        
        # Decodifica e corrige problemas de codificação
        if isinstance(repostaChat, list):
            repostaChatText = [decode_and_fix_encoding(message['content']) for message in repostaChat["resposta"]]
        else:
            repostaChatText = decode_and_fix_encoding(repostaChat["resposta"])

        response = {
            'status': "sucesso",
            "data": {
                "resposta": {
                    "usuario": prompt,
                    "agent": repostaChatText
                },
                "relatorio": {
                    "promptUsuario": prompt,
                    "respostaBuscaRag": repostaChat["data"],
                    "fontes": repostaChat["fonts"]
                }
            }
        }

        # Retorna o JSON com ensure_ascii=False para manter caracteres UTF-8
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return jsonify({'status': "error", 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
