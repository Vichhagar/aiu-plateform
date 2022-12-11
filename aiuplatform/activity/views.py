from django.shortcuts import render, HttpResponse, redirect
from .models import Activity, ActivityParticepationList, User
from .forms import JoinActivityForm, CreateActivityForm, CreateUserForm, UpdateUserForm
from django.http import JsonResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('activity:home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('activity:home')
            else:
                messages.info(request, "username or password is wrong")
                
        context = {

        }
        return render(request, 'activity/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('activity:login')

def register(request):
    if request.user.is_authenticated:
        return redirect('activity:home')
    else:
        form = CreateUserForm()
        print(form)
        if request.method == "POST":
            form = CreateUserForm(request.POST, files=request.FILES)
            
            print(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "account created")
                return redirect('activity:login')

        context = {
            "form" : form
        }
        return render(request, 'activity/registration.html', context)

@login_required(login_url='activity:login')
def home(request):

    allActivities = Activity.objects.all().count()

    activities = []
    pagenation = [0,1,2,3,4]
    parList = []

    for activity in Activity.objects.all().order_by('-activityOpenDate'):
        particepance = ActivityParticepationList.objects.filter(activityID = activity.id) if ActivityParticepationList.objects.filter(activityID = activity.id).count() < 6 else ActivityParticepationList.objects.filter(activityID = activity.id)[:5]
        particepanceList = []
        for i in particepance:
            particepanceList.append(i.userID.id)
        lastestParticepance = ActivityParticepationList.objects.filter(activityID = activity.id).count()
        activityInfo = {"activity" : activity, "particepance" : particepance, "lastestParticepance" : lastestParticepance, "particepanceList" : particepanceList}
        # if activity.activityOrganizer.id != request.user.id:
        activities.append(activityInfo)

    

    context = {
        "activities" : activities,
        "allActivities" : allActivities,
        "pagenation" : pagenation,
        "parList" : parList
    }
    return render(request,'activity/home.html',context)

@login_required(login_url='activity:login')
def JoinActivity(request):
    form = JoinActivityForm()
    if request.method == "POST":
        print('Receiving a post request')
        print(request.POST)
        form = JoinActivityForm(request.POST)
        
        if form.is_valid():
            form.save()
    return HttpResponse(request.POST["activityID"])

@login_required(login_url='activity:login')
def CreateActivity(request):
    form = CreateActivityForm()
    if request.method == "POST":
        activity = form.save(commit=False)

        activity.activityOrganizer = request.user
        activity.activityTitle = request.POST["activityTitle"]
        activity.activityLocation = request.POST["activityLocation"]
        activity.activityDiscription = request.POST["activityDiscription"]
        activity.activityDate = request.POST["activityDate"]
        activity.activityOpenDate = request.POST["activityOpenDate"]
        activity.activityCloseDate = request.POST["activityCloseDate"]



        activity.save()
        return redirect("activity:profile-host")
        
    context = {
        "form" : CreateActivityForm()
    }
    return render(request, "activity/create.html", context)

@login_required(login_url='activity:login')
def ProfileHost(request):
    activities = []
    pagenation = [0,1,2,3,4]
    hostCount = Activity.objects.filter(activityOrganizer = request.user.id).count()
    joinCount = ActivityParticepationList.objects.filter(userID = request.user.id).count()

    for activity in Activity.objects.filter(activityOrganizer = request.user.id).order_by('-activityOpenDate'):
        particepance = ActivityParticepationList.objects.filter(activityID = activity.id) if ActivityParticepationList.objects.filter(activityID = activity.id).count() < 6 else ActivityParticepationList.objects.filter(activityID = activity.id)[:5]
        lastestParticepance = ActivityParticepationList.objects.filter(activityID = activity.id).count()
        activityInfo = {"activity" : activity, "particepance" : particepance, "lastestParticepance" : lastestParticepance}
        activities.append(activityInfo)


    context = {
        "activities" : activities,
        "pagenation" : pagenation,
        "hostCount" : hostCount,
        "joinCount" : joinCount

    }

    return render(request, "activity/profile-host.html", context)

@login_required(login_url='activity:login')
def ProfileJoin(request):
    activities = []
    pagenation = [0,1,2,3,4]

    hostCount = Activity.objects.filter(activityOrganizer = request.user.id).count()
    joinCount = ActivityParticepationList.objects.filter(userID = request.user.id).count()

    join = ActivityParticepationList.objects.filter(userID = request.user.id)
    joinList = []

    for i in join:
        joinList.append(i.activityID)
    for activity in joinList:
        particepance = ActivityParticepationList.objects.filter(activityID = activity.id) if ActivityParticepationList.objects.filter(activityID = activity.id).count() < 6 else ActivityParticepationList.objects.filter(activityID = activity.id)[:5]
        lastestParticepance = ActivityParticepationList.objects.filter(activityID = activity.id).count()
        # particepanceList = []
        # for i in particepance:
        #     particepanceList.append(i.userID.id)
        activityInfo = {"activity" : activity, "particepance" : particepance, "lastestParticepance" : lastestParticepance}
        activities.append(activityInfo)
    

    context = {
        "activities" : activities,
        "pagenation" : pagenation,
        "hostCount" : hostCount,
        "joinCount" : joinCount
        # "par" : par
    }

    return render(request, "activity/profile-join.html", context)

@login_required(login_url='activity:login')
def Moreinfo(request, id):
    activity = Activity.objects.get(id=id)
    parList = ActivityParticepationList.objects.filter(activityID = id)

    listPar = []

    for i in parList:
        # print(i.userID.id)
        listPar.append(i.userID.id)

    context = {
        "activity" : activity,
        "parList" : parList,
        "listPar" : listPar
    }

    return render(request, "activity/more_info.html", context)

@login_required(login_url='activity:login')
def updateActivity(request, id):
    activity = Activity.objects.get(id=id)
    form = CreateActivityForm(instance=activity)

    old = {
        "activityOrganizer" : activity.activityOrganizer,
        "activityTitle" : activity.activityTitle,
        "activityLocation" : activity.activityLocation,
        "activityDiscription" : activity.activityDiscription,

        "activityDate" : activity.activityDate.isoformat(),

        "activityOpenDate" : activity.activityOpenDate.isoformat(),
        "activityCloseDate" : activity.activityCloseDate.isoformat(),
    }


    if request.method == "POST":
        activity = form.save(commit=False)

        activity.activityOrganizer = request.user
        activity.activityTitle = request.POST["activityTitle"]
        activity.activityLocation = request.POST["activityLocation"]
        activity.activityDiscription = request.POST["activityDiscription"]
        activity.activityDate = request.POST["activityDate"]
        activity.activityOpenDate = request.POST["activityOpenDate"]
        activity.activityCloseDate = request.POST["activityCloseDate"]

        activity.save()
        return redirect("activity:profile-host")

    context = {
        "form" : form,
        "old" : old
    }

    return render(request, "activity/update.html", context)

@login_required(login_url='activity:login')
def updateUser(request, id):
    user = User.objects.get(id=id)
    form = UpdateUserForm(instance=user)
    

    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=user, files=request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("activity:profile-host")

    context = {
        "form" : form,
    }

    return render(request, "activity/updateUser.html", context)


@login_required(login_url='activity:login')
def deleteActivity(request, id):
    activity = Activity.objects.get(id=id)
    activity.delete()
    return redirect("activity:profile-host")

@login_required(login_url='activity:login')
def deleteUser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, "The account has been deleted, Sad! anyway...")
    return redirect("activity:login")

@login_required(login_url='activity:login')
def leaveActivity(request):
    leaveItem = ActivityParticepationList.objects.filter(userID = request.user.id, activityID=request.POST["activityID"])
    leaveItem.delete()
    return HttpResponse("JOB DONE")

