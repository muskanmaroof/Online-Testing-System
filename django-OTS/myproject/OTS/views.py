from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from OTS.models import *
import random

# Create your views here.
def welcome(request):
    template=loader.get_template('welcome.html')
    return HttpResponse(template.render())

def candidateRegistrationForm(request):
    return render(request,'registration_form.html')

def candidateRegistration(request):
    if request.method=='POST':
        # isf user exist already
        username=request.POST['username']
        if(len(Candidate.objects.filter(username=username))):
            userStatus=1
        else:
            candidate=Candidate()
            candidate.username=username
            candidate.password=request.POST['password']
            candidate.name=request.POST['name']
            candidate.save()
            userStatus=2
    else:
        #request method is not post
        userStatus=3
    context={
        'userStatus':userStatus
    }
    return render(request, 'registration.html' , context)

def loginView(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        candidate = Candidate.objects.filter(username=username,password=password)
        if len(candidate)==0:
            loginError='Invalid username or password '
            res=render(request,'login.html' ,{'loginError':loginError})
        else:
            #login success
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name
            res=HttpResponseRedirect("/OTS/home")

    else:
        res =render(request, 'login.html' )
    return res



def candidateHome(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect('/OTS/login')
    else:
        res = render(request ,'home.html')
    return res

def testPaper(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect('/OTS/login')
    # fetching questions from database table
    n=int(request.GET['n'])
    questions=list(Question.objects.all())
    # shuffling questions
    random.shuffle(questions)
    # limiting questions to n
    questions=questions[:n]
    context={
        'questions':questions
    }
    return render(request, 'test_paper.html', context)


def calculateTestResult(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect('/OTS/login')
    total_attempt=0
    total_right=0
    total_wrong=0
    qid_list=[]
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question = Question.objects.get(qid=n)
        try:
            ans=request.POST[f'q{n}']
            if ans==question.ans:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except Exception as e:
            print(e)
    points=(total_right-total_wrong)/len(qid_list)*10
    #store result in result table
    result=Result()
    result.username=Candidate.objects.get(username=request.session['username'])
    result.attempt=total_attempt
    result.right=total_right
    result.wrong=total_wrong
    result.points=points
    result.save()
    #update candidate table
    candidate=Candidate.objects.get(username=request.session['username'])
    candidate.test_attempted+=1
    candidate.points=(candidate.points*(candidate.test_attempted-1)+points)/candidate.test_attempted
    candidate.save()
    return redirect('/OTS/result')
    #render result page with result details
    # context={
    #     'total_attempt':total_attempt,
    #     'total_right':total_right,
    #     'total_wrong':total_wrong,
    #     'points':points
    # }
    # return render(request,'result.html', context)




def testResultHistory(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect('/OTS/login')
    # fetch all result from result table
    candidate=Candidate.objects.filter(username=request.session['username'])
    results=Result.objects.filter(username=candidate[0].username)
    context={
        'candidate':candidate[0],
       'results':results
    }
    return render(request,'result_history.html', context)

def showTestResult(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect('/OTS/login')
    # fetch latest result from result table
    result=Result.objects.filter(resultid=Result.objects.latest('resultid').resultid, username=request.session['username'])
    context={
       'result':result
    }
    return render(request,'show_result.html', context)
 
def logoutView(request):
    if 'username' in request.session.keys():
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect('/OTS/login')