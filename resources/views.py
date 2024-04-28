from django.shortcuts import render, redirect
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

from django.shortcuts import render
from .models import UserResource, Domain

@login_required(login_url='accounts:login')
def index(request):
    
    resources = Resource.objects.all()
    user_resources = UserResource.objects.filter(user=request.user)
    saved_resource_ids = [user_resource.resource.uuid for user_resource in user_resources if user_resource.saved]
    domains = Domain.objects.all().order_by('name')
    context = {
        'resources': resources,
        'saved_resource_ids': saved_resource_ids,  # Pass the IDs of saved resources to the template
        'domains': domains
    }
    
    return render(request, 'resources/resources.html', context)


def category_page(request, resource_path):
    resources = Resource.objects.all()
    user_resources = UserResource.objects.filter(user=request.user)
    saved_resource_ids = [user_resource.resource.uuid for user_resource in user_resources if user_resource.saved]
    domains = Domain.objects.all().order_by('name')
    context = {
        'resources': resources,
        'saved_resource_ids': saved_resource_ids,  # Pass the IDs of saved resources to the template
        'domains': domains
    }
    return render(request, 'resources/category.html', context)


def file_page(request, resource_path, category):
    # Fetch all resources
    resources = Resource.objects.filter(category=category)
    
    # Filter resources based on the modified domain names
    converted_resource_paths = [convert_to_lower_and_hyphen(resource.domain.name) for resource in resources]
    filtered_resources = [resource for resource, path in zip(resources, converted_resource_paths) if path == resource_path]
    

    user_resources = UserResource.objects.filter(user=request.user, resource__in=filtered_resources)
    saved_resource_ids = [user_resource.resource.uuid for user_resource in user_resources if user_resource.saved]

    resources_all = Resource.objects.all()
    user_resources_all = UserResource.objects.filter(user=request.user)
    saved_resource_ids_all = [user_resource.resource.uuid for user_resource in user_resources_all if user_resource.saved]
    domains = Domain.objects.all().order_by('name')

    context = {
        'resource_path': resource_path,
        'category': category,
        'resources' : filtered_resources,
        'saved_resource_ids': saved_resource_ids,  # Pass the IDs of saved resources to the template

        'resources_all': resources_all,
        'saved_resource_ids_all': saved_resource_ids_all,  # Pass the IDs of saved resources to the template
        'domains': domains
    }
    return render(request, 'resources/files.html', context)


def convert_to_lower_and_hyphen(domain_name):
    return domain_name.strip().replace(' ', '-').lower()


def download_resource(request, resource_uuid):
    resource = get_object_or_404(Resource, uuid=resource_uuid)
    file_path = resource.file.path  # Assuming your resource model has a 'file' field
    return FileResponse(open(file_path, 'rb'), as_attachment=True)


def save_resource(request, resource_uuid):
    resource = get_object_or_404(Resource, uuid=resource_uuid)
    user_resource, created = UserResource.objects.get_or_create(user=request.user, resource=resource)
    if not created:
        user_resource.saved = True
        user_resource.save()
        # You might want to add a success message here
    # Redirect to appropriate page after saving
    return redirect('resources:file_page',resource_path = convert_to_lower_and_hyphen(resource.domain.name), category = resource.category)


def unsave_resource(request, resource_uuid):
    resource = get_object_or_404(Resource, uuid=resource_uuid)
    user_resource = get_object_or_404(UserResource, user=request.user, resource=resource)
    user_resource.saved = False  # Set saved field to False
    user_resource.save()
    # You might want to add a success message here
    # Redirect to appropriate page after unsaving
    return redirect('resources:file_page',resource_path = convert_to_lower_and_hyphen(resource.domain.name), category = resource.category)


def res_form(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            resource = form.save(commit=False)
            resource.uploader = request.user  # Set the uploader to the current user
            
            # Reverse search the domain UUID based on its name
            domain_name = form.cleaned_data.get('domain')  # Assuming the form field is named 'domain'
            try:
                domain = Domain.objects.get(name=domain_name)
                resource.domain = domain
            except ObjectDoesNotExist:
                # Handle case where domain does not exist
                pass
            
            resource.save()
            # Redirect to a success page or any other page as needed
            return redirect('resources:index')
    else:
        form = ResourceForm()
    return render(request, 'resources/res_form.html', {'form': form})