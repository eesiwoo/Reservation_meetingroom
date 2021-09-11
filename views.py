from django.shortcuts import render
from django.views.generic import View
from reservation.forms import LoginForm, DateForm, addRezForm, addOutsiderForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.db.models import Count, Q
from django.shortcuts import render
import logging
import datetime
import re
from reservation.models import ViRlogin, ViRezlist, ViUser, Meetingroom, RezMeetingroom, RezTimeInfo, RezOutsider, RezTimetable, ViRezlookup, ViOutsider, RezTimeShow

import traceback

logger = logging.getLogger(__name__)

time_lists = RezTimetable.objects.using('bi').all()
            #     {
            # '1' : '09:00', '2' : '09:30', '3' : '10:00', '4' : '10:30', '5' : '11:00',
            # '6' : '11:30', '7' : '12:00', '8' : '12:30', '9' : '13:00', '10' : '13:30',
            # '11' : '14:00', '12' : '14:30', '13' : '15:00', '14' : '15:30', '15' : '16:00',
            # '16' : '16:30', '17' : '17:00', '18' : '17:30', '19' : '18:00', '20' : '18:30',
            # '21' : '19:00'
            # , '1930' : '19:30', '2000' : '20:00', '2030' : '20:30', '2100' : '21:00'
            # }

# Create your views here.
class LoginView(View):
    form_class = LoginForm
    initial = {'key': 'value'}
    template_name = 'reservation/r_login.html'
    def get(self, request, *args, **kwargs):
        msg = ''
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'msg': msg})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            _id = form.cleaned_data['id']
            _pw = form.cleaned_data['pw']
            user = ViRlogin.objects.using('bi').filter(empno=_id)
            try:
                if user.count() == 0:   #아이디가 아예 없음.
                    logger.info('%s id error', _id) #logger.info > 로그 작성하는 명령
                    msg = '사번을 잘못 입력하셨습니다.'# 화면에 뜨는 메시지
                    form = self.form_class(initial=self.initial)
                    return render(request, self.template_name, {'form': form, 'msg': msg})
                elif user.count() > 1:  #공통 사번이 2개 이상일
                    logger.info('%s id error', _id)
                    msg = '로그인상에 오류가 발생하였습니다. 관리자에게 문의해주세요'
                    form = self.form_class(initial=self.initial)
                    return render(request, self.template_name, {'form': form, 'msg': msg})

                if _pw == user[0].passwd:   # 성공하면 세션에 아이디와 부서를 저장.
                    # rlogin = ViRlogin.objects.using('bi').all()
                    request.session['user']=_id
                    request.session['dept']=str(user[0].dept)
                    request.session.set_expiry(3600) #session time : 3600s
                    logger.info('%s login', _id)
                    now = datetime.datetime.now()
                    sysdate = now.strftime('%Y-%m-%d')
                    logger.info('%s user', sysdate)
                    user = ViRlogin.objects.using('bi').filter(empno=_id)
                    rezinfo = ViRezlist.objects.using('bi').filter(rez_date=sysdate)
                    meetingroom = Meetingroom.objects.using('bi').all()
                    time_list = time_lists
                    # sysdate =
                    return render(request, 'reservation/r_rez_list.html', {'sysdate' : sysdate, 'user':user[0], 'rezinfo' : rezinfo, 'meetingroom':meetingroom, 'time_list' : time_list})
                    # return HttpResponseRedirect(reverse('reservation:list')) #화면 이동(리스트로)
                else:
                    logger.info('%s password error', _id)   #비밀번호가 잘못되었을 때
                    msg = '비밀번호를 잘못 입력하셨습니다.'
                    form = self.form_class(initial=self.initial)
                    return render(request, self.template_name, {'form': form, 'msg': msg})
            except: #예외처리
                trace_back=traceback.format_exc()
                logger.info('%s login error', _id)
                logger.error('Login [FAIL] : \n%s', trace_back)
                msg = '로그인상에 오류가 발생하였습니다. 관리자에게 문의해주세요'
                form = self.form_class(initial=self.initial)
                return render(request, self.template_name, {'form': form, 'msg': msg})

        return HttpResponseRedirect(reverse('reservation:r_rez_list.html'))

# def Page(request):

class ListView(View):
    form_class = DateForm
    initial = {'key': 'value'}
    template_name = 'reservation/r_rez_list.html'
    def get(self, request, *args, **kwargs):
        sysdate = datetime.datetime.now().strftime('%Y-%m-%d')
        try :
            _id = request.session['user']
            user = ViRlogin.objects.using('bi').filter(empno=_id)
            rezinfo = ViRezlist.objects.using('bi').filter(rez_date=sysdate)
            meetingroom = Meetingroom.objects.using('bi').all()
            #time_list = time_lists
            return render(request, self.template_name, {'sysdate' : sysdate, 'user':user[0], 'rezinfo' : rezinfo, 'meetingroom':meetingroom, 'time_list' : time_lists})
        except :
            return render(request, 'reservation/r_login.html')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            date = request.POST['date']
            request.session['date']=date
            logger.info('%s', date)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect(reverse('reservation:list'))

class Hidden(View):
    form_class = DateForm
    initial = {'key': 'value'}
    template_name = 'reservation/r_hidden.html'
    def get(self, request, *args, **kwargs):
        try:
            sysdate = datetime.datetime.now().strftime('%Y-%m-%d')
            _id = request.session['user']
            user = ViRlogin.objects.using('bi').filter(empno=_id)
            rezinfo = ViRezlist.objects.using('bi').filter(rez_date=sysdate)
            meetingroom = Meetingroom.objects.using('bi').all()
            time_list = time_lists
            return render(request, self.template_name, {'sysdate' : sysdate, 'user':user[0], 'rezinfo' : rezinfo, 'meetingroom':meetingroom, 'time_list' : time_list})
        except :
            return render(request, 'reservation/r_login.html')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            date = request.POST['date']
            request.session['date']=date
            logger.info('%s', date)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect(reverse('reservation:hidden'))

class AddRezView(View):
    initial = {'key': 'value'}
    template_name = 'reservation/r_addRez.html'
    time_list = time_lists

    def insertTimeInfo(self, str_time, end_time, rez_date, room_name, rezno):
        insert_list = []
        insert_list2 = []
        # logger.info("insertTimeInfo def")
        # logger.info("str_time = %s", str_time)

        for time in self.time_list:
            str_time = int(str_time)
            end_time = int(end_time)
            time.key = int(time.key)
            if str_time <= time.key and time.key < end_time :
                insert_list.append(RezTimeInfo(
                            rezno = rezno,
                            room_name = room_name,
                            rez_date = rez_date,
                            time = time.key
                            ))
            if str_time <= time.key and time.key <= end_time :
                insert_list2.append(RezTimeShow(
                            rezno = rezno,
                            room_name = room_name,
                            rez_date = rez_date,
                            time = time.key
                            ))
        RezTimeInfo.objects.using('bi').bulk_create(insert_list)
        RezTimeShow.objects.using('bi').bulk_create(insert_list2)
        # logger.info("insert_list = %s", insert_list)
        # logger.info("bulk_create2")

    def get(self, request, *args, **kwargs):
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        meetingroom = Meetingroom.objects.using('bi').all()
        userList = ViUser.objects.using('bi').all()
        form = addRezForm()
        sysdate = datetime.datetime.now().strftime('%Y-%m-%d')
        rezlist = ViRezlist.objects.using('bi').all()
        return render(request, self.template_name, {'sysdate' : sysdate, 'user':user[0], 'form':form, 'time_list' : self.time_list, 'meetingroom' : meetingroom, 'userList':userList, 'rezlist':rezlist })

    def post(self, request, *args, **kwargs):
        form = addRezForm(request.POST)
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        now = datetime.datetime.now()
        sysdate = now.strftime('%Y-%m-%d')
        meetingroom = Meetingroom.objects.using('bi').all()
        rezlist = RezMeetingroom.objects.using('bi').all()
        time_list = time_lists
        str_time = request.POST['str_time']
        rez_date = request.POST['rez_date']
        room_name = request.POST['room_name']

        for i in rezlist :
            if i.rez_date == rez_date and i.room_name == room_name and i.str_time == str_time :
                return HttpResponseRedirect(reverse('reservation:list'))

        if form.is_valid():
            data = RezMeetingroom()
            str_time = form.cleaned_data['str_time']
            end_time = form.cleaned_data['end_time']
            rez_date = form.cleaned_data['rez_date']
            room_name = form.cleaned_data['room_name']
            data.room_name= room_name
            data.rez_date= rez_date
            data.str_time = str_time
            data.end_time = end_time
            data.organizer=form.cleaned_data['organizer']
            data.maker=form.cleaned_data['maker']
            data.title=form.cleaned_data['title']
            data.comments=form.cleaned_data['comments']
            data.attendee_1=form.cleaned_data['attendee_1']
            data.attendee_2=form.cleaned_data['attendee_2']
            data.attendee_3=form.cleaned_data['attendee_3']
            data.attendee_4=form.cleaned_data['attendee_4']
            data.attendee_5=form.cleaned_data['attendee_5']
            data.attendee_6=form.cleaned_data['attendee_6']
            data.attendee_7=form.cleaned_data['attendee_7']
            data.attendee_8=form.cleaned_data['attendee_8']
            data.attendee_9=form.cleaned_data['attendee_9']
            data.attendee_10=form.cleaned_data['attendee_10']
            data.save(using='bi')
            #logger.info('save data')
            rezno = RezMeetingroom.objects.using('bi').latest('rezno').rezno
            #logger.info('renzo = %s', rezno)
            self.insertTimeInfo(str_time, end_time, rez_date, room_name, rezno)
            #return HttpResponseRedirect(reverse('reservation:list'))
            rezinfo = ViRezlist.objects.using('bi').filter(rez_date=rez_date)
            return render(request, 'reservation/r_rez_list.html', {'sysdate' : rez_date, 'user':user[0], 'rezinfo' : rezinfo, 'meetingroom':meetingroom, 'time_list' : time_list})
        else:
            return HttpResponse(form.errors)

# 현황 페이지에서 바로 예약하기를 가는 경우
class NewRezView(View):
    initial = {'key': 'value'}
    template_name = 'reservation/r_newRez.html'
    time_list = time_lists

    def insertTimeInfo(self, str_time, end_time, rez_date, room_name, rezno):
        insert_list = []
        insert_list2 = []
        # logger.info("insertTimeInfo def")
        # logger.info("str_time = %s", str_time)

        for time in self.time_list:
            str_time = int(str_time)
            end_time = int(end_time)
            time.key = int(time.key)
            if str_time <= time.key and time.key < end_time :
                insert_list.append(RezTimeInfo(
                            rezno = rezno,
                            room_name = room_name,
                            rez_date = rez_date,
                            time = time.key
                            ))
            if str_time <= time.key and time.key <= end_time :
                insert_list2.append(RezTimeShow(
                            rezno = rezno,
                            room_name = room_name,
                            rez_date = rez_date,
                            time = time.key
                            ))
        RezTimeInfo.objects.using('bi').bulk_create(insert_list)
        RezTimeShow.objects.using('bi').bulk_create(insert_list2)
        # logger.info("insert_list = %s", insert_list)
        # logger.info("bulk_create2")

    def get(self, request, *args, **kwargs):
        time = request.GET['time']
        room = request.GET['room']
        sysdate2 = request.GET['sysdate']
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        meetingroom = Meetingroom.objects.using('bi').all()
        userList = ViUser.objects.using('bi').all()
        form = addRezForm()
        sysdate = datetime.datetime.now().strftime('%Y-%m-%d')
        rezlist = ViRezlist.objects.using('bi').all()
        return render(request, self.template_name, {'sysdate2':sysdate2, 'room':room, 'time':time, 'sysdate' : sysdate, 'user':user[0], 'form':form, 'time_list' : self.time_list, 'meetingroom' : meetingroom, 'userList':userList, 'rezlist':rezlist })

    def post(self, request, *args, **kwargs):
        form = addRezForm(request.POST)
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        now = datetime.datetime.now()
        sysdate = now.strftime('%Y-%m-%d')
        meetingroom = Meetingroom.objects.using('bi').all()
        rezlist = RezMeetingroom.objects.using('bi').all()
        time_list = time_lists
        str_time = request.POST['str_time']
        rez_date = request.POST['rez_date']
        room_name = request.POST['room_name']

        for i in rezlist :
            if i.rez_date == rez_date and i.room_name == room_name and i.str_time == str_time :
                return HttpResponseRedirect(reverse('reservation:list'))

        if form.is_valid():
            data = RezMeetingroom()
            str_time = form.cleaned_data['str_time']
            end_time = form.cleaned_data['end_time']
            rez_date = form.cleaned_data['rez_date']
            room_name = form.cleaned_data['room_name']
            data.room_name= room_name
            data.rez_date= rez_date
            data.str_time = str_time
            data.end_time = end_time
            data.organizer=form.cleaned_data['organizer']
            data.maker=form.cleaned_data['maker']
            data.title=form.cleaned_data['title']
            data.comments=form.cleaned_data['comments']
            data.attendee_1=form.cleaned_data['attendee_1']
            data.attendee_2=form.cleaned_data['attendee_2']
            data.attendee_3=form.cleaned_data['attendee_3']
            data.attendee_4=form.cleaned_data['attendee_4']
            data.attendee_5=form.cleaned_data['attendee_5']
            data.attendee_6=form.cleaned_data['attendee_6']
            data.attendee_7=form.cleaned_data['attendee_7']
            data.attendee_8=form.cleaned_data['attendee_8']
            data.attendee_9=form.cleaned_data['attendee_9']
            data.attendee_10=form.cleaned_data['attendee_10']
            data.save(using='bi')
            #logger.info('save data')
            rezno = RezMeetingroom.objects.using('bi').latest('rezno').rezno
            #logger.info('renzo = %s', rezno)
            self.insertTimeInfo(str_time, end_time, rez_date, room_name, rezno)
            # return HttpResponseRedirect(reverse('reservation:list'))
            rezinfo = ViRezlist.objects.using('bi').filter(rez_date=rez_date)
            return render(request, 'reservation/r_rez_list.html', {'sysdate' : rez_date, 'user':user[0], 'rezinfo' : rezinfo, 'meetingroom':meetingroom, 'time_list' : time_list})
        else:
            return HttpResponse(form.errors)


class EditRezView(View):
    initial = {'key': 'value'}
    template_name = 'reservation/r_editRez.html'
    time_list = time_lists

    def insertTimeInfo(self, str_time, end_time, rez_date, room_name, rezno):
        insert_list = []
        insert_list2 = []
        # logger.info("insertTimeInfo def")
        # logger.info("str_time = %s", str_time)

        for time in self.time_list:
            str_time = int(str_time)
            end_time = int(end_time)
            time.key = int(time.key)
            if str_time <= time.key and time.key < end_time :
                insert_list.append(RezTimeInfo(
                            rezno = rezno,
                            room_name = room_name,
                            rez_date = rez_date,
                            time = time.key
                            ))
            if str_time <= time.key and time.key <= end_time :
                insert_list2.append(RezTimeShow(
                            rezno = rezno,
                            room_name = room_name,
                            rez_date = rez_date,
                            time = time.key
                            ))
        #기존 데이터 삭제 후 재생성
        RezTimeInfo.objects.using('bi').filter(rezno=rezno).delete()
        RezTimeShow.objects.using('bi').filter(rezno=rezno).delete()
        RezTimeInfo.objects.using('bi').bulk_create(insert_list)
        RezTimeShow.objects.using('bi').bulk_create(insert_list2)
        #logger.info("bulk_create2")

    def get(self, request, *args, **kwargs):
        rezno = request.GET['rezno']
        _id = request.session['user']
        datas = ViRezlookup.objects.using('bi').filter(rezno=rezno)
        organizer_temp = RezMeetingroom.objects.using('bi').filter(rezno=rezno).values('organizer')
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        organizer = ViRlogin.objects.using('bi').filter(emp_hname__in=organizer_temp)
        org_len = len(organizer) # 주최자가 내부인인지, 외부인인지 확인한다.
        meetingroom = Meetingroom.objects.using('bi').all()
        userList = ViUser.objects.using('bi').all()
        form = addRezForm()
        sysdate = datetime.datetime.now().strftime('%Y-%m-%d')
        rezlist = ViRezlist.objects.using('bi').filter(~Q(rezno=rezno))
        if org_len < 1 : # 주최자가 외부인일 경우
            organizer = [{'emp_hname' : organizer_temp[0]['organizer'], 'dept_name':'외부인'}]
            return render(request, self.template_name, {'rezlist':rezlist, 'datas':datas, 'organizer':organizer, 'sysdate' : sysdate, 'user':user[0], 'form':form, 'time_list' : self.time_list, 'meetingroom' : meetingroom, 'userList':userList})
        else : # 주최자가 내부인일 경우 (ViRlogin안에 있을 경우)
            return render(request, self.template_name, {'rezlist':rezlist, 'datas':datas, 'organizer':organizer, 'sysdate' : sysdate, 'user':user[0], 'form':form, 'time_list' : self.time_list, 'meetingroom' : meetingroom, 'userList':userList})

    def post(self, request, *args, **kwargs):
        rezno = request.GET['rezno']
        logger.info("in post rezno=%s", rezno)
        form = addRezForm(request.POST)
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        now = datetime.datetime.now()
        sysdate = now.strftime('%Y-%m-%d')
        meetingroom = Meetingroom.objects.using('bi').all()
        rezlist = RezMeetingroom.objects.using('bi').all()
        time_list = time_lists
        str_time = request.POST['str_time']
        rez_date = request.POST['rez_date']
        room_name = request.POST['room_name']
        if form.is_valid():
            data = RezMeetingroom.objects.using('bi').get(rezno=rezno)
            str_time = form.cleaned_data['str_time']
            end_time = form.cleaned_data['end_time']
            rez_date = form.cleaned_data['rez_date']
            room_name = form.cleaned_data['room_name']
            data.room_name = room_name
            data.rez_date= rez_date
            data.str_time = str_time
            data.end_time = end_time
            data.organizer=form.cleaned_data['organizer']
            data.maker=form.cleaned_data['maker']
            data.title=form.cleaned_data['title']
            data.comments=form.cleaned_data['comments']
            data.attendee_1=form.cleaned_data['attendee_1']
            data.attendee_2=form.cleaned_data['attendee_2']
            data.attendee_3=form.cleaned_data['attendee_3']
            data.attendee_4=form.cleaned_data['attendee_4']
            data.attendee_5=form.cleaned_data['attendee_5']
            data.attendee_6=form.cleaned_data['attendee_6']
            data.attendee_7=form.cleaned_data['attendee_7']
            data.attendee_8=form.cleaned_data['attendee_8']
            data.attendee_9=form.cleaned_data['attendee_9']
            data.attendee_10=form.cleaned_data['attendee_10']
            data.save(using='bi')
            # logger.info('test, insert rez')
            self.insertTimeInfo(str_time, end_time, rez_date, room_name, rezno)
            # logger.info('test, insert rez time info done')
            # return HttpResponseRedirect(reverse('reservation:list'))
            rezinfo = ViRezlist.objects.using('bi').filter(rez_date=rez_date)
            return render(request, 'reservation/r_rez_list.html', {'sysdate' : rez_date, 'user':user[0], 'rezinfo' : rezinfo, 'meetingroom':meetingroom, 'time_list' : time_list})
        else:
            return HttpResponse(form.errors)

def timecheck(request):
    roomName = request.GET['room_name']
    rezDate = request.GET['rez_date']
    timeinfo = RezTimeShow.objects.using('bi').filter(rez_date=rezDate, room_name=roomName)
    timeinfo = list(timeinfo.values())
    # logger.info('timeinfo test=%s', timeinfo)
    return JsonResponse(timeinfo, safe=False)


def usercheck(request):
    words = request.GET['words']
    #logger.info("words is = %s", words)
    name = ViUser.objects.using('bi').filter(name=words)
    #logger.info("name is = %s", name)
    name = list(name.values())
    return JsonResponse(name, safe=False)


def search(request):
    words = request.GET['words']
    #logger.info('word test=%s',words)
    user = ViUser.objects.using('bi').filter(name=words)
    user = list(user.values())
    #logger.info('nameList test=%s', nameList)
    return JsonResponse(user, safe=False)

def rezList(request):
    sysdate = request.GET['sysdate']
    rezList = ViRezlist.objects.using('bi').filter(rez_date=sysdate)
    rezList = list(rezList.values())
    return JsonResponse(rezList, safe=False)

class AddOutsiderView(View):
    initial = {'key': 'value'}
    template_name = 'reservation/r_add_outsider.html'

    def get(self, request, *args, **kwargs):
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        outsiderList = RezOutsider.objects.using('bi').all()
        form = addOutsiderForm()
        return render(request, self.template_name, {'user':user[0], 'form': form})

    def post(self, request, *args, **kwargs):
        form = addOutsiderForm(data = request.POST)
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)

        if form.is_valid():
            dataoutsider = RezOutsider()
            dataoutsider.emp_hname = user[0].emp_hname
            out_coname = form.cleaned_data['out_coname']
            out_name = form.cleaned_data['out_name'] + "(외부)"
            out_position = form.cleaned_data['out_position']
            out_phone = form.cleaned_data['out_phone']
            out_email = form.cleaned_data['out_email']
            dataoutsider.out_coname= out_coname
            dataoutsider.out_name= out_name
            dataoutsider.out_position = out_position
            dataoutsider.out_phone = out_phone
            dataoutsider.out_email = out_email

            dataoutsider.save(using='bi')
            # logger.info("333333")

            return HttpResponseRedirect(reverse('reservation:outsiderlist'))

def do_duplicate_check(request): # 외부인 중복 확인 함수
    out_phone = request.GET.get('out_phone')
    # logger.info(out_phone)
    # try:
    _id = RezOutsider.objects.using('bi').filter(out_phone=out_phone)
        # logger.info(_id)
    # except:
        # _id = None

    if _id :
        logger.info("fail")
        duplicate = "fail"
    else:
        logger.info("pass")
        duplicate = "pass"

    logger.info(duplicate)
    context = {'duplicate': duplicate}
    return JsonResponse(context, safe=False)

def email_check(request): #이메일 형식 체크 정규"
    email_ck = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    email = request.GET.get('out_email')

    check = email_ck.match(email)

    if check is None:
        check_email = "fail"
        logger.info("fail")
    else:
        check_email = "pass"
        logger.info("pass")

    context = {'check_email':check_email}
    return JsonResponse(context, safe=False)

def phone_check(request): #핸드폰 형식 체크 정규"
    phone_ck = re.compile('\d{3}-\d{3,4}-\d{4}')
    phone = request.GET.get('out_phone')

    phone = phone_ck.match(phone)

    if phone is None:
        check_phone = "fail"
        logger.info("fail")
    else:
        check_phone = "pass"
        logger.info("pass")

    context = {'check_phone':check_phone}
    return JsonResponse(context, safe=False)

class OutsiderListView(View):
    form_class = DateForm
    initial = {'key': 'value'}
    template_name = 'reservation/r_outsider_list.html'
    page_item_num = 10

    def get(self, request, *args, **kwargs):
        sysdate = datetime.datetime.now().strftime('%Y-%m-%d')
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        outsider = ViOutsider.objects.using('bi').all()
        count_outsider = outsider.values('out_name', 'out_phone').annotate(cnt=Count('out_phone')).order_by('out_name')
        paginator = Paginator(outsider, self.page_item_num)
        page = request.GET.get('page')
        try:
          outsiderlist = paginator.page(page)
        except PageNotAnInteger:
          outsiderlist = paginator.page(1)
        except EmptyPage:
          outsiderlist = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'sysdate' : sysdate, 'user':user[0],'outsiderlist':outsiderlist,'count_outsider':count_outsider})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            date = request.POST['date']
            request.session['date']=date
            outsider = RezOutsider.objects.using('bi').all().order_by('out_name')

            count_outsider = outsider.values('out_name', 'out_phone').annotate(cnt=Count('out_phone')).order_by('out_name')
            paginator = Paginator(outsider, self.page_item_num)
            page = request.GET.get('page')
            try:
              outsiderlist = paginator.page(page)
            except PageNotAnInteger:
              outsiderlist = paginator.page(1)
            except EmptyPage:
              outsiderlist = paginator.page(paginator.num_pages)
            return render(request, self.template_name, {'form': form,'count_outsider':count_outsider})
        else:
            return HttpResponseRedirect(reverse('reservation:outsiderlist'))

def bbs_search(request):
    type = request.POST['type']
    keyword = request.POST['keyword']

    if type == "conname":
        searchs = ViOutsider.objects.using('bi').filter(out_coname__icontains = keyword)
    if type == "name":
        searchs = ViOutsider.objects.using('bi').filter(out_name__icontains = keyword)
    if type == "phone":
        searchs = ViOutsider.objects.using('bi').filter(out_phone__icontains = keyword)

    data = list(searchs.values())
    return JsonResponse(data, safe=False)

class ModifyRezView(View):
    form_class = DateForm
    initial = {'key': 'value'}
    template_name = 'reservation/r_modify_rez.html'

    def get(self, request, *args, **kwargs):
        sysdate = datetime.datetime.now().strftime('%Y-%m-%d')
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        return render(request, self.template_name, {'sysdate' : sysdate, 'user':user[0]})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            date = request.POST['date']
            request.session['date']=date
            logger.info('%s', date)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect(reverse('reservation:modify'))


class FutureRezView(View):
    form_class = DateForm
    initial = {'key': 'value'}
    template_name = 'reservation/r_my_future_rez.html'

    def get(self, request, *args, **kwargs):
        sysdate = datetime.datetime.now() #현재날짜 가져오기
        sysdate2 = datetime.datetime.now().strftime('%Y-%m-%d')
        plus = sysdate + datetime.timedelta(days=30) # +30일
        future = plus.strftime('%Y-%m-%d')

        id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=id)
        name = user[0].emp_hname
        logger.info("여기용")
        logger.info(name)
        reservation = ViRezlookup.objects.using('bi').filter(Q(rez_date__range = [sysdate2, future]) & (Q(maker__icontains = name) | Q(organizer__icontains = name) | Q(attendee_1__icontains = name) #로그인 한 유저 이름이 주최자/참석자에 포함되면 저장
        | Q(attendee_2__icontains = name) | Q(attendee_3__icontains = name) | Q(attendee_4__icontains = name) | Q(attendee_5__icontains = name) | Q(attendee_6__icontains = name) | Q(attendee_7__icontains = name) | Q(attendee_8__icontains = name)
        | Q(attendee_9__icontains = name) | Q(attendee_10__icontains = name))).values_list('rezno').order_by('rez_date')

        data = list(reservation.values())
        logger.info(data)

        return render(request, self.template_name, {'sysdate' : sysdate, 'data':data, 'user':user[0], 'id':id, 'name':name})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        sysdate = datetime.datetime.now() #현재날짜 가져오기
        sysdate2 = datetime.datetime.now().strftime('%Y-%m-%d')
        plus = sysdate + datetime.timedelta(days=30) # +30일
        future = plus.strftime('%Y-%m-%d')

        if form.is_valid():
            _id = request.session['user']
            user = ViRlogin.objects.using('bi').filter(empno=_id)
            name = user[0].emp_hname

            reservation = ViRezlookup.objects.using('bi').filter(Q(rez_date__range = [sysdate2, future]) & (Q(organizer__icontains = name) | Q(attendee_1__icontains = name) #로그인 한 유저 이름이 주최자/참석자에 포함되면 저장
            | Q(attendee_2__icontains = name) | Q(attendee_3__icontains = name) | Q(attendee_4__icontains = name) | Q(attendee_5__icontains = name) | Q(attendee_6__icontains = name) | Q(attendee_7__icontains = name) | Q(attendee_8__icontains = name)
            | Q(attendee_9__icontains = name) | Q(attendee_10__icontains = name))).values_list('rezno').order_by('rez_date')

            data = list(reservation.values())

            return render(request, self.template_name, {'form': form, 'sysdate':sysdate, 'data':data})
        else:
            return HttpResponseRedirect(reverse('reservation:future'))

def delete(request, pk):
    delete1 = RezTimeShow.objects.using('bi').filter(rezno = pk)
    delete2 = RezMeetingroom.objects.using('bi').filter(rezno = pk)
    delete3 = RezTimeInfo.objects.using('bi').filter(rezno = pk)
    # delete4 = ViRezlist.objects.using('bi').filter(rezno = pk)
    delete1.delete()
    delete2.delete()
    delete3.delete()
    # delete4.delete()
    return HttpResponseRedirect(reverse('reservation:future'))

class PastRezView(View):
    form_class = DateForm
    initial = {'key': 'value'}
    template_name = 'reservation/r_my_past_rez.html'

    def get(self, request, *args, **kwargs):
        sysdate = datetime.datetime.now() #현재날짜 가져오기
        sysdate2 = sysdate + datetime.timedelta(days=-1)
        minus = sysdate + datetime.timedelta(days=-30) # +30일
        past = minus.strftime('%Y-%m-%d')

        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        name = user[0].emp_hname

        reservation = ViRezlookup.objects.using('bi').filter(Q(rez_date__range = [past, sysdate2]) & (Q(organizer__icontains = name) | Q(attendee_1__icontains = name) #로그인 한 유저 이름이 주최자/참석자에 포함되면 저장
        | Q(attendee_2__icontains = name) | Q(attendee_3__icontains = name) | Q(attendee_4__icontains = name) | Q(attendee_5__icontains = name) | Q(attendee_6__icontains = name) | Q(attendee_7__icontains = name) | Q(attendee_8__icontains = name)
        | Q(attendee_9__icontains = name) | Q(attendee_10__icontains = name))).order_by('rez_date')

        data = list(reservation.values())
        logger.info(data)

        return render(request, self.template_name, {'sysdate' : sysdate, 'data':data, 'user':user[0]})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        sysdate = datetime.datetime.now() #현재날짜 가져오기
        sysdate2 = sysdate + datetime.timedelta(days=-1)
        minus = sysdate + datetime.timedelta(days=-30) # +30일
        past = minus.strftime('%Y-%m-%d')

        if form.is_valid():
            date = request.POST['date']
            _id = request.session['user']
            user = ViRlogin.objects.using('bi').filter(empno=_id)
            name = user[0].emp_hname

            reservation = ViRezlookup.objects.using('bi').filter(Q(rez_date__range = [past, sysdate2]) & (Q(organizer__icontains = name) | Q(attendee_1__icontains = name) #로그인 한 유저 이름이 주최자/참석자에 포함되면 저장
            | Q(attendee_2__icontains = name) | Q(attendee_3__icontains = name) | Q(attendee_4__icontains = name) | Q(attendee_5__icontains = name) | Q(attendee_6__icontains = name) | Q(attendee_7__icontains = name) | Q(attendee_8__icontains = name)
            | Q(attendee_9__icontains = name) | Q(attendee_10__icontains = name))).order_by('rez_date')

            data = list(reservation.values())

            return render(request, self.template_name, {'form': form, 'data':data})
        else:
            return HttpResponseRedirect(reverse('reservation:past'))


class TblView(View):
    form_class = DateForm
    initial = {'key': 'value'}
    template_name = 'reservation/r_tbl_base.html'

    def get(self, request, *args, **kwargs):
        sysdate = datetime.datetime.now().strftime('%Y-%m-%d')
        _id = request.session['user']
        user = ViRlogin.objects.using('bi').filter(empno=_id)
        return render(request, self.template_name, {'sysdate' : sysdate, 'user':user[0]})

def Logout(request):
    logger.info('logout')
    del request.session['user']
    del request.session['auth']
    return HttpResponseRedirect(reverse('reservation:login'))
