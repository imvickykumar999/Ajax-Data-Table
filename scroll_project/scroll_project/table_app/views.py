from django.http import JsonResponse
from .models import TableRow
from django.core.paginator import Paginator
from django.shortcuts import render

def load_rows(request):
    page = request.GET.get('page', 1)
    filter_value = request.GET.get('filter', '')
    rows_per_page = 20

    rows = TableRow.objects.all().order_by('id')
    if filter_value:
        rows = rows.filter(name=filter_value)  # Adjust the field name accordingly

    paginator = Paginator(rows, rows_per_page)
    page_obj = paginator.get_page(page)
    data = [
        {"id": row.id, "name": row.name, "details": row.details}
        for row in page_obj
    ]
    return JsonResponse({"rows": data, "has_next": page_obj.has_next()})

def index(request):
    range100 = range(1, 101)
    context = {
        'range100' : range100,
    }
    return render(request, 'table_app/index.html', context=context)
