import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we cannot push the price change in prod
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.sanity
@pytest.mark.mobile_only
@pytest.mark.quick_bet
@vtest
class Test_C12834622_Price_changing_live_push_in_Quick_Bet_for_boosted_bet(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C12834622
    NAME: Price changing (live push) in Quick Bet for boosted bet
    DESCRIPTION: This test case verifies price changing (live push) in Quick Bet for boosted bet
    """
    keep_browser_open = True
    bet_amount = 0.3
    change_price = '5/3'
    decimal = False

    def create_events(self):
        event = self.ob_config.add_football_event_to_england_premier_league()
        self.__class__.event_id = event.event_id
        self.__class__.selection_name = event.team1
        self.__class__.selection_name_2 = event.team2
        self.__class__.selection_id = event.selection_ids.get(self.selection_name)
        self.__class__.selection_id_2 = event.selection_ids.get(self.selection_name_2)
        market_name = self.ob_config.football_config.england.premier_league.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def add_selection_to_quick_bet(self, selection_name=None):
        self.site.wait_content_state_changed(timeout=40)
        selection_name = selection_name if selection_name else self.selection_name
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name, selection_name=selection_name)
        self.site.wait_content_state(state_name='EventDetails')
        result = wait_for_result(lambda: self.site.quick_bet_panel.has_odds_boost_button(timeout=5),
                                 expected_result=True,
                                 timeout=20)
        self.assertTrue(result,
                        msg='Odds boost button not displayed')
        quick_bet = self.site.quick_bet_panel
        self.assertTrue(quick_bet.has_odds_boost_button(), msg='Odds boost button is not present on Quickbet panel')
        amount = quick_bet.selection.content.amount_form.input
        self.assertTrue(amount.is_displayed(timeout=3),
                        msg='Amount field is not displayed')
        amount.click()
        self.assertTrue(amount.is_enabled(timeout=1),
                        msg='Amount field is not enabled.')
        amount.value = self.bet_amount
        quick_bet.odds_boost_button.click()

        boosted_button_result = wait_for_result(lambda: quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                                name='"BOOST" button to become "BOOSTED" button with animation',
                                                timeout=2)
        self.assertTrue(boosted_button_result, msg='"BOOST" button to not become "BOOSTED" button with animation')
        boosted_price_result = wait_for_result(lambda: self.site.quick_bet_panel.selection.content.boosted_odds_container.price_value,
                                               name='Waiting for Quick bet boosted pice',
                                               timeout=15)
        self.assertTrue(boosted_price_result, msg='"Quick Bet boosted price" not displayed')

        quick_bet_panel_after_boosted = self.site.quick_bet_panel.selection.content
        self.assertTrue(quick_bet_panel_after_boosted.is_original_odds_crossed,
                        msg='odds are not croosed')
        self.__class__.odds_value_before_price_change = quick_bet_panel_after_boosted.odds_value
        self.__class__.boosted_price_value = quick_bet_panel_after_boosted.boosted_odds_container.price_value

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
        PRECONDITIONS: Quick Bet is enabled
        PRECONDITIONS: Generate for user Odds boost token with Any token in http://backoffice-tst2.coral.co.uk/office
        PRECONDITIONS: How to add OB token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
        PRECONDITIONS: Note: Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
        PRECONDITIONS: Load application
        PRECONDITIONS: Login into App by user with Odds boost token generated (Fractional odds format selected for User)
        PRECONDITIONS: Add selection to the Quickbet
        PRECONDITIONS: Add stake and tap ''BOOST'' button
        PRECONDITIONS: Change price for this selection in TI
        """

        # odds boost
        odds_boost = self.cms_config.get_initial_data(device_type=self.device_type).get('oddsBoost')['enabled']
        if not odds_boost:
            self.cms_config.update_odds_boost_config(enabled=True)
        odds_boost = self.cms_config.get_initial_data(device_type=self.device_type).get('oddsBoost')['enabled']
        self.assertTrue(odds_boost, msg='Odds boost is not enabled in CMS')

        # quickbet
        quick_bet = self.cms_config.get_initial_data(device_type=self.device_type)['systemConfiguration']['quickBet']['EnableQuickBet']
        if not quick_bet:
            self.cms_config.update_system_configuration_structure(config_item='quickBet', field_name='EnableQuickBet', field_value=True)

        # Granting Odds boost offer
        username = tests.settings.betplacement_user
        for i in range(4):
            self.ob_config.grant_odds_boost_token(username=username, level='selection')

        # creation of events
        self.create_events()

        # login
        self.site.login(username=username)
        self.site.wait_content_state_changed()
        self.navigate_to_edp(event_id=self.event_id, sport_name='football', timeout=60)
        self.add_selection_to_quick_bet()

    def test_001_verify_that_inline_message_is_displayed_at_the_topverify_message_content(self, selection_id=None):
        """
        DESCRIPTION: Verify that inline message is displayed at the top
        DESCRIPTION: Verify message content
        EXPECTED: **Before OX 99:**
        EXPECTED: Inline message is displayed at the top.
        EXPECTED: Text: 'Price changed from X/X to Y/Y'
        EXPECTED: **After OX 99:**
        EXPECTED: 'Price changed from 'n' to 'n'' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        """
        selection_id = selection_id if selection_id else self.selection_id
        self.ob_config.change_price(selection_id=selection_id, price=self.change_price)
        result = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_quick_bet_info_panel(timeout=80),
                                 name='Waiting for Quick bet text',
                                 timeout=80)
        self.assertTrue(result, msg='"Quick Bet text" not displayed')
        self.__class__.quick_bet_after_price_change = self.site.quick_bet_panel
        price_change_text_above = self.quick_bet_after_price_change.info_panels.text
        new_price = round(self.convert_fraction_price_to_decimal(initial_price=self.change_price) + 1.00, 2) if self.decimal else self.change_price
        expected_price_change_text = vec.quickbet.PRICE_IS_CHANGED.format(old=self.odds_value_before_price_change, new=new_price)
        self.assertEqual(price_change_text_above, expected_price_change_text,
                         msg=f'Actual text: "{price_change_text_above}" is not same as'
                             f'Expected text: "{expected_price_change_text}"')

    def test_002_verify_that_inline_message_is_displayed_at_the_bottomverify_message_content(self):
        """
        DESCRIPTION: Verify that inline message is displayed at the bottom
        DESCRIPTION: Verify message content
        EXPECTED: **Before OX 99:**
        EXPECTED: Inline message is displayed at the bottom.
        EXPECTED: Text: 'Some of the prices have changed, please re-boost your bet!' (displayed until user takes an action such as re-boost or navigates away from page)
        EXPECTED: **After OX 99:**
        EXPECTED: Info icon and 'The price has changed and new boosted odds will be applied to your bet. Hit Re-Boost to see your new boosted price' message is displayed below the Quick Stake buttons immediately
        """
        price_change_text_below = self.quick_bet_after_price_change.deposit_info_message.text
        self.assertEqual(price_change_text_below, vec.quickbet.REBOOST_PRICE_CHANGED,
                         msg=f'Actual text : "{price_change_text_below}" is not same as'
                             f'Expected text: "{vec.quickbet.REBOOST_PRICE_CHANGED}"')

    def test_003_verify_that_boost_button_text_changes_to_re_boost(self):
        """
        DESCRIPTION: Verify that boost button text changes to 'RE-BOOST'
        EXPECTED: Boost button text changes to 'RE-BOOST'
        """
        re_boost_name = self.quick_bet_after_price_change.odds_boost_button.name
        self.assertEqual(re_boost_name, vec.odds_boost.BOOST_BUTTON.reboost,
                         msg=f'Actual text: "{re_boost_name}" is not same as the'
                             f'Expected text: "{vec.odds_boost.BOOST_BUTTON.reboost}"')

    def test_004_verify_that_place_bet_button_is_changed_to_accept__place_bet(self):
        """
        DESCRIPTION: Verify that 'PLACE BET' button is changed to 'ACCEPT & PLACE BET'
        EXPECTED: 'ACCEPT & PLACE BET' button is shown
        """
        accept_place_bet_button = self.quick_bet_after_price_change.place_bet.name
        self.assertEqual(accept_place_bet_button, vec.quickbet.BUTTONS.accept_place_bet.upper(),
                         msg=f'Actual text: "{accept_place_bet_button}" is not same as the '
                             f'Expected text: "{vec.quickbet.BUTTONS.accept_place_bet}"')

    def test_005_verify_that_the_non_boosted_striked_out_price_is_updated(self):
        """
        DESCRIPTION: Verify that the non-boosted striked out price is updated
        EXPECTED: The non-boosted striked/crossed out price is updated (according to the updated value in TI from preconditions)
        """
        odds_value = self.quick_bet_after_price_change.selection.content.odds_value
        self.assertNotEqual(odds_value, self.odds_value_before_price_change,
                            msg=f'Actual odd value: "{odds_value}" is same as'
                                f'Expected odds vasle: "{self.odds_value_before_price_change}."')

    def test_006_verify_that_boosted_price_remains_unchanged(self):
        """
        DESCRIPTION: Verify that boosted price remains unchanged
        EXPECTED: The boosted price remains unchanged
        """
        self.__class__.previous_value = self.quick_bet_after_price_change.selection.content.boosted_odds_container.price_value
        self.assertEqual(self.previous_value, self.boosted_price_value,
                         msg=f'Actual odd value: "{self.previous_value}" is not same as'
                             f'Expected odds vasle: "{self.boosted_price_value}."')

    def test_007_tap_re_boost_buttonverify_that_boosted_odds_are_updated(self):
        """
        DESCRIPTION: Tap 'RE-BOOST' button
        DESCRIPTION: Verify that boosted odds are updated
        EXPECTED: - Quick bet is reloaded
        EXPECTED: - Boosted odds are updated
        """
        self.quick_bet_after_price_change.odds_boost_button.click()
        result = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_quick_bet_info_panel(timeout=40, expected_result=False),
                                 name='Waiting for Quick bet text',
                                 timeout=40)
        self.assertFalse(result, msg='"Quick Bet text PLACE BET" is displayed')
        self.__class__.quick_bet_after_reboost = self.site.quick_bet_panel
        self.__class__.after_odds = self.quick_bet_after_reboost.selection.content.boosted_odds_container.price_value
        self.assertNotEqual(self.after_odds, self.previous_value,
                            msg=f' Actual Value: "{self.after_odds}" is same as'
                                f' Expected value: "{self.previous_value}"')

    def test_008_verify_that_accept__place_bet_button_is_changed_back_to_place_bet(self):
        """
        DESCRIPTION: Verify that 'ACCEPT & PLACE BET' button is changed back to 'PLACE BET'
        EXPECTED: 'PLACE BET' button is shown
        """
        place_bet_button = self.quick_bet_after_reboost.place_bet.name
        self.assertEqual(place_bet_button, vec.quickbet.BUTTONS.place_bet.upper(),
                         msg=f'Actual text: "{place_bet_button}" is not same as the '
                             f'Expected text: "{vec.quickbet.BUTTONS.place_bet.upper()}"')

    def test_009_tap_place_bet_buttonverify_that_the_bet_is_placed_at_the_boosted_odds(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        DESCRIPTION: Verify that the bet is placed at the boosted odds
        EXPECTED: The bet is placed at the boosted odds
        """
        self.quick_bet_after_reboost.place_bet.click()
        result = wait_for_result(lambda: self.site.quick_bet_panel,
                                 name='Waiting for Quick bet',
                                 timeout=10)
        self.assertTrue(result, msg='"Quick Bet" not displayed')
        odds = self.site.quick_bet_panel.bet_receipt.odds
        self.assertIn(self.after_odds, odds,
                      msg=f'Bets are not placed at boosted odds')
        self.site.quick_bet_panel.close()

    def test_010_add_selection_to_the_quick_bet_one_more_timeadd_stake_and_tap_boost_button(self):
        """
        DESCRIPTION: Add selection to the Quick bet one more time
        DESCRIPTION: Add stake and tap ''BOOST'' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED'
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        """
        self.add_selection_to_quick_bet(selection_name=self.selection_name_2)

    def test_011_change_price_for_this_selection_in_tirepeat_steps_1_6(self):
        """
        DESCRIPTION: Change price for this selection in TI
        DESCRIPTION: Repeat steps #1-6
        EXPECTED: Results are the same
        """
        self.test_001_verify_that_inline_message_is_displayed_at_the_topverify_message_content(selection_id=self.selection_id_2)
        self.test_002_verify_that_inline_message_is_displayed_at_the_bottomverify_message_content()
        self.test_003_verify_that_boost_button_text_changes_to_re_boost()
        self.test_004_verify_that_place_bet_button_is_changed_to_accept__place_bet()
        self.test_005_verify_that_the_non_boosted_striked_out_price_is_updated()
        self.test_006_verify_that_boosted_price_remains_unchanged()

    def test_012_tap_accept__place_bet_buttonverify_that_the_updated_boosted_prices_are_retrievedverify_that_the_bet_is_placed_at_the_boosted_odds(self):
        """
        DESCRIPTION: Tap 'ACCEPT & PLACE BET' button
        DESCRIPTION: Verify that the updated boosted prices are retrieved
        DESCRIPTION: Verify that the bet is placed at the boosted odds
        EXPECTED: Updated boosted prices are retrieved
        EXPECTED: The bet is placed at the boosted odds
        """
        self.site.quick_bet_panel.place_bet.click()
        result = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_quick_bet_info_panel(timeout=40, expected_result=False),
                                 name='Waiting for Quick bet',
                                 timeout=40)
        self.assertFalse(result, msg='"Quick Bet" not displayed')
        odds = self.site.quick_bet_panel.bet_receipt.odds
        self.assertNotEqual(odds, self.previous_value,
                            msg=f' Actual Value: "{odds}" are same as '
                                f' Expected Value: "{self.previous_value}"')
        self._logger.info("Bet is placed with updated Price")
        self.site.quick_bet_panel.close()

    def test_013_provide_same_verifications_with_decimal_odds_format(self):
        """
        DESCRIPTION: Provide same verifications with decimal odds format
        """
        self.__class__.decimal = True
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.create_events()
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.add_selection_to_quick_bet()
        self.test_001_verify_that_inline_message_is_displayed_at_the_topverify_message_content()
        self.test_002_verify_that_inline_message_is_displayed_at_the_bottomverify_message_content()
        self.test_003_verify_that_boost_button_text_changes_to_re_boost()
        self.test_004_verify_that_place_bet_button_is_changed_to_accept__place_bet()
        self.test_005_verify_that_the_non_boosted_striked_out_price_is_updated()
        self.test_006_verify_that_boosted_price_remains_unchanged()
        self.test_007_tap_re_boost_buttonverify_that_boosted_odds_are_updated()
        self.test_008_verify_that_accept__place_bet_button_is_changed_back_to_place_bet()
        self.test_009_tap_place_bet_buttonverify_that_the_bet_is_placed_at_the_boosted_odds()
        self.test_010_add_selection_to_the_quick_bet_one_more_timeadd_stake_and_tap_boost_button()
        self.test_011_change_price_for_this_selection_in_tirepeat_steps_1_6()
        self.test_012_tap_accept__place_bet_buttonverify_that_the_updated_boosted_prices_are_retrievedverify_that_the_bet_is_placed_at_the_boosted_odds()
