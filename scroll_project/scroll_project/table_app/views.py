from django.http import JsonResponse
from .models import TableRow
from django.core.paginator import Paginator
from django.shortcuts import render

def load_rows(request):
    page = request.GET.get('page', 1)
    rows_per_page = 20
    rows = TableRow.objects.all().order_by('id')
    paginator = Paginator(rows, rows_per_page)
    page_obj = paginator.get_page(page)
    data = [
        {"id": row.id, "name": row.name, "details": row.details}
        for row in page_obj
    ]
    return JsonResponse({"rows": data, "has_next": page_obj.has_next()})

def index(request):
    return render(request, 'table_app/index.html')
