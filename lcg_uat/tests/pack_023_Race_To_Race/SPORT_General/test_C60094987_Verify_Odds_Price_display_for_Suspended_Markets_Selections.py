import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #  Event creation is involved
@pytest.mark.races
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.slow
@vtest
class Test_C60094987_Verify_Odds_Price_display_for_Suspended_Markets_Selections(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C60094987
    NAME: Verify Odds/Price display for Suspended Markets/Selections
    DESCRIPTION: Verify that price/odds button is displayed as SUSP, grayed out and disabled when the market or selection is suspended for any sport in both Landing page and Event details page.
    PRECONDITIONS: 1: Login to TI to trigger market or selection suspension
    """
    keep_browser_open = True
    event_dict = {}

    def SLP_event_suspension(self, sport):

        event_id = self.event_dict.get(sport).event_id
        market_id = self.event_dict.get(sport).default_market_id
        team1 = self.event_dict.get(sport).team1
        event_name = team1 + ' v ' + self.event_dict.get(sport).team2
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, query_builder=self.ss_query_builder)
        league_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        # Verifying odds/price in decimal format
        event = self.site.sports_page.tab_content.accordions_list.get_event_from_league_by_event_id(league=league_name,
                                                                                                    event_id=event_id)
        self.assertTrue(event, msg=f'Event with name "{event_name}" not found')
        price_buttons = list(event.get_all_prices().items())
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')

        for selection_name, price_button in price_buttons:
            if price_button is not None:
                self.assertRegexpMatches(price_button.name, self.decimal_pattern,
                                         msg=f'Stake odds value "{price_button.name}" not match decimal pattern: "{self.decimal_pattern}"')

        self.ob_config.change_market_state(event_id, market_id, displayed=True)
        self.navigate_to_page(name='sport/' + sport)
        self.site.wait_content_state_changed(timeout=60)
        self.site.wait_splash_to_hide()
        result = wait_for_result(lambda: self.site.sports_page.tab_content.accordions_list.is_displayed(timeout=60) is True, timeout=60)
        self.assertTrue(result, msg='Sport landing page is not loaded completely')

        # Verifying odd/price post suspending it - verifying susp text
        event = self.site.sports_page.tab_content.accordions_list.get_event_from_league_by_event_id(league=league_name,
                                                                                                    event_id=event_id)
        self.assertTrue(event, msg=f'Event with name "{event_name}" not found')
        price_buttons = list(event.get_all_prices().items())
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')

        for selection_name, price_button in price_buttons:

            if price_button is not None:
                self.assertEqual(price_button.name, vec.bet_history.SUSPENDED.upper(),
                                 msg=f'Actual button text: "{price_button.name}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
                exp_button_status = price_button.is_enabled()
                self.assertFalse(exp_button_status,
                                 msg='Bet button is not disabled, but was expected to be disabled')

        self.ob_config.change_market_state(event_id, market_id, displayed=True, active=True)

    def EDP_event_supension(self, sport):

        event_details_event_id = self.event_dict.get(sport).event_id
        event_details_market_id = self.event_dict.get(sport).default_market_id
        self.navigate_to_edp(event_id=event_details_event_id, sport_name=sport)
        self.site.wait_content_state(state_name='EventDetails', timeout=5)
        self.site.wait_splash_to_hide()
        result = wait_for_result(lambda: self.site.sport_event_details.tab_content.accordions_list.is_displayed(timeout=60) is True, timeout=60)
        self.assertTrue(result, msg='Event details page is not loaded completely')

        if sport == 'Football':
            self.__class__.market_name = self.expected_market_sections.match_result
        elif sport == 'Basketball':
            self.__class__.market_name = self.expected_market_sections.money_line
        elif sport == 'Tennis':
            self.__class__.market_name = self.expected_market_sections.match_betting

        # Verifying odd/price in decimal format

        market = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(market, msg='No items found on market selection list')
        outcomes = market[self.market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')

        for outcome_name, outcome in outcomes.items():
            self.assertRegexpMatches(outcome.bet_button.name.lower(), self.decimal_pattern,
                                     msg=f'Stake odds value "{outcome.bet_button.name}" not match fractional pattern: "{self.decimal_pattern}"')

        self.ob_config.change_market_state(event_details_event_id, event_details_market_id, displayed=True)

        self.navigate_to_edp(event_id=event_details_event_id, sport_name=sport)
        self.site.wait_content_state(state_name='EventDetails', timeout=60)
        self.site.wait_splash_to_hide()
        result = wait_for_result(lambda: self.site.sport_event_details.tab_content.accordions_list.is_displayed(timeout=60) is True, timeout=60)
        self.assertTrue(result, msg='Event details page is not loaded completely')

        # Verifying odd/price post suspending it - verifying susp text
        market = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(market, msg='No items found on market selection list')
        outcomes = market[self.market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')

        for outcome_name, outcome in outcomes.items():
            self.assertEqual(outcome.bet_button.name, vec.bet_history.SUSPENDED.upper(),
                             msg=f'Actual button text: "{outcome.bet_button.name}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
            self.assertFalse(outcome.bet_button.is_enabled(expected_result=False, timeout=60, poll_interval=1),
                             msg='Bet button is not disabled, but was expected to be disabled')

        self.navigate_to_page('HomePage')

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: Create a event
        """
        event_football = self.ob_config.add_autotest_premier_league_football_event()
        event_tennis = self.ob_config.add_tennis_event_to_european_open()
        event_basketball = self.ob_config.add_basketball_event_to_autotest_league()

        self.event_dict.update({'Football': event_football, 'Tennis': event_tennis, 'Basketball': event_basketball})

        self.__class__.football_event_id = self.event_dict.get('Football').event_id
        self.__class__.football_market_id = self.event_dict.get('Football').default_market_id
        self.__class__.football_selection_id = list(self.event_dict.get('Football').selection_ids.values())[0]

    def test_001_launch_ladbrokescoral_urlfor_mobile_app_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile App: Launch the app
        EXPECTED: URL should be launched
        """
        # Covered in Step-2

    def test_002_navigate_to_any_sport(self):
        """
        DESCRIPTION: Navigate to any <Sport>
        EXPECTED: User should be navigated to <Sport> landing page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL')

    def test_003_tap_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: User should be navigated to <Sport> event details page
        """
        self.navigate_to_edp(event_id=self.football_event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=60)

    def test_004_verify_data_of_priceodds_buttons_in_fractional_format(self, format=None):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in fractional format
        EXPECTED: 'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        """
        if format == 'decimal':
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state('football')
            self.site.login()
            self.site.wait_splash_to_hide()
            self.site.close_all_dialogs()
            self.site.wait_content_state('football')

            # Changing the odd format to decimal from setting form
            result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
            self.assertTrue(result, msg='Odds format is not changed to Decimal')

            # Changing event state to Active
            self.ob_config.change_market_state(self.football_event_id, self.football_market_id, displayed=True,
                                               active=True)

            self.navigate_to_edp(event_id=self.football_event_id, sport_name='football')
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='EventDetails', timeout=60)
            result = wait_for_result(lambda: self.site.contents.tab_content.accordions_list.is_displayed(timeout=60) is True, timeout=60)
            self.assertTrue(result, msg='Event details page is not loaded completely')

        market_name = self.expected_market_sections.match_result
        market = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(market, msg='No items found on market selection list')
        outcomes = market[market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')

        for outcome_name, outcome in outcomes.items():

            if format == 'decimal':
                self.assertRegexpMatches(outcome.bet_button.name, self.decimal_pattern,
                                         msg=f'Stake odds value "{outcome.bet_button.name}" not match decimal pattern: "{self.decimal_pattern}"')
            else:
                self.assertRegexpMatches(outcome.bet_button.name, self.fractional_pattern,
                                         msg=f'Stake odds value "{outcome.bet_button.name}" not match fractional pattern: "{self.fractional_pattern}"')

    def test_005_login_to_ti_and_suspend_any_market_which_is_displayed_in_sport_event_details_pageindexphpattachmentsget120936825indexphpattachmentsget120936827(
            self):
        """
        DESCRIPTION: Login to TI and suspend any market which is displayed in <Sport> event details page
        DESCRIPTION: ![](index.php?/attachments/get/120936825)
        DESCRIPTION: ![](index.php?/attachments/get/120936827)
        EXPECTED: 1: The price/Odd button for the selection in the suspended market should be greyed out
        EXPECTED: 2: "SUSP" should be displayed
        EXPECTED: 3: The price/ odd button should be disabled
        """
        self.ob_config.change_market_state(self.football_event_id, self.football_market_id, displayed=True)
        self.navigate_to_edp(event_id=self.football_event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=60)
        result = wait_for_result(lambda: self.site.contents.tab_content.accordions_list.is_displayed(timeout=60) is True, timeout=60)
        self.assertTrue(result, msg='Event details page is not loaded completely')

        market_name = self.expected_market_sections.match_result
        market = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(market, msg='No items found on market selection list')
        outcomes = market[market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')

        for outcome_name, outcome in outcomes.items():
            self.assertEqual(outcome.bet_button.name, vec.bet_history.SUSPENDED.upper(),
                             msg=f'Actual button text: "{outcome.bet_button.name}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
            self.assertFalse(outcome.bet_button.is_enabled(expected_result=False, timeout=30, poll_interval=1),
                             msg='Bet button is not disabled, but was expected to be disabled')
            try:
                outcome.bet_button.click()
                self.assertFalse(outcome.bet_button.is_enabled(expected_result=True, timeout=30, poll_interval=1),
                                 msg='Bet button is not disabled, but was expected to be disabled')
            except Exception:
                continue

    def test_006_click_on_the_suspended_selection(self):
        """
        DESCRIPTION: Click on the suspended selection
        EXPECTED: User should not be able to select the selection price
        """
        # Covered in Step-5

    def test_007_verify_data_of_priceodds_buttons_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in Decimal format
        EXPECTED: 'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        """
        self.test_004_verify_data_of_priceodds_buttons_in_fractional_format(format='decimal')

    def test_008_login_to_ti_and_suspend_any_market_which_is_displayed_in_sport_event_details_pageindexphpattachmentsget120936825indexphpattachmentsget120936827(
            self):
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

    def test_010_login_to_ti_and_suspended_any_selection_in_a_market_which_is_displayed_in_sport_event_details_page(
            self):
        """
        DESCRIPTION: Login to TI and suspended any selection in a market which is displayed in <Sport> event details page
        EXPECTED: 1: The price/Odd button for the suspended selection should be greyed out
        EXPECTED: 2: "SUSP" should be displayed
        EXPECTED: 3: The price/ odd button should be disabled
        """
        self.ob_config.change_market_state(self.football_event_id, self.football_market_id, displayed=True, active=True)
        self.navigate_to_edp(event_id=self.football_event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=5)
        result = wait_for_result(lambda: self.site.contents.tab_content.accordions_list.is_displayed(timeout=60) is True, timeout=60)
        self.assertTrue(result, msg='Event details page is not loaded completely')

        self.ob_config.change_selection_state(selection_id=self.football_selection_id, displayed=True, active=False)

        market_name = self.expected_market_sections.match_result
        market = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(market, msg='No items found on market selection list')
        outcomes = market[market_name].outcomes.items_as_ordered_dict

        self.assertTrue(outcomes, msg='No items found on market outcomes')
        self.suspended_selection1_text = list(outcomes.items())[0][1].output_price
        self.assertEqual(self.suspended_selection1_text, vec.bet_history.SUSPENDED.upper(),
                         msg=f'Actual button text: "{self.suspended_selection1_text}" is not same as Expected button text: "{vec.bet_history.SUSPENDED.upper()}"')
        self.assertFalse(list(outcomes.items())[0][1].bet_button.is_enabled(expected_result=False, timeout=60, poll_interval=1),
                         msg='Bet button is not disabled, but was expected to be disabled')

        # Changing selection state back to active - since football event to be used in below steps
        self.ob_config.change_selection_state(selection_id=self.football_selection_id, displayed=True, active=True)

    def test_011_validate_for_both_in_play_and_pre_play_markets_for_all_sports_in_both_sport_landing_page_and_event_details_page(
            self):
        """
        DESCRIPTION: Validate for both In play and Pre-play markets for all Sports in both Sport Landing page and Event details page
        """
        self.navigate_to_page('HomePage')
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='HomePage', timeout=60)

        for sport in ['Basketball', 'Football', 'Tennis']:

            if self.device_type == 'mobile':
                all_items = self.site.home.menu_carousel.items_as_ordered_dict
                self.assertTrue(all_items, msg='No items on MenuCarousel found')
                all_items.get(vec.sb.ALL_SPORTS).click()
                try:
                    self.site.wait_content_state(state_name='AllSports')
                except Exception:
                    all_items.get(vec.sb.ALL_SPORTS).click()
                self.site.wait_content_state(state_name='AllSports')
                self.site.close_all_dialogs()
                self.az_sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            else:
                self.az_sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(self.az_sports, msg='"Sports" list not found')
            self.az_sports[sport].click()
            self.site.wait_content_state(sport)
            self.site.wait_content_state_changed(timeout=60)
            self.site.wait_splash_to_hide()
            # result = wait_for_result(lambda: self.site.sports_page.tab_content.accordions_list.is_displayed(timeout=60) is True, timeout=60)
            # self.assertTrue(result, msg='Sport landing page is not loaded completely')
            self._logger.info(f'*** page is redirected to "{sport}" ***')

            # Below functions will verify odds suspension on both Sport Landing and Event Details page
            self.SLP_event_suspension(sport)
            self.EDP_event_supension(sport)
