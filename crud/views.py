from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Genders, Users
from django.contrib.auth.hashers import make_password

# Create your views here.

def gender_list(request):
    try:
        genders = Genders.objects.all() # SELECT * FROM tbl_genders

        data = {
            'genders': genders
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during load genders: {e}')

def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')

            Genders.objects.create(gender=gender) # INSERT INTO tbl_genders(gender) VALUES(gender);
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during add gender: {e}')

def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE gender_id = genderId;

            gender = request.POST.get('gender')

            genderObj.gender = gender
            genderObj.save() # UPDATE tbl_genders SET gender = gender WHERE gender_id = genderId;

            messages.success(request, 'Gender updated successfully!')

            data = {
                'gender': genderObj
            }

            return render(request, 'gender/EditGender.html', data)
        else: 
            genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE gender_id = genderId;

            data = {
                'gender': genderObj
            }

            return render(request, 'gender/EditGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during edit gender: {e}')
    
def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE gender_id = genderId;
            genderObj.delete() # DELETE FROM tbl_gender_id = genderId

            messages.success(request, 'Gender deleted successfully!')
            return redirect('/gender/list')
        else:
            genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE gender_id = genderId;

            data = {
                'gender': genderObj
            }

            return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during delete gender: {e}')
    
def user_list(request):
    try:
        users = Users.objects.select_related('gender')
        paginator = Paginator(users, 15)  # 15 rows per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        data = {'users': page_obj}
        return render(request, 'user/UsersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during load users: {e}')

def add_user(request):
    try:
        if request.method == 'POST':
            fullName = request.POST.get('full_name', '').strip()
            gender = request.POST.get('gender', '').strip()
            birthDate = request.POST.get('birth_date', '').strip()
            address = request.POST.get('address', '').strip()
            contactNumber = request.POST.get('contact_number', '').strip()
            email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            confirmPassword = request.POST.get('confirm_password', '').strip()
            profilePicture = request.FILES.get('profile_picture')

            if not fullName:
                messages.error(request, 'Full name is required.')
                return redirect('/user/add')

            if not email:
                messages.error(request, 'Email is required.')
                return redirect('/user/add')

            if not gender:
                messages.error(request, 'Gender is required.')
                return redirect('/user/add')

            if not username:
                messages.error(request, 'Username is required.')
                return redirect('/user/add')

            if not birthDate:
                messages.error(request, 'Birth date is required.')
                return redirect('/user/add')

            if not address:
                messages.error(request, 'Address is required.')
                return redirect('/user/add')

            if not contactNumber:
                messages.error(request, 'Contact number is required.')
                return redirect('/user/add')

            if not password:
                messages.error(request, 'Password is required.')
                return redirect('/user/add')

            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
                return redirect('/user/add')

            if password != confirmPassword:
                messages.error(request, 'Passwords do not match.')
                return redirect('/user/add')

            if Users.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken.')
                return redirect('/user/add')

            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('/user/add')

            Users.objects.create(
                full_name=fullName,
                gender=Genders.objects.get(pk=gender),
                birth_date=birthDate,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                profile_picture=profilePicture,
                password=make_password(password)
            )

            messages.success(request, 'User added successfully!')
            return redirect('/user/add')

        else:
            genderObj = Genders.objects.all()
            data = {'genders': genderObj}
            return render(request, 'user/Adduser.html', data)

    except Exception as e:
        return HttpResponse(f'Error occurred during add user: {e}')

def edit_user(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)

            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            profilePicture = request.FILES.get('profile_picture')

            userObj.full_name = fullName
            userObj.gender = Genders.objects.get(pk=gender)
            userObj.birth_date = birthDate
            userObj.address = address
            userObj.contact_number = contactNumber
            userObj.email = email
            userObj.username = username

            if profilePicture:
                userObj.profile_picture = profilePicture

            userObj.save()

            messages.success(request, 'User updated successfully!')

            genderObj = Genders.objects.all()

            data = {
                'user': userObj,
                'genders': genderObj
            }

            return render(request, 'user/EditUser.html', data)

        else:
            userObj = Users.objects.get(pk=userId)
            genderObj = Genders.objects.all()

            data = {
                'user': userObj,
                'genders': genderObj
            }

            return render(request, 'user/EditUser.html', data)

    except Exception as e:
        return HttpResponse(f'Error occurred during edit user: {e}')


def delete_user(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)
            userObj.delete()

            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list')

        else:
            userObj = Users.objects.get(pk=userId)

            data = {
                'user': userObj
            }

            return render(request, 'user/DeleteUser.html', data)

    except Exception as e:
        return HttpResponse(f'Error occurred during delete user: {e}')