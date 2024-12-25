import openpyxl
from django.shortcuts import render
# from django.contrib import messages
# from .forms import UploadFileForm
# from .models import Book
# from datetime import datetime



def upload_file(request):
    if "GET" == request.method:
        return render(request, 'books_catalog/upload.html', {})
    elif request.method == "POST":
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        return render(request, 'books_catalog/upload.html', {"excel_data":excel_data})
