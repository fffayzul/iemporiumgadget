import json
from datetime import date
from dateutil.relativedelta import relativedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from store.models import Order, OrderItem, Product


@staff_member_required
def dashboard_index(request):
    # ── Headline stats ──────────────────────────────────────────────────────
    total_orders = Order.objects.count()

    revenue_qs = Order.objects.filter(
        status__in=['confirmed', 'shipped', 'delivered']
    ).aggregate(rev=Sum('total'))
    total_revenue = revenue_qs['rev'] or 0

    total_products = Product.objects.filter(is_active=True).count()

    low_stock_count = Product.objects.filter(
        is_active=True, stock__lte=F('low_stock_threshold'), stock__gt=0
    ).count()

    out_of_stock_count = Product.objects.filter(is_active=True, stock=0).count()

    # ── Orders by status ────────────────────────────────────────────────────
    orders_by_status = list(
        Order.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )
    orders_by_status_json = json.dumps(orders_by_status)

    # ── Top 10 products by revenue ──────────────────────────────────────────
    top_products = list(
        OrderItem.objects.values('product_name')
        .annotate(units_sold=Sum('quantity'), revenue=Sum('line_total'))
        .order_by('-revenue')[:10]
    )

    # ── Recent 20 orders ────────────────────────────────────────────────────
    recent_orders = Order.objects.order_by('-created_at')[:20]

    # ── Monthly revenue last 12 months ──────────────────────────────────────
    start_date = date.today() - relativedelta(months=11)
    monthly_qs = (
        Order.objects
        .filter(status__in=['confirmed', 'shipped', 'delivered'], created_at__date__gte=start_date)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total'))
        .order_by('month')
    )
    monthly_data = {row['month'].strftime('%b %Y'): float(row['revenue']) for row in monthly_qs}

    # Fill in all 12 months, including those with zero revenue
    labels, data = [], []
    for i in range(11, -1, -1):
        m = date.today() - relativedelta(months=i)
        label = m.strftime('%b %Y')
        labels.append(label)
        data.append(monthly_data.get(label, 0))

    monthly_revenue_json = json.dumps({'labels': labels, 'data': data})

    context = {
        'title': 'Statistics Dashboard',
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'orders_by_status': orders_by_status,
        'orders_by_status_json': orders_by_status_json,
        'top_products': top_products,
        'recent_orders': recent_orders,
        'monthly_revenue_json': monthly_revenue_json,
    }
    return render(request, 'dashboard/index.html', context)


@staff_member_required
def revenue_data(request):
    start_date = date.today() - relativedelta(months=11)
    monthly_qs = (
        Order.objects
        .filter(status__in=['confirmed', 'shipped', 'delivered'], created_at__date__gte=start_date)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total'))
        .order_by('month')
    )
    monthly_data = {row['month'].strftime('%b %Y'): float(row['revenue']) for row in monthly_qs}
    labels, data = [], []
    for i in range(11, -1, -1):
        m = date.today() - relativedelta(months=i)
        label = m.strftime('%b %Y')
        labels.append(label)
        data.append(monthly_data.get(label, 0))
    return JsonResponse({'labels': labels, 'data': data})
