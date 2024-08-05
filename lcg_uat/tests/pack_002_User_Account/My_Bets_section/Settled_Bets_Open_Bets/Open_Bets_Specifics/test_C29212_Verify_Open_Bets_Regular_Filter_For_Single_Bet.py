import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.bet_history_open_bets
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29212_Verify_Open_Bets_Regular_Filter_For_Single_Bet(BaseBetSlipTest):
    """
    TR_ID: C29212
    VOL_ID: C9698401
    NAME: Verify Open Bets tab Regular filter for Single bet
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as Oxygen user, create test event, add selections with deep link and place single bets
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_ids = list(event_selection.values())
            self.__class__.expected_selection_names = list(event_selection.keys())
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            selection_ids = [event_params.selection_ids[event_params.team1],
                             event_params.selection_ids['Draw'],
                             event_params.selection_ids[event_params.team2]]
            self.__class__.expected_selection_names = [event_params.team1, 'Draw', event_params.team2]
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_and_validate_single_bet(number_of_stakes=len(self.expected_selection_names))
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state(state_name='HomePage')

    def test_001_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        EXPECTED: 'My Bets' page / 'Bet Slip' widget is opened
        EXPECTED: 'Open Bets' tab is shown next to 'Cash Out' tab
        """
        self.site.open_my_bets_cashout()
        page_title = self.site.cashout.header_line.page_title.title
        self.assertEqual(page_title, self.expected_my_bets_page_title,
                         msg=f'Page title "{page_title}" '
                             f'doesn\'t match expected text "{self.expected_my_bets_page_title}"')

        tabs = self.site.cashout.tabs_menu.items_names
        expected_tabs = self.get_expected_my_bets_tabs()
        self.assertListEqual(tabs, expected_tabs,
                             msg=f'Actual tabs order: "{tabs}" '
                             f'is not as expected: "{expected_tabs}"')

    def test_002_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: 'Regular' sort filter is selected by default
        """
        self.site.cashout.tabs_menu.open_tab(tab_name=vec.bet_history.OPEN_BETS_TAB_NAME)
        result = wait_for_result(lambda: self.site.open_bets.tab_content.grouping_buttons.current == self.expected_active_btn_open_bets,
                                 name=f'"{self.expected_active_btn_open_bets}" to became active',
                                 timeout=2)
        self.assertTrue(result, msg=f'"{self.expected_active_btn_open_bets}" sorting type is not selected by default')

    def test_003_verify_bet_overview_displaying(self):
        """
        DESCRIPTION: Verify Bet overview displaying
        EXPECTED: All sections are displayed chronologically
        EXPECTED: If there are more than 20 sections, they are loaded after scrolling by portions
        """
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        actual_selection_names = []
        for section_name, selection in list(sections.items())[:len(self.expected_selection_names)]:
            bet_legs = selection.items_as_ordered_dict
            self.assertEquals(len(bet_legs), 1,
                              msg=f'Single bet: "{section_name}" contains "{len(bet_legs)}" '
                              f'bet legs: \n[{bet_legs.keys()}]')
            bet_leg_name, bet_leg = list(bet_legs.items())[0]
            actual_selection_names.append(bet_leg.outcome_name)
        # All sections are displayed chronologically
        self.assertListEqual(actual_selection_names, self.expected_selection_names,
                             msg=f'Expected list of names {self.expected_selection_names} does not match Actual'
                                 f'values {actual_selection_names}')
        self.site.open_bets.scroll_to_bottom()
        self.site.open_bets.tab_content.accordions_list.wait_for_sections()
        # If there are more than 20 sections, they are loaded after scrolling by portions
        # Skip this validation for Open Bets, will be covered for Settled Bets
