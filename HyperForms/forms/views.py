from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Participant, FormModel, FormRecord, FormData


# Create your views here.
class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "context"

    def get_queryset(self):
        record_data_list = []
        record_list = FormRecord.objects.all()
        for record in record_list:
            record_data = record.form_data.all()
            record_data_list.append(record_data)
        form = FormModel.objects.filter(name="participants").first()
        if form:
            table_headings = form.form_fields.all()
        else:
            table_headings = None
        return {"record_data_list": record_data_list, "table_headings": table_headings}


class RegistrationFormView(FormView):
    form_class = RegistrationForm
    template_name = "registration.html"
    success_url = "/"

    def form_valid(self, form):
        Participant.objects.create(name=form.cleaned_data["name"], age=form.cleaned_data["age"],
                                   favorite_book=form.cleaned_data["favorite_book"])
        return super().form_valid(form)


def registration_view(request):
    if request.method == "GET":
        form = FormModel.objects.filter(name="participants").first()
        form_fields = form.form_fields.all()
        return render(request, template_name="registration.html", context={"form": form_fields})
    if request.method == "POST":
        FormRecord.objects.create()
        record_id = FormRecord.objects.last()
        post_data = dict(request.POST)
        del post_data["csrfmiddlewaretoken"]
        for data in post_data:
            FormData.objects.create(record=record_id, data=post_data[data][0])
        return redirect("/")

