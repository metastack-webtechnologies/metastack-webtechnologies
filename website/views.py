
from django.shortcuts import render
from .models import Service, Project, Technology

def homepage(request):
    """
    Renders the homepage of the website, fetching data from models.
    """
    services = Service.objects.all() # Fetch all services
    projects = Project.objects.all() # Fetch all projects

    context = {
        'company_name': 'MetaStack Web Technologies',
        'services': services,
        'projects': projects,
    }
    return render(request, 'website/homepage.html', context)

def about_us(request):
    """
    Renders the About Us page.
    """
    context = {
        'company_name': 'MetaStack Web Technologies',
    }
    return render(request, 'website/about.html', context)

def contact_page(request):
    """
    Renders the Contact Us page with a form.
    """
    context = {
        'company_name': 'MetaStack Web Technologies',
    }
    return render(request, 'website/contact.html', context)

def portfolio_detail(request):
    """
    Renders a generic portfolio detail page.
    (Later, this will be modified to accept a project ID for dynamic content)
    """
    context = {
        'company_name': 'MetaStack Web Technologies',
    }
    return render(request, 'website/portfolio_detail.html', context)