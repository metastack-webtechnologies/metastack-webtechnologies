
from django.db import models

class Service(models.Model):
    """
    Represents a service offered by MetaStack Web Technologies.
    """
    title = models.CharField(max_length=100, help_text="Title of the service (e.g., 'Web Development')")
    description = models.TextField(help_text="Detailed description of the service")
    icon_class = models.CharField(max_length=50, blank=True, null=True,
                                help_text="Font Awesome or other icon class (e.g., 'fas fa-code')")
    order = models.IntegerField(default=0, help_text="Order in which services should appear")

    class Meta:
        ordering = ['order', 'title'] # Order services by 'order' then 'title'
        verbose_name_plural = "Services" # Correct plural name in Django Admin

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

    class Meta:
        ordering = ['-date_completed', 'title'] # Order by most recent completion date
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
        ordering = ['-timestamp'] # Order by most recent message first
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} ({self.email})"