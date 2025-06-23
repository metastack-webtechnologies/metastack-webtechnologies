from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# Import all necessary models, including Comment
from .models import Service, Project, ContactMessage, BlogPost, Category, Testimonial, TeamMember, Technology, Tag, Comment, NewsletterSubscriber
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.http import require_POST # Import require_POST decorator

def homepage(request):
    """
    Renders the homepage of the website, fetching data from models,
    with added filtering for projects based on technology or industry.
    """
    services = Service.objects.all()

    projects = Project.objects.all()

    filter_technology_slug = request.GET.get('technology')
    filter_industry = request.GET.get('industry')

    if filter_technology_slug:
        projects = projects.filter(technologies__slug=filter_technology_slug).distinct()
    if filter_industry:
        projects = projects.filter(industry__iexact=filter_industry).distinct()

    all_technologies = Technology.objects.all()

    all_industries = Project.objects.exclude(industry__isnull=True).exclude(industry__exact='').values_list('industry', flat=True).distinct().order_by('industry')

    testimonials = Testimonial.objects.filter(is_approved=True)

    context = {
        'company_name': 'MetaStack Web Technologies',
        'services': services,
        'projects': projects,
        'testimonials': testimonials,
        'all_technologies': all_technologies,
        'all_industries': all_industries,
        'current_technology': filter_technology_slug,
        'current_industry': filter_industry,
    }
    return render(request, 'website/homepage.html', context)

def service_detail(request, slug):
    """
    Renders the detail page for a specific service.
    Fetches the service object based on its slug.
    Processes key features for display.
    """
    service = get_object_or_404(Service, slug=slug)

    # Process key features from the TextField (one per line)
    processed_key_features = []
    if service.key_features:
        for line in service.key_features.splitlines():
            stripped_line = line.strip()
            if stripped_line: # Only add non-empty lines
                processed_key_features.append(stripped_line)

    context = {
        'company_name': 'MetaStack Web Technologies',
        'service': service,
        'processed_key_features': processed_key_features,
    }
    return render(request, 'website/service_detail.html', context)

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
    Handles displaying and submitting the contact form.
    """
    context = {
        'company_name': 'MetaStack Web Technologies',
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', '')
        message_content = request.POST.get('message')

        if not name or not email or not message_content:
            messages.error(request, 'Please fill in all required fields (Name, Email, Message).')
            return render(request, 'website/contact.html', context)

        try:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_content
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect(reverse('contact'))
        except Exception as e:
            messages.error(request, f'An error occurred while sending your message: {e}')
            return render(request, 'website/contact.html', context)

    return render(request, 'website/contact.html', context)

def portfolio_detail(request, pk):
    """
    Renders the portfolio detail page for a specific project.
    Args:
        request: HttpRequest object.
        pk (int): Primary key of the Project to display.
    """
    project = get_object_or_404(Project, pk=pk)

    processed_key_features = []
    if project.key_features:
        for line in project.key_features.splitlines():
            stripped_line = line.strip()
            if stripped_line:
                processed_key_features.append(stripped_line)

    context = {
        'company_name': 'MetaStack Web Technologies',
        'project': project,
        'processed_key_features': processed_key_features,
    }
    return render(request, 'website/portfolio_detail.html', context)

def blog_list(request):
    """
    Displays a list of all published blog posts, with pagination, search, category, and tag filtering.
    """
    all_posts = BlogPost.objects.filter(is_published=True)
    categories = Category.objects.all()
    all_tags = Tag.objects.all()
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')

    if query:
        all_posts = all_posts.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    if category_slug:
        all_posts = all_posts.filter(category__slug=category_slug)
        selected_category = get_object_or_404(Category, slug=category_slug)
    else:
        selected_category = None

    if tag_slug:
        all_posts = all_posts.filter(tags__slug=tag_slug).distinct()
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
    else:
        selected_tag = None

    all_posts = all_posts.order_by('-pub_date')


    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page')
    try:
        blog_posts = paginator.page(page_number)
    except PageNotAnInteger:
        blog_posts = paginator.page(1)
    except EmptyPage:
        blog_posts = paginator.page(paginator.num_pages)

    context = {
        'company_name': 'MetaStack Web Technologies',
        'blog_posts': blog_posts,
        'categories': categories,
        'all_tags': all_tags,
        'query': query,
        'selected_category': selected_category,
        'selected_tag': selected_tag,
    }
    return render(request, 'website/blog_list.html', context)

def blog_detail(request, slug):
    """
    Displays the full content of a single blog post.
    Handles comment submission and fetches approved comments.
    Fetches recent posts and next/previous posts.
    """
    blog_post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(pk=blog_post.pk).order_by('-pub_date')[:5]
    categories = Category.objects.all()
    all_tags = Tag.objects.all()

    # Handle comment submission (POST request)
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        author_email = request.POST.get('author_email')
        comment_text = request.POST.get('comment_text')

        if not author_name or not comment_text:
            messages.error(request, "Name and comment cannot be empty.")
        else:
            try:
                Comment.objects.create(
                    blog_post=blog_post,
                    author_name=author_name,
                    author_email=author_email,
                    comment_text=comment_text,
                    is_approved=False # Comments need to be approved by default
                )
                messages.success(request, "Your comment has been submitted for moderation. Thank you!")
                # Redirect to the same blog post to prevent re-submission on refresh
                return redirect('blog_detail', slug=slug)
            except Exception as e:
                messages.error(request, f"An error occurred while submitting your comment: {e}")

    # Fetch approved comments for this blog post
    approved_comments = blog_post.comments.filter(is_approved=True).order_by('pub_date')

    next_post = BlogPost.objects.filter(is_published=True, pub_date__gt=blog_post.pub_date).order_by('pub_date').first()
    previous_post = BlogPost.objects.filter(is_published=True, pub_date__lt=blog_post.pub_date).order_by('-pub_date').first()

    context = {
        'company_name': 'MetaStack Web Technologies',
        'blog_post': blog_post,
        'recent_posts': recent_posts,
        'categories': categories,
        'all_tags': all_tags,
        'next_post': next_post,
        'previous_post': previous_post,
        'approved_comments': approved_comments, # Pass approved comments to the template
    }
    return render(request, 'website/blog_detail.html', context)

def our_team(request):
    """
    Renders the 'Our Team' page, fetching all team members.
    """
    team_members = TeamMember.objects.all()
    context = {
        'company_name': 'MetaStack Web Technologies',
        'team_members': team_members,
    }
    return render(request, 'website/team.html', context)

@require_POST
def newsletter_subscribe(request):
    """
    Handles newsletter subscription form submission.
    """
    email = request.POST.get('email')

    if not email:
        messages.error(request, "Please provide an email address to subscribe.")
    else:
        try:
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.info(request, "This email is already subscribed to our newsletter.")
            else:
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Successfully subscribed to our newsletter! Thank you.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    # Redirect back to the page where the form was submitted, or homepage as a fallback
    return redirect(request.META.get('HTTP_REFERER', reverse('homepage'))) # Use HTTP_REFERER to redirect back to originating page
