// Функция для отображения результата
function showResult(data) {
    const container = document.getElementById('result-container');
    if (data.error) {
        container.innerHTML = `<p class="error">${data.error}</p>`;
    } else {
        // Проверяем, является ли результат URL-адресом
        if (isValidUrl(data.data)) {
            container.innerHTML = `
                <div class="result-link">
                    <p>Найден URL:</p>
                    <a href="${data.data}" target="_blank" class="url-button">
                        Перейти на сайт
                    </a>
                    <p class="url-text">${data.data}</p>
                </div>
            `;
        } else {
            container.innerHTML = `<p class="result">Результат: <strong>${data.data}</strong></p>`;
        }
    }
}

// Функция проверки URL
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// Вставка через Ctrl+V
document.addEventListener('paste', async (e) => {
    const items = e.clipboardData.items;
    for (let item of items) {
        if (item.type.indexOf('image') !== -1) {
            const blob = item.getAsFile();
            const reader = new FileReader();
            reader.onload = async (event) => {
                const preview = document.getElementById('preview-image');
                preview.src = event.target.result;
                preview.style.display = 'block';
                
                try {
                    const response = await fetch('/decode', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: `image_data=${encodeURIComponent(event.target.result)}`
                    });
                    const data = await response.json();
                    showResult(data);
                } catch (error) {
                    console.error('Ошибка:', error);
                    showResult({error: 'Ошибка при расшифровке'});
                }
            };
            reader.readAsDataURL(blob);
            break;
        }
    }
});

// Обработка выбора файла
document.getElementById('browse-btn').addEventListener('click', () => {
    document.getElementById('file').click();
});

document.getElementById('file').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        const preview = document.getElementById('preview-image');
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/decode', { method: 'POST', body: formData });
            const data = await response.json();
            showResult(data);
        } catch (error) {
            console.error('Ошибка:', error);
            showResult({error: 'Ошибка при загрузке файла'});
        }
    }
});