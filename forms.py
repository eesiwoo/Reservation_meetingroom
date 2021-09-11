from django import forms
from reservation.models import ViRlogin, RezMeetingroom, RezTimeInfo, RezOutsider
import datetime

class LoginForm(forms.Form):    #로그인을 위한 form
    id = forms.CharField(max_length=10, help_text='아이디')
    pw = forms.CharField(widget=forms.PasswordInput, max_length=20, help_text='비밀번호')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'autofocus':'autofocus'})

class DateForm(forms.Form):
    date = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.DateInput(format='%Y/%m/%d', attrs={'class':'fromdatepicker'}), initial=datetime.date.today, label='날짜 ')
    # room = forms.ChoiceField(choices=R_CHOICE, label='회의실', required=True)

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'autofocus':'autofocus'})

class addRezForm(forms.Form):
    room_name = forms.CharField(required=True)
    rez_date = forms.CharField(required=True)
    str_time = forms.CharField(required=True)
    end_time = forms.CharField(required=True)
    organizer = forms.CharField(required=True)
    maker = forms.CharField(required=True)
    title = forms.CharField(required=True)
    comments = forms.CharField(required=True)
    attendee_1 = forms.CharField(required=True)
    attendee_2 = forms.CharField(required=False)
    attendee_3 = forms.CharField(required=False)
    attendee_4 = forms.CharField(required=False)
    attendee_5 = forms.CharField(required=False)
    attendee_6 = forms.CharField(required=False)
    attendee_7 = forms.CharField(required=False)
    attendee_8 = forms.CharField(required=False)
    attendee_9 = forms.CharField(required=False)
    attendee_10 = forms.CharField(required=False)

class addOutsiderForm(forms.Form):
    out_coname = forms.CharField(required=True)
    out_name = forms.CharField(required=True)
    out_position = forms.CharField(required=False)
    out_phone = forms.CharField(required=True)
    out_email = forms.CharField(required=False)
