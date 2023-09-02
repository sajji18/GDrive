// QR Code Rendering script in JS 

document.addEventListener('DOMContentLoaded', function() {
    const qrTriggers = document.querySelectorAll('.qr-trigger');
    const qrTooltip = document.querySelector('.qr-tooltip');
    const qrImage = document.getElementById('qr-image'); 

    qrTriggers.forEach(qrTrigger => {
        qrTrigger.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default behavior of the link
            // Get the data-qrdata attribute containing the file URL
            const qrData = qrTrigger.getAttribute('data-qrdata');
            const file_id = qrTrigger.getAttribute('data-fileid');

            // Make an AJAX request to fetch the QR code image data
            fetch(`/generate_qr_code/${file_id}/`)
                .then(response => response.blob()) // Change response type to blob
                .then(blob => {
                    // Create an object URL from the blob
                    const objectURL = URL.createObjectURL(blob);
                    
                    // Set the src attribute of the img element
                    qrImage.src = objectURL;
                    qrImage.alt = `QR Code for ${qrData}`;

                    // Adjust the dimensions of the tooltip div
                    qrTooltip.style.width = `${qrImage.width}px`;
                    qrTooltip.style.height = `${qrImage.height}px`;

                    // Show the tooltip
                    qrTooltip.style.display = 'block';
                })
                .catch(error => {
                    console.error('Error fetching QR code:', error);
                });
        });
    });
});
