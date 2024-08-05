import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_history
@pytest.mark.bet_history_open_bets
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C28139_Verify_Settled_Bets_tab_when_Settled_Bets_is_empty(BaseBetSlipTest):
    """
    TR_ID: C28139
    NAME: Verify Settled Bets tab when Settled Bets is empty
    DESCRIPTION: This test case verifies Settled Bets tab when Settled Bets is empty.
    PRECONDITIONS: * User should be logged in to view their settled bets (bet history)
    PRECONDITIONS: * User should have never place a bet
    """
    keep_browser_open = True

    def test_001_login_as_user_that_have_never_placed_bet(self):
        """
        DESCRIPTION: Login as user that has never placed bet
        EXPECTED: Successfully logged in
        """
        self.__class__.expected_page_title = vec.bet_history.TAB_TITLE
        self.site.login(username=tests.settings.no_bet_history_user, async_close_dialogs=False)

    def test_002_navigate_to_bet_history_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 1. 'Settled Bets' tab is opened
        EXPECTED: 2. Four sort filters are present :
        EXPECTED: *   Regular (selected by default)
        EXPECTED: *   Player Bets
        EXPECTED: *   Lotto
        EXPECTED: *   Pools
        EXPECTED: 3. Sorting section with four options is present:
        EXPECTED: *   Last 2 days (selected by default)
        EXPECTED: *   Last 7 days
        EXPECTED: *   Last 14 days
        EXPECTED: *   Show All
        EXPECTED: Note: Sorting option is not shown for 'Player Bets' sort filter
        EXPECTED: 4. 'You have no betslip history.' message is displayed
        """
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state(state_name='BetHistory')
        page_title = self.site.bet_history.header_line.page_title.title
        self.assertEqual(
            page_title,
            self.expected_page_title,
            msg=f'Page title "{page_title}" doesn\'t match expected text "{self.expected_page_title}"')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.site.wait_content_state('open-bets')
        self.site.open_bets.tabs_menu.items_as_ordered_dict.get(vec.bet_history.SETTLED_BETS_TAB_NAME).click()
        self.site.wait_content_state(state_name='BetHistory')
        active_tab = self.site.bet_history.tabs_menu.current
        self.assertEqual(active_tab, vec.bet_history.SETTLED_BETS_TAB_NAME,
                         msg=f'"{vec.bet_history.SETTLED_BETS_TAB_NAME}" is not active tab, active tab is: "{active_tab}"')

        self.check_bet_sorting_types(tab=vec.bet_history.SETTLED_BETS_TAB_NAME)
        no_bet_history_label = self.site.bet_history.tab_content.accordions_list.no_bets_message
        self.assertEqual(no_bet_history_label, vec.bet_history.NO_HISTORY_INFO,
                         msg=f'Text "{no_bet_history_label}" is not the same as expected "{ vec.bet_history.NO_HISTORY_INFO}"')

    def test_003_check_page_when_lotto_sort_filter_is_selected(self):
        """
        DESCRIPTION: Check page when 'Lotto' sort filter is selected
        """
        self.site.bet_history.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
        self.check_bet_sorting_types(tab=vec.bet_history.SETTLED_BETS_TAB_NAME, expected_active_btn=vec.bet_history.LOTTO_TAB_NAME)
        no_bet_history_label = self.site.bet_history.tab_content.accordions_list.no_bets_message
        self.assertEqual(no_bet_history_label, vec.bet_history.NO_LOTTO_BETS,
                         msg=f'Text "{no_bet_history_label}" is not the same as expected "{vec.bet_history.NO_LOTTO_BETS}"')

    def test_004_check_page_when_pools_sort_filter_is_selected(self):
        """
        DESCRIPTION: Check page when 'Pools' sort filter is selected
        """
        self.site.bet_history.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        self.check_bet_sorting_types(tab=vec.bet_history.SETTLED_BETS_TAB_NAME, expected_active_btn=vec.bet_history.POOLS_TAB_NAME)
        no_bet_history_label = self.site.bet_history.tab_content.accordions_list.no_bets_message
        self.assertEqual(no_bet_history_label, vec.bet_history.NO_HISTORY_INFO,
                         msg=f'Text "{no_bet_history_label}" is not the same as expected "{vec.bet_history.NO_HISTORY_INFO}"')
