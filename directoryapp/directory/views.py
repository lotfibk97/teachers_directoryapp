from django.shortcuts import render, redirect, reverse
import csv, io
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import include

#@login_required(login_url='/accounts/login')
def teachers(request):
    """all teachers """
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    form = SubjectForm()
    data = {'teachers':teachers,'subjects':subjects,'form':form}
    return render(request, 'teachers.html',data)

#@login_required(login_url='/accounts/login')
def add_teacher(request):
    """ add a teacher """
    if request.method == "POST":
        form = TeacherForm(request.POST or None)
        if form.is_valid():
            """ if the form is valid """
            obj = form.save(commit=False)
            if request.FILES.get('profile_picture') is None:
                obj.profile_picture = 'default.png'
            else:    
                obj.profile_picture = request.FILES.get('profile_picture')
            subjects = Subject.objects.all()
            obj.save()
            for subject in subjects:
                if request.POST.get(str(subject.id)) is not None:
                    a, _ = TeachingSubject.objects.update_or_create(subject=subject,teacher=obj)
            
            a.save()
            messages.success(request, 'The teacher has been added successfully!')
            return redirect(reverse('teachers'))
            """ redirect to teachers list """

        else:
            for field in form:
                if field.errors:
                    for error in field.errors:
                        messages.error(request, error)
                        print(error,field)            
            return redirect(reverse('teachers'))
            """ redirect to teachers list """
    else:
        form = TeacherForm()
        subjects = Subject.objects.all()
        data = {'form':form,'subjects':subjects}
        return render(request, 'add_teacher.html', data)

#@login_required(login_url='/accounts/login')
def edit_teacher(request, id):
    """ Edit teacher where id = id """

    
    try:
        teacher = Teacher.objects.get(id=id)
        """ get the teacher with id = id """

        if request.method == "POST":

            form = TeacherForm(request.POST or None,instance=teacher)

            if form.is_valid():
                """ if the form is valid """
                print("test")
                obj = form.save(commit=False)
                if request.FILES.get('profile_picture') is None:
                    obj.profile_picture = 'default.png'
                else:    
                    obj.profile_picture = request.FILES.get('profile_picture')
                subjects = Subject.objects.all()
                obj.save()
                for subject in subjects:
                    if request.POST.get(str(subject.id)) is not None:
                        a, _ = TeachingSubject.objects.update_or_create(subject=subject,teacher=obj)
                
                a.save()
                messages.success(request, "The teacher's informations have been updated successfully")
                """ show success message """

                return redirect(reverse('teachers'))
                """ redirect to teachers list """
            else:
                """ if the form is invalid """

                for field in form:
                    if field.errors:
                        for error in field.errors:
                            messages.error(request, error)
                            print(field)
                            """ show error message """

                return redirect(reverse('teachers'))
                """ redirect to teachers list """
        else:
            subjects = Subject.objects.all()
            teaching_subjects = TeachingSubject.objects.filter(teacher=teacher)
            subject_teached = []
            for teaching_subject in teaching_subjects:
                subject_teached.append(teaching_subject.subject)
            form = TeacherForm(instance=teacher)


            data = {'subject_teached':subject_teached,'teacher':teacher,'form':form,"teaching_subjects":teaching_subjects, 'subjects':subjects}
            return render(request, 'edit_teacher.html',data)

    except Teacher.DoesNotExist:
        """ if the teacher with id = id does not exist"""
        print("fail")
        messages.error(request, "this teacher doesn't exist")
        """ show error message """

        return redirect(reverse('teachers'))
        """ redirect to teachers list """

#@login_required(login_url='/accounts/login')
def delete_teacher(request, id):
    """ delete teacher where id = id"""

    try:
        teacher = Teacher.objects.get(id=id)
        """ get the teacher with id = id """
        valid = False
        if teacher != None:
            valid = True
        if valid:
            """ if pressed button is confirm  """
            try:
                teacher.delete()
                """ delete the teacher """
                messages.success(request, "The teacher have been deleted successfully.")
                """ show success message """
                return redirect(reverse('teachers'))
                """ redirect to teachers list """

            except Teacher.DoesNotExist:
                """
                if the teacher with id = id does not exist anymore
                """

                messages.error(request, "This teacher doesn't exist anymore.")
                """ show error message """

                return redirect(reverse('teachers'))
                """ redirect to teachers list """

            
            except:
                """
                if there are other exception
                """

                messages.error(request, "Error !")
                """ show error message """

                return redirect(reverse('teachers'))
                """ redirect to teachers list """

        data = {'teacher':teacher}
        return render(request, 'delete_teacher.html', data)

    except Teacher.DoesNotExist:
        """
        if the teacher with id = id does not exist
        """

        messages.error(request, "This teacher does not exist")
        """ show error message """

        return redirect(reverse('teachers'))
        """ redirect to teachers list """            

def teacher_profile(request, id):
    """getting the teacher with his id """
    teacher = Teacher.objects.get(pk=id)
    teaching_subjects = TeachingSubject.objects.filter(teacher=teacher)
    data = {'teacher':teacher, 'teaching_subjects':teaching_subjects,'count':teaching_subjects.count()}
    return render(request, 'teacher_profile.html',data)

def teacher_filtering_by_subject(request, content):
    #print(request.GET)
    filtered_teachers = []
    teaching_subjects = TeachingSubject.objects.all()
    for teaching_subject in teaching_subjects:
        print(teaching_subject.subject)
        print(content)
        if teaching_subject.subject.name.lower() == content.lower():
            filtered_teachers.append(teaching_subject.teacher)
    subjects = Subject.objects.all()        
    data = {'teachers':filtered_teachers,'subjects':subjects}
    return render(request, 'teachers.html',data)


def teacher_filtering_by_lastname(request, content):
    filtered_teachers = []
    teachers = Teacher.objects.all()
    #print(request.GET)
    for teacher in teachers:
        print(teacher)
        print(content)
        if teacher.last_name[0].lower()==content.lower():
            filtered_teachers.append(teacher)
    subjects = Subject.objects.all()        
    data = {'teachers':filtered_teachers,'subjects':subjects}
    return render(request, 'teachers.html',data)

@login_required(login_url='/accounts/login')
def csv_mass_import(request):
    #print("test")
    if request.method == 'GET':
        return redirect(reverse('teachers'))
    else:
        subjects = []
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            if column[0]!='First Name' and column[0]!='':
                if len(column[2]) > 5:
                    teacher, _ = Teacher.objects.update_or_create(
                        first_name=column[0],
                        last_name=column[1],
                        profile_picture=column[2],
                        email=column[3],
                        phone=column[4],
                        room_number=column[5],
                    )
                else:
                    teacher, _ = Teacher.objects.update_or_create(
                        first_name=column[0],
                        last_name=column[1],
                        profile_picture='default.png',
                        email=column[3],
                        phone=column[4],
                        room_number=column[5],
                    )    
                subjects=column[6].split(', ')
                for i in range(6,len(column)):
                    obj = Subject.objects.get_or_create(name=column[i].replace(' ','').replace('\"',''))
                    mySubject = Subject.objects.get(name=column[i].replace(' ','').replace('\"',''))
                    teaching_subject, _ = TeachingSubject.objects.update_or_create(
                        subject = mySubject,
                        teacher = teacher,
                    )    
        return redirect(reverse('teachers'))

#@login_required(login_url='/accounts/login')
def add_subject(request):
    """ add a teacher """
    if request.method == "POST":
        form = SubjectForm(request.POST or None)
        if form.is_valid():
            """ if the form is valid """
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, 'The subject has been added successfully!')
            return redirect(reverse('teachers'))
            """ redirect to teachers list """

        else:
            for field in form:
                if field.errors:
                    for error in field.errors:
                        messages.error(request, error)
                        print(error,field)            
            return redirect(reverse('teachers'))
            """ redirect to teachers list """
    else:
        fform = SubjectForm()
        data = {'fform':fform,}
        return redirect(reverse('teachers'))
