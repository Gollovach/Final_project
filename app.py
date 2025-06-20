import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import qrcode
from io import BytesIO
import base64

# Получаем абсолютный путь к папке проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__,
    template_folder=os.path.join(project_root, 'page'),
    static_folder=os.path.join(project_root, 'static')
)

def generate_qr_code(text):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=12,
            border=2,
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
    """Главная страница"""
    # Проверка существования файла
    template_path = os.path.join(app.template_folder, 'qr_generate.html')
    if not os.path.exists(template_path):
        return f"Файл не найден: {template_path}", 404
    return render_template('qr_generate.html')

@app.route('/generate_qr', methods=['POST'])
def handle_qr():
    """Обработчик генерации QR"""
    text = request.form.get('link')
    if not text:
        return jsonify({'error': 'Введите текст'}), 400
    
    qr_image = generate_qr_code(text)
    return jsonify({'qr_image': qr_image}) if qr_image else jsonify({'error': 'Ошибка генерации'}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Отдача статики"""
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    # Проверка перед запуском
    print(f"Корень проекта: {project_root}")
    print(f"Шаблоны: {os.listdir(app.template_folder)}")
    print(f"Статика: {os.listdir(app.static_folder)}")
    
    app.run(debug=True, port=5000, use_reloader=False)