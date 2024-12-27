import os.path

import pandas as pd
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
import openpyxl
from django.views import View

from django.http import FileResponse, HttpResponse
from django.contrib import messages
from books_catalog.models import Book
from .forms import DataUploadForm


# Create your views here.
@login_required
@permission_required('books_catalog.can_mark_returned', raise_exception=True)
def data_upload(request):
    if "GET" == request.method and request.GET.get('download_template'):
        file_path = os.path.join('media', 'test.xlsx')
        if not os.path.exists(file_path):
            return HttpResponse("Template file not found", status=404)
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='template.xlsx')

        return response
    elif "POST" == request.method and request.FILES.get('excel_file'):
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)

        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over rows
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)


        return render(request, 'data_import/data_upload.html', {"excel_data": excel_data})
    return render(request, 'data_import/data_upload.html')

