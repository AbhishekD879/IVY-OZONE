import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.prod  # cannot grant odds boost tokens on prod endpoints
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.popup
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C2507411_Verify_Log_In_and_Bet_for_the_User_with_popups_after_Login(BaseBetSlipTest):
    """
    TR_ID: C2507411
    NAME: Verify 'Log In & Bet' for the User with popups after Login
    DESCRIPTION: This test case verifies 'Log In & Bet' button for a logged out and logged in user
    PRECONDITIONS: Make sure you have user account with added credit cards with positive balance,
    PRECONDITIONS: however for this user popups are expected after login (e.g., Freebet popup, NetVerify, Bonuses, etc.)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        self.__class__.username = tests.settings.betplacement_user
        self.__class__.password = tests.settings.default_password
        self.ob_config.grant_odds_boost_token(self.username)

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')
            self._logger.info(f'*** Found Football event with selection ids "{self.selection_ids}" and team "{self.team1}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids
        self.__class__.selection_id = self.selection_ids[self.team1]

    def test_001_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip
        EXPECTED: 1. Betslip is opened
        EXPECTED: 2. Added single selection(s) present
        EXPECTED: 3. 'Log in & Bet' button is disabled
        """
        self.open_betslip_with_selections(self.selection_id)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'"{self.team1}" stake was not found')
        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" button is not disabled')

    def test_002_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: 'Log in & Bet' button becomes enabled
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(timeout=1.5),
                        msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" button is not enabled')

    def test_003_tap_on_log_in__bet_button(self):
        """
        DESCRIPTION: Tap on 'Log in & Bet' button
        EXPECTED: 'Log In' pop-up is opened
        """
        self.get_betslip_content().bet_now_button.click()
        self.__class__.login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=3)
        self.assertTrue(self.login_dialog, msg='No "Log In" pop-up opened')

    def test_004_log_in_with_user_that_has_added_credit_cards_with_positive_balance(self):
        """
        DESCRIPTION: Log in with user that has **added credit cards with positive balance**
        EXPECTED: 1. User is logged in
        EXPECTED: 2. Expected popup is shown
        """
        self.login_dialog.username = self.username
        self.login_dialog.password = self.password
        self.login_dialog.click_login()
        self.assertTrue(self.login_dialog.wait_dialog_closed(), msg='Log in popup not closed')
        self.site.close_all_dialogs(ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)

    def test_005_close_popup(self):
        """
        DESCRIPTION: Close popup
        EXPECTED: 1. Popup is closed
        EXPECTED: 2. Bet is NOT placed automatically
        EXPECTED: 3. Button states 'Bet Now'
        EXPECTED: 4. 'Bet Now' button is enabled
        """
        self.site.close_all_dialogs(async_close=False)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'"{self.team1}" stake was not found')
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertEqual(bet_now_button.name, vec.betslip.BET_NOW,
                         msg=f'Actual button name: {bet_now_button.name} '
                             f'is not as expected: "{vec.betslip.BET_NOW}"')
        self.assertTrue(bet_now_button.is_enabled(),
                        msg=f'"{vec.betslip.BET_NOW}" button is disabled')
