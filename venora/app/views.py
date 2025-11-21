from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

def home(request):
    return render(request, 'home.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        company = request.POST.get('company', 'Not provided')  # Added company field
        message = request.POST.get('message')

        # Basic validation
        if not name or not email or not message:
            messages.error(request, "Please fill in all required fields.")
            return redirect('/contact')

        try:
            # Admin email - Enhanced with better formatting
            admin_subject = f'New Contact Form Submission - {name}'
            admin_message = f'''
New contact form submission received:

Name: {name}
Email: {email}
Company: {company}
Message:
{message}

---
This message was sent from the Venora Digitech contact form.
'''

            # Send email to admin
            send_mail(
                subject=admin_subject,
                message=admin_message.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # Confirmation email to user - Enhanced formatting
            confirmation_subject = "Thank You for Contacting Venora Digitech"
            confirmation_message = f'''
Hi {name},

Thank you for reaching out to Venora Digitech! We're excited to hear from you.

We have received your message and our team will review it carefully. We strive to respond to all inquiries within 24 hours.

Here's a summary of your submission:
- Name: {name}
- Email: {email}
- Company: {company}
- Message: {message}

We'll get back to you soon with a detailed response.

Warm regards,
Team Venora Digitech
'''

            # Send confirmation email to user
            send_mail(
                subject=confirmation_subject,
                message=confirmation_message.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully! We'll get back to you within 24 hours.")

        except Exception as e:
            # Log the error for debugging
            print(f"Email sending failed: {e}")
            messages.error(request,
                           "Sorry, there was an error sending your message. Please try again or contact us directly at venoradigitech@gmail.com")

        return redirect('/contact')  # Redirect back to contact page

    # If GET request, render the contact page
    return render(request, 'contact.html')  # Make sure you have a contact.html template

def pricing(request):
    return render(request, 'pricing.html')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_503_view(request, exception):
    return render(request, '503.html', status=503)