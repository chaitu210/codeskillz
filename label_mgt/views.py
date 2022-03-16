from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Category, DataPoint
from .forms import AuthenticationForm
from django.contrib.auth.models import User


def index(request):
    """
    Handles login functionality based on type of HTTP method.

    In GET: Returns a login.html page.
        - If the user is active and already authenticated redirect to dashboard.
    IN POST: 
        - Validates username and password.
        - Returns JSONResponse with a redirect url to which the user should be landed.
        - Returns JSONResponse with error data if data is invalid.

    GET parameters:
    GET['next'] : URL to redirect to after submit form
    """
    next_url = request.GET.get('next')
    if request.method == "POST":
        authentication_form = AuthenticationForm(request.POST)
        if authentication_form.is_valid():
            login(request, authentication_form.get_user())
            request.session.set_expiry(3600)
            if request.POST.get('next'):
                data = {"error": False,
                        "redirect_url": request.POST.get('next')}
            else:
                data = {"error": False,
                        "redirect_url": reverse("dashboard")}
        else:
            data = {"error": True, "response": authentication_form.errors}
        return JsonResponse(data)
    if request.user.is_active and request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard"))
    return render(request, "login.html", {'next_url': next_url})


@login_required(login_url='/')
def dashboard(request):
    """
    Display analytics for the logged in user..

    **Context**

    ``datapoints``
        Queryset of :model:`label_mgt.DataPoint`.
    ``user_labelled_points_count``
        Count of user labelled datapoints :model:`label_mgt.DataPoint`.
    ``unlabelled_points_count``
        Count of unlabelled datapoints :model:`label_mgt.DataPoint`.

    **Template:**

    :template:`dashboard.html`

    """
    latest_labelled_datapoints = DataPoint.objects.filter(label__isnull=False)[:10]
    user_labelled_points = DataPoint.objects.filter(labelled_by=request.user)
    unlabelled_points = DataPoint.objects.filter(label__isnull=True)
    return render(request, 'dashboard.html', {
        'datapoints': latest_labelled_datapoints,
        'user_labelled_points_count': user_labelled_points.count(),
        'unlabelled_points_count': unlabelled_points.count()
    })


@login_required(login_url='/')
def datapoints(request):
    data_points = DataPoint.objects.all()
    if request.GET.get('title'):
        data_points = data_points.filter(title__icontains=request.GET.get('title'))
    if request.GET.get('username'):
        user = User.objects.filter(username__icontains=request.GET.get('username'))
        data_points = data_points.filter(labelled_by__in=user)
    if request.GET.get('label'):
        category = Category.objects.get(id=request.GET.get('label'))
        data_points = data_points.filter(label=category)

    categories = Category.objects.all()
    return render(request, 'datapoints_list.html', {'datapoints': data_points, 'categories': categories})


@login_required(login_url='/')
def label_datapoint(request, pk):
    if request.method == "POST":
        if request.POST.get('label'):
            category = Category.objects.get(id=request.POST.get('label'))
            datapoint = DataPoint.objects.get(pk=pk)
            datapoint.label = category
            datapoint.labelled_by = request.user
            datapoint.save()
            data = {"error": False}
        else:
            data = {"error": True,
                    "response": {'label': ['Please select label.']}}

        return JsonResponse(data)
    return HttpResponseNotAllowed(['post'])


@login_required(login_url='/')
def signout(request):
    logout(request)
    return redirect("/")
