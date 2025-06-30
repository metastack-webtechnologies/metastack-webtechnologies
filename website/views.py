# website/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# Import all necessary models
from .models import Service, Project, ContactMessage, BlogPost, Category, Testimonial, TeamMember, Technology, Tag, Comment, NewsletterSubscriber
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count # Import Count for related_name aggregation
import json # Import json module - needed for manual serialization if not using json_script directly on values()
from django.views.decorators.http import require_POST # MODIFICATION: Added import for require_POST

# --- Main Page Views ---

def homepage(request):
    """
    Renders the homepage, fetching featured content and handling filtering for projects.
    Includes serialization of services for JavaScript usage.
    """
    # Retrieve all services, ordered by pk to ensure consistent order for JS navigation
    # MODIFICATION: Manually serialize the queryset to a list of dictionaries for JSON serialization
    services_queryset = Service.objects.all().order_by('pk') 
    
    services_data = []
    for service in services_queryset:
        services_data.append({
            'pk': service.pk,
            'fields': { # Mimic Django's default serializer structure
                'title': service.title,
                'slug': service.slug,
                'short_description': service.short_description,
                'icon_class': service.icon_class,
                # Add any other service fields needed by your JavaScript here
            }
        })

    # Retrieve projects, optionally filtered by technology or industry
    current_technology_slug = request.GET.get('technology')
    current_industry = request.GET.get('industry')

    projects_queryset = Project.objects.all()

    if current_technology_slug:
        projects_queryset = projects_queryset.filter(technologies__slug=current_technology_slug)
    
    if current_industry:
        # Ensure 'industry' field exists and is not null/empty before filtering
        projects_queryset = projects_queryset.filter(industry=current_industry)

    # Order projects to ensure consistent display - MODIFICATION: Changed 'date_added' to 'date_completed'
    projects_queryset = projects_queryset.order_by('-date_completed') # Or '-id' if no date_completed exists/desired

    # Get all unique technologies and industries for filters
    # Filter technologies to only show those associated with at least one project
    # MODIFICATION: Changed Count('project') to Count('projects') as per error message
    all_technologies = Technology.objects.annotate(num_projects=Count('projects')).filter(num_projects__gt=0).order_by('name')
    # Exclude null or empty industries
    all_industries = Project.objects.exclude(industry__isnull=True).exclude(industry__exact='').values_list('industry', flat=True).distinct().order_by('industry')
    
    # Retrieve testimonials - MODIFICATION: Changed 'created_at' to 'date_created'
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-date_created')[:3] # Get latest 3 approved testimonials

    context = {
        'company_name': 'MetaStack Web Technologies', # Ensure company_name is always in context
        'services': services_data, # MODIFICATION: Pass the serialized list of dictionaries
        'projects': projects_queryset,
        'testimonials': testimonials,
        'all_technologies': all_technologies,
        'all_industries': all_industries,
        'current_technology': current_technology_slug, # Pass current filter values
        'current_industry': current_industry,           # Pass current filter values
    }
    return render(request, 'website/homepage.html', context)

def about(request):
    """
    Renders the About Us page.
    """
    team_members = TeamMember.objects.all()
    context = {
        'company_name': 'MetaStack Web Technologies',
        'team_members': team_members,
    }
    return render(request, 'website/about.html', context)

def contact(request):
    """
    Handles displaying and submitting the contact form.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', '')
        message_content = request.POST.get('message')

        if not name or not email or not message_content:
            messages.error(request, 'Please fill in all required fields (Name, Email, Message).')
        else:
            try:
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message_content
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact')
            except Exception as e:
                messages.error(request, f'An error occurred while sending your message: {e}')
    
    context = {
        'company_name': 'MetaStack Web Technologies',
    }
    return render(request, 'website/contact.html', context)

# --- Services Views ---

def services(request):
    """
    Displays a list of all available services.
    """
    all_services = Service.objects.all()
    context = {
        'services': all_services,
        'company_name': "MetaStack Web Technologies",
    }
    # FIX: Changed 'services.html' to 'services_list.html'
    return render(request, 'website/services_list.html', context)

def service_detail(request, slug):
    """
    Renders the detail page for a specific service.
    """
    service = get_object_or_404(Service, slug=slug)
    processed_key_features = [line.strip() for line in service.key_features.splitlines() if line.strip()]
    context = {
        'company_name': 'MetaStack Web Technologies',
        'service': service,
        'processed_key_features': processed_key_features,
    }
    return render(request, 'website/service_detail.html', context)

# --- Portfolio Views ---

def portfolio(request):
    """
    Displays the portfolio grid page.
    """
    projects = Project.objects.all()
    context = {
        'company_name': 'MetaStack Web Technologies',
        'projects': projects,
    }
    return render(request, 'website/portfolio.html', context)

def portfolio_detail(request, pk):
    """
    Renders the portfolio detail page for a specific project.
    """
    project = get_object_or_404(Project, pk=pk)
    processed_key_features = [line.strip() for line in project.key_features.splitlines() if line.strip()]
    context = {
        'company_name': 'MetaStack Web Technologies',
        'project': project,
        'processed_key_features': processed_key_features,
    }
    return render(request, 'website/portfolio_detail.html', context)

# --- Blog Views ---

def blog_list(request):
    """
    Displays a list of all published blog posts with pagination and filtering.
    """
    all_posts = BlogPost.objects.filter(is_published=True).order_by('-pub_date')
    query = request.GET.get('q')

    if query:
        all_posts = all_posts.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        ).distinct()

    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page')
    blog_posts = paginator.get_page(page_number)

    context = {
        'company_name': 'MetaStack Web Technologies',
        'blog_posts': blog_posts,
        'categories': Category.objects.all(),
        'all_tags': Tag.objects.all(),
    }
    return render(request, 'website/blog_list.html', context)

def blog_detail(request, slug):
    """
    Displays a single blog post and handles comments.
    """
    blog_post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        comment_text = request.POST.get('comment_text')
        if author_name and comment_text:
            Comment.objects.create(
                blog_post=blog_post,
                author_name=author_name,
                comment_text=comment_text,
            )
            messages.success(request, "Your comment has been submitted for moderation.")
            return redirect('blog_detail', slug=slug)
        else:
            messages.error(request, "Name and comment cannot be empty.")

    context = {
        'company_name': 'MetaStack Web Technologies',
        'blog_post': blog_post,
        'approved_comments': blog_post.comments.filter(is_approved=True).order_by('pub_date'),
        'recent_posts': BlogPost.objects.filter(is_published=True).exclude(pk=blog_post.pk).order_by('-pub_date')[:5],
        'categories': Category.objects.all(),
        'all_tags': Tag.objects.all(),
    }
    return render(request, 'website/blog_detail.html', context)

# --- Other Views ---

def team(request):
    """
    Renders the 'Our Team' page.
    """
    team_members = TeamMember.objects.all()
    context = {
        'company_name': 'MetaStack Web Technologies',
        'team_members': team_members,
    }
    return render(request, 'website/team.html', context)

@require_POST
def subscribe_newsletter(request):
    """
    Handles newsletter subscription form submission.
    """
    email = request.POST.get('email')
    if email:
        if not NewsletterSubscriber.objects.filter(email=email).exists():
            NewsletterSubscriber.objects.create(email=email)
        else:
            messages.info(request, "This email is already subscribed.")
    else:
        messages.error(request, "Please provide an email address.")
    
    return redirect(request.META.get('HTTP_REFERER', 'homepage'))
