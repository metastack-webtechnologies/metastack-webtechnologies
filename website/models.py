from django.db import models
from django.utils.text import slugify # Import slugify

class Service(models.Model):
    """
    Represents a service offered by MetaStack Web Technologies.
    """
    title = models.CharField(max_length=100, help_text="Title of the service (e.g., 'Web Development')")
    slug = models.SlugField(max_length=100, unique=True, blank=True,
                            help_text="A URL-friendly version of the service title (auto-generated)")
    short_description = models.CharField(max_length=255, help_text="A brief summary of the service for cards/listings.")
    detailed_description = models.TextField(help_text="Detailed description of the service for its dedicated page.")
    image = models.ImageField(upload_to='services/', blank=True, null=True,
                              help_text="Image representing the service.")
    icon_class = models.CharField(max_length=50, blank=True, null=True,
                                  help_text="Font Awesome or other icon class (e.g., 'fas fa-cogs')")
    key_features = models.TextField(blank=True, null=True,
                                    help_text="List key features of the service, one per line (e.g., 'Custom Design', 'Responsive Layout')")
    order = models.IntegerField(default=0, help_text="Order in which services should appear")
    is_featured = models.BooleanField(default=False, help_text="Check to feature this service on the homepage or dedicated section.")

    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = "Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Technology(models.Model):
    """
    Represents a technology used in projects (e.g., Python, React, AWS).
    """
    name = models.CharField(max_length=50, unique=True, help_text="Name of the technology (e.g., 'Python', 'React')")
    icon_class = models.CharField(max_length=50, blank=True, null=True,
                                  help_text="Font Awesome or other icon class for the technology")

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name

class Project(models.Model):
    """
    Represents a project in the company's portfolio.
    """
    title = models.CharField(max_length=200, help_text="Title of the project")
    short_description = models.CharField(max_length=255, blank=True,
                                         help_text="A brief summary of the project")
    description = models.TextField(help_text="Detailed description of the project")
    technologies = models.ManyToManyField(Technology, related_name='projects',
                                          help_text="Technologies used in this project")
    project_url = models.URLField(max_length=200, blank=True, null=True,
                                  help_text="URL to the live project (optional)")
    image = models.ImageField(upload_to='projects/', blank=True, null=True,
                              help_text="Image representing the project")
    date_completed = models.DateField(blank=True, null=True,
                                      help_text="Date the project was completed")
    client_name = models.CharField(max_length=100, blank=True, null=True,
                                   help_text="Name of the client for this project (optional)")
    industry = models.CharField(max_length=100, blank=True, null=True,
                                 help_text="Industry of the client (e.g., 'Fintech', 'Healthcare') (optional)")
    key_features = models.TextField(blank=True, null=True,
                                     help_text="List key features, one per line (e.g., 'User Authentication', 'Payment Gateway Integration')")

    class Meta:
        ordering = ['-date_completed', 'title']
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    """
    Represents a message submitted through the website's contact form.
    """
    name = models.CharField(max_length=100, help_text="Name of the sender")
    email = models.EmailField(help_text="Email address of the sender")
    subject = models.CharField(max_length=200, blank=True, null=True,
                               help_text="Subject of the message")
    message = models.TextField(help_text="Content of the message")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Date and time the message was received")
    is_read = models.BooleanField(default=False, help_text="Indicates if the message has been read by an admin")

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class Tag(models.Model):
    """
    Represents a tag for blog posts.
    """
    name = models.CharField(max_length=50, unique=True, help_text="Name of the tag (e.g., 'Python', 'AI', 'Frontend')")
    slug = models.SlugField(max_length=50, unique=True, blank=True,
                            help_text="A URL-friendly version of the tag name (auto-generated)")

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Tags"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    """
    Represents a category for blog posts.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Name of the blog category (e.g., 'Web Development')")
    slug = models.SlugField(max_length=100, unique=True, blank=True,
                             help_text="A URL-friendly version of the category name (auto-generated)")

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    """
    Represents a blog post.
    """
    title = models.CharField(max_length=200, help_text="Title of the blog post")
    slug = models.SlugField(max_length=200, unique=True, blank=True,
                             help_text="A URL-friendly version of the title (auto-generated)")
    author = models.CharField(max_length=100, help_text="Author of the blog post")
    pub_date = models.DateTimeField(auto_now_add=True, help_text="Date and time the post was published")
    summary = models.CharField(max_length=300, help_text="A short summary of the blog post")
    content = models.TextField(help_text="Full content of the blog post (can include HTML)")
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True,
                                        help_text="Featured image for the blog post")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='blogposts', help_text="Category of the blog post")
    tags = models.ManyToManyField('Tag', blank=True, related_name='blogposts', help_text="Tags associated with this blog post.")
    is_published = models.BooleanField(default=True, help_text="Check to publish the blog post")

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "Blog Posts"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    Represents a comment left on a blog post.
    """
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments',
                                  help_text="The blog post this comment belongs to.")
    author_name = models.CharField(max_length=100, help_text="Name of the person leaving the comment.")
    author_email = models.EmailField(blank=True, null=True, help_text="Email of the person leaving the comment (optional).")
    comment_text = models.TextField(help_text="The content of the comment.")
    pub_date = models.DateTimeField(auto_now_add=True, help_text="Date and time the comment was published.")
    is_approved = models.BooleanField(default=False, help_text="Whether the comment has been approved for display.")

    class Meta:
        ordering = ['pub_date']
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.author_name} on {self.blog_post.title[:30]}..."

class Testimonial(models.Model):
    """
    Represents a client testimonial.
    """
    client_name = models.CharField(max_length=100, help_text="Name of the client giving the testimonial")
    role = models.CharField(max_length=100, blank=True, null=True,
                            help_text="Role or title of the client (optional)")
    company_name = models.CharField(max_length=100, blank=True, null=True,
                                     help_text="Company name of the client (optional)")
    quote = models.TextField(help_text="The actual testimonial quote from the client")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)],
                                  help_text="Star rating (1-5)")
    is_approved = models.BooleanField(default=False,
                                       help_text="Check to display this testimonial on the website")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"Testimonial from {self.client_name}"

class TeamMember(models.Model):
    """
    Represents a team member of MetaStack Web Technologies.
    """
    name = models.CharField(max_length=100, help_text="Full name of the team member")
    role = models.CharField(max_length=100, help_text="Role or title of the team member (e.g., 'CEO', 'Lead Developer')")
    bio = models.TextField(blank=True, null=True, help_text="A short biography or description of the team member's expertise.")
    profile_picture = models.ImageField(upload_to='team_members/', blank=True, null=True,
                                         help_text="Profile picture of the team member")
    linkedin_url = models.URLField(max_length=200, blank=True, null=True,
                                    help_text="LinkedIn profile URL (optional)")
    twitter_url = models.URLField(max_length=200, blank=True, null=True,
                                   help_text="Twitter profile URL (optional)")
    github_url = models.URLField(max_length=200, blank=True, null=True,
                                  help_text="GitHub profile URL (optional)")
    order = models.IntegerField(default=0, help_text="Order in which team members should appear (lower number first)")

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.role}"

class NewsletterSubscriber(models.Model): # THIS IS THE NEW MODEL
    """
    Represents a subscriber to the website's newsletter.
    """
    email = models.EmailField(unique=True, help_text="The subscriber's email address.")
    date_subscribed = models.DateTimeField(auto_now_add=True, help_text="Date and time of subscription.")

    class Meta:
        ordering = ['-date_subscribed']
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email