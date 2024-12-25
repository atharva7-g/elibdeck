from django.contrib import admin
from .models import Book, Author, Genre, BookInstance, Language

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

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


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)


