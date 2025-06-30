# website/context_processors.py

from django.conf import settings

def company_details(request):
    """
    Context processor to make company details (like logo URL)
    available globally in all templates.
    """
    return {
        # Constructs the URL for the company logo using STATIC_URL.
        # Assumes the logo is located at `your_project_root/static/images/company_logo.png`
        'COMPANY_LOGO_URL': settings.STATIC_URL + 'images/company_logo.png',
        'company_name': 'MetaStack Web Technologies', # Example company name, adjust as needed
        # You can add other global company-wide details here, e.g., 'COMPANY_ADDRESS', 'COMPANY_PHONE'
    }
