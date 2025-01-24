import os.path
from zoneinfo import available_timezones

import pandas as pd
from allauth.core.internal.httpkit import redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
import openpyxl
from django.views import View

from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from books_catalog.models import Genre, Book, Author, BookInstance
from .forms import DataUploadForm


# Create your views here.
def data_upload(request):
    if "GET" == request.method and request.GET.get('download_template'):
        file_path = os.path.join(settings.MEDIA_ROOT, 'template.xlsx')
        if not os.path.exists(file_path):
            return HttpResponse("Template file not found", status=404)
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='template.xlsx')
        return response
    elif "POST" == request.method:
        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["file"]
            try:
                df = pd.read_excel(excel_file)
                books = []
                book_instances = []



                for _, row in df.iterrows():
                    author_full_name = row['Author']
                    first_name, last_name = (author_full_name.split(' ', 1) + [""])[
                                            :2]

                    author, created = Author.objects.get_or_create(
                        first_name=first_name,
                        last_name=last_name
                    )

                    book = Book(
                        title=row['Title'],
                        author=author,
                        publication_date=row['Publication Year'],
                        isbn=row['ISBN']
                    )
                    books.append(book)

                    # genres = [g.strip() for g in row['Genre'].split(',')] if row['Genre'] else []
                    # genre_objects = [Genre.objects.get_or_create(name=genre)[0] for genre in genres]
                    # book.genre.set(genre_objects)

                    available_copies = int(row['Copies']) if not pd.isna(row['Copies']) else 0  # Number of copies from the Excel file
                    for _ in range(available_copies):
                        book_instance = BookInstance(
                            book=book,
                            status='a'
                        )
                        book_instances.append(book_instance)


                Book.objects.bulk_create(books)
                BookInstance.objects.bulk_create(book_instances)

                for book, row in zip(books, df.iterrows()):
                    genres = [g.strip() for g in row[1]['Genre'].split(',')] if row[1]['Genre'] else []
                    genre_objects = [Genre.objects.get_or_create(name=genre)[0] for genre in genres]
                    book.genre.set(genre_objects)

                messages.success(request, 'Books successfully added!', extra_tags='add-book-success')
                return redirect('data_import:data-upload')

            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
        else:
            messages.error(request, 'Invalid form submission.')
            return render(request, 'data_import/data_upload.html', {'form': form})

        return render(request, 'data_import/data_upload.html', {"form": form})
    return render(request, 'data_import/data_upload.html')
