from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from labgeeks.forms import LoginForm
import datetime
from labgeeks_hermes.models import Notification
from labgeeks_hermes.forms import NotificationForm


def hello(request):
    """ The site dashboard.
    """
    #when a user is logged-in correctly
    if request.user.is_authenticated():
        locations = request.user.location_set.all()
        shifts = request.user.shift_set.all()
        clockin_time = 0
        if locations and shifts:
            clockin_time = shifts[len(shifts) - 1].intime

        now = datetime.datetime.now()

        notifications = Notification.objects.all()
        events = []
        alerts = []
        for noti in notifications:
            if noti.due_date:
                if now.date() - noti.due_date.date() >= datetime.timedelta(days=1):
                    noti.archived = True
                elif not noti.due_date - now > datetime.timedelta(days=7) and not noti.archived:
                    events.append(noti)
            else:
                if not noti.archived:
                    alerts.append(noti)
        events.sort(key=lambda x: x.due_date)

        c = {}
        c.update(csrf(request))

        can_Add = False
        if request.user.has_perm('labgeeksrpg_config.add_notification'):
            can_Add = True

        form_is_valid = True
        if request.method == 'POST':
            archive_ids = request.POST.getlist('pk')
            if archive_ids:
                for archive_id in archive_ids:
                    notif = Notification.objects.get(pk=archive_id)
                    notif.archived = True
                    notif.save()
                return HttpResponseRedirect('/')

            form = NotificationForm(request.POST)
            if form.is_valid():
                form_is_valid = True
                notification = form.save(commit=False)
                notification.user = request.user
                if notification.due_date:
                    if now.date() - notification.due_date.date() >= datetime.timedelta(days=1):
                        notification.archived = True
                notification.save()
                return HttpResponseRedirect('/')
            else:
                form_is_valid = False
        else:
            form = NotificationForm()

        workshifts = request.user.workshift_set.all()
        today_past_shifts = []
        today_future_shifts = []
        for shift in workshifts:
            in_time = shift.scheduled_in
            out_time = shift.scheduled_out
            if (in_time.year == now.year and in_time.month == now.month and in_time.day == now.day):
                if now - out_time > datetime.timedelta(seconds=1):
                    today_past_shifts.append(shift)
                else:
                    today_future_shifts.append(shift)
        args = {
            'request': request,
            'locations': locations,
            'clockin_time': clockin_time,
            'today_past_shifts': today_past_shifts,
            'today_future_shifts': today_future_shifts,
            'events': events,
            'alerts': alerts,
            'can_Add': can_Add,
        }
        return render_to_response('dashboard.html', locals(), context_instance=RequestContext(request))
    else:
        return render_to_response('hello.html', locals())


def labgeeks_login(request):
    """ Login a user. Called by the @login_required decorator.
    """

    # Get a token to protect from cross-site request forgery
    c = {}
    c.update(csrf(request))
    if request.user.is_authenticated():
        try:
            return HttpResponseRedirect(request.GET['next'])
        except:
            return HttpResponseRedirect('/')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    # Return a disabled account error
                    return HttpResponseRedirect('/inactive/')
    else:
        form = LoginForm()

    return render_to_response('login.html', locals(), context_instance=RequestContext(request))


def labgeeks_logout(request):
    """ Manually log a user out.
    """
    logout(request)
    return HttpResponseRedirect('/')


def inactive(request):
    """ Return if a user's account has been disabled.
    """
    return render_to_response('inactive.html', locals())

def pages(request):
    """ Display this list of flatpages
    """
    params = {"request": request}
    return render_to_response('pages.html', params)
