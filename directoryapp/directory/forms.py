from django import forms
#from datetime import date, time ,datetime
from .models import *
#from customauth.models import MyUser

# Monadim forms
class TeacherForm(forms.ModelForm):

    class Meta:

        model = Teacher
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['phone'].widget.attrs.update({'class':'form-control'})
        self.fields['room_number'].widget.attrs.update({'class':'form-control'})
        self.fields['profile_picture'].widget.attrs.update({'class':'form-control'})
        
 

class SubjectForm(forms.ModelForm):
    
    class Meta:

        model = Subject
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control'})