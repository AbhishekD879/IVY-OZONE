import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod // cannot create events for popular score market
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28551_Verify_selection_data_and_placing_a_bet_on_Popular_Goalscorer_Markets(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28551
    NAME: Verify selection data and placing a bet on Popular Goalscorer Markets
    DESCRIPTION: This test case verifies selection data and placing a bet on Popular Goalscorer Markets
    PRECONDITIONS: 1) Football events with goalscorer markets (First Goalscorer, Anytime Goalscorer, Goalscorer - 2 or More)
    PRECONDITIONS: 2) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is logged in
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Anytime Goalscorer"
    PRECONDITIONS: *   PROD: name="Goal Scorer - Anytime"
    PRECONDITIONS: **Jira tickets: **BMA-3866
    """
    keep_browser_open = True
    markets = [('first_goalscorer', {'cashout': True}),
               ('anytime_goalscorer', {'cashout': True}),
               ('goalscorer_2_or_more', {'cashout': True})]
    odds_price = []
    price_dec = []

    def test_000_preconditions(self):
        event = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        self.__class__.eventID = event.event_id
        self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event.team1, event.team2, event.selection_ids
        if self.brand == 'bma':
            self.__class__.market_names = ['First Goalscorer', 'Anytime Goalscorer', 'Goalscorer - 2 or More']
        else:
            self.__class__.market_names = ['First Goalscorer', 'Anytime Goalscorer', 'Goalscorer - 2 Or More']

        for market in event.ss_response['event']['children']:
            if market['market']['templateMarketName'] == self.market_names[0]:
                self.__class__.first_goalscorer_market = market['market']['children']
            elif market['market']['templateMarketName'] == self.market_names[1]:
                self.__class__.anytime_goalscorere_market = market['market']['children']
            elif market['market']['templateMarketName'] == self.market_names[2]:
                self.__class__.goalscorer_two_or_more_market = market['market']['children']

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.login()
        self.__class__.balance = self.site.header.user_balance
        self.site.wait_content_state('Home')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No one market found on event details page')

    def test_003_go_to_popular_goalscorer_markets_section(self):
        """
        DESCRIPTION: Go to 'Popular Goalscorer Markets' section
        EXPECTED: Section is expanded and displayed correctly
        """
        self.__class__.popular_goalscorer_section = self.markets.get(
            self.expected_market_sections.popular_goalscorer_markets)
        self.assertTrue(self.popular_goalscorer_section, msg='POPULAR GOALSCORER MARKETS section is not found')

        self.popular_goalscorer_section.collapse()
        self.assertFalse(self.popular_goalscorer_section.is_expanded(),
                         msg='"POPULAR GOALSCORER MARKETS" is not collapsible')
        self.popular_goalscorer_section.expand()
        self.assertTrue(self.popular_goalscorer_section.is_expanded(),
                        msg='"POPULAR GOALSCORER MARKETS" is not expandable')

    def test_004_verify_selection_section(self):
        """
        DESCRIPTION: Verify selection section
        EXPECTED: Selection section is displayed within Market section and contains the following:
        EXPECTED: *   Player name
        EXPECTED: *   Price/odds buttons of  available Goalscorer markets: 'First Goalscorer', 'Anytime Goalscorer', 'Goalscorer - 2or More'
        EXPECTED: *   If price of any of those markets is not available - corresponding price/odds button is not shown
        """
        self.__class__.market_grouping_buttons = self.popular_goalscorer_section.grouping_buttons.items_as_ordered_dict
        self.assertIn(self.team1.upper(), self.market_grouping_buttons.keys(),
                      msg=f'Tab name "{self.team1.upper()}" is not available, one of "{list(self.market_grouping_buttons.keys())}" expected')
        self.assertIn(self.team2.upper(), self.market_grouping_buttons,
                      msg=f'Tab name "{self.team2.upper()}" is not available, one of "{list(self.market_grouping_buttons.keys())}" expected')

        actual_players = sorted(self.popular_goalscorer_section.outcome_table.players)
        expected_home_players = sorted(self.selection_ids['first_goalscorer'].keys())[1::2]
        self.assertListEqual(actual_players, expected_home_players,
                             msg='Incorrect players. Actual: "%s", Expected:"%s"'
                                 % (actual_players, expected_home_players))
        self.__class__.selection_name = []
        self.__class__.selection_price = []
        for name, switcher in self.market_grouping_buttons.items():
            switcher.click()
            sleep(3)
            selections_list = self.popular_goalscorer_section.outcome_table.items
            for selection in range(len(selections_list)):
                self.selection_name.append(selections_list[selection].event_name)
                self.selection_price.append(selections_list[selection].bet_button.outcome_price_text)
                self.assertTrue(self.selection_name, msg=f'selection name: "{self.selection_name}" is not displayed')
                self.__class__.selection = selections_list[selection].bet_button
                self.assertTrue(self.selection.is_displayed(),
                                msg=f'selection bet button: "{self.selection}" is not displayed')

    def test_005_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to '**name**' attribute on the outcome level for first market in the list for verified player
        """
        # covered in step 6

    def test_006_verify_priceodds_buttons_correspondence_to_goalscorer_markets(self):
        """
        DESCRIPTION: Verify Price/Odds buttons correspondence to Goalscorer markets
        EXPECTED: *   Price/odds buttons in '1st' column correspond to 'First Goalscorer' market data in SS response
        EXPECTED: *   Price/odds buttons in 'Anytime' column correspond to 'Anytime Goalscorer' market data in SS response
        EXPECTED: *   Price/odds buttons in '2 or More' column correspond to 'Goalscorer - 2 or More' market data in SS response
        """
        self.__class__.expected_selection_name = []
        for i in self.goalscorer_two_or_more_market:
            self.expected_selection_name.append(i['outcome']['name'])
            price_num = i['outcome']['children'][0]['price']['priceNum']
            price_den = i['outcome']['children'][0]['price']['priceDen']
            self.odds_price.append(f'{price_num}/{price_den}')
            self.price_dec.append(i['outcome']['children'][0]['price']['priceDec'])
        self.assertCountEqual(self.selection_name, self.expected_selection_name,
                              msg=f'Actual selection name: "{self.selection_name}" is not same as '
                                  f'Expected selection name: "{self.expected_selection_name}"')

    def test_007_verify_data_of_priceodds_buttons_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Selection is greyed out and disabled if it is suspended
        """
        self.assertEquals(self.selection_price, self.odds_price,
                          msg=f'Actual odds price: "{self.selection_price}" is not in '
                              f'Expected odds price: "{self.odds_price}"')

    def test_008_verify_data_of_priceodds_buttons_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Selection is greyed out and disabled if it is suspended
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.test_002_go_to_event_details_page_of_football_event()
        self.test_003_go_to_popular_goalscorer_markets_section()
        self.test_004_verify_selection_section()
        self.assertEqual(self.selection_price, self.price_dec,
                         msg=f'Actual odds price: "{self.selection_price}" is not same as '
                             f'Expected odds price: "{self.price_dec}"')

    def test_009_selectunselect_same_priceodds_button(self):
        """
        DESCRIPTION: Select/unselect same Price/Odds button
        EXPECTED: Button is highlighted/unhighlighted respectively
        """
        self.selection.click()
        self.assertTrue(self.selection.is_selected(), msg=f'selection "{self.selection}" is not selected')

    def test_010_add_single_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single selection to bet slip
        EXPECTED: Bet indicator displays 1.
        """
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.verify_betslip_counter_change(expected_value=1)

    def test_011_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: The bet is present
        """
        self.site.open_betslip()
        self.site.close_all_dialogs(timeout=3)
        singles_section = self.get_betslip_sections().Singles
        _, self.__class__.stake = list(singles_section.items())[0]
        self.assertTrue(self.stake, msg=f'"{self.stake}" stake was not found in "{singles_section.keys()}"')

    def test_012_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event name (event **'name'** attribute)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        event_name = self.stake.name
        self.assertEqual(event_name, self.selection_name[8],
                         msg=f'Selection name "{event_name.upper()}" is not the same as expected "{self.selection_name[8]}"')
        market_name = self.stake.market_name
        self.assertEqual(market_name, self.market_names[0],
                         msg=f'Actual Market name: "{market_name}" is not the same as'
                             f'Expected Market name: "{self.market_names[0]}"')
        odds = self.stake.odds
        self.assertEquals(odds, self.selection.outcome_price_text,
                          msg=f'odd "{odds}" is not same as expected "{self.selection.outcome_price_text}"')

    def test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Estimated Returns**
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Total Est. Returns**
        """
        self.stake.amount_form.input.value = self.bet_amount
        self.verify_estimated_returns(
            est_returns=float(self.get_betslip_content().total_estimate_returns),
            odds=self.stake.odds, bet_amount=self.bet_amount)

    def test_014_tapplace_bet_button(self):
        """
        DESCRIPTION: Tap **'PLACE BET**' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User balance is changed accordingly
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.balance - self.bet_amount)
