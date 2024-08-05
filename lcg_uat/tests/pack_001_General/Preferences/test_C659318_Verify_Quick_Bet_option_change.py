import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.preferences
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.navigation
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C659318_Verify_Quick_Bet_option_change(BaseUserAccountTest, BaseSportTest):
    """
    TR_ID: C659318
    VOL_ID: C9697678
    NAME: Verify 'Quick Bet' option change
    DESCRIPTION: This test case verifies 'Quick Bet' option change within 'Preferences' page
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. 'Quick Bet' functionality is enabled in CMS
    PRECONDITIONS: 3. 'Quick Bet' functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/find test event
        DESCRIPTION: Load application
        DESCRIPTION: Login
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]

            self.__class__.eventID = event['event']['id']
            outcomes, expected_market = next(((market['market']['children'], market['market']['name']) for market in event['event']['children']
                             if market['market'].get('children') and market['market']['templateMarketName'] == 'Match Betting'), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            team1 = next((outcome['outcome']['name'] for outcome in outcomes
                          if outcome['outcome'].get('outcomeMeaningMinorCode') and
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not team1:
                raise SiteServeException('No Home team found')
            self.__class__.team1 = normalize_name(team1)
            self.__class__.expected_market = expected_market
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            self.__class__.team1 = event_params.team1
            expected_market = normalize_name(self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
            self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)

        self._logger.info(f'*** Football event with event id "{self.eventID}" and team "{self.team1}" and market "{self.expected_market}"')
        self.site.login()

    def test_001_go_to_right_menu_settings_item(self):
        """
        DESCRIPTION: Navigate to 'Settings' page
        EXPECTED: 'Preferences' page is opened
        EXPECTED: 'Allow Quick Bet' option is present
        """
        self.navigate_to_page(name='settings')
        self.site.wait_content_state('Settings')
        self.assertTrue(self.site.settings.allow_quick_bet.is_displayed(), msg='"Allow Quick Bet" option is not shown')

    def test_002_verify_default_value_set_for_allow_quick_bet_option(self):
        """
        DESCRIPTION: Verify default value set for 'Allow Quick Bet' option
        EXPECTED: Default value is 'ON'
        """
        self.assertTrue(self.site.settings.allow_quick_bet.is_enabled(), msg='"Allow Quick Bet" option is not enabled')

    def test_003_go_to_any_sport_race_page_and_add_one_selection_to_betslip(self):
        """
        DESCRIPTION: Go to any <Sport>/<Race> page and add one selection to Betslip
        EXPECTED: 'Quick Bet' section is displayed at the bottom of the page immediately
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

        self.add_selection_from_event_details_to_quick_bet(selection_name=self.team1, market_name=self.expected_market)

    def test_004_remove_selection_from_betslip(self):
        """
        DESCRIPTION: Remove selection from Betslip
        EXPECTED: 'Quick Bet' section is NOT displayed anymore
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False),
                         msg='"Quick Bet" section is not closed')

    def test_005_go_back_to_settings_page(self):
        """
        DESCRIPTION: Go back to 'Settings' page
        """
        self.navigate_to_page(name='settings')
        self.site.wait_content_state('Settings')

    def test_006_set_allow_quick_bet_option_to_off(self):
        """
        DESCRIPTION: Set 'Allow Quick Bet' option to 'OFF'
        """
        self.site.settings.allow_quick_bet.click()

    def test_007_go_to_any_sport_race_page_and_add_one_selection_to_betslip(self):
        """
        DESCRIPTION: Go to any <Sport>/<Race> page and add one selection to Betslip
        EXPECTED: 'Quick Bet' section is NOT displayed at the bottom of the page immediately
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

        bet_button = self.get_selection_bet_button(selection_name=self.team1, market_name=self.expected_market)
        bet_button.click()

        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False),
                         msg='"Quick Bet" section still displayed at the bottom of the page')
