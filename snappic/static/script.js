document.addEventListener('DOMContentLoaded', () => {
    // Service Worker registration
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js')
            .then(() => console.log('Service Worker registered'))
            .catch(err => console.error('Service Worker registration failed', err));
    }

    // Upload form handling
    const form = document.getElementById('upload-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('file-input');
            const comment = document.getElementById('comment').value;
            const file = fileInput.files[0];
            if (!file) return;
            const formData = new FormData();
            formData.append('file', file);
            formData.append('comment', comment);
            const loading = document.getElementById('loading');
            loading.style.display = 'block';
            try {
                const response = await fetch('/upload', { method: 'POST', body: formData });
                const data = await response.json();
                if (data.success) {
                    alert('Upload successful!');
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            } catch (err) {
                alert('Upload failed: ' + err.message);
            }
            loading.style.display = 'none';
        });
    }

    // Gallery update
    const galleryContainer = document.getElementById('gallery-container');
    if (galleryContainer) {
        const updateGallery = async () => {
            try {
                const response = await fetch('/api/images');
                const images = await response.json();
                const currentIds = new Set(images.map(img => img.filename));

                // Remove missing items
                Array.from(galleryContainer.children).forEach(child => {
                    if (!currentIds.has(child.id)) {
                        galleryContainer.removeChild(child);
                    }
                });

                // Add or update items
                images.forEach(img => {
                    let item = document.getElementById(img.filename);
                    if (!item) {
                        item = document.createElement('div');
                        item.classList.add('image-item');
                        item.id = img.filename;
                        const image = document.createElement('img');
                        image.src = `/uploads/${img.filename}`;
                        image.alt = img.comment;
                        const p = document.createElement('p');
                        p.textContent = img.comment;
                        item.appendChild(image);
                        item.appendChild(p);
                        galleryContainer.appendChild(item);
                    }
                    // Update opacity
                    const age = img.age;
                    if (age < 5) {
                        item.style.opacity = 1;
                    } else {
                        const fadeProgress = (age - 5) / 10;
                        item.style.opacity = Math.max(0, 1 - fadeProgress);
                    }
                });
            } catch (err) {
                console.error('Failed to update gallery', err);
            }
        };
        updateGallery();
        setInterval(updateGallery, 2000);
    }
});
