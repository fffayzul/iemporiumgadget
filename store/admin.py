from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Category, Brand, Product, ProductImage, Order, OrderItem
from .emails import send_order_confirmed_email, send_dispatch_notification_email


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    @admin.display(description='Products')
    def product_count(self, obj):
        return obj.products.count()


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    @admin.display(description='Products')
    def product_count(self, obj):
        return obj.products.count()


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'condition', 'price_display', 'stock',
                    'stock_status_badge', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active')
    list_filter = ('category', 'brand', 'condition', 'is_featured', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline]
    list_per_page = 25

    @admin.display(description='Price (₦)')
    def price_display(self, obj):
        return f'₦{obj.price:,.0f}'

    @admin.display(description='Stock Status')
    def stock_status_badge(self, obj):
        if obj.stock == 0:
            colour = '#dc3545'
            label = f'Out of Stock'
        elif obj.stock <= obj.low_stock_threshold:
            colour = '#fd7e14'
            label = f'Low ({obj.stock})'
        else:
            colour = '#28a745'
            label = f'In Stock ({obj.stock})'
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 8px;border-radius:4px;font-size:12px">{}</span>',
            colour, label
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.stock <= obj.low_stock_threshold and obj.stock > 0:
            messages.warning(
                request,
                f'Low stock alert: "{obj.name}" only has {obj.stock} unit(s) remaining.'
            )
        elif obj.stock == 0:
            messages.warning(request, f'"{obj.name}" is now out of stock.')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'quantity', 'line_total')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'state', 'total_display',
                    'status_badge', 'payment_method', 'created_at')
    list_filter = ('status', 'state', 'payment_method', 'created_at')
    search_fields = ('order_number', 'full_name', 'phone', 'email')
    readonly_fields = ('order_number', 'subtotal', 'delivery_fee', 'total', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    list_per_page = 30
    date_hierarchy = 'created_at'
    actions = ['mark_as_confirmed', 'mark_as_shipped', 'mark_as_delivered']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')

    @admin.display(description='Total')
    def total_display(self, obj):
        return f'₦{obj.total:,.0f}'

    @admin.display(description='Status')
    def status_badge(self, obj):
        colours = {
            'pending': '#6c757d',
            'confirmed': '#0d6efd',
            'shipped': '#fd7e14',
            'delivered': '#28a745',
            'cancelled': '#dc3545',
        }
        colour = colours.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 8px;border-radius:4px;font-size:12px">{}</span>',
            colour, obj.get_status_display()
        )

    @admin.action(description='Mark selected orders as Confirmed')
    def mark_as_confirmed(self, request, queryset):
        updated = 0
        for order in queryset.exclude(status=Order.STATUS_CONFIRMED):
            order.status = Order.STATUS_CONFIRMED
            order.save()
            send_order_confirmed_email(order)
            updated += 1
        self.message_user(request, f'{updated} order(s) marked as confirmed and customers notified.')

    @admin.action(description='Mark selected orders as Shipped')
    def mark_as_shipped(self, request, queryset):
        count = queryset.update(status=Order.STATUS_SHIPPED)
        self.message_user(request, f'{count} order(s) marked as shipped.')

    @admin.action(description='Mark selected orders as Delivered')
    def mark_as_delivered(self, request, queryset):
        count = queryset.update(status=Order.STATUS_DELIVERED)
        self.message_user(request, f'{count} order(s) marked as delivered.')

    def save_model(self, request, obj, form, change):
        if change:
            old = Order.objects.get(pk=obj.pk)
            old_status = old.status
        else:
            old_status = None
        super().save_model(request, obj, form, change)
        if old_status != Order.STATUS_CONFIRMED and obj.status == Order.STATUS_CONFIRMED:
            send_order_confirmed_email(obj)

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                '<int:order_id>/send-dispatch/',
                self.admin_site.admin_view(self.send_dispatch_view),
                name='order_send_dispatch',
            ),
        ]
        return custom + urls

    def send_dispatch_view(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        send_dispatch_notification_email(order)
        self.message_user(request, f'Dispatch notification sent for order {order.order_number}.', messages.SUCCESS)
        return HttpResponseRedirect(
            reverse('admin:store_order_change', args=[order_id])
        )
