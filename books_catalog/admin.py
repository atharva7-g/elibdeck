from django.contrib import admin
from .models import Book, Author, Genre, BookInstance, Language, Feedback

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    filter_horizontal = ('borrowers',)

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_date', 'id')
    list_filter = ('status', 'due_date')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_date', 'borrower')
        }),
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'subject', 'created_at')  # Columns in the admin list view
    list_filter = ('rating', 'created_at', 'book')  # Filters in the sidebar
    search_fields = ('subject', 'body', 'book__title')
    ordering = ('-created_at',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)


