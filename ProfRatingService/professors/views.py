from django.shortcuts import render
from functools import wraps
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Module, Professor, Rating, Iteration
from django.db.models import Sum, Count



def must_be_logged_out(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse({"error": "You must be logged out"}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def login_required_no_redirect(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "You must be logged in"}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def list(request):
    module_data = []  

    modules = Module.objects.all()
    for module in modules:
        professor_id_list = Iteration.objects.filter(module_id=module.module_id).values_list('professor_id', flat=True)
        professors_list = Professor.objects.filter(professor_id__in=professor_id_list)

        module_data.append({
            "module": {
                "code": str(module.department)+str(module.year_group)+str(module.module_id),
                "name": module.name,
                "year": module.year,
                "semester": module.semester,
            },
            "professors": [
                { "name": prof.name} for prof in professors_list
            ]
        })

    return JsonResponse(module_data, safe=False, status=200)


def view(request):
    professor_list = Professor.objects.all()
    professor_ratings = []

    for prof in professor_list:
        ratings = Rating.objects.filter(iteration_id__professor_id=prof.professor_id).aggregate(
            total=Sum('rating'), count=Count('rating')
        )
        average_rating = round(ratings['total'] / ratings['count']) if ratings['count'] else 0

        professor_ratings.append({
            'name': prof.name,
            'prof_code': prof.professor_id,
            'average_rating': "*" * average_rating
        })

    return JsonResponse(professor_ratings, safe=False, status=200)


def average(request, professorId, moduleId):
    mod = Module.objects.filter(module_id=moduleId).values_list('name', flat=True).first()
    prof = Professor.objects.filter(professor_id=professorId).values_list('name', flat=True).first()

    ratings = Rating.objects.filter(
        iteration_id__in=Iteration.objects.filter(professor_id=professorId, module_id=moduleId)
    ).aggregate(
        total=Sum('rating'), count=Count('rating')
    )

    average_rating = round(ratings['total'] / ratings['count']) if ratings['count'] else 0

    response_data = {
        "professor": prof if prof else "Professor Unknown",
        "module": mod if mod else "Module Unknown",
        "average_rating": "*" * average_rating if average_rating else "No ratings available",
    }

    return JsonResponse(response_data, safe=False, status=200)


@login_required_no_redirect
@csrf_exempt
def rate(request):
    try:
        data = json.loads(request.body)
        professorId, moduleId, year, semester, rating = data.get("professor_id"), data.get("module_id"), data.get("year"), data.get("semester"), data.get("rating")

        if not all([professorId, moduleId, year, semester, rating]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if not (1<= rating <=5):
            return JsonResponse({"error": "Rating must be between 1 and 5"}, status=400)
        
        if not (isinstance(rating, int)):
            return JsonResponse({"error": "Rating must be an integer"}, status=400)

        iteration = Iteration.objects.filter(module_id=moduleId, professors__id=professorId).first()

        if not iteration:
            return JsonResponse({"error": "Module instance not found for given professor, module, year, and semester"}, status=404)

        user = request.user

        newRating = Rating.objects.create(
            iteration_id=iteration.iteration_id,
            student_id=user.student_id,
            rating=rating
        )

        return JsonResponse({"message": "Rating successfully recorded", "rating_id": newRating.id}, status=200)

    except Professor.DoesNotExist:
        return JsonResponse({"error": "Professor not found"}, status=404)
    except Module.DoesNotExist:
        return JsonResponse({"error": "Module not found"}, status=404)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

@csrf_exempt
@must_be_logged_out
def register(request):
    data = json.loads(request.body)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return JsonResponse({"error": "All fields are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already taken"}, status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already taken"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    
    return JsonResponse({"message": "Successfully registered user", "user_id": user.id}, status=201)

@csrf_exempt
@must_be_logged_out
def loginUser(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if not all([username, password]):
        return JsonResponse({"error": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Login successful"}, status=200)
    else:
        return JsonResponse({"error": "Invalid username or password"}, status=401)

def logoutUser(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"}, status=200)

