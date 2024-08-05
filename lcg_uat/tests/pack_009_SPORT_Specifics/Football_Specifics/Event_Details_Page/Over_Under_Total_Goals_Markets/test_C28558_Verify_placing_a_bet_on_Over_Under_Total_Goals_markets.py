import tests
import pytest
import voltron.environments.constants as vec
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.reg165_fix
@vtest
class Test_C28558_Verify_placing_a_bet_on_Over_Under_Total_Goals_markets(BaseBetSlipTest):
    """
    TR_ID: C28558
    NAME: Verify placing a bet on Over/Under Total Goals markets
    DESCRIPTION: This test case verifies markets data and bet placement on Over/Under Total Goals markets
    PRECONDITIONS: Football events with over/under markets (Total Goals Over/Under <figure afterward>, Over/Under First Half <figure afterward>, Over/Under Second Half <figure afterward>)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Note: **<figure afterward> **- variable part of market name shown in format 'X.5' as a amount of goals (e.g. 0.5, 1.5, 2.5 etc)
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Total Goals Over/Under x.x"
    PRECONDITIONS: *   PROD: name="Over/Under Total Goals x.x"
    PRECONDITIONS: **Jira ticket: **BMA-3901
    """
    keep_browser_open = True

    def get_outcome(self):

        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

        section = self.markets_list[self.expected_market_name]
        if not section.is_expanded():
            section.expand()
            if self.markets_list.get(self.expected_market_name).has_show_all_button:
                self.markets_list.get(self.expected_market_name).show_all_button.click()
        self.__class__.outcomes = section.outcomes.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No items found on market outcomes')

        return self.outcomes

    def get_outcome_from_event(self):

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.football_config.category_id)
        ss_event_details = ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                               query_builder=self.ss_query_builder)[0]
        self.__class__.final_outcome_value = {}
        for market in ss_event_details['event']['children']:
            if market.get('market').get('templateMarketName') in ['Total Goals Over/Under', 'Over/Under Total Goals']:
                outcome_value = {}
                if market['market']['children']:
                    for outcomes in market['market']['children']:
                        outcome_value.update(
                            {outcomes['outcome']['name']: outcomes['outcome']['children'][0]['price']['priceDec']})
                self.final_outcome_value[market.get('market')['rawHandicapValue']] = outcome_value

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event and navigate to football/matches
        EXPECTED: Navigate to Football Matches tab
        """
        markets = [('over_under_total_goals', {'over_under': 2.5}), ]
        self.__class__.handicap_value = []

        if tests.settings.backend_env == 'prod':

            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)
            for event in events:
                for market in event['event']['children']:
                    if market.get('market').get('templateMarketName') in ['Total Goals Over/Under', 'Over/Under Total Goals']:
                        self.__class__.eventID = market.get('market').get('eventId')
                        self.__class__.event_name = event['event']['name']
                        self.handicap_value.append(market.get('market')['rawHandicapValue'])
            if self.eventID is None:
                raise SiteServeException('There are no available market with Half-time/Full-time market')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(markets=markets, is_live=True)
            self.__class__.eventID = event.event_id
            self.__class__.event_name = event.ss_response['event']['name']
            self.__class__.outcome_value = {}
            for markets in event.ss_response['event']['children']:
                if markets['market']['templateMarketName'] in ['Total Goals Over/Under', 'Over/Under Total Goals']:
                    self.handicap_value.append(markets['market']['rawHandicapValue'])

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')
        self.site.login(username=tests.settings.betplacement_user)
        result = wait_for_result(lambda:self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC),timeout=5)
        self.assertTrue(result, msg='Odds format is not changed to fractional')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(self.eventID, timeout=30)
        self.site.wait_content_state(state_name='EventDetails', timeout=30)

    def test_003_go_to_overunder_total_goals_section(self):
        """
        DESCRIPTION: Go to 'Over/Under Total Goals' section
        EXPECTED: Section is expanded and displayed correctly
        """
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

        if self.site.brand == 'bma':
            self.__class__.expected_market_name = 'OVER/UNDER TOTAL GOALS' if self.device_type == 'mobile' else 'Over/Under Total Goals'
        else:
            self.__class__.expected_market_name = 'Over/Under Total Goals'

        under_total_goals = self.markets_list.get(self.expected_market_name)
        self.assertTrue(under_total_goals,
                        msg=f'"{self.expected_market_name}" section is not found in "{self.markets_list.keys()}"')
        if not under_total_goals.is_expanded():
            under_total_goals.expand()

        self.assertTrue(under_total_goals.is_expanded(),
                        msg=f'"{self.expected_market_name}" section is not expanded')
        if under_total_goals.has_show_all_button:
            under_total_goals.show_all_button.click()

    def test_004_verify_market_section(self):
        """
        DESCRIPTION: Verify market section
        EXPECTED: Market section is displayed within 'Over/Under Total Goals' section and contains the following:
        EXPECTED: *   Market name
        EXPECTED: *   Price/odds buttons of  available options: 'Over', 'Under'
        EXPECTED: *   If price of any of those markets is not available - corresponding price/odds button is not shown
        """
        self.assertIn(self.expected_market_name, self.markets_list,
                      msg=f'"{self.expected_market_name}" section is not present')
        # Expected-2- Covered in step-8

    def test_005_verify_market_name(self):
        """
        DESCRIPTION: Verify market name
        EXPECTED: Selection name corresponds to <figure afterward> part of '**name**' attribute on the market level (e.g. **0.5 **of market with name="Total Goals Over/Under 0.5")
        """
        outcome = self.markets_list[self.expected_market_name].outcomes.items_as_ordered_dict
        actual_selection_names = outcome.keys()

        handicap_value = self.handicap_value

        self.assertListEqual(sorted(handicap_value), sorted(actual_selection_names),
                             msg=f'Selection name "{handicap_value}" is not the same as expected "{actual_selection_names}"')

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
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        outcomes = self.get_outcome()
        for outcome_name, outcome in outcomes.items():
            for price in outcome.items:
                if price.outcome_price_text:
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
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if outcome is suspended
        """
        # Changing the odd format to decimal from setting form
        result = wait_for_result(lambda:self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC) ,timeout=5)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')

        self.navigate_to_edp(self.eventID, timeout=30)
        self.site.wait_content_state(state_name='EventDetails', timeout=30)
        self.test_007_verify_data_of_priceodds_buttons_in_fractional_format(format='decimal')

        # Below is the validation for step-6
        outcomes = self.outcomes
        self.get_outcome_from_event()

        outcome_name, outcome = list(outcomes.items())[0]

        ui_outcome_data = {}
        ui_outcome_data.update({'Over': outcome.items_as_ordered_dict['Over'].outcome_price_text,
                                'Under': outcome.items_as_ordered_dict['Under'].outcome_price_text})

        self.assertDictEqual(ui_outcome_data,  self.final_outcome_value[outcome_name],
                             msg=f'Outcome/Price values is different from actual outcome "{ui_outcome_data}" and expected outcomes "{self.final_outcome_value[outcome_name]}" ')

    def test_009_selectunselect_same_priceodds_button(self):
        """
        DESCRIPTION: Select/unselect same Price/Odds button
        EXPECTED: Button is highlighted/unhighlighted respectively
        """
        outcomes = self.markets_list[self.expected_market_name].outcomes.items_as_ordered_dict
        outcome_name, outcome = list(outcomes.items())[0]
        self.__class__.selection_name = outcome_name
        self.assertFalse(outcome.items[0].is_selected(expected_result=False),
                         msg=f'Bet button "{outcome_name}" is highlighted')
        outcome.items[0].click()
        self.site.wait_splash_to_hide()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(outcome.items[0].is_selected(expected_result=True),
                        msg=f'Bet button "{outcome_name}" is not highlighted')

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
        selection_name = f'Over {self.selection_name}'
        self.assertEqual(self.stake_name, selection_name,
                         msg=f'Selection "{selection_name}" should be present in betslip, but "{self.stake_name}" is displayed ')
        self.assertEqual(len(singles_section), 1,
                         msg='Only one selection should be present in betslip')
        event_name = self.stake.event_name
        self.assertEqual(event_name, self.event_name,
                         msg=f'Event name "{event_name}" is not the same as expected "{self.event_name}"')

        odd = self.stake.odds
        self.assertRegexpMatches(odd, self.decimal_pattern,
                                 msg=f'Stake odds value "{odd}" not match decimal pattern: "{self.decimal_pattern}"')

        expected_market_name = f'Over/Under Total Goals {self.selection_name}'
        self.assertEqual(self.stake.market_name, expected_market_name,
                         msg=f'Market-name is not equal, actual "{self.stake.market_name}" and expected "{expected_market_name}""')

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
                                 timeout=5)
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
        self.assertTrue(self.site.is_bet_receipt_displayed(), msg='Bet Receipt is not displayed.')
        result = wait_for_result(lambda: self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC),timeout=5)
        self.assertTrue(result, msg='Odds format is not changed to fractional')
