from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import transaction
from django.db.models import Q

from .models import Category, Brand, Product, Order, OrderItem
from .emails import send_order_placed_email


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


# ─── Home ─────────────────────────────────────────────────────────────────────

def home(request):
    featured = Product.objects.filter(is_featured=True, is_active=True).prefetch_related('images')[:8]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'featured_products': featured,
        'categories': categories,
    })


# ─── Product List / Search ────────────────────────────────────────────────────

def product_list(request):
    qs = Product.objects.filter(is_active=True).prefetch_related('images').select_related('category', 'brand')

    # Filters
    cat_slugs = request.GET.getlist('category')
    brand_slugs = request.GET.getlist('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')
    condition = request.GET.get('condition')
    sort = request.GET.get('sort', '-created_at')

    active_category = None

    if cat_slugs:
        qs = qs.filter(category__slug__in=cat_slugs)
    if brand_slugs:
        qs = qs.filter(brand__slug__in=brand_slugs)
    if min_price:
        try:
            qs = qs.filter(price__gte=Decimal(min_price))
        except Exception:
            pass
    if max_price:
        try:
            qs = qs.filter(price__lte=Decimal(max_price))
        except Exception:
            pass
    if in_stock:
        qs = qs.filter(stock__gt=0)
    if condition:
        qs = qs.filter(condition=condition)

    sort_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        '-created_at': '-created_at',
    }
    qs = qs.order_by(sort_map.get(sort, '-created_at'))

    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))

    all_brands = Brand.objects.all()
    all_categories = Category.objects.all()

    return render(request, 'store/product_list.html', {
        'page_obj': page,
        'all_brands': all_brands,
        'all_categories': all_categories,
        'selected_cats': cat_slugs,
        'selected_brands': brand_slugs,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'in_stock': in_stock,
        'condition': condition or '',
        'sort': sort,
        'active_category': active_category,
        'page_title': 'All Products',
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    qs = Product.objects.filter(category=category, is_active=True).prefetch_related('images').select_related('brand')

    sort = request.GET.get('sort', '-created_at')
    sort_map = {'price_asc': 'price', 'price_desc': '-price', 'name_asc': 'name', '-created_at': '-created_at'}
    qs = qs.order_by(sort_map.get(sort, '-created_at'))

    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'store/product_list.html', {
        'page_obj': page,
        'all_brands': Brand.objects.all(),
        'all_categories': Category.objects.all(),
        'selected_cats': [slug],
        'selected_brands': [],
        'min_price': '',
        'max_price': '',
        'in_stock': None,
        'condition': '',
        'sort': sort,
        'active_category': category,
        'page_title': category.name,
    })


def search(request):
    q = request.GET.get('q', '').strip()
    qs = Product.objects.filter(is_active=True).prefetch_related('images').select_related('category', 'brand')

    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q) |
            Q(brand__name__icontains=q)
        )

    sort = request.GET.get('sort', '-created_at')
    sort_map = {'price_asc': 'price', 'price_desc': '-price', 'name_asc': 'name', '-created_at': '-created_at'}
    qs = qs.order_by(sort_map.get(sort, '-created_at'))

    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'store/product_list.html', {
        'page_obj': page,
        'all_brands': Brand.objects.all(),
        'all_categories': Category.objects.all(),
        'selected_cats': [],
        'selected_brands': [],
        'min_price': '',
        'max_price': '',
        'in_stock': None,
        'condition': '',
        'sort': sort,
        'active_category': None,
        'page_title': f'Search results for "{q}"' if q else 'All Products',
        'search_query': q,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk).prefetch_related('images')[:4]

    return render(request, 'store/product_detail.html', {
        'product': product,
        'images': images,
        'related_products': related,
    })


# ─── Cart ─────────────────────────────────────────────────────────────────────

def cart_detail(request):
    cart = _get_cart(request)
    cart_items = []
    for product_id, item in cart.items():
        cart_items.append({
            'product_id': product_id,
            'name': item['name'],
            'price': Decimal(str(item['price'])),
            'quantity': item['quantity'],
            'image': item.get('image'),
            'slug': item.get('slug', ''),
            'line_total': Decimal(str(item['price'])) * item['quantity'],
        })
    subtotal = sum(i['line_total'] for i in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
    })


def cart_add(request, product_id):
    if request.method != 'POST':
        return redirect('store:product_detail', slug=request.GET.get('slug', ''))

    product = get_object_or_404(Product, pk=product_id, is_active=True)
    try:
        qty = max(1, int(request.POST.get('quantity', 1)))
    except ValueError:
        qty = 1

    cart = _get_cart(request)
    key = str(product_id)

    primary = product.primary_image()
    image_url = primary.image.url if primary else ''

    if key in cart:
        cart[key]['quantity'] = min(cart[key]['quantity'] + qty, product.stock)
    else:
        cart[key] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': qty,
            'image': image_url,
            'slug': product.slug,
        }

    _save_cart(request, cart)
    messages.success(request, f'"{product.name}" added to cart.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


def cart_update(request, product_id):
    if request.method != 'POST':
        return redirect('store:cart_detail')

    cart = _get_cart(request)
    key = str(product_id)
    try:
        qty = int(request.POST.get('quantity', 0))
    except ValueError:
        qty = 0

    if qty <= 0:
        cart.pop(key, None)
    else:
        if key in cart:
            cart[key]['quantity'] = qty

    _save_cart(request, cart)
    return redirect('store:cart_detail')


def cart_remove(request, product_id):
    if request.method != 'POST':
        return redirect('store:cart_detail')

    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    _save_cart(request, cart)
    return redirect('store:cart_detail')


# ─── Checkout & Orders ────────────────────────────────────────────────────────

def checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart_detail')

    cart_items = []
    for product_id, item in cart.items():
        cart_items.append({
            'product_id': product_id,
            'name': item['name'],
            'price': Decimal(str(item['price'])),
            'quantity': item['quantity'],
            'line_total': Decimal(str(item['price'])) * item['quantity'],
        })
    subtotal = sum(i['line_total'] for i in cart_items)

    from .models import NIGERIAN_STATES
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'nigerian_states': NIGERIAN_STATES,
    })


def place_order(request):
    if request.method != 'POST':
        return redirect('store:checkout')

    cart = _get_cart(request)
    if not cart:
        return redirect('store:cart_detail')

    # Collect form data
    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()
    city = request.POST.get('city', '').strip()
    state = request.POST.get('state', '').strip()
    payment_method = request.POST.get('payment_method', 'cod')
    notes = request.POST.get('notes', '').strip()

    if not all([full_name, phone, address, city, state]):
        messages.error(request, 'Please fill in all required delivery fields.')
        return redirect('store:checkout')

    # Calculate totals
    subtotal = Decimal('0')
    order_lines = []
    for product_id, item in cart.items():
        price = Decimal(str(item['price']))
        qty = item['quantity']
        subtotal += price * qty
        order_lines.append({
            'product_id': product_id,
            'name': item['name'],
            'price': price,
            'quantity': qty,
        })

    delivery_fee = Decimal('0')
    total = subtotal + delivery_fee

    with transaction.atomic():
        order = Order.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            payment_method=payment_method,
            notes=notes,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
        )

        for line in order_lines:
            try:
                product = Product.objects.select_for_update().get(pk=line['product_id'])
                if product.stock >= line['quantity']:
                    product.stock -= line['quantity']
                    product.save(update_fields=['stock'])
                product_ref = product
            except Product.DoesNotExist:
                product_ref = None

            OrderItem.objects.create(
                order=order,
                product=product_ref,
                product_name=line['name'],
                product_price=line['price'],
                quantity=line['quantity'],
                line_total=line['price'] * line['quantity'],
            )

    # Clear cart
    request.session['cart'] = {}
    request.session.modified = True

    # Send confirmation email
    send_order_placed_email(order)

    return redirect('store:order_confirmation', order_number=order.order_number)


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    items = order.items.all()
    return render(request, 'store/order_confirmation.html', {
        'order': order,
        'items': items,
    })
