from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        try:
            # Admin email
            admin_subject = f'New Contact Query'
            admin_message = f'''
You received a new query from the website:

Name: {name}
Email: {email}
Message:
{message}
'''

            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,  # ✅ always use this
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # Confirmation email to user
            confirmation_subject = "Venora Digitech - We Received Your Query"
            confirmation_message = f'''
Hi {name},

Thank you for reaching out to us at Venora Digitech.

We have received your message and our team will get back to you shortly. Here’s a copy of your message:

Message: {message}

Warm regards,
Team Venora Digitech
            '''

            send_mail(
                subject=confirmation_subject,
                message=confirmation_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, " Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f" Failed to send message: {e}")

        return redirect('/#contact')  # ✅ back to contact section on landing page

    return render(request, 'home.html')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_503_view(request, exception):
    return render(request, '503.html', status=503)