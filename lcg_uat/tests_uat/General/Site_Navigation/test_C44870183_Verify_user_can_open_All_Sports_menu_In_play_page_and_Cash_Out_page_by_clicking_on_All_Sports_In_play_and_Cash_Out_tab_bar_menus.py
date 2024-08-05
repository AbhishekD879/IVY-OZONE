import pytest

import tests
import voltron.environments.constants as vec
from random import choice
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.content_manager import ContentManager
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from datetime import timedelta
from datetime import date


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.navigation
@pytest.mark.mobile_only
@pytest.mark.uat
@pytest.mark.in_play
@pytest.mark.my_bets
@pytest.mark.cash_out
@pytest.mark.all_sports
@vtest
class Test_C44870183_Verify_user_can_open_All_Sports_menu_In_play_page_and_Cash_Out_page_by_clicking_on_All_Sports_In_play_and_Cash_Out_tab_bar_menus(BaseBetSlipTest):
    """
    TR_ID: C44870183
    AUTOTEST: C49050590
    NAME: Verify user can open 'All Sports' menu , 'In-play' page and 'Cash Out' page by clicking on 'All Sports' , 'In-play' and 'Cash Out' tab bar menus.
    PRECONDITIONS: App should be loaded.
    """
    keep_browser_open = True

    def place_bet(self, selection_id):
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active cashout event on prod
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                               OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True,
                                                         additional_filters=cashout_filter,
                                                         in_play_event=False)
            event = choice(events)
            match_result_market = next((market['market'] for market in event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(all_selection_ids.values())[0]
            self.__class__.event_name = event['event']['name']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            all_selection_ids = event.selection_ids
            self.__class__.selection_id = list(all_selection_ids.values())[0]
            self.__class__.event_name = event.team1 + ' v ' + event.team2

    def test_001_tap_on_menu_from_bottom_menu_bar(self):
        """
        DESCRIPTION: Tap on 'Menu' from bottom menu bar
        EXPECTED: 'All Sports' opens with 'Top Sports' followed by 'A-Z Sports' Sections.
        EXPECTED: User should be able to tap on any of the menu items and corresponding page should load.
        """
        footer_items = self.site.navigation_menu.items_as_ordered_dict
        self.assertTrue(footer_items, msg='No items on bottom menu bar')
        if self.brand == 'bma':
            footer_items.get(vec.SB.ALL_SPORTS_FOOTER_ITEM).click()
        else:
            footer_items.get(vec.SB.MENU_FOOTER_ITEM).click()
        self.site.wait_content_state(state_name='AllSports')
        top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(top_sports, msg='No sports found in "Top Sports" section')
        az_sports = self.site.all_sports.a_z_sports_section.name
        self.assertEqual(az_sports, vec.SB.AZ_SPORTS.upper(),
                         msg=f'"{vec.SB.AZ_SPORTS.upper()}" section is not displayed')
        sport_name, sport_value = next(((sport_name, sport_value) for sport_name, sport_value in top_sports.items()
                                        if sport_name.lower() in ContentManager().pages.keys()), (None, None))
        self.assertTrue(sport_name, msg=f'No known sport found in top menu "{top_sports.keys()}"')
        sport_value.click()
        self.site.wait_content_state(state_name=sport_name)
        self.site.back_button.click()

    def test_002_while_on_all_sports_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'All Sports' page tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        self.site.wait_content_state(state_name='AllSports')
        self.site.back_button.click()
        self.site.wait_content_state(state_name='HomePage')

    def test_003_tap_on_in_play_from_bottom_menu_bar(self):
        """
        DESCRIPTION: Tap on 'In-Play' from bottom menu bar
        EXPECTED: 'In-Play' page is loaded and all the events which are live should appear followed by Upcoming events.
        EXPECTED: User should be able to switch between sports from the sub header by tapping on corresponding sport icon.
        EXPECTED: User should be able to see list of Live events for which streaming is available by tapping on 'Watch Live' icon.
        """
        footer_items = self.site.navigation_menu.items_as_ordered_dict
        self.assertTrue(footer_items, msg='No items on bottom menu bar')
        if self.brand == 'bma':
            footer_items.get(vec.inplay.BY_IN_PLAY.upper()).click()
        else:
            footer_items.get(vec.inplay.BY_IN_PLAY).click()
        in_play_events = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        self.assertTrue(in_play_events, msg=f'No "{vec.Inplay.LIVE_NOW_SWITCHER}" events found')
        upcoming_events = self.site.inplay.tab_content.upcoming.items_as_ordered_dict
        self.assertTrue(upcoming_events, msg=f'No "{vec.Inplay.UPCOMING_SWITCHER}" events found')
        events_in_play = self.site.home.menu_carousel.items_as_ordered_dict
        for event_name, event in events_in_play.items():
            event.click()
            if event_name == vec.SB.WATCH_LIVE_LABEL:
                watch_live_events = self.site.inplay.tab_content.live_now.items_as_ordered_dict
                if len(watch_live_events) > 0:
                    self.assertTrue(watch_live_events, msg='No events found in "Watch Live"')
                    for tab_name, tab in watch_live_events.items():
                        for _, watch_live_event in list(tab.items_as_ordered_dict.items()):
                            self.assertTrue(watch_live_event.has_watch_live_icon,
                                            msg='"Watch Live" icon is not displayed')

    def test_004_while_on_in_play_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'In Play' page tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        self.site.wait_content_state(state_name='In-Play')
        self.site.back_button.click()

    def test_005_tap_on_cash_out_from_bottom_menu_bar_for_a_logged_out_user(self):
        """
        DESCRIPTION: Tap on 'CASH OUT' from bottom menu bar for a Logged out user
        EXPECTED: 'My Bets' page should open with 'CASH OUT' tab expanded by default.
        EXPECTED: 'Please log in to see your cash out bets' will appear along with 'Login' tab.
        """
        if self.brand == 'bma':
            self.site.navigation_menu.items_as_ordered_dict.get(vec.BetHistory.CASH_OUT_TAB_NAME).click()
        else:
            self.site.navigation_menu.items_as_ordered_dict.get(vec.SB.MY_BETS_FOOTER_ITEM).click()
        active_tab = self.site.cashout.tabs_menu.current
        if self.brand == 'ladbrokes':
            self.assertEqual(active_tab, vec.BetHistory.OPEN_BETS_TAB_NAME,
                             msg=f'Current tab is: "{active_tab}", not the same as expected: "{vec.BetHistory.OPEN_BETS_TAB_NAME}"')
        else:
            self.assertEqual(active_tab, vec.BetHistory.CASH_OUT_TAB_NAME,
                             msg=f'Current tab is: "{active_tab}", not the same as expected: "{vec.BetHistory.CASH_OUT_TAB_NAME}"')
        cashout = self.site.cashout.tab_content
        if self.brand == 'bma':
            self.assertEqual(cashout.please_login_text, vec.BetHistory.CASHOUT_PLEASE_LOGIN_MESSAGE,
                             msg=f'Actual: "{cashout.please_login_text}" is not equal '
                                 f'to expected: "{vec.BetHistory.CASHOUT_PLEASE_LOGIN_MESSAGE}"')
        else:
            self.assertEqual(cashout.please_login_text, vec.BetHistory.OPEN_BETS_PLEASE_LOGIN_MESSAGE,
                             msg=f'Actual: "{cashout.please_login_text}" is not equal '
                                 f'to expected: "{vec.BetHistory.OPEN_BETS_PLEASE_LOGIN_MESSAGE}"')

    def test_006_while_on_my_bets_page_tap_on_open_bets_for_a_logged_out_user(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'OPEN BETS' for a logged out user
        EXPECTED: 'Please log in to see your open bets' message is seen along with 'Log in' tab.
        """
        self.site.cashout.tabs_menu.items_as_ordered_dict.get(vec.BetHistory.OPEN_BETS_TAB_NAME).click()
        open_bets = self.site.open_bets.tab_content
        self.assertEqual(open_bets.please_login_text, vec.BetHistory.OPEN_BETS_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual: "{open_bets.please_login_text}" is not equal '
                             f'to expected: "{vec.BetHistory.OPEN_BETS_PLEASE_LOGIN_MESSAGE}"')

    def test_007_while_on_my_bets_page_tap_on_settled_bets_for_a_logged_out_user(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'SETTLED BETS' for a logged out user
        EXPECTED: 'Please log in to see your settled bets' message is seen along with 'Log in' tab.
        """
        self.site.open_bets.tabs_menu.items_as_ordered_dict.get(vec.BetHistory.SETTLED_BETS_TAB_NAME).click()
        settled_bets = self.site.bet_history.tab_content
        self.assertEqual(settled_bets.please_login_text, vec.BetHistory.SETTLED_BETS_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual: "{settled_bets.please_login_text}" is not equal '
                             f'to expected: "{vec.BetHistory.SETTLED_BETS_PLEASE_LOGIN_MESSAGE}"')

    def test_008_tap_on_cashout_from_bottom_menu_bar_for_a_logged_in_user(self):
        """
        DESCRIPTION: Tap on 'CASH OUT' from bottom menu bar for a Logged in user
        EXPECTED: 'My Bets' page should open with 'CASH OUT' tab expanded by default.
        EXPECTED: The current cash out bets of the user will be displayed with the latest bet placed at the top.
        """
        self.site.login()
        self.place_bet(selection_id=self.selection_id)
        if self.brand == 'bma':
            self.site.navigation_menu.items_as_ordered_dict.get(vec.BetHistory.CASH_OUT_TAB_NAME).click()
        else:
            self.site.navigation_menu.items_as_ordered_dict.get(vec.SB.MY_BETS_FOOTER_ITEM).click()
        active_tab = self.site.cashout.tabs_menu.current
        if self.brand == 'ladbrokes':
            self.assertEqual(active_tab, vec.BetHistory.OPEN_BETS_TAB_NAME,
                             msg=f'Current tab is: "{active_tab}", not the same as expected: "{vec.BetHistory.OPEN_BETS_TAB_NAME}"')
        else:
            self.assertEqual(active_tab, vec.BetHistory.CASH_OUT_TAB_NAME,
                             msg=f'Current tab is: "{active_tab}", not the same as expected: "{vec.BetHistory.CASH_OUT_TAB_NAME}"')
        cashout_bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(cashout_bets,
                        msg=f'No "{vec.BetHistory.CASH_OUT_TAB_NAME}" bets are present for logged in User')
        for event_name, event in cashout_bets.items():
            self.assertTrue(self.event_name in event_name, msg=f'The latest bet placed is not on the top')
            break

    def test_009_navigate_to_open_bets_on_cashout_tab_for_a_logged_in_user(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'OPEN BETS' for a logged in user
        EXPECTED:The current open bets of the user will be displayed with the latest bet placed at the top.
        EXPECTED: User should be able to switch between Sports / Lotto / Pools under OPEN BETS tab
        """
        if self.brand == 'bma':
            self.site.cashout.tabs_menu.items_as_ordered_dict.get(vec.BetHistory.OPEN_BETS_TAB_NAME).click()
        open_bet = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        for event_name, event in open_bet.items():
            self.assertTrue(self.event_name in event_name, msg=f'The latest bet placed is not on the top')
            break
        self.assertTrue(open_bet, msg=f'No "{vec.BetHistory.OPEN_BETS_TAB_NAME}" are present for logged in User')
        tabs = self.site.open_bets.tab_content.grouping_buttons.items_as_ordered_dict
        for tab_name, tab in tabs.items():
            tab.click()
            expected_tab_name = self.site.open_bets.tab_content.grouping_buttons.current
            self.assertEqual(tab_name, expected_tab_name,
                             msg=f'Not the correct tab under "{vec.BetHistory.OPEN_BETS_TAB_NAME}".'
                                 f'Actual: "{tab_name}", Expected: "{expected_tab_name}"')

    def test_010_navigate_to_settled_bets_on_cashout_tab_for_a_logged_in_user(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'SETTLED BETS' for a logged in user
        EXPECTED: all the settled bets of the user for the set period of time should be displayed.
        EXPECTED: User should be able to switch between Sports / Lotto / Pools under OPEN BETS tab.
        EXPECTED: User should be able to set From and To dates to view all the settled bets between that period.
        """
        self.site.open_bets.tabs_menu.items_as_ordered_dict.get(vec.BetHistory.SETTLED_BETS_TAB_NAME).click()
        new_date = date.today() - timedelta(days=5)
        past_date = new_date.__format__('%d/%m/%Y')
        self.site.bet_history.tab_content.accordions_list.date_picker.date_picker_value = past_date
        settled_bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        if len(settled_bets) is 0:
            self._logger.info(f'No "{vec.BetHistory.SETTLED_BETS_TAB_NAME}" are present for logged in User')
        else:
            self.assertTrue(settled_bets,
                            msg=f'No "{vec.BetHistory.SETTLED_BETS_TAB_NAME}" are present for logged in User')
            tabs = self.site.bet_history.tab_content.grouping_buttons.items_as_ordered_dict
            for tab_name, tab in tabs.items():
                tab.click()
                expected_tab_name = self.site.bet_history.tab_content.grouping_buttons.current
                self.assertEqual(tab_name, expected_tab_name,
                                 msg=f'Not the correct tab under "{vec.BetHistory.SETTLED_BETS_TAB_NAME}".'
                                     f' Actual: "{tab_name}", Expected: "{expected_tab_name}"')

    def test_011_while_on_my_bets_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        self.site.back_button.click()
        self.site.wait_content_state('OpenBets')
