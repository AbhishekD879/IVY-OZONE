import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C518423_Verify_Log_In_and_Bet_for_the_User_with_Positive_Balance(BaseBetSlipTest):
    """
    TR_ID: C518423
    NAME: Verify Log In and Bet for the User with Positive Balance
    DESCRIPTION: This test case verifies 'Log In & Bet' button for a logged out and logged in user
    PRECONDITIONS: Make sure you have user account with added credit cards and positive balance
    """
    keep_browser_open = True

    def test_000_create_events(self):
        """
        DESCRIPTION: Create test events
        EXPECTED: Events are created
        """
        self.__class__.username = tests.settings.betplacement_user
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children']
                             if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes
                                         if outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')
            self._logger.debug(f'*** Found Football event with selection ids "{self.selection_ids}" and team "{self.team1}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids
        # This is a workaround for handling case of placing Bet automatically without pressing Bet Now button
        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.logout()

    def test_001_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip
        EXPECTED: Added selection(s) present on the Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Verify Betslip is opened
        EXPECTED: 1. Betslip is opened
        EXPECTED: 2. 'Log in & Bet' button is disabled
        """
        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg='Log In & Bet button is not disabled')

    def test_003_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: 'Log in & Bet' button becomes enabled
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(timeout=5),
                        msg='Log In & Bet button is disabled')

    def test_004_tap_on_log_in_bet_button(self):
        """
        DESCRIPTION: Tap on 'Log in & Bet' button
        EXPECTED: 'Log In' pop-up is opened
        """
        self.get_betslip_content().bet_now_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='No login dialog present on page')

    def test_005_log_in_with_user_that_has_added_credit_cards_and_positive_balance(self):
        """
        DESCRIPTION: Log in with user that has **added credit cards and positive balance**
        EXPECTED: 1. Betslip is NOT refreshed
        EXPECTED: 2. User is logged in
        EXPECTED: 3. Bet is placed automatically (NOTE: if at least one pop-up is expected after login, Bet is NOT placed automatically)
        EXPECTED: 4. Bet Receipt is shown
        """
        self.site.login(username=self.username,
                        timeout_wait_for_dialog=1,
                        ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST,
                        close_free_bets_notification=False,
                        async_close_dialogs=False)

        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=3)
        if dialog:
            dialog.close_dialog()
            self.assertFalse(self.site.is_bet_receipt_displayed(expected_result=False), msg='Bet Receipt is displayed')
        else:
            self.check_bet_receipt_is_displayed()
