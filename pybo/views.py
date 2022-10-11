import re
from django.shortcuts import render, get_object_or_404, redirect
# 로그인 ㅈ
# from django.http import HttpResponseNotAllowed
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
    #question get 은 질문id만 가져온다. id 가져온다 그 id를 보내주는데
    #id=question_id 이름 정해주고 그걸 전달 context로
    #왜 html에서 question. 으로 사용가능하냐 id로 넘어가는데
    #하나의 객체를 들고온다

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
    # print(dir(question))
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # context = {'question': question}
    # return redirect('pybo:detail', question_id=question.id)
    # url으로 다시보내주는 방식
    #이게 보니까 바로 디테일 함수로 보내주니까 여기서 사용하는 .id로 보내주는듯
    # return render(request, 'pybo/question_detail.html', context )
    #해당페이지에 머물러 있어야 하기때문에
    #속성값을 쓸 수 있다. render는 html과 정보를 같이보내준다
    #context없어도 된다 딕셔너리 형태로 넣어도되지만 깔끔하지 않아서 변수 설정

    # question = get_objects_or_404(Question, pk = question_id)
    # Answer.objects.create(quetion = question, content = request.POST.get('content'))
    #역참조 안한건데 비교해보자
    #models 로 기능생각했고 만들어 놓으면 활용하면 다 만들 수 있다.
    #url매핑

#중요부분


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

"""
 게시글 볼 수 있는 index 함수 만든다.
 필요한거.
 아 이제 알았다. 버튼을 누르면 url로 넘어가서 함수 작동시키고 렌더, 리다이렉트로 화면을 돌려준다.
 url detail 라는 링크가 걸려있다. 그링크로 들어가면 링크에 연결된 함수가 실행
 함수로 디테일 페이지에 들어와서 질문 세부내용을 보여줌 밑에 댓글창이 있다.댓글창의 댓글달기를 누르면 그것도 링크 들어감
 그럼 실행하는 페이지에서 다음페이지에 필요한 정보를 넣어줘야하는가? url에 사용하려고 넘기는걸까?
 <form action="{% url 'pybo:answer_create' question.id %}" method="post">
    {% csrf_token %}
    <textarea name="content" id="content" rows="15"></textarea>
    <input type="submit" value="답변등록">
    </form>
    url pybo 앱에서 url이름을 실행할건데  question.id 를 사용하겠다.
    함수 실행보다는 url로 이동해서
    {% for answer in question.answer_set.all %} 바라보는 답글을 모두 가져와라
    url을 가져온다 

        answer/create/<int:question_id>/
        <form action="{% url 'pybo:answer_create' question.id %}" method="post">
            <int:question_id>자리에 question.id 가 들어간다고 생각
"""