import pytest
import tests
from tests.base_test import vtest
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


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
@vtest
class Test_C9701595_Verify_blocking_an_access_to_Jackpot_after_registration_of_a_German_user(BaseSportTest):
    """
    TR_ID: C9701595
    NAME: Verify blocking an access to Jackpot after registration of a German user
    DESCRIPTION: This test case verifies whether just registered German user doesn't have access to Football Jackpot
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. devtool > Application tab > Local Storage > is cleared (so no "OX.countryCode" is available)
    PRECONDITIONS: 2. Login pop-up is opened on mobile
    """
    keep_browser_open = True
    dialog = None
    username = None
    password = None
    is_mobile = None

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1. devtool > Application tab > Local Storage > is cleared (so no "OX.countryCode" is available)
        PRECONDITIONS: 2. Login pop-up is opened on mobile
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   category_id=self.ob_config.backend.ti.football.category_id,
                                   brand=self.brand)
        jackpot_present = ss_req.ss_pool(query_builder=self.jackpot_query, raise_exceptions=False)
        if not jackpot_present:
            raise SiteServeException('No Football Jackpot pools available')
        self.site.wait_content_state('Homepage')

    def test_001___tap_join_now__fill_in_all_necessary_fields_to_register_user__select_country_germany__tap_open_account_save_my_preferences__close_deposit_page(self):
        """
        DESCRIPTION: - Tap 'Join now'
        DESCRIPTION: - Fill in all necessary fields to register user
        DESCRIPTION: - Select Country 'Germany'
        DESCRIPTION: - Tap 'Open account', 'Save my preferences'
        DESCRIPTION: - Close Deposit page
        EXPECTED: - German user is navigated back to an app
        EXPECTED: - German user is logged in
        EXPECTED: - German user is navigated to Home page
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.register_new_user(country='Germany', currency='EUR', state='Berlin')
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is {key_value}')

    def test_002___go_to_football_landing_page__verify_availability_of_jackpot_tab(self):
        """
        DESCRIPTION: - Go to Football landing page
        DESCRIPTION: - Verify availability of 'Jackpot' tab
        EXPECTED: 'Jackpot' tab is NOT available
        """
        self.site.home.menu_carousel.click_item('Football')
        tab_names = self.site.football.tabs_menu.items_names
        self.assertFalse('JACKPOT' in tab_names, msg='Jackpot tab is available for German user')
