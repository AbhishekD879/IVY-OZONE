import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.banach
@pytest.mark.build_your_bet
@pytest.mark.quick_bet
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C1922185_Banach_Removing_selections_from_Quick_Bet_Betslip(BaseBanachTest):
    """
    TR_ID: C1922185
    NAME: Banach. Removing selections from Quick Bet Betslip
    DESCRIPTION: Test case verifies Banach selections removal from Quick bet betslip and storing in dashboard
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for details on adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: |||:Operation|:Banach code
    PRECONDITIONS: || Client adds selections to remote betslip | 50001
    PRECONDITIONS: || Response message for adding selections | 51001
    PRECONDITIONS: || Client message to remove selections from betslip |30001
    PRECONDITIONS: || Response message when selections removed |30002
    PRECONDITIONS: **Build Your Bet tab on event details page is loaded and selections are added to dashboard**
    """
    keep_browser_open = True
    proxy = None
    bet_amount = 0.4
    expected_dashboard_all_markets_and_selections = []
    blocked_hosts = ['*spark-br.*']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Login and navigate to EDP using derived event_id
        """
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        byb_markets = self.cms_config.get_build_your_bet_markets()
        markets_list = [market['bybMarket'] for market in byb_markets]
        if self.expected_market_tabs.build_your_bet.title() and self.expected_market_sections.match_betting.title() \
                and self.expected_market_sections.both_teams_to_score.title() not in markets_list:
            raise CmsClientException(f'BYB Markets "{self.expected_market_tabs.build_your_bet.title()}" or'
                                     f'"{self.expected_market_sections.match_betting.title()}" or'
                                     f'"{self.expected_market_sections.both_teams_to_score.title()}" was not found')
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID)
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(byb_tab, msg=f'{self.expected_market_tabs.build_your_bet} tab is not active')

        # Match betting 90 mins selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.__class__.initial_match_betting_selection_name = match_betting.set_market_selection(selection_index=1)[0]
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(self.initial_match_betting_selection_name, msg='No selections added to Dashboard')
        match_betting_default_switcher = match_betting.time_period_outcomes_list.current
        self.assertTrue(self.initial_match_betting_selection_name, msg='Match betting selection is not added to Dashboard')
        if "Minutes" in match_betting_default_switcher:
            match_betting_default_switcher = match_betting_default_switcher.replace("Minutes", "mins")
        match_betting_market_and_selection_name = f'{self.initial_match_betting_selection_name} ' \
                                                  f'{self.expected_market_sections.match_betting.title()} ' \
                                                  f'{match_betting_default_switcher}'

        self.__class__.expected_dashboard_all_markets_and_selections.append(match_betting_market_and_selection_name)
        match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1

        # Both Teams To Score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        self.assertTrue(both_teams_to_score_market,
                        msg=f'"{self.expected_market_sections.both_teams_to_score}" market does not exist')
        self.__class__.initial_both_teams_to_score_selection_name = both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(self.initial_both_teams_to_score_selection_name, msg='No one selection added to Dashboard')
        self.expected_dashboard_all_markets_and_selections.append(self.initial_both_teams_to_score_selection_name)
        both_teams_to_score_market.add_to_betslip_button.click()

        self.__class__.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

    def test_001_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on "Place bet" button
        EXPECTED: - Betslip with price field and numeric keyboard appears
        """
        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')

        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='Build Your Bet Betslip not appears')
        self.site.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)
        self.assertTrue(self.site.byb_betslip_panel.selection.content.odds,
                        msg='Odds/price are not shown')

    def test_002_tap_back_button(self):
        """
        DESCRIPTION: Tap "Back" button
        EXPECTED: - Betslip is removed
        EXPECTED: - Dashboard with "Place bet" button is shown
        EXPECTED: - Selections are present on UI (selections are highlighted in market accordions)
        """
        self.site.byb_betslip_panel.back_button.click()

        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(timeout=10),
                        msg='"Build Your Bet" dashboard is not shown')
        place_bet_button = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet
        self.assertTrue(place_bet_button.is_displayed(), msg='"Place bet" button is not shown')

        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'Can not get market "{self.expected_market_sections.match_betting}"')
        match_betting_outcomes = match_betting.outcomes.items_as_ordered_dict
        self.assertTrue(match_betting_outcomes,
                        msg=f'No outcomes found in "{self.expected_market_sections.match_betting}" section')
        match_betting_selection_name, match_betting_selection = tuple(match_betting_outcomes.items())[0]
        self.assertEqual(match_betting_selection_name, self.initial_match_betting_selection_name,
                         msg=f'Selection name "{match_betting_selection_name}" is not the same '
                             f'as expected "{self.initial_match_betting_selection_name}"')

        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        self.assertTrue(both_teams_to_score_market,
                        msg=f'Can not get market "{self.expected_market_sections.both_teams_to_score}"')
        both_teams_to_score_outcomes = both_teams_to_score_market.outcomes.items_as_ordered_dict
        self.assertTrue(both_teams_to_score_outcomes,
                        msg=f'No outcomes found in "{self.expected_market_sections.both_teams_to_score}" section')
        both_teams_to_score_selection_name,  both_teams_to_score_selection = tuple(both_teams_to_score_outcomes.items())[0]
        self.assertEqual(both_teams_to_score_selection_name, 'Both',
                         msg=f'Selection name "{both_teams_to_score_selection_name}" is not the same '
                             f'as expected "Both"')

    def test_003_expand_dashboard(self):
        """
        DESCRIPTION: Expand dashboard
        EXPECTED: Selections are saved in dashboard
        """
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.click()
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(timeout=5)
        self.assertTrue(is_expanded, msg='Dashboard is not expanded')

        byb_selections = list(self.get_byb_dashboard_outcomes().keys())
        self.assertTrue(byb_selections, msg=f'Dashboard selections "{byb_selections}" are not displayed ')
