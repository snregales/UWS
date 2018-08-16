from datetime import datetime

from .models import Athlete
from profiles.forms import (
    forms,
    ProfileRegisterForm,
)
from profiles.utils import (
    send_activation_email,
    prep_dict,
)


class AthleteRegisterForm(ProfileRegisterForm):
    class Meta:
        current_year = datetime.now().year
        model = Athlete
        fields = ('first_name', 'last_name', 'dob')
        widgets = {
            'dob': forms.SelectDateWidget(
                empty_label=("Year", "Month", "Day"),
                years=list(range(current_year-60, current_year-10+1))
            ),
        }

    def save(self, commit=True):
        super(AthleteRegisterForm, self).save(commit=False)
        athlete = Athlete.objects.create_athlete(
            **prep_dict(**self.cleaned_data)
        )
        if commit:
            athlete.save()
            send_activation_email(athlete.user)
        return athlete
