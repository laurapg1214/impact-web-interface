from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import *
from .utils import get_object_or_error


def index(request):
    question_list = Question.objects.all()
    context = {
        "question_list": question_list,
    }
    return render(request, "obwob/index.html", context)


# custom error page
# def custom_404_view(request):
#     context = {
#         'error_message': "Oops! The page you're looking for doesn't exist."
#     }
#     print('there should be an error message!')
#     return render(request, '404.html', context, status=404)


# functions below use custom encapsulated get_object_or_error function from .utils:
# def get_object_or_error(request, model, object_id, template_path, extra_context=None):
def event(request, event_id, event_name):
    return get_object_or_error(request, Event, event_id, "event.html", event_name)


def event_questions(request, event_id, event_name):
    extra_context = {
        "questions": Question.objects.filter(events=event_id)
    }
    return get_object_or_error(request, Event, event_id, "event_questions.html", extra_context, event_name)


def responses(request, question_id):
    question = Question.objects.get(pk=question_id)
    extra_context = {
        "responses": Response.objects.filter(questions=question)
    }
    return get_object_or_error(request, Question, question_id, "responses.html", extra_context)
