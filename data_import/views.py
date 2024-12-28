import os.path

import pandas as pd
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
import openpyxl
from django.views import View

from django.http import FileResponse, HttpResponse
from django.contrib import messages
from books_catalog.models import Book, Author
from .forms import DataUploadForm


# Create your views here.
def data_upload(request):
    if "GET" == request.method and request.GET.get('download_template'):
        file_path = os.path.join('media', 'test.xlsx')
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



                for _, row in df.iterrows():

                    author_full_name = row['Author']
                    first_name, last_name = (author_full_name.split(' ', 1) + [""])[
                                            :2]

                    author, created = Author.objects.get_or_create(
                        first_name=first_name,
                        last_name=last_name
                    )

                    books.append(Book(
                        title=row['Title'],
                        author=author,
                        isbn=row['ISBN'],
                    ))

                Book.objects.bulk_create(books)

                messages.success(request, 'Books successfully added!')
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")

        return render(request, 'data_import/data_upload.html', {"form": form})
    return render(request, 'data_import/data_upload.html')
