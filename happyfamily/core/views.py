from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from .mongo import students_col, users_col
from bson.objectid import ObjectId
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


@login_required
def student_pdf(request):
    grade = request.GET.get('grade')
    group = request.GET.get('group')
    query = {}
    if grade:
        query['grade'] = int(grade)
    if group:
        query['group'] = int(group)
    students = list(students_col.find(query))

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="tolibalar_{grade}_{group}.pdf"'

    # Register the DejaVuSans font
    font_path = os.path.join(os.path.dirname(
        __file__), 'fonts', 'DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    p = canvas.Canvas(response)
    y = 800
    p.setFont("DejaVuSans", 14)
    p.drawString(200, y, f"{grade}-sinf, {group}-gurux tolibalar ro'yxati")
    y -= 40
    p.setFont("DejaVuSans", 12)
    no = 1
    for s in students:
        line = f"{no}. {s.get('userId', '')} - {s.get('name', '')} {s.get('surname', '')}"
        p.drawString(50, y, line)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800
            p.setFont("DejaVuSans", 12)
        no += 1

    p.showPage()
    p.save()
    return response


@login_required
def student_list(request):
    if not request.user.role == 'admin':
        return HttpResponse("Access Denied", status=403)

    grade = request.GET.get('grade')
    group = request.GET.get('group')

    query = {}
    if grade:
        query['grade'] = int(grade)
    if group:
        query['group'] = int(group)

    students = []
    for s in students_col.find(query):
        s['id'] = str(s['_id'])
        students.append(s)

    return render(request, 'core/student_list.html', {'students': students})


@login_required
def user_list(request):
    if not request.user.role == 'admin':
        return HttpResponse("Access Denied", status=403)

    search_id = request.GET.get('userId')
    query = {}
    if search_id:
        try:
            query['userId'] = int(search_id)
        except ValueError:
            query['userId'] = -1  # no match fallback

    users = []
    for u in users_col.find(query):
        u['id'] = str(u['_id'])
        users.append(u)

    return render(request, 'core/user_list.html', {'users': users})


# @login_required
# def add_user(request):
#     if request.method == 'POST':
#         if request.user.role != 'admin':
#             return HttpResponse("Access Denied", status=403)

#         userId = int(request.POST.get('userId'))
#         role = request.POST.get('role')

#         # prevent duplicates
#         existing = users_col.find_one({'userId': userId})
#         if existing:
#             return HttpResponse("User ID already exists", status=400)

#         users_col.insert_one({'userId': userId, 'role': role})
#         return redirect('user_list')

@login_required
def add_user(request):
    if request.method == 'POST':
        if request.user.role != 'admin':
            return HttpResponse("Access Denied", status=403)

        userId = request.POST.get('userId')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')

        if not all([userId, first_name, last_name, phone_number, role]):
            return HttpResponse("Missing required fields", status=400)

        # prevent duplicates
        existing = users_col.find_one({'userId': userId})
        if existing:
            return HttpResponse("User ID already exists", status=400)

        user_data = {
            'userId': userId,
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'role': role
        }

        users_col.insert_one(user_data)
        return redirect('user_list')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            return HttpResponse("Invalid credentials", status=401)
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@csrf_exempt
@login_required
def update_student(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        students_col.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': data['name'],
                'surname': data['surname'],
                'grade': int(data['grade']),
                'group': int(data['group']),
            }}
        )
        return HttpResponse(status=204)


@csrf_exempt
@login_required
def delete_student(request, id):
    if request.method == 'POST':
        students_col.delete_one({'_id': ObjectId(id)})
        return HttpResponse(status=204)


@csrf_exempt
@login_required
def update_user(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        users_col.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'userId': int(data['userId']),
                'role': data['role'],
            }}
        )
        return HttpResponse(status=204)


@csrf_exempt
@login_required
def delete_user(request, id):
    if request.method == 'POST':
        users_col.delete_one({'_id': ObjectId(id)})
        return HttpResponse(status=204)


@csrf_protect
@login_required
def add_student(request):
    if request.method == 'POST':
        if request.user.role != 'admin':
            return HttpResponse("Access Denied", status=403)

        telegram_id = request.POST.get('telegram_id')
        surname = request.POST.get('surname')
        name = request.POST.get('name')
        grade = int(request.POST.get('grade'))
        group = int(request.POST.get('group'))

        # Default approval to "approved"
        approval = "approved"

        new_student = {
            "userId": int(telegram_id),
            "surname": surname,
            "name": name,
            "grade": grade,
            "group": group,
            "approval": approval,
        }
        students_col.insert_one(new_student)
        return redirect('student_list')
    else:
        return HttpResponse("Method not allowed", status=405)
