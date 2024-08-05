import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from random import uniform


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't grant freebets
# @pytest.mark.hl
@pytest.mark.freebets
@pytest.mark.quick_bet
@pytest.mark.user_account
@pytest.mark.mobile_only
@pytest.mark.low
@pytest.mark.login
# todo: VOL-5699 Adapt C884503 "Verify Free Bets when Session is over"
@vtest
class Test_C884503_Verify_Free_Bets_when_Session_is_over(BaseSportTest, BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C884503
    VOL_ID: C9698236
    NAME: Verify Free Bets when Session is over
    """
    keep_browser_open = True
    freebet_value = f'{uniform(1, 2):.2f}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Login as a user with Freebets available
        """
        self.__class__.eventID = self.ob_config.add_football_event_to_england_championship().event_id
        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username, freebet_value=self.freebet_value)

        self.site.login(username=username)
        market_name = self.ob_config.football_config.england.championship.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Selected price/odds are highlighted in green
        EXPECTED: Quick Bet is displayed at the bottom of the page
        EXPECTED: 'Use Free bet' link is displayed under event name
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content
        self.assertTrue(self.quick_bet.has_use_free_bet_link(), msg='"Use Free Bet" link is not present')

    def test_002_tap_use_free_bet_link_and_select_free_bet_from_the_pop_up(self):
        """
        DESCRIPTION: Tap "Use Free Bet" link and select Free bet from the pop-up
        EXPECTED: Free bet is selected
        """
        self.site.quick_bet_panel.selection.content.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value))

    def test_003_make_steps_listed_in_preconditions(self):
        """
        DESCRIPTION: Duplicate tab
        DESCRIPTION: Log out from the second tab
        EXPECTED: User session is over
        """
        self.device.open_new_tab()

        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_logged_in(timeout=5), msg='User is not logged in')
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

        self.site.logout()
        self.device.close_current_tab()
        self.device.open_tab(tab_index=0)

    def test_004_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick Bet
        EXPECTED: 'Log out' pop-up is displayed
        EXPECTED: Quick Bet stays opened
        EXPECTED: Free bet drop-down is NOT displayed
        """
        if self.brand != 'ladbrokes':
            self.verify_logged_out_state()
            self.site.wait_content_state('EventDetails')
        else:
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

            quick_bet = self.site.quick_bet_panel.selection.content
            self.assertFalse(quick_bet.has_remove_free_bet_link(expected_result=False),
                             msg='"Remove Free Bet" link is present after logout')
