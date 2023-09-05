// QR Code Rendering script in JS 

document.addEventListener('DOMContentLoaded', function() {
    const qrTriggers = document.querySelectorAll('.qr-trigger');
    const qrTooltip = document.querySelector('.qr-tooltip');
    const qrImage = document.getElementById('qr-image'); 

    qrTriggers.forEach(qrTrigger => {
        qrTrigger.addEventListener('click', function(event) {
            event.preventDefault(); 
            const qrData = qrTrigger.getAttribute('data-qrdata');
            const file_id = qrTrigger.getAttribute('data-fileid');

            fetch(`/generate_qr_code/${file_id}/`)
                .then(response => response.blob()) 
                .then(blob => {
                    const objectURL = URL.createObjectURL(blob);
                    
                    qrImage.src = objectURL;
                    qrImage.alt = `QR Code for ${qrData}`;

                    qrTooltip.style.width = `${qrImage.width}px`;
                    qrTooltip.style.height = `${qrImage.height}px`;
                    qrTooltip.style.display = 'block';
                })
                .catch(error => {
                    console.error('Error fetching QR code:', error);
                });
        });
    });
});
