from django.contrib import admin
from .models import Service, Technology, Project, ContactMessage, Category, BlogPost, Testimonial, TeamMember, Tag, Comment, NewsletterSubscriber # Import NewsletterSubscriber

# Custom Admin for Service to display new fields and auto-generate slug
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'icon_class', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description', 'detailed_description')
    list_filter = ('order', 'is_featured')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description', 'detailed_description', 'image', 'icon_class', 'order', 'key_features', 'is_featured')
        }),
    )
    actions = ['make_featured', 'make_unfeatured']

    @admin.action(description='Mark selected services as featured')
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} services were successfully marked as featured.")

    @admin.action(description='Mark selected services as unfeatured')
    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} services were successfully marked as unfeatured.")


# Custom Admin for Project to display more fields
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'industry', 'date_completed', 'project_url')
    list_filter = ('date_completed', 'technologies', 'industry')
    search_fields = ('title', 'short_description', 'description', 'client_name', 'industry')
    filter_horizontal = ('technologies',)

    fieldsets = (
        (None, {
            'fields': ('title', 'short_description', 'description', 'image', 'date_completed')
        }),
        ('Client & Industry', {
            'fields': ('client_name', 'industry')
        }),
        ('Project Details', {
            'fields': ('technologies', 'project_url', 'key_features')
        }),
    )

# Custom Admin for Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


# Custom Admin for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# Custom Admin for BlogPost
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'pub_date', 'is_published')
    list_filter = ('category', 'is_published', 'pub_date', 'tags')
    search_fields = ('title', 'content', 'summary', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'pub_date'
    actions = ['make_published', 'make_unpublished']

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'tags', 'featured_image', 'summary', 'content')
        }),
        ('Publication Information', {
            'fields': ('is_published',),
            'classes': ('collapse',)
        }),
    )

    @admin.action(description='Mark selected blog posts as published')
    def make_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} blog posts were successfully marked as published.")

    @admin.action(description='Mark selected blog posts as unpublished')
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} blog posts were successfully unmarked as published.")

# Custom Admin for Testimonial
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company_name', 'rating', 'is_approved', 'date_created')
    list_filter = ('is_approved', 'rating', 'date_created')
    search_fields = ('client_name', 'quote')
    actions = ['approve_testimonials', 'disapprove_testimonials']

    fieldsets = (
        (None, {
            'fields': ('client_name', 'company_name', 'role', 'quote', 'rating')
        }),
        ('Approval & Date', {
            'fields': ('is_approved',),
            'classes': ('collapse',)
        }),
    )

    @admin.action(description='Approve selected testimonials')
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} testimonials were successfully approved.")

    @admin.action(description='Disapprove selected testimonials')
    def disapprove_testimonials(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} testimonials were successfully disapproved.")

# Custom Admin for Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'blog_post', 'pub_date', 'is_approved')
    list_filter = ('is_approved', 'pub_date', 'blog_post')
    search_fields = ('author_name', 'comment_text')
    actions = ['approve_comments', 'disapprove_comments']
    fieldsets = (
        (None, {
            'fields': ('blog_post', 'author_name', 'author_email', 'comment_text')
        }),
        ('Moderation', {
            'fields': ('is_approved',),
            'classes': ('collapse',)
        }),
    )

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} comments were successfully approved.")

    @admin.action(description='Disapprove selected comments')
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} comments were successfully disapproved.")

# Custom Admin for NewsletterSubscriber # NEW ADMIN CLASS
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)


# No need to use admin.site.register(Service) here anymore as it's handled by @admin.register(Service)
admin.site.register(Technology)
admin.site.register(ContactMessage)
admin.site.register(TeamMember)