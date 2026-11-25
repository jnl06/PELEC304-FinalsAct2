from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BackgroundForm, StudentForm, StudentSearchForm
from .models import Student


def student_list(request, pk=None):
    search_form = StudentSearchForm(request.GET or None)
    students = Student.objects.all()

    if search_form.is_valid():
        q = search_form.cleaned_data.get("q")
        status = search_form.cleaned_data.get("status")
        if q:
            students = students.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(student_number__icontains=q)
                | Q(course__icontains=q)
            )
        if status:
            students = students.filter(status=status)

    page_obj = Paginator(students, 12).get_page(request.GET.get("page"))

    # keep search in links, but drop page
    params = request.GET.copy()
    params.pop("page", None)

    selected = None
    if pk is not None:
        selected = get_object_or_404(
            Student.objects.select_related("background"), pk=pk
        )

    context = {
        "search_form": search_form,
        "page_obj": page_obj,
        "selected": selected,
        "querystring": params.urlencode(),
        "total": students.count(),
    }
    return render(request, "students/student_list.html", context)


def student_create(request):
    student_form = StudentForm(request.POST or None)
    background_form = BackgroundForm(request.POST or None, prefix="bg")

    if request.method == "POST" and student_form.is_valid() and background_form.is_valid():
        student = student_form.save()
        background = background_form.save(commit=False)
        background.student = student
        background.save()
        messages.success(request, f"{student.full_name} added.")
        return redirect("students:detail", pk=student.pk)

    return render(
        request,
        "students/student_form.html",
        {
            "student_form": student_form,
            "background_form": background_form,
            "title": "Add Student",
        },
    )


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    background = getattr(student, "background", None)  
    student_form = StudentForm(request.POST or None, instance=student)
    background_form = BackgroundForm(
        request.POST or None, instance=background, prefix="bg"
    )

    if request.method == "POST" and student_form.is_valid() and background_form.is_valid():
        student = student_form.save()
        background = background_form.save(commit=False)
        background.student = student
        background.save()
        messages.success(request, f"{student.full_name} updated.")
        return redirect("students:detail", pk=student.pk)

    return render(
        request,
        "students/student_form.html",
        {
            "student_form": student_form,
            "background_form": background_form,
            "title": f"Edit {student.full_name}",
            "student": student,
        },
    )
