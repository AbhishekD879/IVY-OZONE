from voltron.pages.coral.contents.registration.forms.step1of3 import CoralStep1Of3Form
from voltron.pages.shared.contents.registration.three_steps.three_steps import ThreeSteps


class CoralThreeSteps(ThreeSteps):
    _step1_form_type = CoralStep1Of3Form

    def complete_all_registration_steps(
            self,
            username=None,
            password=None,
            **kwargs):

        currency = kwargs.get('currency', 'GBP')
        email = kwargs.get('email')
        social_title = kwargs.get('social_title', 'Mr.')
        first_name = kwargs.get('first_name', 'Automated')
        last_name = kwargs.get('last_name', 'Tester')
        country = kwargs.get('country', 'United Kingdom')
        birth_date = kwargs.get('birth_date', '01-Jun-1977')

        self.form_step1.country.dropdown.value = country

        self.form_step1.currency.dropdown.value = currency

        self.form_step1.email.input.value = email

        self.form_step1.password.input.value = password

        self._logger.info(f'*** Registering {currency} user "{username}" with password "{password}"')

        self.submit_step1()

        self.form_step2.enter_values(social_title=social_title,
                                     first_name=first_name,
                                     last_name=last_name,
                                     birth_date=birth_date)

        self.submit_step2()

        self.form_step3.enter_values(
            **kwargs)

        self.submit_step3()
