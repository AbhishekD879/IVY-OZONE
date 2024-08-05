import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Event can not be created in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.slow
@vtest
class Test_C28559_Verify_placing_a_bet_on_Over_Under_Home_Away_Team_Goals_markets(BaseBetSlipTest):
    """
    TR_ID: C28559
    NAME: Verify placing a bet on Over/Under <Home/Away Team> Goals markets
    DESCRIPTION: This test case verifies placing a bet on 'Over/Under <Home/Away Team> Goals' market sections
    PRECONDITIONS: Football events with 'Over/Under <Home/Away Team> Goals' markets (Over/Under <Home/Away Team> Goals <figure afterward>, Over/Under First Half <Home/Away Team> Goals <figure afterward>, Over/Under Second Half <Home/Away Team> Goals <figure afterward>)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: *   **<figure afterward> **- variable part of market name shown in format 'X.5' as an amount of goals (e.g. 0.5, 1.5, 2.5 etc)
    PRECONDITIONS: *   **<Home Team>** - name of the team that is shown first in the Event Name
    PRECONDITIONS: *   **<Away Team>** - name of the team that is shown second in the Event Name
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Total Goals Over/Under x.x"
    PRECONDITIONS: *   PROD: name="Over/Under Total Goals x.x"
    PRECONDITIONS: **Jira ticket: **BMA-3902
    """
    keep_browser_open = True

    def get_markets(self, market=None):
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')
        if self.brand == 'bma' and self.device_type == 'mobile':
            self.__class__.expected_market_name = market.upper()
        else:
            self.__class__.expected_market_name = market
        self.assertIn(self.expected_market_name, list(self.markets_list.keys()),
                      msg=f'"{self.expected_market_name}" section is not present')
        self.__class__.over_under_home_team_total_goals = self.markets_list.get(self.expected_market_name)
        self.assertTrue(self.over_under_home_team_total_goals,
                        msg=f'"{self.expected_market_name}" section is not found in "{self.markets_list.keys()}"')
        if not self.over_under_home_team_total_goals.is_expanded():
            sleep(2)
            self.over_under_home_team_total_goals.expand()
        self.assertTrue(self.over_under_home_team_total_goals.is_expanded(),
                        msg=f'"{self.over_under_home_team_total_goals}" section is not expanded')

    def get_outcome(self):

        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

        outcomes = self.markets_list[self.expected_market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')

        return outcomes

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event and navigate to football/matches
        EXPECTED: Navigate to Football Matches tab
        """
        markets = [('over_under_home_team_total_goals', {'over_under': 1.5}),
                   ('over_under_away_team_total_goals', {'over_under': 1.5}),
                   ('over_under_first_half_home_team_total_goals', {'over_under': 1.5}),
                   ('over_under_first_half_away_team_total_goals', {'over_under': 1.5}),
                   ('over_under_second_half_home_team_total_goals', {'over_under': 1.5}),
                   ('over_under_second_half_away_team_total_goals', {'over_under': 1.5}), ]

        event = self.ob_config.add_autotest_premier_league_football_event(markets=markets)
        self.__class__.eventID = event.event_id
        self.__class__.outcome_value = {}
        self.__class__.event_name = '%s v %s' % (event.team1, event.team2)
        self.__class__.market_name = [f'Over/Under Goals {event.team1}', f'Over/Under Goals {event.team2}']
        if self.brand == 'bma':
            if self.device_type == 'mobile':
                self.__class__.market_name = [f'Over/Under Goals {event.team1}'.upper(),
                                              f'Over/Under Goals {event.team2}'.upper()]
            else:
                self.__class__.market_name = [f'Over/Under Goals {event.team1}'.title(),
                                              f'Over/Under Goals {event.team2}'.title()]
        else:
            self.__class__.market_name = [f'Over/Under Goals {event.team1}'.title().replace('Auto Test', 'Auto test'),
                                          f'Over/Under Goals {event.team2}'.title().replace('Auto Test', 'Auto test')]
        for market in event.ss_response['event']['children']:
            self.__class__.market_names = ['Over/Under Home Team Total Goals',
                                           'Over/Under Away Team Total Goals']
            if market['market']['templateMarketName'] == self.market_names[0]:
                self.__class__.first_half_market = market['market']['children']
                for outcomes in self.first_half_market:
                    self.outcome_value.update(
                        {outcomes['outcome']['name']: outcomes['outcome']['children'][0]['price']['priceDec']})

            elif market['market']['templateMarketName'] == self.market_names[1]:
                self.__class__.second_half_market = market['market']['children']
                for outcomes in self.second_half_market:
                    self.outcome_value.update(
                        {outcomes['outcome']['name']: outcomes['outcome']['children'][0]['price']['priceDec']})

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('homepage')
        self.site.login()

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(self.eventID, timeout=30)
        wait_for_result(lambda: self.site.wait_content_state(state_name='EventDetails'), timeout=120)
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)
        markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.all_markets)

    def test_003_go_to_overunder_home_team_goals__section(self):
        """
        DESCRIPTION: Go to 'Over/Under **<Home Team> **Goals**** ****' section
        EXPECTED: Section is expanded and displayed correctly
        """
        self.get_markets(market=self.market_name[0])

    def test_004_verify_market_section(self):
        """
        DESCRIPTION: Verify market section
        EXPECTED: Market section is displayed within 'Over/Under <Team Name> Goals' section and contains the following:
        EXPECTED: *   Market name
        EXPECTED: *   Price/odds buttons of  available options: 'Over', 'Under'
        EXPECTED: *   If price of any of those markets is not available - corresponding price/odds button is not shown
        """
        self.assertIn(self.expected_market_name, self.markets_list,
                      msg=f'"{self.expected_market_name}" section is not present')
        self.get_outcome()

    def test_005_verify_market_name(self):
        """
        DESCRIPTION: Verify market name
        EXPECTED: Selection name corresponds to <figure afterward> part of '**name**' attribute on the market level (e.g. **0.5 **of market with name="Over/Under <Home Team> Goals 0.5")
        """
        outcome = self.get_outcome()
        actual_selection_names = outcome.keys()

        self.assertIn('1.5', actual_selection_names,
                      msg=f'Selection name "{1.5}" is not the same as expected "{actual_selection_names}"')

    def test_006_verify_priceodds_buttons_correspondence_to_verified_markets(self):
        """
        DESCRIPTION: Verify Price/Odds buttons correspondence to verified markets
        EXPECTED: *   Price/odds buttons in 'Over' column correspond to 'Over' outcome data in SS response
        EXPECTED: *   Price/odds buttons in 'Under' column correspond to 'Under' outcome data in SS response
        """
        # Covered in step-8

    def test_007_verify_data_of_priceodds_buttons_in_fractional_format(self, format=None):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        outcomes = self.get_outcome()
        for outcome_name, outcome in outcomes.items():
            for price in outcome.items:
                if format == 'decimal':
                    self.assertRegexpMatches(price.outcome_price_text, self.decimal_pattern,
                                             msg=f'Stake odds value "{price.outcome_price_text}" not match decimal pattern: "{self.decimal_pattern}"')
                else:
                    self.assertRegexpMatches(price.outcome_price_text, self.fractional_pattern,
                                             msg=f'Stake odds value "{price.outcome_price_text}" not match fractional pattern: "{self.fractional_pattern}"')

    def test_008_verify_data_of_priceodds_buttons_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        current_url = self.device.get_current_url()

        # Changing the odd format to decimal from setting form
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')
        self.device.navigate_to(url=current_url)
        self.test_007_verify_data_of_priceodds_buttons_in_fractional_format(format='decimal')

        # Below is the validation for step-6
        outcomes = self.get_outcome()
        outcome_name, outcome = list(outcomes.items())[0]

        ui_outcome_data = {}
        ui_outcome_data.update({'Over': outcome.items_as_ordered_dict['Over'].outcome_price_text,
                                'Under': outcome.items_as_ordered_dict['Under'].outcome_price_text})

        self.assertDictEqual(ui_outcome_data, self.outcome_value,
                             msg=f'Outcome/Price values is different from actual outcome "{ui_outcome_data}" and expected outcomes "{self.outcome_value}" ')

    def test_009_selectunselect_same_priceodds_button(self):
        """
        DESCRIPTION: Select/unselect same Price/Odds button
        EXPECTED: Button is highlighted/unhighlighted respectively
        """
        outcomes = self.get_outcome()
        outcome_name, outcome = list(outcomes.items())[0]
        self.assertFalse(outcome.items[0].is_selected(expected_result=False),
                         msg=f'Bet button "{outcome_name}" is highlighted')
        outcome.items[0].click()
        self.site.wait_splash_to_hide()
        if self.device_type == 'mobile':
            sleep(3)
            self.site.wait_for_quick_bet_panel(timeout=60)
            sleep(7)
            self.site.quick_bet_panel.add_to_betslip_button.click()

    def test_010_add_single_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single selection to bet slip
        EXPECTED: Bet indicator displays 1.
        """
        # Covered in step-9

    def test_011_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: The bet is present
        """
        self.site.open_betslip()

    def test_012_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event start time and event name (**'startTime'** and event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        selection_name = "Over (+1.5)"
        self.assertEqual(self.stake_name, selection_name,
                         msg=f'Selection "{selection_name}" should be present in betslip')
        self.assertEqual(len(singles_section), 1,
                         msg='Only one selection should be present in betslip')
        event_name = self.stake.event_name
        self.assertEqual(event_name, self.event_name,
                         msg=f'Event name "{event_name}" is not the same as expected "{self.event_name}"')

        odd = self.stake.odds
        self.assertRegexpMatches(odd, self.decimal_pattern,
                                 msg=f'Stake odds value "{odd}" not match decimal pattern: "{self.decimal_pattern}"')

    def test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Estimated Returns**
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Total Est. Returns**
        """
        old_est_returns = self.stake.est_returns

        stake_name = self.stake.name
        stake_value = "0.10"

        self.__class__.stake_bet_amounts = {
            stake_name: stake_value,
        }
        self.enter_stake_amount(stake=(stake_name, self.stake), stake_bet_amounts=self.stake_bet_amounts)

        result = wait_for_result(lambda: self.stake.est_returns != old_est_returns,
                                 name='Estimated Returns value to change',
                                 timeout=2)
        self.assertTrue(result,
                        msg=f'"Est. Returns" field value "{self.stake.est_returns}" has not changed after stake was entered')

        total_stake = self.get_betslip_content().total_stake
        self.assertNotEqual(total_stake, '0.00',
                            msg=f'"Total Stake" field value "{total_stake}" has not changed after stake was entered')

    def test_014_tapbet_now_button(self):
        """
        DESCRIPTION: Tap **'Bet Now**' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_015_repeat_steps__4_14_for_overunderaway_teamgoals_market_section(self):
        """
        DESCRIPTION: Repeat steps № 4-14 for 'Over/Under **<Away Team> **Goals' market section
        EXPECTED:
        """
        self.test_002_go_to_event_details_page_of_football_event()
        self.get_markets(market=self.market_name[1])
        self.test_004_verify_market_section()
        self.test_005_verify_market_name()
        self.test_006_verify_priceodds_buttons_correspondence_to_verified_markets()
        current_url = self.device.get_current_url()

        # Changing the odd format to decimal from setting form
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')
        self.device.navigate_to(url=current_url)
        self.get_markets(market=self.market_name[1])
        self.test_007_verify_data_of_priceodds_buttons_in_fractional_format(format='decimal')

        # Below is the validation for step-6
        outcomes = self.get_outcome()
        outcome_name, outcome = list(outcomes.items())[0]

        ui_outcome_data = {}
        ui_outcome_data.update({'Over': outcome.items_as_ordered_dict['Over'].outcome_price_text,
                                'Under': outcome.items_as_ordered_dict['Under'].outcome_price_text})

        self.assertDictEqual(ui_outcome_data, self.outcome_value,
                             msg=f'Outcome/Price values is different from actual outcome "{ui_outcome_data}" and expected outcomes "{self.outcome_value}" ')
        self.test_009_selectunselect_same_priceodds_button()
        self.test_011_go_to_betslip()
        self.test_012_verify_selection()
        self.test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons()
        self.test_014_tapbet_now_button()
