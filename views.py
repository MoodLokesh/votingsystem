import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Voter, Candidate
from django.contrib.auth.hashers import make_password, check_password


# ---------- PAGE VIEWS ----------
def login_view(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'registration.html')


def voting(request):
    if not request.session.get('user'):
        return redirect('/')
    candidates = Candidate.objects.all()
    return render(request, 'voting.html', {'candidates': candidates})


# ---------- API VIEWS ----------
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if Voter.objects.filter(username=data['username']).exists():
            return JsonResponse({
                "success": False,
                "message": "Username already exists"
            })

        Voter.objects.create(
            full_name=data.get('full_name', ''),
            guardian=data.get('guardian', ''),
            gender=data.get('gender', ''),
            dob=data.get('dob'),
            nationality=data.get('nationality', ''),
            constituency=data.get('constituency', ''),
            username=data['username'],
            password=make_password(data['password'])  # 🔐 encrypted
        )

        return JsonResponse({
            "success": True,
            "message": "Registration successful"
        })


def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        voter = Voter.objects.filter(username=data['username']).first()

        if not voter or not check_password(data['password'], voter.password):
            return JsonResponse({
                "success": False,
                "message": "Invalid credentials"
            })

        request.session['user'] = voter.username
        return JsonResponse({
            "success": True,
            "message": "Login successful"
        })


def submit_vote(request):
    if request.method == "POST":

        if not request.session.get('user'):
            return JsonResponse({
                "success": False,
                "message": "Not logged in"
            })

        voter = Voter.objects.get(username=request.session['user'])

        # 🔒 HARD LOCK: stop everything immediately
        if voter.has_voted:
            return JsonResponse({
                "success": False,
                "message": "You have already voted"
            })

        data = json.loads(request.body)
        candidate_name = data.get('candidate')

        if not candidate_name:
            return JsonResponse({
                "success": False,
                "message": "Invalid candidate selected"
            })

        candidate = Candidate.objects.filter(name=candidate_name).first()

        if not candidate:
            return JsonResponse({
                "success": False,
                "message": "Invalid candidate selected"
            })

        # ✅ SAVE ONCE ONLY
        candidate.votes += 1
        candidate.save()

        voter.has_voted = True
        voter.save(update_fields=["has_voted"])

        # 🔒 DESTROY SESSION AFTER VOTE
        request.session.flush()

        return JsonResponse({
            "success": True,
            "message": "Vote submitted successfully"
        })


def results(request):
    candidates = Candidate.objects.all()
    return render(request, 'results.html', {'candidates': candidates})
