from django import forms
from django.core.exceptions import ValidationError
from datetime import date, datetime
from django.utils.timezone import now
from adminapp.models import LeaveApplication


class LeaveApplicationForm(forms.ModelForm):

    HALF_SESSION_CHOICES = [
        ("Morning", "Morning"),
        ("Noon", "Noon"),
    ]

    half_day_session = forms.ChoiceField(
        choices=HALF_SESSION_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = LeaveApplication
        fields = [
            "leave_type",
            "start_date",
            "end_date",
            "day_type",
            "reason",
        ]

        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "day_type": forms.Select(attrs={"class": "form-control"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        day_type = cleaned_data.get("day_type")
        half_session = cleaned_data.get("half_day_session")

        today = date.today()
        current_time = now().time()

        # ❌ No past dates
        if start and start < today:
            raise ValidationError("Past dates are not allowed.")

        # ❌ End date validation
        if start and end and end < start:
            raise ValidationError("End date cannot be before start date.")

        # ❌ Prevent duplicate leave request same day
        if start and self.user:
            exists = LeaveApplication.objects.filter(
                user=self.user,
                start_date=start,
                status__in=["Pending", "Approved"]
            ).exists()

            if exists:
                raise ValidationError("You already applied leave for this date.")

        # HALF DAY LOGIC
        if day_type == "Half":

            if not half_session:
                raise ValidationError("Select Morning or Noon for half day.")

            # Today's leave restrictions
            if start == today:

                # After 9:30 → Morning not allowed
                if current_time >= datetime.strptime("09:30", "%H:%M").time():
                    if half_session == "Morning":
                        raise ValidationError(
                            "Morning half day cannot be applied after 9:30 AM."
                        )

                # After 12:30 → No half day allowed
                if current_time >= datetime.strptime("12:30", "%H:%M").time():
                    raise ValidationError(
                        "Half day leave cannot be applied after 12:30 PM."
                    )

        return cleaned_data