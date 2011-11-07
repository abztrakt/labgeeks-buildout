from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf

from people.models import UserProfile, TimePeriod
from chronos.models import Location
from schedule.models import *
from schedule.forms import SelectTimePeriodForm, SelectDailyScheduleForm, CreateDailyScheduleForm

#EDIT LATER
from datetime import date, datetime, time, timedelta
def list_options(request):

    if not request.user.is_superuser:
        message = 'Permission Denied'
        reason = 'You do not have permission to visit this part of the page.'
        return render_to_response('fail.html', locals(),context_instance=RequestContext(request))

    c = {}
    c.update(csrf(request))

    timeperiod_stats = []
    timeperiod_users = []
    timeperiods = TimePeriod.objects.all().order_by('start_date')

    for timeperiod in timeperiods:
        people = UserProfile.objects.filter(working_periods__name=timeperiod.name)
        data = {
            'timeperiod': timeperiod.name,
            'start_date': timeperiod.start_date,
            'end_date': timeperiod.end_date,
            'count': people.count()
            }

        users = {
            'timeperiod': timeperiod.name,
            'people': people
        }
        timeperiod_stats.append(data)
        timeperiod_users.append(users)

    if not timeperiods:
        message = 'Nobody available for timeperiods or nobody filled out preferences'
        
    return render_to_response('schedule_home.html',locals(), context_instance=RequestContext(request))

def view_available_shifts(request):
    ''' Display a list of all available shifts. (Shifts that have no user attached to them)
    '''
    #Grab all available shifts
    data = WorkShift.objects.filter(person=None)

    shifts=[]
    for shift in data:
        x = {'day':shift.scheduled_in.date(),'scheduled_in':shift.scheduled_in.time(),'scheduled_out':shift.scheduled_out.time(),'location':shift.location}
        shifts.append(x)
    
    if not shifts:
        message = "No available shifts."

    return render_to_response('available.html', locals(), context_instance=RequestContext(request))

def view_shifts(request):
    ''' Display a list of scheduled work shifts. Allows user to specify which day they want to look at.
    '''
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = SelectDailyScheduleForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            location = form.cleaned_data['location']
            data = WorkShift.objects.filter(scheduled_in__day=day.day,scheduled_in__month=day.month,scheduled_in__year=day.year,person__isnull=False,location__name=location).order_by('person__username')
            if not data:
                message = 'Nobody scheduled for %s' %  (day)
            else:

                # TODO EDIT LATER
                x_axis = []
                y_axis = []
                grouping = []

                # x_axis
                # maybe dont need this... for now.
                '''
                weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                starting = day - timedelta(days = day.weekday())
                for i in range(0,7):
                    x = {'day' : weekdays[i],'date':starting + timedelta(days = i)}
                    x_axis.append(x)
                '''

                # y_axis - The time scale
                counter = datetime(day.year,day.month,day.day,7,0)

                while counter.hour != 1:
                    y_axis.append(counter.time())
                    counter += timedelta(minutes=30)
                
                #Grab the unique users from the shifts.
                unique_people = data.values('person__username').distinct()
                people = []
                for person in unique_people:
                    people.append(person['person__username'])

                shifts = []
                        
                for time in y_axis:
                    x = {'time':time, 'people':[]}

                    for shift in data:
                        if shift.scheduled_in.time() <= time and shift.scheduled_out.time() >= time:
                            x['people'].append(shift.person)
                        else:
                            x['people'].append(None)

                    while len(x['people']) != len(people):
                        x['people'].append(None)


                    shifts.append(x)
        
    else:
        form = SelectDailyScheduleForm()

    return render_to_response('view_shifts.html', locals(),context_instance=RequestContext(request))


def create_default_daily_schedule(request):
    if request.method == 'POST':
        form = CreateDailyScheduleForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            day_defaults = DefaultShift.objects.filter(day=day).order_by('in_time')

            if not day_defaults:
                message = 'No default shifts created for %s' % (day)
    else:
        form = CreateDailyScheduleForm()
    
    return render_to_response('create_schedule.html', locals(), context_instance=RequestContext(request))

def view_preferences(request,form):
    pass


def edit_preferences(request):
    pass


