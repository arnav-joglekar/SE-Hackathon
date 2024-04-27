from django.shortcuts import render, redirect
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import *
import os

# Create your views here.

def index(request):
    domains = Domain.objects.all().order_by('name')
    return render(request, 'resources/resources.html', {'domains': domains})

def category_page(request, resource_path):
    return render(request, 'resources/category.html')

def file_page(request, resource_path, category):
    # Fetch all resources
    resources = Resource.objects.filter(category=category)
    
    # Filter resources based on the modified domain names
    converted_resource_paths = [convert_to_lower_and_hyphen(resource.domain.name) for resource in resources]
    filtered_resources = [resource for resource, path in zip(resources, converted_resource_paths) if path == resource_path]
    
    context = {
        'resource_path': resource_path,
        'category': category,
        'resources' : filtered_resources,
    }
    return render(request, 'resources/files.html', context)

def convert_to_lower_and_hyphen(domain_name):
    return domain_name.strip().replace(' ', '-').lower()

def download_resource(request, resource_uuid):
    resource = get_object_or_404(Resource, uuid=resource_uuid)
    file_path = resource.file.path  # Assuming your resource model has a 'file' field
    return FileResponse(open(file_path, 'rb'), as_attachment=True)