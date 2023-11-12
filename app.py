import base64
import json
from flask import Flask, request, jsonify
from vosk import Model, KaldiRecognizer
import wave
import io

app = Flask(__name__)

# Загрузка модели Vosk
model = Model("/app/model")


@app.route('/')
def hello_world():  # put application's code here
    return 'ready'

@app.route('/parse', methods=['POST'])
def parse():
    data = request.json

    if not data or 'wave' not in data:
        return jsonify({'error': 'No wave data provided'}), 400

    try:
        # Декодирование данных из base64
        audio_data = base64.b64decode(data['wave'])
        audio_stream = io.BytesIO(audio_data)

        # Чтение аудиофайла
        wf = wave.open(audio_stream, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            return jsonify({'error': 'Unsupported wave file'}), 400

        rec = KaldiRecognizer(model, wf.getframerate())
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                pass

        result = json.loads(rec.FinalResult())

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
