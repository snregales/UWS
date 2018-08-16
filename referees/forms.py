from .models import Referee
from profiles.forms import (
    forms,
    ProfileRegisterForm,
)
from profiles.utils import (
    send_activation_email,
    prep_dict,
)


class RefereeRegistrationForm(ProfileRegisterForm):
    class Meta:
        model = Referee
        fields = ('first_name', 'last_name')

    def save(self, commit=True):
        super(RefereeRegistrationForm, self).save(commit=False)
        referee = Referee.objects.create_referee(
            **prep_dict(**self.cleaned_data)
        )
        if commit:
            referee.save()
            send_activation_email(referee.user)
        return referee


class ExamForm(forms.ModelForm):
    class Meta:
        model = Referee
        fields = ('certified',)
        widgets = {
            'certified': forms.TextInput(attrs={'hidden': True, 'initial': False})
        }

    choices = (('Pass', 'Pass'), ('Fail', 'Fail'))
    examination = forms.CharField(widget=forms.ChoiceField(choices=choices))
