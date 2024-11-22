from django import forms
from .models import Post
from PIL import Image
import io

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Écrivez une légende... (utilisez # pour les hashtags)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Vérifier le format
            if not image.content_type.startswith('image'):
                raise forms.ValidationError('Le fichier doit être une image.')
            
            # Vérifier la taille
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('L\'image ne doit pas dépasser 5MB.')
            
            # Redimensionner l'image si nécessaire
            img = Image.open(image)
            if img.height > 1080 or img.width > 1080:
                output_size = (1080, 1080)
                img.thumbnail(output_size)
                # Sauvegarder l'image redimensionnée
                output = io.BytesIO()
                img.save(output, format=img.format)
                output.seek(0)
                image = output
            
            return image 