from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import Questions
from.models import UserData
from django.utils import timezone
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.


def nextpage(request):
        if 'op' in request.GET:
            Qdict = request.session['answer']
            Qdict[request.GET["qno"]] = [
                request.GET["qno"], 
                request.GET["qtext"], 
                request.GET["answer"], 
                request.GET["op"]
            ]
            print(Qdict)
            
        
        queryset=Questions.objects.filter(subject=request.session['subject'])
        allquestions=list(queryset)


            
        if request.session['questionindex'] < len(allquestions) -1:
                request.session['questionindex'] = request.session['questionindex'] +1
                is_last_question=request.session['questionindex']==len(allquestions)-1
                question=allquestions[request.session['questionindex']]
                
                
                questionno=request.session['questionindex'] + 1
                print(f"Question number :-{questionno}")
                if request.session['questionindex']==len(allquestions)-1:
                    disable = True
                else:
                    disable = False
                    
                
                
                check=None
                answer_dict=request.session['answer']
                print(f"User submitted Answers:_{answer_dict}")
                if str(question.qno) in request.session['answer']:
                    check=answer_dict[str(question.qno)][3]
                    print(f'this is value :-{answer_dict}')
                        
                
                return render(request,'app1/question.html',{'is_last_question':is_last_question,'question':question,'disable': disable,'check':check,"questionno":questionno})
            
        else:
                questionno = len(allquestions)
                
                return render(request,'app1/question.html',{'question':allquestions[len(allquestions)-1],"questionno":questionno})




def previousQuestion(request):
    
    if 'op' in request.GET:
            Qdict = request.session['answer']
            Qdict[request.GET["qno"]] = [
                request.GET["qno"], #0
                request.GET["qtext"], #1
                request.GET["answer"], #2
                request.GET["op"]#3
            ]
    
    
    queryset=Questions.objects.filter(subject=request.session['subject'])
    allquestions=list(queryset)
    
    
    if request.session['questionindex']>0:

        request.session['questionindex']=request.session['questionindex'] - 1 
        question=allquestions[request.session['questionindex']]
        
        questionno=request.session['questionindex']+1 
        disable = False
        print(f"Question number:{question.qno}")
        
        check=None
        answer_dict=request.session['answer']
        print(f" User submitted answer:_{answer_dict}")
        
        
        if str(question.qno) in answer_dict:
            check=answer_dict[str(question.qno)][3]
            print(f'this is value :-{answer_dict}')
        
        return render(request,'app1/question.html',{'question':question,'disable': disable,'check':check,"questionno":questionno})
            
    else:
        disable = False
        questionno = 1

        return render(request,'app1/question.html',{'question':allquestions[0],'disable': disable,"questionno":questionno})
    
def endexam(request):
    if 'answer' in request.session:
        if 'op' in request.GET:
            Qdict = request.session['answer']
            Qdict[request.GET["qno"]] = [
                request.GET["qno"], 
                request.GET["qtext"], 
                request.GET["answer"], 
                request.GET["op"]
            ]
        correct_and_wronganslist=[]
        ans_dict=request.session['answer']
        lists=ans_dict.values()
        for list in lists:
            if list[2]==list[3]:
                request.session['score']=request.session['score']+1
                correct_and_wronganslist.append({'qno':list[0],'qtext':list[1],'answer':list[2],'wrong_ans':list[3],'status':'correct'})
            else:
                request.session["w_score"]= request.session["w_score"]+1
                correct_and_wronganslist.append({'qno':list[0],'qtext':list[1],'answer':list[2],'wrong_ans':list[3],'status':'wrong'})
                
        ans_dict=request.session['answer']
        score=request.session['score'] 
        wrong= request.session['w_score']  
        username= request.session['username']
        subject=  request.session["subject"]
        profile_pic= request.session.get('image')
        
        totalquestion=len(ans_dict)
        print(score)
        if totalquestion >0:
            percentage=int((score/totalquestion)*100)
            print(percentage)
            
        request.session["percentage"]=percentage
        per= request.session["percentage"]
        if percentage >= 90:
            feedback = "Excellent"
        elif percentage >= 50:
            feedback = "Good"
        else:
            feedback = "Needs Improvement"
        
            
        login_date=timezone.now().date()
        
        user=UserData(username=username,percentage=per,subject=subject,login_date=login_date)
        user.save()
        # print(Qdict)
        # auth.logout(request) 
        return render(request,'app1/results.html',{'feedback':feedback,'score':score,'wrong':wrong,'username':username,'percentage':percentage,'total_question':totalquestion,"profile_pic":profile_pic})
    
    else:
        
        return render(request,'app1/login.html',{'message1':'Login aging...!'})


def view_answers(request):
    # Get session data
    ans_dict = request.session.get('answer', None)
    
    if not ans_dict:
        # If no answers are found in the session, redirect to login or show a message
        return render(request, 'app1/login.html', {'message1': 'Please login again to view your answers.'})
    
    # Prepare correct and wrong answers list
    correct_and_wronganslist = []
    lists = ans_dict.values()
    for list in lists:
        if list[2] == list[3]:
            correct_and_wronganslist.append({
                'qno': list[0],
                'qtext': list[1],
                'answer': list[2],
                'wrong_ans': list[3],
                'status': 'correct'
            })
        else:
            correct_and_wronganslist.append({
                'qno': list[0],
                'qtext': list[1],
                'answer': list[2],
                'wrong_ans': list[3],
                'status': 'wrong'
            })

    # Debugging output (optional)
    print(f"Correct and Wrong Answers: {correct_and_wronganslist}")
    
    # Render the answers page
    return render(request, 'app1/answers.html', {'correct_wrong': correct_and_wronganslist})


@login_required(login_url='/login')
def starTest(request):
    if request.method=='GET':
        subject_name=request.GET.get('subject')
        request.session["subject"]=subject_name
        queryset=Questions.objects.filter(subject=request.session["subject"])
        questionlist=list(queryset.values())
        print(f"list :-{queryset}")
        print(f"qurestionlist :- {questionlist}")
        
        
        
        request.session['questionlist']=questionlist
        question=request.session['questionlist'][0]
        print(question)
        return render(request,"app1/question.html",{'question':question,"questionno":1})
    return render(request,"app1/question.html",{"questionno":1})





@login_required(login_url='/login') 
def view_resultdata(request):
    today = timezone.now().date() # current day
    print(today)
    yesterday = today - timedelta(days=1) 
    print(yesterday)

    date_filter = request.GET.get('date_filter')
    specific_date = request.GET.get('specific_date')

    if date_filter == 'today':
        data1 = UserData.objects.filter(login_date=today)
    elif date_filter == 'yesterday':

        data1 = UserData.objects.filter(login_date=yesterday)
    elif  specific_date:

        specific_date =  specific_date  #YYYY-MM-DD 
        data1 = UserData.objects.filter(login_date=specific_date)
    else:

        data1 = UserData.objects.all()

    return render(request, 'app1/admin.html', {"data": data1,'today':today,'yesterday':yesterday})

def view_resultdata(request):
    # Example: Fetch data from the database (modify this based on your logic)
    search_query = request.GET.get('search', '')
    date_filter = request.GET.get('date_filter', '')
    specific_date = request.GET.get('specific_date', '')
    
    # Filter the data as needed (update the filtering logic based on your requirements)
    data = UserData.objects.all()
    if search_query:
        data = data.filter(Q(username__icontains=search_query) | Q(subject__icontains=search_query))
    if date_filter == "today":
        data = data.filter(login_date=date.today())
    elif date_filter == "yesterday":
        data = data.filter(login_date=date.today() - timedelta(days=1))
    elif specific_date:
        data = data.filter(login_date=specific_date)
    print(data)
    
    # Apply pagination
    paginator = Paginator(data, 10)  # Show 10 entries per page
    page_number = request.GET.get('page')  # Get the current page number from query parameters
    page_obj = paginator.get_page(page_number)  # Get the relevant page data

    return render(request, 'app1/admin.html', {'page_obj': page_obj, 'search': search_query})



def search_user(request):
    search=request.GET["search"]
    request.session["search"]=search
    data1= UserData.objects.filter(subject=search) or UserData.objects.filter(username=search)
    i=data1.count()
    count=0
    
    while i>0:
        count=count+1    
        i=i-5
    print(f"aaaaaaaaaa{data1} and {count}")
    request.session["count"]=0
    
    data2=UserData.objects.filter(subject=search) or UserData.objects.filter(username=search)
    data2=data2[0:5]
    print(f"dsaaaaaaaaaaaaaaaaaaffffffffff{data2}")
    l=[]
    for i in range(0,count):
        l.append(i+1)
    print(f"dsddddddddddddddddddddaf{l}")
    
    return render(request, 'app1/admin.html', {"data": data2,"listofint":l})





def addquestions(request):
    if request.method=="POST":
        qno=request.POST["qno"]
        qtext=request.POST['qtext']
        answer=request.POST['answer']
        subject=request.POST['subject']
        op1=request.POST["op1"]
        op2=request.POST["op2"]
        op3=request.POST["op3"]
        op4=request.POST["op4"]
        
        Que=Questions.objects.create(qno=qno,qtext=qtext,answer=answer,op1=op1,op2=op2,op3=op3,op4=op4,subject=subject)
        Que.save()
        return render(request,"app1/questionmangment.html",{"message":'question added...'})
    if request.method=="GET":
            return render(request,"app1/questionmangment.html")

def updatequestions(request):
    if request.method=="POST":
        qno=request.POST["qno"]
        qtext=request.POST['qtext']
        answer=request.POST['answer']
        subject=request.POST['subject']
        op1=request.POST["op1"]
        op2=request.POST["op2"]
        op3=request.POST["op3"]
        op4=request.POST["op4"]
        
        que=Questions.objects.get(qno=qno)
        que.qtext=qtext
        que.answer=answer
        que.subject=subject
        que.op1=op1
        que.op2=op2
        que.op3=op3
        que.op4=op4
        que.save()
        return render(request,"app1/questionmangment.html",{"message":'question updated...'})
    return render(request,"app1/questionmangment.html") 


def viewquestions(request):
    if request.method=="POST":
        qno=request.POST["qno"]
        subject=request.POST['subject']
    
        que=Questions.objects.get(qno=qno,subject=subject) 
        return render(request,"app1/questionmangment.html",{'qno':que.qno,'qtext':que.qtext,'answer':que.answer,'op1':que.op1,'op2':que.op2,'op3':que.op3,'op4':que.op4,"message":"question displayed...."})
    return render(request,"app1/questionmangment.html")

def deletequestion(request):
    if request.method=="POST":
        qno=request.POST["qno"]
        subject=request.POST['subject']
        
        Questions.objects.get(qno=qno,subject=subject).delete()
        return render(request,"app1/questionmangment.html",{'message':'question deleteed.....'})
    return render(request,"app1/questionmangment.html")

@login_required(login_url='/login')
def managequestiondata(request):
    if request.method=="POST":
         return render(request,'app1/questionmangment.html')
    return render(request,'app1/questionmangment.html')

def backtodashboard(request):
    return render(request,'app1/dashboard.html')