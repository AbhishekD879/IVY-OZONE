import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
import tests
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from voltron.utils.exceptions.siteserve_exception import SiteServeException
import voltron.environments.constants as vec


# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
# disabled due to https://ladbrokescoral.slack.com/archives/C8R7VS19V/p1567168223033200
# Nataliia Drozdovska 3:29 PM
# Hi all
# Maybe do you know when the Football Jackpot will be available on Ladbrokes Prod env?
#
# Gregor Smith 3:30 PM
# It won’t be a Ladbrokes feature
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.jackpot
@pytest.mark.login
@vtest
class Test_C9698972_Verify_hiding__blocking_access_to_Football_Jackpot_page_for_a_German_user(BaseSportTest):
    """
    TR_ID: C9698972
    NAME: Verify hiding & blocking access to 'Football Jackpot' page for a German user
    DESCRIPTION: This test case verifies not displaying 'Jackpot' tab on 'Football' landing page & blocking access to 'Jackpot' tab via url for a German user.
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    """
    keep_browser_open = True
    sport_name = 'Football'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Football Jackpot is available
        PRECONDITIONS: 2. A German user is registered (with "signupCountryCode": "DE" - select Germany as a country during registration)
        PRECONDITIONS: 3. Local storage is cleared (so no "OX.countryCode" is available)
        PRECONDITIONS: 4. A user is not logged in
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   category_id=self.ob_config.backend.ti.football.category_id,
                                   brand=self.brand)
        jackpot_present = ss_req.ss_pool(query_builder=self.jackpot_query, raise_exceptions=False)
        if not jackpot_present:
            raise SiteServeException('No Football Jackpot pools available')
        self.site.login(username=tests.settings.german_betplacement_user)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is {key_value}')
        self.site.logout()
        self.delete_cookies()

    def test_001_log_in_as_a_german_user(self):
        """
        DESCRIPTION: Log in as a German user
        EXPECTED: - German user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.login(username=tests.settings.german_betplacement_user)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is {key_value}')

    def test_002___navigate_to_football_landing_page__verify_availability_of_jackpot_tab(self):
        """
        DESCRIPTION: - Navigate to Football landing page
        DESCRIPTION: - Verify availability of 'Jackpot' tab
        EXPECTED: - Football landing page is opened
        EXPECTED: - 'Jackpot' tab is not available
        """
        self.site.open_sport(name=self.sport_name)
        tab_names = self.site.football.tabs_menu.items_names
        self.assertFalse('JACKPOT' in tab_names, msg='Jackpot tab is available for German user')

    def test_003___add_sportfootballjackpot_route_to_an_app_url__press_enter(self):
        """
        DESCRIPTION: - Add "/sport/football/jackpot" route to an app url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: - German user is navigated to home page
        EXPECTED: - 'Country Restriction' pop up appears with text: "We are unable to offer Football Jackpot betting in your jurisdiction." and 'OK' button
        """
        url = '/sport/football/jackpot'
        self.device.navigate_to(url=f'{tests.HOSTNAME}{url}')
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.bma.COUNTRY_RESTRICTION.header)
        self.assertTrue(self.dialog.name, msg='Country Restriction dialog is not shown')
        actual_text = self.dialog.text
        expected_text = vec.bma.COUNTRY_RESTRICTION.jackpot_message_body
        self.assertEquals(actual_text, expected_text,
                          msg=f'Actual error message: "{actual_text}" is not equal to expected error message: "{expected_text}"')
        self.assertTrue(self.dialog.ok_button.is_displayed(), msg='OK button is not shown')

    def test_004_tap_ok_button_anywhere_outside_the_pop_up(self):
        """
        DESCRIPTION: Tap 'OK' button/anywhere outside the pop up
        EXPECTED: Pop up is closed
        """
        self.dialog.close_dialog()

    def test_005_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.logout()
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is {key_value}')

    def test_006_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        """
        self.test_002___navigate_to_football_landing_page__verify_availability_of_jackpot_tab()
        self.test_003___add_sportfootballjackpot_route_to_an_app_url__press_enter()
        self.test_004_tap_ok_button_anywhere_outside_the_pop_up()
