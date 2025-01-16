from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CompanyUser, File
from django.contrib.auth.hashers import make_password
from django.core import signing
import os
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse

VALID_EXTENSIONS = ['.pptx', '.docx', '.xlsx']
def homepage(request):
    return render(request, 'homepage.html')
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if CompanyUser.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
        if CompanyUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)
        user = CompanyUser.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            user_type="Client"  
        )
        signed_url = signing.dumps({'user_id': user.id})
        verification_url = f"http://127.0.0.1:8000/verify-email/?token={signed_url}"
        subject = "Email Verification"
        message = f"Please verify your email by clicking the following link: {verification_url}"
        from_email = settings.DEFAULT_FROM_EMAIL  
        send_mail(subject, message, from_email, [email])
        return JsonResponse({"msg": "User created successfully. Please check your email for verification."}, status=201)
    return render(request, "signup.html")
def verify_email(request):
    token = request.GET.get('token')
    if not token:
        return JsonResponse({"error": "Invalid token."}, status=400)
    try:
        data = signing.loads(token)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({"error": "Invalid token."}, status=400)
        user = CompanyUser.objects.get(id=user_id)
        user.email_verified = True
        user.save()
        return redirect('email_verified_success')

    except signing.BadSignature:
        return JsonResponse({"error": "Invalid token."}, status=400)
    except CompanyUser.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
def email_verified_success(request):
    return render(request, 'email_verified_success.html')
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.user_type not in ['Ops', 'Client']:  
                return JsonResponse({"error": "Unauthorized access. Invalid user type."}, status=403)
            login(request, user)
            if user.user_type == 'Client':
                return redirect('client_dashboard')  
            elif user.user_type == 'Ops':
                return redirect('ops_dashboard')
            return JsonResponse({"error": "Unknown user type."}, status=400)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    return render(request, 'login.html')
VALID_EXTENSIONS = ['.pptx', '.docx', '.xlsx']
def validate_file_type(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in VALID_EXTENSIONS:
        raise ValidationError(f"Invalid file type. Only {', '.join(VALID_EXTENSIONS)} files are allowed.")
def upload_file(request):
    if request.user.user_type != 'Ops':
        return JsonResponse({"error": "Unauthorized access. Only Ops users can upload files."}, status=403)
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        try:
            validate_file_type(file)
            max_size_mb = 5
            if file.size > max_size_mb * 1024 * 1024:
                return JsonResponse({"error": f"File size exceeds {max_size_mb}MB limit."}, status=400)
            file_instance = File(file=file, name=file.name, uploaded_by=request.user)
            file_instance.save()
            return JsonResponse({"message": "File uploaded successfully."}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "No file provided."}, status=400)
def ops_dashboard(request):
    if request.user.is_authenticated and request.user.user_type == 'Ops':
        files = File.objects.all()
        return render(request, "ops_dashboard.html", {"files": files})
    return JsonResponse({"error": "Unauthorized"}, status=403)
def client_dashboard(request):
    if request.user.is_authenticated and request.user.user_type == 'Client':
        files = File.objects.filter(uploaded_by__user_type='Ops')
        file_links = []
        for file in files:
            signed_url = signing.dumps({'file_id': file.id})
            download_link = f"http://127.0.0.1:8000/download-file/?token={signed_url}"
            file_links.append({'name': file.name, 'download_link': download_link})
        return render(request, "client_dashboard.html", {"file_links": file_links})
    return JsonResponse({"error": "Unauthorized"}, status=403)
def download_file(request):
    token = request.GET.get('token')
    if not token:
        return JsonResponse({"error": "Invalid token."}, status=400)
    try:
        data = signing.loads(token)
        file_id = data.get('file_id')
        if not file_id:
            return JsonResponse({"error": "Invalid token."}, status=400)
        if not request.user.is_authenticated or request.user.user_type != 'Client':
            return JsonResponse({"error": "Unauthorized access. Only clients can download files."}, status=403)
        file = get_object_or_404(File, id=file_id)
        response = HttpResponse(file.file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.name}"'
        return response
    except signing.BadSignature:
        return JsonResponse({"error": "Invalid or expired token."}, status=400)
    except File.DoesNotExist:
        return JsonResponse({"error": "File not found."}, status=404)
