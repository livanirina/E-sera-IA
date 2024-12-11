from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def home(request):
    return render(request, 'chat/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat_page')
    else:
        form = UserLoginForm()
    return render(request, 'chat/login.html', {'form': form})

@login_required
def chat_page(request):
    return render(request, "chat/chat.html")

@csrf_exempt
def get_gemini_response(request):
    """Obtient une réponse de Gemini pour un message utilisateur."""
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        try:
            response = model.generate_content(user_message)
            return JsonResponse({"response": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=400)

