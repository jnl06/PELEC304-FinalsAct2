from django import forms
from .models import BackgroundInfo, Student


class StyledFormMixin:

    def _style_fields(self):
        for field in self.fields.values():
            widget = field.widget
            css = "form-control"
            if isinstance(widget, forms.Select):
                css = "form-select"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {css}".strip()


class StudentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        exclude = ["date_enrolled", "created_at", "updated_at"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class BackgroundForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = BackgroundInfo
        exclude = ["student"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class StudentSearchForm(StyledFormMixin, forms.Form):
    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search name, number, course...", "type": "search"}
        ),
    )
    status = forms.ChoiceField(
        required=False,
        label="",
        choices=[("", "All status")] + list(Student.EnrollmentStatus.choices),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
