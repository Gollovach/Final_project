document.addEventListener('DOMContentLoaded', function() {
    const qrForm = document.getElementById('qr-form');
    const qrContainer = document.getElementById('qr-container');
    const generateBtn = document.getElementById('generate-btn');

    if (qrForm) {
        qrForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            generateBtn.disabled = true;
            generateBtn.textContent = 'Генерация...';
            
            const link = document.getElementById('link').value.trim();
            qrContainer.innerHTML = '<p class="loading">Генерация QR-кода...</p>';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `link=${encodeURIComponent(link)}`
                });

                const data = await response.json();

                if (data.error) {
                    qrContainer.innerHTML = `<p class="error">${data.error}</p>`;
                } else if (data.qr_image) {
                    qrContainer.innerHTML = `
                        <img src="data:image/png;base64,${data.qr_image}" 
                             alt="QR код для ${link}" 
                             class="qr-image">
                    `;
                }
            } catch (error) {
                console.error('Error:', error);
                qrContainer.innerHTML = '<p class="error">Ошибка при генерации QR-кода</p>';
            } finally {
                generateBtn.disabled = false;
                generateBtn.textContent = 'Сгенерировать QR-код';
            }
        });
    }
});