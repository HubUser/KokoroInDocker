import os
import ssl
import tempfile
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from sound_generator import generate_sound

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT", 3000))
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/api/tts', methods=['POST'])
def tts():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Text is required in the request body'}), 400

    text = data['text']
    speed = data.get('speed', 1.0)
    fd, output_file = tempfile.mkstemp(suffix=".wav", dir=OUTPUT_DIR)
    os.close(fd)  # Close the file descriptor, as you will overwrite the file

    try:
        generate_sound(text, output_file, speed)
        def generate():
            with open(output_file, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    yield chunk
            os.remove(output_file)

        headers = {
            'Content-Type': 'audio/wav',
            'Content-Disposition': f'attachment; filename="{os.path.basename(output_file)}"'
        }
        return Response(generate(), headers=headers)
    except Exception as e:
        if os.path.exists(output_file):
            os.remove(output_file)
        return jsonify({'error': f'Failed to process text-to-speech conversion: {str(e)}'}), 500

@app.route('/')
def index():
    return '''
    <html>
      <body>
        <h1>Text-to-Speech API</h1>
        <p>Send a POST request to /api/tts with JSON body: {"text": "your text here"}</p>
      </body>
    </html>
    '''

if __name__ == '__main__':
    ssl_key = os.environ.get('SSL_KEY_PATH', 'certs/server.key')
    ssl_cert = os.environ.get('SSL_CERT_PATH', 'certs/server.cert')
    if not (os.path.exists(ssl_key) and os.path.exists(ssl_cert)):
        print("SSL certificate or key not found. Please ensure they exist in the certs directory.")
        exit(1)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(ssl_cert, ssl_key)
    app.run(host='0.0.0.0', port=PORT, ssl_context=context)