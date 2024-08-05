import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


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
@pytest.mark.desktop
@vtest
class Test_C29212_Verify_Open_Bets_Regular_Filter_For_Multiple_Bets(BaseCashOutTest):
    """
    TR_ID: C29212
    VOL_ID: C9698293
    NAME: Verify Open Bets tab Regular filter for Multiple bets
    """
    keep_browser_open = True
    num_of_events = 3
    events_info = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as Oxygen user, create test event, add selections with deep link and place single bets
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            even = []
            for event in events:
                outcomes_1 = next(((market['market']['children']) for market in event['event']['children'] if
                                   market['market'].get('children')), None)

                if outcomes_1:
                    team1_1 = next((outcome['outcome']['name'] for outcome in outcomes_1 if
                                    outcome['outcome'].get('outcomeMeaningMinorCode') and
                                    outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
                    if team1_1:
                        even.append(event)
                if len(even) == 3:
                    break
            else:
                raise SiteServeException('There are no available outcomes')

            outcomes = next(((market['market']['children']) for market in even[0]['event']['children'] if
                             market['market'].get('children')), None)
            outcomes2 = next(((market['market']['children']) for market in even[1]['event']['children'] if
                              market['market'].get('children')), None)
            outcomes3 = next(((market['market']['children']) for market in even[2]['event']['children']if
                              market['market'].get('children')), None)

            event_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            event2_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes2}
            event3_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes3}
            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                          outcome['outcome'].get('outcomeMeaningMinorCode') and
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            team2 = next((outcome['outcome']['name'] for outcome in outcomes2 if
                          outcome['outcome'].get('outcomeMeaningMinorCode') and
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            team3 = next((outcome['outcome']['name'] for outcome in outcomes3 if
                          outcome['outcome'].get('outcomeMeaningMinorCode') and
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not team1 or not team2 or not team3:
                raise SiteServeException('No Home teams found')
            self.__class__.expected_names = [team1, team2, team3]
            selection_ids = [event_selection_ids[team1], event2_selection_ids[team2], event3_selection_ids[team3]]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            event2 = self.ob_config.add_autotest_premier_league_football_event()
            event3 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.expected_names = [event.team1, event2.team1, event3.team1]
            selection_ids = [event.selection_ids[event.team1], event2.selection_ids[event2.team1],
                             event3.selection_ids[event3.team1]]
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_multiple_bet()
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state(state_name='HomePage')

    def test_001_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        EXPECTED: 'My Bets' page / 'Bet Slip' widget is opened
        EXPECTED: 'Open Bets' tab is shown before 'Cash Out' tab
        """
        self.site.open_my_bets_cashout()

        if self.device_type == 'desktop':
            if self.brand == 'ladbrokes':
                page_title = self.site.betslip.name.title()
            else:
                page_title = self.site.betslip.name
        else:
            page_title = self.site.cashout.header_line.page_title.title
        self.assertEqual(page_title, self.expected_my_bets_page_title,
                         msg=f'Page title "{page_title}" is not as expected: "{self.expected_my_bets_page_title}"')

        if self.device_type == 'desktop':
            tabs = self.site.betslip.tabs_menu.items_names
        else:
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
        self.site.open_my_bets_open_bets()
        result = wait_for_result(lambda: self.site.open_bets.tab_content.grouping_buttons.current == self.expected_active_btn_open_bets,
                                 name=f'"{self.expected_active_btn_open_bets}" to became active',
                                 timeout=2)
        self.assertTrue(result, msg=f'"{self.expected_active_btn_open_bets}" sorting type is not selected by default')

    def test_003_verify_list_view_for_multiples(self):
        """
        DESCRIPTION: Verify Bet overview
        EXPECTED: All sections are displayed chronologically (**'settled=N'** attribute is set for all displayed bets
        EXPECTED: (from response select 'Network' tab-> 'All' filter -> choose last request that appears after bet line expanding ->'Preview' tab))
        EXPECTED: If there are more than 20 sections, they are loaded after scrolling by portions (20 sections by portion)
        """
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one Open Bet section found')

        section_name, self.__class__.section = list(sections.items())[0]
        bets = self.section.items_as_ordered_dict
        self.assertTrue(bets, msg=f'No one Open Bet found is section: "{section_name}"')

        actual_selection_name = []
        [actual_selection_name.append(bet_leg.outcome_name) for bet_leg_name, bet_leg in bets.items()]
        self.assertListEqual(actual_selection_name, self.expected_names,
                             msg=f'\nActual sections order: "{actual_selection_name}"'
                             f'\nis not as expected: \n"{self.expected_names}"')
