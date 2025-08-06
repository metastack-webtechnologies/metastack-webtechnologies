from django.shortcuts import render

def clinic_landing_page(request):
    """
    This view renders the main Clinic App Link page.
    """
    return render(request, 'clinic/Clinic_App_Link.html')

def clinic_guide_page(request):
    """
    This view renders the interactive Clinic Guide page.
    """
    return render(request, 'clinic/Clinic.html')
