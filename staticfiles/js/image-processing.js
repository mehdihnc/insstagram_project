class ImageProcessor {
    constructor(maxWidth = 1080, maxHeight = 1080, maxSizeMB = 5) {
        this.maxWidth = maxWidth;
        this.maxHeight = maxHeight;
        this.maxSizeBytes = maxSizeMB * 1024 * 1024;
    }

    async processImage(file) {
        if (!file.type.startsWith('image/')) {
            throw new Error('Le fichier doit être une image');
        }

        const img = await this.createImage(file);
        let { width, height } = this.calculateDimensions(img);

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        let quality = 0.9;
        let blob = await this.canvasToBlob(canvas, file.type, quality);

        // Réduire la qualité si nécessaire pour atteindre la taille maximale
        while (blob.size > this.maxSizeBytes && quality > 0.1) {
            quality -= 0.1;
            blob = await this.canvasToBlob(canvas, file.type, quality);
        }

        return blob;
    }

    createImage(file) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = URL.createObjectURL(file);
        });
    }

    calculateDimensions(img) {
        let { width, height } = img;
        if (width > this.maxWidth || height > this.maxHeight) {
            const ratio = Math.min(this.maxWidth / width, this.maxHeight / height);
            width *= ratio;
            height *= ratio;
        }
        return { width, height };
    }

    canvasToBlob(canvas, type, quality) {
        return new Promise(resolve => {
            canvas.toBlob(blob => resolve(blob), type, quality);
        });
    }
}

// Utilisation dans le formulaire
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('post-form');
    const imageProcessor = new ImageProcessor();

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const fileInput = form.querySelector('input[type="file"]');
        const file = fileInput.files[0];

        if (file) {
            try {
                const processedImage = await imageProcessor.processImage(file);
                
                // Créer un nouveau FileList avec l'image traitée
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(new File([processedImage], file.name, {
                    type: file.type
                }));
                fileInput.files = dataTransfer.files;
                
                // Soumettre le formulaire
                form.submit();
            } catch (error) {
                console.error('Erreur lors du traitement de l\'image:', error);
                alert('Erreur lors du traitement de l\'image. Veuillez réessayer.');
            }
        } else {
            form.submit();
        }
    });
}); 