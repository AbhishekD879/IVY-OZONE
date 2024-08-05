import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Event creation is involved
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28539_Verify_selection_data_and_placing_a_bet_on_Handicap_market(BaseBetSlipTest):
    """
    TR_ID: C28539
    NAME: Verify selection data and placing a bet on Handicap market
    DESCRIPTION: This test case verifies selection data and bet placement on Handicap market
    PRECONDITIONS: Football events with Handicap markets (name="Handicap Match Result", name="Handicap First Half", name="Handicap Second Half")
    PRECONDITIONS: To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. EN)
    PRECONDITIONS: Jira ticket: BMA-3900
    """
    keep_browser_open = True

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
        markets = [('over_under_total_goals', {'cashout': True, 'over_under': 1}),
                   ('over_under_first_half', {'cashout': True, 'over_under': 2}),
                   ('over_under_second_half', {'cashout': True, 'over_under': 3})]

        event = self.ob_config.add_autotest_premier_league_football_event(markets=markets, is_live=True)
        self.__class__.eventID = event.event_id
        self.__class__.event_name = event.ss_response['event']['name']
        self.__class__.outcomename = {}
        self.__class__.outcome_prices = {}
        prices = {}
        for markets in event.ss_response['event']['children']:
            if markets['market']['templateMarketName'] not in ['Match Betting', 'Match Result']:
                market_template_name = markets['market']['templateMarketName']
                self.outcomename[market_template_name] = markets['market']['rawHandicapValue']
                for outcomes in markets['market']['children']:
                    prices.update({outcomes['outcome']['name']: outcomes['outcome']['children'][0]['price']['priceDec']})
                self.outcome_prices[market_template_name] = prices

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(self.eventID, timeout=60)
        self.site.wait_content_state(state_name='EventDetails', timeout=60)

    def test_003_go_to_handicap_results_market_section(self):
        """
        DESCRIPTION: Go to Handicap Results market section
        EXPECTED: Market section is expandable/collapsible and consists of '90 mins / 1st Half / 2nd Half' sections
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

        self.assertTrue(under_total_goals.is_expanded(),
                        msg=f'"{self.expected_market_name}" section is not expanded')

        self.assertIn(self.expected_market_name, self.markets_list,
                      msg=f'"{self.expected_market_name}" section is not present')

        sections = self.markets_list[self.expected_market_name].grouping_buttons.items_as_ordered_dict
        expected_section = vec.sb.EXPECTED_OVER_UNDER_TOTAL_GOALS_BUTTONS

        self.assertListEqual(list(sections.keys()), expected_section,
                             msg=f'Actual section "{list(sections.keys())}" under "{self.expected_market_name}" is not matching'
                                 f'with expected section "{expected_section}" ')

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: Selection section is displayed within '90 mins / 1st Half / 2nd Half' sections and contains the following:
        EXPECTED: *   outcomes names correspond to the SS attribute 'name's for appropriate 'outcome ID'
        EXPECTED: *   Price/odds buttons
        EXPECTED: *   If price is not available - corresponding price/odds button is not shown
        """
        # Covered in step-8

    def test_005_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to '**name**' attribute on the outcome level for verified market
        """
        # Covered in step-8

    def test_006_verify_priceodds_button_correspondence_to_verified_market(self):
        """
        DESCRIPTION: Verify Price/Odds button correspondence to verified market
        EXPECTED: *   Price/odds buttons in '**90 mins**' filter correspond to 'Handicap Match Result' market data in SS response
        EXPECTED: *   Price/odds buttons in '**1st Half**' filter correspond to 'Handicap First Half' market data in SS response
        EXPECTED: *   Price/odds buttons in '**2nd Half**' filter correspond to 'Handicap Second Half' market data in SS response
        """
        # Covered in step-8

    def test_007_verify_data_of_priceodds_button_in_fractional_format(self, format=None):
        """
        DESCRIPTION: Verify data of Price/Odds button in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled button is displayed with prices if outcome is suspended
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

    def test_008_verify_data_of_priceodds_button_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled button is displayed with prices if outcome is suspended
        """
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')

        self.navigate_to_edp(self.eventID, timeout=60)
        self.site.wait_content_state(state_name='EventDetails', timeout=60)

        self.test_007_verify_data_of_priceodds_button_in_fractional_format(format='decimal')

        # Below is the validation for step-4/5/6
        total_over_markets_tabs = vec.SB.EXPECTED_OVER_UNDER_TOTAL_GOALS_BUTTONS
        i = 0
        for tab in total_over_markets_tabs:

            ss_marketlist = ['Total Goals Over/Under', 'Over/Under First Half', 'Over/Under Second Half']
            if self.site.brand == 'ladbrokes': ss_marketlist[0] = 'Over/Under Total Goals'

            self.markets_list[self.expected_market_name].grouping_buttons.items_as_ordered_dict[tab].click()

            outcomes = self.get_outcome()
            actual_outcome_name = ' '.join(list(outcomes.keys()))

            expected_outcome_name = self.outcomename[ss_marketlist[i]]

            self.assertEqual(actual_outcome_name, expected_outcome_name,
                             msg=f'Actual outcome_name: "{actual_outcome_name}" '
                                 f'for tab "{tab}" is not same as expected "{expected_outcome_name}" ')

            expected_outcome_price = self.outcome_prices[ss_marketlist[i]]

            outcome_name, outcome = list(outcomes.items())[0]

            ui_outcome_data = {}
            ui_outcome_data.update({'Over': outcome.items_as_ordered_dict['Over'].outcome_price_text,
                                    'Under': outcome.items_as_ordered_dict['Under'].outcome_price_text})

            self.assertDictEqual(ui_outcome_data, expected_outcome_price,
                                 msg=f'For tab "{tab}" , Outcome/Price values is different from actual outcome "{ui_outcome_data}" and expected outcomes "{expected_outcome_price}" ')
            i = i+1

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
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(outcome.items[0].is_selected(expected_result=True),
                        msg=f'Bet button "{outcome_name}" is not highlighted')

    def test_010_add_single_selection_to_betslip(self):
        """
        DESCRIPTION: Add single selection to Betslip
        EXPECTED: Bet indicator displays 1
        """
        self.verify_betslip_counter_change(expected_value=1)

    def test_011_go_to_betslip(self):
        """
        DESCRIPTION: Go to 'Betslip'
        EXPECTED: The bet is present
        """
        self.site.open_betslip()

    def test_012_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name (event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fractional format or **'price Dec'** in decimal format)
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        selection_name = "Over (+3.0)"
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

        expected_market_name = 'Over/Under Second Half 3' if self.site.brand == 'bma' else 'Over/Under Second Half 3'
        self.assertEqual(self.stake.market_name, expected_market_name,
                         msg=f'Market-name is not equal, actual "{self.stake.market_name}" and expected "{expected_market_name}""')

    def test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Est. Returns**(Coral)/ **Pot. Returns** (Ladbrokes)
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Estimated Returns**(Coral)/ **Potential Returns** (Ladbrokes)
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

    def test_014_tapplace_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        self.get_betslip_content().bet_now_button.click()
        self.assertTrue(self.site.is_bet_receipt_displayed(), msg='Bet Receipt is not displayed.')
