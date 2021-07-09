from django.shortcuts import render, redirect
from .models import Puzzle
from django.contrib import auth
from .models import School 
from django.contrib.auth.decorators import login_required 
from datetime import datetime
# Create your views here.
@login_required
def puzzles(request, level):
    if level == 10: 
        return redirect('finish')
    else:
        request.session['level'] = level
        puzzle = Puzzle.objects.get(level=level, user=request.user)
        school = School.objects.get(user=request.user)
        error_message = 'The code entered is wrong. Please try again'
    if request.method == 'POST':
        code = request.POST['code']
        if puzzle.code.lower() == code.lower():
            school.level = level+1
            school.submission_time = datetime.now()
            school.save()
            return redirect('cluehunt', level+1)
        else:
            return render(request, 'cluehunt/puzzle.html', {'error': error_message, 'resources': puzzle.resources, 'level': level, 'hintsLeft': school.hintsLeft, 'skipsLeft': school.skipsLeft, 'hintNumber': puzzle.hintNumber, 'title': puzzle.title, 'hints': puzzle.hints, 'name': school.name})
    else: 
        if level == school.level:
            if request.session['hint']:
                request.session['hint'] = False
                return render(request, 'cluehunt/puzzle.html', {'resources': puzzle.resources, 'error': False, 'level': level, 'hintsLeft': school.hintsLeft, 'skipsLeft': school.skipsLeft, 'hints': puzzle.hints, 'hintNumber': puzzle.hintNumber, 'title': puzzle.title, 'name': school.name})
            else: 
                if request.session['skip']:
                    request.session['skip'] = False
                    school.level = school.level +1
                    school.save()
                    return redirect('cluehunt', school.level)
            return render(request, 'cluehunt/puzzle.html', {'resources': puzzle.resources, 'error': False, 'level': level, 'hintsLeft': school.hintsLeft, 'skipsLeft': school.skipsLeft, 'hintNumber': puzzle.hintNumber, 'title': puzzle.title, 'hints': puzzle.hints, 'name': school.name})
        else:
            auth.logout(request)
            return redirect('home')

def home(request):
    if request.method == 'POST':
        name = request.POST['schoolName']
        name = name.replace(" ", "")
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password)
        school = School.objects.get(user=user)
        if user is not None: 
            if school.level == 10: 
                return render(request, 'cluehunt/home.html', {'error': 'You have already finished the cluehunt.'})
            else: 
                auth.login(request, user)
                request.session['hint'] = False
                request.session['skip'] = False
                return redirect('cluehunt', school.level)
        else: 
            return render(request, 'cluehunt/home.html', {'error': 'Wrong credentials. Please try again.'})
    else: 
        return render(request, 'cluehunt/home.html')

def finish(request): 
    if request.method == 'GET':
        school = School.objects.get(user=request.user)
        if school.level == 10: 
            school.submission_time = datetime.now()
            school.save()
            auth.logout(request)
            return render(request, 'cluehunt/finish.html')
        else: 
            auth.logout(request)
            return redirect('home')

def hints(request):
    school = School.objects.get(user=request.user)
    puzzle = Puzzle.objects.get(level=request.session['level'], user=request.user)
    if request.method == 'GET':
        school.hintsLeft = school.hintsLeft-1
        request.session['hint'] = True
        school.save()
        puzzle.hintNumber = puzzle.hintNumber -1
        puzzle.save()
        return redirect('cluehunt', school.level)
    else: 
        pass

def skip(request):
    school = School.objects.get(user=request.user)
    puzzle = Puzzle.objects.get(level=school.level, user=request.user)
    if request.method == 'GET':
        school.skipsLeft = school.skipsLeft -1 
        request.session['skip'] = True
        school.save()
        return redirect('cluehunt', school.level)
    else: 
        pass

def blackHole(request):
    if request.method == 'GET':
        return render(request, 'cluehunt/blackHole.html')
    else: 
        pass

def upload(request):
    schools = {'GEMSModernSchool': 'alphaCluehunta', 'HopetownGirlsSchool': 'alphaCluehuntb', 'MayoCollegeGirlsSchool': 'alphaCluehuntc', 'ShivNadarSchool': 'alphaCluehuntd', 'TheDalyCollege': 'alphaCluehunte', 'TheDoonSchool': 'alphaCluehuntf', 'TheLawrenceSchool':'alphaCluehuntg', 'TheScindiaSchool': 'alphaCluehunth', 'TheShriRamSchool':'alphaCluehunti', 'WelhamBoysSchool': 'alphaCluehuntj'}
    for name, password in schools.items(): 
        puzzle = Puzzle()
        puzzle.code = "Franklin Roosevelt"
        puzzle.resources = "https://drive.google.com/file/d/1BX3G0AfXl9OAOuQVrEa2lGxiWWiHA3Py/view?usp=sharing"
        puzzle.hints = "Look at your keyboard"
        puzzle.hintNumber = 1
        puzzle.title = "Secret code from Snowden"
        puzzle.level = 1
        puzzle.user = auth.authenticate(username=name, password=password)
        puzzle.save()
    return redirect('home')