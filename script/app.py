import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import qrcode
from io import BytesIO
import base64

# Инициализация Flask с правильными путями
app = Flask(__name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'page'),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
)

def generate_qr_code(text):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=12,  # Увеличиваем размер каждого "пикселя" QR-кода (было 10)
            border=2,     # Уменьшаем белую рамку вокруг QR-кода (было 4)
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#4a90e2", back_color="white")
        
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Ошибка генерации QR: {e}")
        return None

@app.route('/')
def home():
    """Главная страница с формой"""
    return render_template('qr_generate.html')

@app.route('/generate_qr', methods=['POST'])
def handle_qr_generation():
    """Обработчик генерации QR"""
    try:
        text = request.form.get('link')
        if not text:
            return jsonify({'error': 'Введите текст для QR-кода'}), 400
        
        qr_image = generate_qr_code(text)
        if not qr_image:
            return jsonify({'error': 'Ошибка генерации QR'}), 500
            
        return jsonify({'qr_image': qr_image})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Отдача статических файлов"""
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    # Создаем папки если их нет
    os.makedirs(app.template_folder, exist_ok=True)
    os.makedirs(app.static_folder, exist_ok=True)
    
    # Запускаем сервер
    app.run(debug=True, port=5000)