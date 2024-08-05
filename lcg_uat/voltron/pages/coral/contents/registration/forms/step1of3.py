from voltron.pages.shared.contents.registration.forms.step1of3 import Step1Of3Form


class CoralStep1Of3Form(Step1Of3Form):

    @property
    def username(self):
        raise NotImplementedError('"Username" field is not present anymore on coral registration 1st step page')

    def enter_values(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        country = kwargs.get('country')
        if email:
            self.email.input.value = email
        if password:
            self.password.input.value = password
        if country:
            self.country.dropdown.value = country
