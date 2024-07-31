from django.db import connection
from django.contrib.auth.hashers import make_password
from datetime import datetime

def execute_query(query, params=None, fetchone=False, fetchall=False):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if fetchone:
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row)) if row else None
        if fetchall:
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        connection.commit()

def extract_user_data(request):
    errors = []
    data = {
        'first_name': request.POST.get('first_name'),
        'middle_name': request.POST.get('middle_name'),
        'last_name': request.POST.get('last_name'),
        'email_address': request.POST.get('email_address'),
        'password': request.POST.get('password'),
        'phone_number': request.POST.get('phone_number'),
        'gender': request.POST.get('gender'),
        'date_of_birth': request.POST.get('date_of_birth'),
        'address': request.POST.get('address'),
        'major': request.POST.get('major_or_department'),
        'bio': request.POST.get('bio'),
        'facebook': request.POST.get('facebook'),
        'twitter': request.POST.get('twitter'),
        'linkedIn': request.POST.get('linkedIn'),
        'github': request.POST.get('github'),
        'profile_picture': request.POST.get('profile_picture'),
    }

    if not data['first_name']:
        errors.append('First name is required.')
    if not data['middle_name']:
        errors.append('Middle name is required.')
    if not data['last_name']:
        errors.append('Last name is required.')
    
    if not data['phone_number']:
        errors.append('Phone number is required.')
    if not data['gender']:
        errors.append('Gender is required.')
    if not data['date_of_birth']:
        errors.append('Date of birth is required.')
    if not data['address']:
        errors.append('Address is required.')
    if not data['major']:
        errors.append('Major is required.')

    # check if is string the first name, middle name, last name, address, major
    if not data['first_name'].isalpha():
        errors.append('First name must be alphabetic.')

    if not data['middle_name'].isalpha():
        errors.append('Middle name must be alphabetic.')

    if not data['last_name'].isalpha():
        errors.append('Last name must be alphabetic.')


    # Validate email
    if data['email_address']:
        query = "SELECT * FROM students WHERE email_address = %s"
        student = execute_query(query, [data['email_address']], fetchone=True)
        if student:
            errors.append('Email address already exists.')


    if data['password']:
        if len(data['password']) < 8:
            errors.append('Password must be at least 8 characters long.')   

        if data['password'] != request.POST.get('confirm_password'):
            errors.append('Password and confirm password must be the same.')
    

    # Validate age
    if data['date_of_birth']:
        try:
            dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            age = (datetime.now() - dob).days // 365
            if age < 10:
                errors.append('Age must be greater than 10 years.')
        except ValueError:
            errors.append('Invalid date of birth format.')


    

    return data, errors


def hash_password(password):
    return make_password(password)

