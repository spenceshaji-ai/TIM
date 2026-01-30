from django import forms
from adminapp.models import LeaveApplication


class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ["leave_type", "start_date", "end_date", "reason"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "reason": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        leave_type = cleaned_data.get("leave_type")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if leave_type and start_date and end_date:
            days = (end_date - start_date).days + 1
            if days > leave_type.max_days:
                raise forms.ValidationError(
                    f"Maximum {leave_type.max_days} days allowed for {leave_type.leave_name}"
                )

        return cleaned_data
