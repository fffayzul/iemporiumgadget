from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def _send(subject, template, context, to_email):
    if not to_email:
        return
    html_body = render_to_string(template, context)
    text_body = f"Order {context['order'].order_number} — {subject}"
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send(fail_silently=True)


def send_order_placed_email(order):
    _send(
        subject=f'Order Confirmed — {order.order_number} | iEmporium Gadgets',
        template='emails/order_placed.html',
        context={'order': order, 'items': order.items.all()},
        to_email=order.email,
    )


def send_order_confirmed_email(order):
    _send(
        subject=f'Your Order {order.order_number} Has Been Confirmed!',
        template='emails/order_confirmed.html',
        context={'order': order, 'items': order.items.all()},
        to_email=order.email,
    )


def send_dispatch_notification_email(order):
    _send(
        subject=f'Your Order {order.order_number} Is On Its Way! 🚚',
        template='emails/order_dispatched.html',
        context={'order': order, 'items': order.items.all()},
        to_email=order.email,
    )
