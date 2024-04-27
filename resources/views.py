from django.shortcuts import render, redirect
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import *
import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def index(request):
    domains = Domain.objects.all().order_by('name')
    return render(request, 'resources/resources.html', {'domains': domains})

def category_page(request, resource_path):
    return render(request, 'resources/category.html')

@login_required
def file_page(request, resource_path, category):
    # Fetch all resources
    resources = Resource.objects.filter(category=category)
    
    # Filter resources based on the modified domain names
    converted_resource_paths = [convert_to_lower_and_hyphen(resource.domain.name) for resource in resources]
    filtered_resources = [resource for resource, path in zip(resources, converted_resource_paths) if path == resource_path]
    

    user_resources = UserResource.objects.filter(user=request.user, resource__in=filtered_resources)
    saved_resource_ids = [user_resource.resource.uuid for user_resource in user_resources if user_resource.saved]

    context = {
        'resource_path': resource_path,
        'category': category,
        'resources' : filtered_resources,
        'saved_resource_ids': saved_resource_ids,  # Pass the IDs of saved resources to the template
    }
    return render(request, 'resources/files.html', context)

def convert_to_lower_and_hyphen(domain_name):
    return domain_name.strip().replace(' ', '-').lower()

def download_resource(request, resource_uuid):
    resource = get_object_or_404(Resource, uuid=resource_uuid)
    file_path = resource.file.path  # Assuming your resource model has a 'file' field
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@login_required
def save_resource(request, resource_uuid):
    resource = get_object_or_404(Resource, uuid=resource_uuid)
    user_resource, created = UserResource.objects.get_or_create(user=request.user, resource=resource)
    if not created:
        user_resource.saved = True
        user_resource.save()
        # You might want to add a success message here
    # Redirect to appropriate page after saving
    return redirect('resources:file_page',resource_path = convert_to_lower_and_hyphen(resource.domain.name), category = resource.category)

@login_required
def unsave_resource(request, resource_uuid):
    resource = get_object_or_404(Resource, uuid=resource_uuid)
    user_resource = get_object_or_404(UserResource, user=request.user, resource=resource)
    user_resource.saved = False  # Set saved field to False
    user_resource.save()
    # You might want to add a success message here
    # Redirect to appropriate page after unsaving
    return redirect('resources:file_page',resource_path = convert_to_lower_and_hyphen(resource.domain.name), category = resource.category)