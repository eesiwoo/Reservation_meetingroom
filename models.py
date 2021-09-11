# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViRlogin(models.Model):
    empno = models.BigIntegerField(primary_key=True)
    passwd = models.TextField(blank=True, null=True)
    emp_hname = models.TextField(blank=True, null=True)
    dept_name = models.TextField(blank=True, null=True)
    position_name = models.TextField(blank=True, null=True)
    h_phone = models.TextField(blank=True, null=True)
    dept = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VI_RLOGIN'


class RezMeetingroom(models.Model):
    rezno = models.CharField(primary_key=True, max_length=255)
    room_name = models.CharField(unique=True, max_length=255)
    rez_date = models.CharField(unique=True, max_length=255)
    str_time = models.CharField(unique=True, max_length=255)
    end_time = models.CharField(unique=True, max_length=255)
    organizer = models.CharField(unique=True, max_length=255)
    maker = models.CharField(unique=True, max_length=255)
    title = models.CharField(unique=True, max_length=255)
    comments = models.TextField(unique=True)
    attendee_1 = models.CharField(unique=True, max_length=255)
    attendee_2 = models.CharField(blank=True, null=True, max_length=255)
    attendee_3 = models.CharField(blank=True, null=True, max_length=255)
    attendee_4 = models.CharField(blank=True, null=True, max_length=255)
    attendee_5 = models.CharField(blank=True, null=True, max_length=255)
    attendee_6 = models.CharField(blank=True, null=True, max_length=255)
    attendee_7 = models.CharField(blank=True, null=True, max_length=255)
    attendee_8 = models.CharField(blank=True, null=True, max_length=255)
    attendee_9 = models.CharField(blank=True, null=True, max_length=255)
    attendee_10 = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'REZ_MEETINGROOM'


class RezOutsider(models.Model):
    emp_hname = models.CharField(max_length=127)
    out_coname = models.CharField(null=False, max_length=255)
    out_name = models.CharField(null=False, max_length=127)
    out_position = models.CharField(blank=True, null=True, max_length=63)
    out_phone = models.CharField(primary_key=True, null=False, max_length=16)
    out_email = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'REZ_OUTSIDER'


class RezTimeInfo(models.Model):
    rezno = models.CharField(blank=True, null=True, primary_key=True)
    room_name = models.CharField(blank=True, null=True)
    rez_date = models.CharField(blank=True, null=True)
    time = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'REZ_TIME_INFO'

class RezTimeShow(models.Model):
    rezno = models.CharField(blank=True, null=True, primary_key=True)
    room_name = models.CharField(blank=True, null=True)
    rez_date = models.CharField(blank=True, null=True)
    time = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'REZ_TIME_SHOW'


class RezTimetable(models.Model):
    key = models.CharField(blank=True, null=True, primary_key=True)
    time = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'REZ_TIMETABLE'


class Meetingroom(models.Model):
    room_name = models.TextField(primary_key=True)
    max_number = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MEETINGROOM'


class ViRezlist(models.Model):
    time = models.CharField(max_length=20, db_collation='USING_NLS_COMP', blank=True, null=True)
    rezno = models.BigIntegerField(primary_key=True)
    rez_date = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    room_name = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    str_time = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    str_timetable = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    end_time = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    end_timetable = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    organizer = models.CharField(max_length=40, db_collation='USING_NLS_COMP')
    maker = models.CharField(max_length=40, db_collation='USING_NLS_COMP')
    title = models.CharField(max_length=400, db_collation='USING_NLS_COMP')
    comments = models.CharField(max_length=4000, db_collation='USING_NLS_COMP')
    attendee_1 = models.CharField(max_length=40, db_collation='USING_NLS_COMP')
    attendee_2 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_3 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_4 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_5 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_6 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_7 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_8 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_9 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_10 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vi_rezlist'

class ViRezlookup(models.Model):
    rezno = models.BigIntegerField(primary_key=True)
    rez_date = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    room_name = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    str_time = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    str_timetable = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    end_time = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    end_timetable = models.CharField(max_length=20, db_collation='USING_NLS_COMP')
    organizer = models.CharField(max_length=40, db_collation='USING_NLS_COMP')
    maker = models.CharField(max_length=40, db_collation='USING_NLS_COMP')
    title = models.CharField(max_length=400, db_collation='USING_NLS_COMP')
    comments = models.CharField(max_length=4000, db_collation='USING_NLS_COMP')
    attendee_1 = models.CharField(max_length=40, db_collation='USING_NLS_COMP')
    attendee_2 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_3 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_4 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_5 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_6 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_7 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_8 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_9 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    attendee_10 = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vi_rezlookup'


class ViUser(models.Model):
    num = models.CharField(max_length=3, db_collation='USING_NLS_COMP', blank=True, null=True)
    name = models.CharField(max_length=40, db_collation='USING_NLS_COMP', blank=True, null=True)
    position = models.CharField(max_length=4000, db_collation='USING_NLS_COMP', blank=True, null=True, primary_key=True)
    phone = models.CharField(max_length=200, db_collation='USING_NLS_COMP', blank=True, null=True)
    dept = models.CharField(max_length=200, db_collation='USING_NLS_COMP', blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vi_user'

class ViOutsider(models.Model):
    emp_hname = models.CharField(max_length=127)
    out_coname = models.CharField(null=False, max_length=255)
    out_name = models.CharField(null=False, max_length=127)
    out_position = models.CharField(blank=True, null=True, max_length=63)
    out_phone = models.CharField(primary_key=True, null=False, max_length=16)
    out_email = models.CharField(blank=True, null=True, max_length=255)
    masking = models.CharField(max_length=4000, db_collation='USING_NLS_COMP', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VI_OUTSIDER'
