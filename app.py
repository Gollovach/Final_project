import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import qrcode
from io import BytesIO
import base64
from PIL import Image
from pyzbar.pyzbar import decode

app = Flask(__name__)

# Указываем правильные пути к шаблонам и статике
app.template_folder = os.path.join(os.path.dirname(__file__), 'page')
app.static_folder = os.path.join(os.path.dirname(__file__), 'static')

def generate_qr(text):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#4a90e2", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Ошибка генерации QR: {e}")
        return None

def decode_qr(image_file):
    try:
        img = Image.open(image_file)
        decoded = decode(img)
        if decoded:
            return decoded[0].data.decode('utf-8')
        return None
    except Exception as e:
        print(f"Ошибка декодирования QR: {e}")
        return None

@app.route('/')
def index():
    return render_template('qr_generate.html')

@app.route('/decode', methods=['GET', 'POST'])
def handle_decode():
    if request.method == 'GET':
        return render_template('qr_decode.html')
    
    # Обработка POST запроса
    if 'file' not in request.files and 'image_data' not in request.form:
        return jsonify({'error': 'Необходимо загрузить изображение или вставить из буфера'}), 400

    try:
        if 'image_data' in request.form:  # Если вставка через Ctrl+V
            image_data = request.form['image_data'].split(',')[1]  # Удаляем "data:image/png;base64,"
            img = Image.open(BytesIO(base64.b64decode(image_data)))
        else:  # Если загрузка файла
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Файл не выбран'}), 400
            img = Image.open(file.stream)

        decoded = decode(img)
        if decoded:
            return jsonify({'data': decoded[0].data.decode('utf-8')})
        return jsonify({'error': 'QR-код не найден'}), 400
    except Exception as e:
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
def handle_generate():
    text = request.form.get('link', '').strip()
    if not text:
        return jsonify({'error': 'Введите текст или ссылку'}), 400
    qr_image = generate_qr(text)
    if not qr_image:
        return jsonify({'error': 'Ошибка при генерации QR-кода'}), 500
    return jsonify({'qr_image': qr_image})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)