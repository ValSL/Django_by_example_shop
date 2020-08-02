from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)

    # create invoice email
    subject = f'My shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject=subject, body=message, from_email='ValSLTest@yandex.by', to=[order.email])

    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    
    # attach PDF file
    email.attach(filename=f'order_{order_id}.pdf',
                 content=out.getvalue(),
                 mimetype='application/pdf')
    email.send()
