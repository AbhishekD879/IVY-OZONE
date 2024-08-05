import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot suspend markets on prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60011520_Verify_Odds_Price_display_for_Suspended_Markets_Selections(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C60011520
    NAME: Verify Odds/Price display for Suspended Markets/Selections
    DESCRIPTION: Verify that price/odds button is displayed as SUSP, grayed out and disabled when the market or selection is suspended for any sport in both Landing page and Event details page.
    PRECONDITIONS: 1: Login to TI to trigger market or selection suspension
    """
    keep_browser_open = True
    event_dict = {}

    def other_sport_verification(self, sport):
        self.test_003_tap_event_name_or_more_link_on_the_event_section(sport=sport)
        self.test_004_verify_data_of_priceodds_buttons_in_fractional_format(sport=sport)
        self.test_005_login_to_ti_and_suspend_any_market_which_is_displayed_in_sport_event_details_pageindexphpattachmentsget120936825indexphpattachmentsget120936827(sport=sport)
        self.test_007_verify_data_of_priceodds_buttons_in_decimal_format(sport=sport)
        self.test_008_login_to_ti_and_suspend_any_market_which_is_displayed_in_sport_event_details_pageindexphpattachmentsget120936825indexphpattachmentsget120936827()
        self.test_010_login_to_ti_and_suspended_any_selection_in_a_market_which_is_displayed_in_sport_event_details_page(sport=sport)

    def SLP_verification(self, sport='Football', decimal=False):
        sleep(2)
        self.navigate_to_page(name='sport/' + sport)
        event_id = self.event_dict.get(sport).event_id
        market_id = self.event_dict.get(sport).default_market_id
        selection_id = list(self.event_dict.get(sport).selection_ids.values())[0]
        event_name = self.event_dict.get(sport).ss_response['event']['name']
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, query_builder=self.ss_query_builder)
        league_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        event = self.site.sports_page.tab_content.accordions_list.get_event_from_league_by_event_id(league=league_name, event_id=event_id)
        self.assertTrue(event, msg=f'Event with name "{event_name}" not found')
        price_buttons = event.get_all_prices()
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')
        for price_button in list(price_buttons.values()):
            if decimal:
                self.assertRegexpMatches(price_button.name, self.decimal_pattern,
                                         msg=f'Stake odds value "{price_button.name}" not match decimal pattern: "{self.decimal_pattern}"')
            else:
                self.assertRegexpMatches(price_button.name, self.fractional_pattern,
                                         msg=f'Stake odds value "{price_button.name}" not match decimal pattern: "{self.decimal_pattern}"')

        self.ob_config.change_market_state(event_id, market_id, displayed=True)
        event = self.site.sports_page.tab_content.accordions_list.get_event_from_league_by_event_id(league=league_name, event_id=event_id)
        self.assertTrue(event, msg=f'Event with name "{event_name}" not found')
        price_buttons = event.get_all_prices()
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')
        for price_button in list(price_buttons.values()):
            self.assertEqual(price_button.name, vec.bet_history.SUSPENDED.upper(),
                             msg=f'Actual button text: "{price_button.name}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
            self.assertFalse(price_button.is_enabled(),
                             msg='Bet button is not disabled')

        self.ob_config.change_market_state(event_id, market_id, displayed=True, active=True)
        self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=False)
        selection1 = list(event.get_all_prices().values())[0]
        self.suspended_selection1_text = selection1.name
        self.assertEqual(self.suspended_selection1_text, vec.bet_history.SUSPENDED.upper(),
                         msg=f'Actual button text: "{self.suspended_selection1_text}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
        self.assertFalse(selection1.is_enabled(expected_result=False), msg='Bet button is not disabled')
        self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)

    def get_market_name(self, sport='Football'):
        if sport == 'Football':
            self.__class__.market_name = self.expected_market_sections.match_result if self.brand == 'bma' else 'Match Result'
        elif sport == 'Basketball':
            self.__class__.market_name = self.expected_market_sections.money_line
        elif sport == 'Tennis':
            self.__class__.market_name = self.expected_market_sections.match_betting if self.brand == 'bma' else 'Match Result'
        return self.market_name

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: Create a event
        """
        event_football = self.ob_config.add_autotest_premier_league_football_event()
        event_tennis = self.ob_config.add_tennis_event_to_european_open()
        event_basketball = self.ob_config.add_basketball_event_to_autotest_league()
        self.event_dict.update({'Football': event_football, 'Tennis': event_tennis, 'Basketball': event_basketball})

    def test_001_launch_ladbrokescoral_urlfor_mobile_app_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile App: Launch the app
        EXPECTED: URL should be launched
        """
        self.site.wait_content_state('Homepage')
        self.site.login()

    def test_002_navigate_to_any_sport(self):
        """
        DESCRIPTION: Navigate to any <Sport>
        EXPECTED: User should be navigated to <Sport> landing page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL')

    def test_003_tap_event_name_or_more_link_on_the_event_section(self, sport='Football'):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: User should be navigated to <Sport> event details page
        """
        self.navigate_to_edp(event_id=self.event_dict.get(sport).event_id)
        self.site.wait_content_state(state_name='EventDetails', timeout=60)

    def test_004_verify_data_of_priceodds_buttons_in_fractional_format(self, decimal=False, sport='Football'):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in fractional format
        EXPECTED: 'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        """
        self.get_market_name(sport=sport)
        market = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(market, msg='No items found on market selection list')
        outcomes = market[self.market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')
        for outcome_name, outcome in outcomes.items():
            if decimal:
                self.assertRegexpMatches(outcome.bet_button.name, self.decimal_pattern,
                                         msg=f'Stake odds value "{outcome.bet_button.name}" not match decimal pattern: "{self.decimal_pattern}"')
            else:
                self.assertRegexpMatches(outcome.bet_button.name, self.fractional_pattern,
                                         msg=f'Stake odds value "{outcome.bet_button.name}" not match fractional pattern: "{self.fractional_pattern}"')

    def test_005_login_to_ti_and_suspend_any_market_which_is_displayed_in_sport_event_details_pageindexphpattachmentsget120936825indexphpattachmentsget120936827(self, sport='Football'):
        """
        DESCRIPTION: Login to TI and suspend any market which is displayed in <Sport> event details page
        DESCRIPTION: ![](index.php?/attachments/get/120936825)
        DESCRIPTION: ![](index.php?/attachments/get/120936827)
        EXPECTED: 1: The price/Odd button for the selection in the suspended market should be greyed out
        EXPECTED: 2: "SUSP" should be displayed
        EXPECTED: 3: The price/ odd button should be disabled
        """
        event_id = self.event_dict.get(sport).event_id
        market_id = self.event_dict.get(sport).default_market_id
        self.ob_config.change_market_state(event_id, market_id, displayed=True)
        market = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(market, msg='No items found on market selection list')
        outcomes = market[self.market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')
        for outcome_name, outcome in outcomes.items():
            self.assertEqual(outcome.bet_button.name, vec.bet_history.SUSPENDED.upper(),
                             msg=f'Actual button text: "{outcome.bet_button.name}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
            self.assertFalse(outcome.bet_button.is_enabled(expected_result=False, timeout=30, poll_interval=1),
                             msg='Bet button is not disabled, but was expected to be disabled')

    def test_006_click_on_the_suspended_selection(self):
        """
        DESCRIPTION: Click on the suspended selection
        EXPECTED: User should not be able to select the selection price
        """
        # Covered in Step-5

    def test_007_verify_data_of_priceodds_buttons_in_decimal_format(self, sport='Football'):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in Decimal format
        EXPECTED: 'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        """
        event_id = self.event_dict.get(sport).event_id
        market_id = self.event_dict.get(sport).default_market_id
        # Changing the odd format to decimal from setting form
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')
        self.ob_config.change_market_state(event_id, market_id, displayed=True, active=True)
        self.test_003_tap_event_name_or_more_link_on_the_event_section()
        self.test_004_verify_data_of_priceodds_buttons_in_fractional_format(decimal=True)

    def test_008_login_to_ti_and_suspend_any_market_which_is_displayed_in_sport_event_details_pageindexphpattachmentsget120936825indexphpattachmentsget120936827(self):
        """
        DESCRIPTION: Login to TI and suspend any market which is displayed in <Sport> event details page
        DESCRIPTION: ![](index.php?/attachments/get/120936825)
        DESCRIPTION: ![](index.php?/attachments/get/120936827)
        EXPECTED: 1: The price/Odd button for the selection in the suspended market should be greyed out
        EXPECTED: 2: "SUSP" should be displayed
        EXPECTED: 3: The price/ odd button should be disabled
        """
        self.test_005_login_to_ti_and_suspend_any_market_which_is_displayed_in_sport_event_details_pageindexphpattachmentsget120936825indexphpattachmentsget120936827()

    def test_009_click_on_the_suspended_selection(self):
        """
        DESCRIPTION: Click on the suspended selection
        EXPECTED: User should not be able to select the selection price
        """
        # Covered in step-8

    def test_010_login_to_ti_and_suspended_any_selection_in_a_market_which_is_displayed_in_sport_event_details_page(self, sport='Football'):
        """
        DESCRIPTION: Login to TI and suspended any selection in a market which is displayed in <Sport> event details page
        EXPECTED: 1: The price/Odd button for the suspended selection should be greyed out
        EXPECTED: 2: "SUSP" should be displayed
        EXPECTED: 3: The price/ odd button should be disabled
        """
        event_id = self.event_dict.get(sport).event_id
        market_id = self.event_dict.get(sport).default_market_id
        selection_id = list(self.event_dict.get(sport).selection_ids.values())[0]
        self.ob_config.change_market_state(event_id, market_id, displayed=True, active=True)
        self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=False)
        market = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(market, msg='No items found on market selection list')
        outcomes = market[self.market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')
        selection1 = list(outcomes.values())[0]
        self.suspended_selection1_text = selection1.output_price
        self.assertEqual(self.suspended_selection1_text, vec.bet_history.SUSPENDED.upper(),
                         msg=f'Actual button text: "{self.suspended_selection1_text}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
        self.assertFalse(selection1.bet_button.is_enabled(expected_result=False), msg='Bet button is not disabled')
        self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)
        self.SLP_verification(decimal=True, sport=sport)
        sleep(1)
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        self.assertTrue(result, msg='Odds format is not changed to Fractional')
        self.SLP_verification(sport=sport)

    def test_011_validate_for_both_in_play_and_pre_play_markets_for_all_sports_in_both_sport_landing_page_and_event_details_page(self):
        """
        DESCRIPTION: Validate for both In play and Pre-play markets for all Sports in both Sport Landing page and Event details page
        EXPECTED:
        """
        self.other_sport_verification(sport='Tennis')
        self.other_sport_verification(sport='Basketball')
