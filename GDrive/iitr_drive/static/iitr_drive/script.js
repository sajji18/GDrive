document.addEventListener('DOMContentLoaded', function() {
    const qrTriggers = document.querySelectorAll('.qr-trigger');
    const qrTooltip = document.querySelector('.qr-tooltip');

    qrTriggers.forEach(qrTrigger => {
        qrTrigger.addEventListener('mouseenter', function() {
            // Get the data-qrdata attribute containing the file URL
            const qrData = qrTrigger.getAttribute('data-qrdata');
            const file_id = qrTrigger.getAttribute('data-fileid'); // Add this line

            // Make an AJAX request to fetch the QR code image data
            fetch(`/generate_qr_code/${file_id}/`)
                .then(response => response.json())
                .then(data => {
                    // Create an image element with the QR code
                    const qrImage = document.createElement('img');
                    qrImage.src = `data:image/png;base64,${data.qr_image_base64}`;
                    qrImage.alt = `QR Code for ${qrData}`;

                    // Clear the tooltip and add the QR code image
                    qrTooltip.innerHTML = '';
                    qrTooltip.appendChild(qrImage);
                })
                .catch(error => {
                    console.error('Error fetching QR code:', error);
                });
        });

        qrTrigger.addEventListener('mouseleave', function() {
            // Hide the tooltip when the mouse leaves the link
            qrTooltip.style.display = 'none';
        });
    });
});
