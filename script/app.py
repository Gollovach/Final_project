import os
from flask import Flask, render_template, request, jsonify
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

def generate_qr_code(text):
    try:
        if not text:
            return None
        
        qr = qrcode.QRCode(
            version=1,  # Вы можете изменить это на большее значение для более крупных кодов, если необходимо
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,  # Увеличиваем размер каждого "квадратика" в QR-коде
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")  # Черный QR-код на белом фоне
        
        # Сохраняем изображение в памяти
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Конвертируем изображение в формат Base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return img_base64
    except Exception as e:
        print(f"Ошибка при генерации QR-кода: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    try:
        text = request.form['link']  # Получаем ссылку из формы
        if not text:
            return jsonify({'error': 'No text provided for QR generation'}), 400

        qr_image = generate_qr_code(text)  # Генерируем QR код
        if qr_image is None:
            return jsonify({'error': 'Failed to generate QR code'}), 500
        
        return jsonify({'qr_image': qr_image})  # Отправляем изображение в формате base64
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
