document.getElementById('qr-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const link = document.getElementById('link').value;
    const qrContainer = document.getElementById('qr-container');
    
    if (!link) {
        alert('Пожалуйста, введите ссылку или текст');
        return;
    }

    try {
        const response = await fetch('/generate_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `link=${encodeURIComponent(link)}`
        });

        const data = await response.json();
        
        if (data.qr_image) {
            qrContainer.innerHTML = `<img src="data:image/png;base64,${data.qr_image}" alt="QR Code">`;
        } else if (data.error) {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка при генерации QR-кода');
    }
});