from django.shortcuts import render
from .forms import HideDataForm, RevealDataForm
from .steganography import hide_data_in_image, reveal_data_from_image  # Assuming you implement these.
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def home(request):
    return render(request, 'home.html')

def hide_data(request):
    if request.method == 'POST':
        form = HideDataForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            message = form.cleaned_data['message']

            # Generate new image with hidden data
            new_image_content = hide_data_in_image(image, message)
            
            # Create a response with the new image as a downloadable file
            response = HttpResponse(new_image_content, content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="hidden_message.png"'
            return response
    else:
        form = HideDataForm()
    return render(request, 'hide_data.html', {'form': form})

def reveal_data(request):
    if request.method == 'POST':
        form = RevealDataForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            message = reveal_data_from_image(image)
            return render(request, 'reveal_data.html', {'message': message})
    else:
        form = RevealDataForm()
    return render(request, 'reveal_data.html', {'form': form})
