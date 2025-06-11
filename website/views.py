# website/views.py (Initial view for the homepage)

from django.shortcuts import render

def homepage(request):
    """
    Renders the homepage of the website.
    """
    return render(request, 'website/homepage.html', {'company_name': 'MetaStack Web Technologies'})