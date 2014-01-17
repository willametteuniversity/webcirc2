from django import forms

class RegistrationForm(forms.Form):
    '''
    This Form is for people to register for an account
    '''
    username = forms.CharField(
        label='Username:',
        max_length=15,
        required=True,
    )

    email = forms.CharField(
        label='E-Mail:',
        max_length=30,
        required=True,
    )

    password = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(render_value=False),
    )

    confirmPassword = forms.CharField(
        label='Confirm Password:',
        widget=forms.PasswordInput(render_value=False),
    )
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.formId = 'registerNewUserForm'
        self.helper.formMethod = 'post'
        self.helper.formAction = 'registerNewUser'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'username',
            'email',
            'password',
            'confirmPassword',
            Submit('submit', 'Register'),
        )
        super(RegistrationForm, self).__init__(*args, **kwargs)


