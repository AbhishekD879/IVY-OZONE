from faker import Faker
from selenium.common.exceptions import StaleElementReferenceException

import tests
from voltron.pages.coral.tablet_site import TabletSite
from voltron.pages.ladbrokes.components.header_tablet import GlobalHeaderTabletLadbrokes
from voltron.pages.ladbrokes.components.right_column_widgets.right_column import LadbrokesRightColumn
from voltron.pages.ladbrokes.dialogs.dialog_contents.login import LadbrokesLogInDialog
from voltron.pages.ladbrokes.dialogs.dialog_manager import DialogManagerLadbrokes
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import string_generator
from voltron.utils.waiters import wait_for_result


class LadbrokesTabletSite(TabletSite):
    _betslip = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"]'
    _cash_out = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="slideContent.cashOut" or @data-crlat="slideContent.1"]]'
    _open_bets = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="slideContent.openBets" or @data-crlat="slideContent.2"]]'
    _bet_history = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="slideContent.betHistory" or @data-crlat="slideContent.3"]]'
    _favourites = 'xpath=.//*[@data-crlat="widgetAccordion.favourites"]'
    _header_type = GlobalHeaderTabletLadbrokes
    _wait_login_dialog_closed = 20

    @property
    def back_button(self):
        return self.header.back_button

    @property
    def login_dialog(self):
        return LadbrokesLogInDialog(selector=self._login_dialog, timeout=3)

    @property
    def dialog_manager(self):
        return DialogManagerLadbrokes()

    @property
    def right_column(self):
        return LadbrokesRightColumn(selector=self._right_column, timeout=5)

    def wait_logged_out(self, timeout=10):
        return wait_for_result(lambda: self.header.sign_in_join_button.is_displayed(),
                               name='Login Button should be visible',
                               expected_result=True,
                               timeout=timeout,
                               bypass_exceptions=(StaleElementReferenceException, VoltronException))

    def register_new_user(
            self,
            social_title='Mr.',
            first_name=Faker().first_name_female(),
            last_name=Faker().last_name_female(),
            birth_date='01-Jun-1977',
            country='United Kingdom',
            post_code='PO16 7GZ',
            address_one='1 Owen Close',
            city='Fareham',
            mobile='+447537152317',
            email=None,
            username=None,
            password=tests.settings.default_password,
            currency='GBP',
            deposit_limit=None,
            terms_and_conditions=True,
            **kwargs
    ):
        expected_content_state = kwargs.get('expected_content_state', 'Homepage')
        self.header.join_us.click()
        self.login_dialog.join_us.click()
        username = username if username else f'{tests.settings.registration_pattern_prefix}{string_generator(size=5)}'[:15]
        email = email if email else f'test+{username}@internalgvc.com'
        self.three_steps_registration.complete_all_registration_steps(social_title=social_title,
                                                                      first_name=first_name,
                                                                      last_name=last_name,
                                                                      birth_date=birth_date,
                                                                      country=country,
                                                                      post_code=post_code,
                                                                      address_one=address_one,
                                                                      city=city,
                                                                      mobile=mobile,
                                                                      email=email,
                                                                      username=username,
                                                                      password=password,
                                                                      currency=currency)
        if country == 'United Kingdom':
            self.set_your_deposit_limits.set_limits(deposit_limit=deposit_limit)
        self.select_deposit_method.close_button.click()
        self.wait_content_state(expected_content_state)
        self.close_all_dialogs(async_close=False, timeout=4) if kwargs.get('close_dialogs', True) else self._logger.info('*** Bypassing close all dialogs')
        self.close_all_banners(async_close=False) if kwargs.get('close_banners', True) else self._logger.info('*** Bypassing close all banners')
